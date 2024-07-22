DROP TABLE IF EXISTS users;

CREATE TABLE users (
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL
);


-- 创建用户上传记录表
CREATE TABLE uploads (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username type VARCHAR(50) NOT NULL,
    file_name VARCHAR(255) NOT NULL UNIQUE,
    type VARCHAR(255),
    status VARCHAR(50) DEFAULT 'pending',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);


-- 创建存储上下文对话表
CREATE TABLE conversations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    task_id TEXT NOT NULL, --用于message和reply对应
    username type VARCHAR(50) NOT NULL,
    message TEXT, --用户输入
    reply TEXT, --LLM输出
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
