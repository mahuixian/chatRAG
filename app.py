from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
# import mimetypes
# from rag.files.files import processFile
# from werkzeug.utils import secure_filename
from rag.utils import logger
import os
import sqlite3
import jwt
import datetime
from dotenv import load_dotenv


app = Flask(__name__, static_folder='dist')
CORS(app)

load_dotenv()
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
database_url = os.getenv('DATABASE')


def get_user_from_db(username):
    conn = sqlite3.connect(database_url.replace('sqlite:///', ''))
    cursor = conn.cursor()
    cursor.execute(
        "SELECT user_id, password FROM users WHERE username=?", (username,))
    user = cursor.fetchone()
    conn.close()
    return user


@app.route('/api/urls', methods=['POST'])
def receive_urls():
    data = request.json
    urls = data.get('urls')
    username = data.get('username')
    logger.info('From %s Received URLs: %s', username, urls)
    conn = sqlite3.connect(database_url.replace('sqlite:///', ''))
    cursor = conn.cursor()
    for url in urls:
        cursor.execute("""
            INSERT INTO uploads (username, type, file_name, status)
            VALUES (?, 'URL', ?, 'pending')
        """, (username, url))
    conn.commit()
    conn.close()

    # 在这里处理接收到的URL
    return jsonify({'message': 'URLs received'}), 200


@app.route('/api/files', methods=['POST', 'DELETE'])
def receive_files():
    if 'files' not in request.files:
        return jsonify({'message': 'No files provided'}), -2000

    files = request.files.getlist('files')
    username = request.form.get('username')
    logger.info('From %s Received Files: %s', username, files)
    conn = sqlite3.connect(database_url.replace('sqlite:///', ''))
    cursor = conn.cursor()

    for file in files:
        if file and file.filename:
            file_name = file.filename
            cursor.execute("""INSERT INTO uploads (username, type, file_name) VALUES (?, 'File', ?)""", (username, file_name))

    conn.commit()
    conn.close()

    return jsonify({'message': 'URLs received'}), 200


@app.route('/api/images', methods=['POST', 'DELETE'])
def receive_images():
    # TODO 接收到image，读取image中的内容后存入数据库
    if 'images' not in request.files:
        return jsonify({'message': 'No images provided'}), 400
    images = request.files.getlist('images')
    username = request.form.get('username')
    logger.info('From %s Received images: %s', username, images)

    conn = sqlite3.connect(database_url.replace('sqlite:///', ''))
    cursor = conn.cursor()
    for image in images:
        image_name = image.filename
        cursor.execute("""
                           INSERT INTO uploads (username, type, file_name)
                           VALUES (?, 'File', ?)
                           """, (username, image_name))
    return jsonify({'message': 'images received'}), 200


@app.route('/api/remove', methods=['DELETE'])
def remove():
    file_name = request.json.get('filename')
    conn = sqlite3.connect(database_url.replace('sqlite:///', ''))
    cursor = conn.cursor()
    cursor.execute("""
                    DELETE FROM uploads WHERE file_name = ?
                    """, (file_name,))
    return jsonify({'message': 'file removed'}), 200


@app.route("/api/chat", methods=["POST"])
def chat():
    data = request.get_json()
    message = data.get('content', '')
    
    reply = "这是助手的回复：啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊" + message

    return jsonify({'reply': reply}), 200


@app.route("/api/login", methods=["POST"])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    user = get_user_from_db(username)

    if user and user[1] == password:
        token = jwt.encode({
            'user_id': user[0],
            'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)
        }, app.config['SECRET_KEY'], algorithm='HS256')
        print(token)
        return jsonify({'success': True, 'token': token})
    else:
        return jsonify({'success': False, 'message': 'Invalid credentials'})


if __name__ == '__main__':
    app.run(debug=True)
