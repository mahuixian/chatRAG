import os
import jwt
import datetime
import json
from dotenv import load_dotenv
from database.connect import execute_query, fetch_one, fetch_all
from flask import Flask, request, jsonify
from flask_cors import CORS
from rag.utils.logger import Logger
from groq import Groq
from uuid import uuid1
load_dotenv()
logger = Logger('logs/rag.log').logger

app = Flask(__name__, static_folder='dist')
CORS(app)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

@app.route('/api/urls', methods=['POST'])
def receive_urls():
    data = request.json
    urls = data.get('urls')
    username = data.get('username')
    logger.info(f'From {username} Received URLs: {urls}')

    for url in urls:
        execute_query(
            "INSERT INTO uploads (username, type, file_name, status) VALUES (?, 'URL', ?, 'pending')",
            (username, url)
        )
    return jsonify({'message': 'URLs received'}), 200


@app.route('/api/files', methods=['POST', 'DELETE'])
def receive_files():
    if 'files' not in request.files:
        return jsonify({'message': 'No files provided'}), 400

    files = request.files.getlist('files')
    username = request.form.get('username')
    logger.info(f'From {username} Received Files: {[file.filename for file in files]}')
    
    for file in files:
        if file and file.filename:
            execute_query(
                "INSERT INTO uploads (username, type, file_name) VALUES (?, 'File', ?)",
                (username, file.filename)
            )

    return jsonify({'message': 'Files received'}), 200


@app.route('/api/images', methods=['POST', 'DELETE'])
def receive_images():
    if 'images' not in request.files:
        return jsonify({'message': 'No images provided'}), 400

    images = request.files.getlist('images')
    username = request.form.get('username')
    logger.info(f'From {username} Received images: {[image.filename for image in images]}')
    
    for image in images:
        execute_query(
            "INSERT INTO uploads (username, type, file_name) VALUES (?, 'File', ?)",
            (username, image.filename)
        )

    return jsonify({'message': 'Images received'}), 200


@app.route('/api/remove', methods=['DELETE'])
def remove():
    file_name = request.json.get('filename')
    execute_query(
        "DELETE FROM uploads WHERE file_name = ?",
        (file_name,)
    )
    logger.info(f'Removed file: {file_name}')
    return jsonify({'message': 'File removed'}), 200


@app.route("/api/chat", methods=["POST"])
def chat():
    data = request.get_json()
    message = data.get('message')
    username = data.get('username')
    
    task_id = uuid1()
    print(type(task_id))
    #将query存储到数据库中
    message = {'role': 'user', 'content': message}
    
    execute_query(
        "INSERT INTO conversations (task_id, username, message) VALUES (?, ?, ?)",
        (str(task_id), username, json.dumps(message))
    )
    
    #从数据库中取history
    history = fetch_all(
        "SELECT task_id, message, reply FROM conversations WHERE username = ? ORDER BY created_at DESC",
        (username,)
    )
    
    task_id, query, reply = history[0]
    if reply is None:
        LLM = Groq(api_key="")
        llm_reply = LLM.chat.completions.create(
            model='llama3-70b-8192',
            messages=[json.loads(query)],
            temperature=0,
            stream=False
        )
        reply = llm_reply.choices[0].message.content
        print("===================================")
        print(reply)
    # history.append({'role': 'assistant', 'message': reply})
        reply = {'role': 'assistant', 'content': reply}
    execute_query(
        "UPDATE conversations set reply = ? WHERE task_id = ? and username = ?",
        (json.dumps(reply), task_id, username)
    )
    
    return jsonify({'reply': reply['content']}), 200


@app.route("/api/login", methods=["POST"])
def login():
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


@app.route('/api/uploads/<username>', methods=['GET'])
def get_uploads(username):
    query = '''
    SELECT id, username, type, file_name, status, created_at
    FROM uploads
    WHERE username = ?
    ORDER BY created_at
    '''
    rows = fetch_all(query, (username,))
    
    # 将结果转换为字典列表
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
    
    return jsonify(uploads)


@app.route('/api/conversations/<username>', methods=['GET'])
def get_conversations(username):
    query = '''
    SELECT id, task_id, username, message, reply, created_at
    FROM conversations
    WHERE username = ?
    ORDER BY created_at
    '''
    rows = fetch_all(query, (username,))
    
    # 将结果转换为字典列表
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
    
    return jsonify(conversations)


if __name__ == '__main__':
    app.run(debug=True)
