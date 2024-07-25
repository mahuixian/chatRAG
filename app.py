import os
import jwt
import datetime
import json
from dotenv import load_dotenv
from database.connect import execute_query, fetch_one, fetch_all
from flask import Flask, request, jsonify
from flask_cors import CORS
from database.models import Upload, Conversation
from rag.utils import logger
from groq import Groq
from uuid import uuid1

app = Flask(__name__, static_folder='dist')
CORS(app)

load_dotenv()
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

@app.route('/api/urls', methods=['POST'])
def receive_urls():
    data = request.json
    urls = data.get('urls')
    username = data.get('username')
    logger.info('From %s Received URLs: %s', username, urls)
    
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
    logger.info('From %s Received Files: %s', username, [file.filename for file in files])
    
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
    logger.info('From %s Received images: %s', username, [image.filename for image in images])
    
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
    logger.info('Removed file: %s', file_name)
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
        LLM = Groq(api_key="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")
        llm_reply = LLM.chat.completions.create(
            model='llama3-8b-8192',
            messages=[json.loads(query)],
            temperature=0,
            stream=False
        )
        reply = llm_reply.choices[0].message.content
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
        logger.info('User %s logged in successfully', username)
        return jsonify({'success': True, 'token': token})
    else:
        logger.warning('Invalid login attempt for user %s', username)
        return jsonify({'success': False, 'message': 'Invalid credentials'})

@app.route('/api/uploads/<username>', methods=['GET'])
def get_uploads(username):
    print("============")
    uploads = Upload.query.filter_by(username=username).order_by(Upload.created_at).all() #按照时间升序排序
    return jsonify([upload.to_dict() for upload in uploads])

@app.route('/api/conversations/<username>', methods=['GET'])
def get_conversations(username):
    conversations = Conversation.query.filter_by(username=username).order_by(Conversation.created_at).all() #按照时间升序排序
    return jsonify([conversation.to_dict() for conversation in conversations])


if __name__ == '__main__':
    app.run(debug=True)
