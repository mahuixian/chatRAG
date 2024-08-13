import os
import jwt
import datetime
import json
from dotenv import load_dotenv
from uuid import uuid1
from fastapi import FastAPI, File, UploadFile, Form, HTTPException, Depends, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from database.connect import execute_query, fetch_all, fetch_one
from rag.utils import logger
from rag.llm.llm import llm_generator as LLM
from rag.files.files import processFile
from typing import Optional, Union
load_dotenv(override=True)

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

class ChatRequest(BaseModel):
    message: str = Form(...)
    username: str = Form(...)


@app.post('/api/uploadfile')
async def receive(request: Request):
    content_type = request.headers.get('Content-Type')
    try:
        if 'application/json' in content_type:
            body = await request.json()
            username = body.get('username')
            url = body.get('url')
            execute_query(
                "INSERT INTO uploads (username, type, file_name, status) VALUES (?, 'URL', ?, 'pending')",
                (username, url)
            )
            logger.info(f"From {username} receive URL: {url}")
            return JSONResponse(content={'message': 'URLS received'}, status_code=200)
        elif 'multipart/form-data' in content_type:
            form = await request.form()
            username = form.get('username')
            file = form.get('file')

            await processFile(file, username)
            
            logger.info(f"From {username} receive File: {file.filename}")
            
            return JSONResponse(content={'message': 'Files received'}, status_code=200)
    except Exception as e:
        logger.error(f'Error storing uploadfile for {username}: {str(e)}')
        raise HTTPException(status_code=500, detail="An error occurred while storing uploadfile")

    
@app.delete('/api/remove')
async def remove(request: Request):
    body = await request.json()
    filename = body['filename']
    username = body['username']
    try:
        execute_query(
            "DELETE FROM uploads WHERE file_name = ?",
            (filename,)
        )
        logger.info(f'Removed file: {filename}')
        return JSONResponse(content={'message': 'File removed'}, status_code=200)
    except Exception as e:
        logger.error(f'Error removing file {filename}: {str(e)}')
        raise HTTPException(status_code=500, detail='An error occurred while removing the file')
    

@app.post("/api/chat")
async def chat(request: ChatRequest):
    try:
        message = request.message
        username = request.username
        
        task_id = uuid1()
        logger.info(f'{username} initiated chat with task_id {task_id}')
        
        user_message = {'role': 'user', 'content': message}
        execute_query(
            "INSERT INTO conversations (task_id, username, message) VALUES (?, ?, ?)",
            (str(task_id), username, json.dumps(user_message))
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
        
            reply_message = {'role': 'assistant', 'content': reply}
            execute_query(
                "UPDATE conversations set reply = ? WHERE task_id = ? and username = ?",
                (json.dumps(reply_message), task_id, username)
            )
        
        return JSONResponse(content={'reply': reply_message['content']}, status_code=200)
    except Exception as e:
        logger.error(f'Error processing chat for {username}: {str(e)}')
        raise HTTPException(status_code=500, detail='An error occurred during chat processing')


@app.post("/api/login")
async def login(request: Request):
    body = await request.json()
    username = body['username']
    password = body['password']
    try:
        user = fetch_one(
            "SELECT user_id, password FROM users WHERE username=?",
            (username,)
        )

        print(user)
        if user and user[1] == password:
            token = jwt.encode({
                'user_id': user[0],
                'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)
            }, os.getenv('SECRET_KEY'), algorithm='HS256')
            logger.info(f'User {username} logged in successfully')
            return JSONResponse(content={'success': True, 'token': token}, status_code=200)
        else:
            logger.warning(f'Invalid login attempt for user {username}')
            return JSONResponse(content={'success': False, 'message': 'Invalid credentials'}, status_code=401)
    except Exception as e:
        logger.error(f'Error during login for {username}: {str(e)}')
        raise HTTPException(status_code=500, detail='An error occurred during login')


@app.get('/api/uploads/{username}')
async def get_uploads(username: str):
    try:
        query = '''
        SELECT id, username, type, file_name, status, created_at
        FROM uploads
        WHERE username = ?
        ORDER BY created_at
        '''
        rows = fetch_all(query, (username,))
        
        uploads = [{'id': row[0], 'username': row[1], 'type': row[2], 'file_name': row[3], 'status': row[4], 'created_at': row[5]} for row in rows]
        
        logger.info(f'Retrieved uploads for {username}')
        return uploads
    except Exception as e:
        logger.error(f'Error retrieving uploads for {username}: {str(e)}')
        raise HTTPException(status_code=500, detail='An error occurred while retrieving uploads')


@app.get('/api/conversations/{username}')
async def get_conversations(username: str):
    try:
        query = '''
        SELECT id, task_id, username, message, reply, created_at
        FROM conversations
        WHERE username = ?
        ORDER BY created_at
        '''
        rows = fetch_all(query, (username,))
        
        conversations = [{'id': row[0], 'task_id': row[1], 'username': row[2], 'message': row[3], 'reply': row[4], 'created_at': row[5]} for row in rows]
        
        logger.info(f'Retrieved conversations for {username}')
        return conversations
    except Exception as e:
        logger.error(f'Error retrieving conversations for {username}: {str(e)}')
        raise HTTPException(status_code=500, detail='An error occurred while retrieving conversations')


if __name__ == '__main__':
    logger.info("Starting the FastAPI application")
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5000, debug=True)
