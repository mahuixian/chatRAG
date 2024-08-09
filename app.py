import os
import jwt
import datetime
import json
from dotenv import load_dotenv
from database.connect import execute_query, fetch_one, fetch_all
from flask import Flask, request, jsonify
from flask_cors import CORS
from rag.utils import logger
from rag.llm.llm import llm_generator as LLM
from uuid import uuid1
load_dotenv()

app = Flask(__name__, static_folder='dist')
CORS(app)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

@app.route('/api/urls', methods=['POST'])
def receive_urls():
    try:
        data = request.json
        urls = data.get('urls')
        username = data.get('username')
        for url in urls:
            execute_query(
                "INSERT INTO uploads (username, type, file_name, status) VALUES (?, 'URL', ?, 'pending')",
                (username, url)
            )
 
        logger.info(f'From {username} Received URLs: {urls}')
        return jsonify({'message': 'URLs received'}), 200
    except Exception as e:
        logger.error(f'Error storing URLs for {username}: {str(e)}')
        return jsonify({'message': 'An error occurred while storing URLs'}), 500


@app.route('/api/files', methods=['POST', 'DELETE'])
def receive_files():
    try:
        if 'files' not in request.files:
            logger.warning(f'No files provided by {request.form.get("username")}')
            return jsonify({'message': 'No files provided'}), 400

        files = request.files.getlist('files')
        username = request.form.get('username')
        
        for file in files:
            if file and file.filename:
                execute_query(
                    "INSERT INTO uploads (username, type, file_name, status) VALUES (?, 'File', ?, 'pending')",
                    (username, file.filename)
                )
        logger.info(f'From {username} Received Files: {[file.filename for file in files]}')
        return jsonify({'message': 'Files received'}), 200
    except Exception as e:
        logger.error(f'Error storing files for {username}: {str(e)}')
        return jsonify({'message': 'An error occurred while storing files'}), 500


@app.route('/api/images', methods=['POST', 'DELETE'])
def receive_images():
    try:
        if 'images' not in request.files:
            logger.warning(f'No images provided by {request.form.get("username")}')
            return jsonify({'message': 'No images provided'}), 400

        images = request.files.getlist('images')
        username = request.form.get('username')
        
        for image in images:
            execute_query(
                "INSERT INTO uploads (username, type, file_name, status) VALUES (?, 'File', ?, 'pending')",
                (username, image.filename)
            )
        logger.info(f'From {username} Received images: {[image.filename for image in images]}')
        return jsonify({'message': 'Images received'}), 200
    except Exception as e:
        logger.error(f'Error storing images for {username}: {str(e)}')
        return jsonify({'message': 'An error occurred while storing images'}), 500


@app.route('/api/remove', methods=['DELETE'])
def remove():
    try:
        file_name = request.json.get('filename')
        execute_query(
            "DELETE FROM uploads WHERE file_name = ?",
            (file_name,)
        )
        logger.info(f'Removed file: {file_name}')
        return jsonify({'message': 'File removed'}), 200
    except Exception as e:
        logger.error(f'Error removing file {file_name}: {str(e)}')
        return jsonify({'message': 'An error occurred while removing the file'}), 500


@app.route("/api/chat", methods=["POST"])
def chat():
    try:
        data = request.get_json()
        message = data.get('message')
        username = data.get('username')
        
        task_id = uuid1()
        logger.info(f'{username} initiated chat with task_id {task_id}')
        
        message = {'role': 'user', 'content': message}
        execute_query(
            "INSERT INTO conversations (task_id, username, message) VALUES (?, ?, ?)",
            (str(task_id), username, json.dumps(message))
        )
        logger.info(f'Stored user message for task_id {task_id}')

        history = fetch_all(
            "SELECT task_id, message, reply FROM conversations WHERE username = ? ORDER BY created_at DESC",
            (username,)
        )
        
        task_id, query, reply = history[0]
        if reply is None:
            llm_reply = LLM.generate(json.loads(query)['content'])
            reply = llm_reply.choices[0].message.content
            logger.info(f"================= {task_id} =====================")
            logger.info(f"user: {json.loads(query)['content']}")
            logger.info(f"assistant: {reply}")
            logger.info(f"=================================================")
        
            reply = {'role': 'assistant', 'content': reply}
            execute_query(
                "UPDATE conversations set reply = ? WHERE task_id = ? and username = ?",
                (json.dumps(reply), task_id, username)
            )
        
        return jsonify({'reply': reply['content']}), 200
    except Exception as e:
        logger.error(f'Error processing chat for {username}: {str(e)}')
        return jsonify({'message': 'An error occurred during chat processing'}), 500


@app.route("/api/login", methods=["POST"])
def login():
    try:
        data = request.json
        username = data.get('username')
        password = data.get('password')

        user = fetch_one(
            "SELECT user_id, password FROM users WHERE username=?",
            (username,)
        )

        if user and user[1] == password:
            token = jwt.encode({
                'user_id': user[0],
                'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)
            }, app.config['SECRET_KEY'], algorithm='HS256')
            logger.info(f'User {username} logged in successfully')
            return jsonify({'success': True, 'token': token})
        else:
            logger.warning(f'Invalid login attempt for user {username}')
            return jsonify({'success': False, 'message': 'Invalid credentials'})
    except Exception as e:
        logger.error(f'Error during login for {username}: {str(e)}')
        return jsonify({'message': 'An error occurred during login'}), 500


@app.route('/api/uploads/<username>', methods=['GET'])
def get_uploads(username):
    try:
        query = '''
        SELECT id, username, type, file_name, status, created_at
        FROM uploads
        WHERE username = ?
        ORDER BY created_at
        '''
        rows = fetch_all(query, (username,))
        
        uploads = []
        for row in rows:
            uploads.append({
                'id': row[0],
                'username': row[1],
                'type': row[2],
                'file_name': row[3],
                'status': row[4],
                'created_at': row[5]
            })
        
        logger.info(f'Retrieved uploads for {username}')
        return jsonify(uploads)
    except Exception as e:
        logger.error(f'Error retrieving uploads for {username}: {str(e)}')
        return jsonify({'message': 'An error occurred while retrieving uploads'}), 500


@app.route('/api/conversations/<username>', methods=['GET'])
def get_conversations(username):
    try:
        query = '''
        SELECT id, task_id, username, message, reply, created_at
        FROM conversations
        WHERE username = ?
        ORDER BY created_at
        '''
        rows = fetch_all(query, (username,))
        
        conversations = []
        for row in rows:
            conversations.append({
                'id': row[0],
                'task_id': row[1],
                'username': row[2],
                'message': row[3],
                'reply': row[4],
                'created_at': row[5]
            })
        
        logger.info(f'Retrieved conversations for {username}')
        return jsonify(conversations)
    except Exception as e:
        logger.error(f'Error retrieving conversations for {username}: {str(e)}')
        return jsonify({'message': 'An error occurred while retrieving conversations'}), 500


if __name__ == '__main__':
    logger.info("Starting the Flask application")
    app.run(debug=True)
