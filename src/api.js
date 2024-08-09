import axios from 'axios';

const API_BASE_URL = 'http://127.0.0.1:5000/api';

export const api = {
    //登录接口
    login(data) {
        return axios.post(`${API_BASE_URL}/login`, data);
    },

    //获取用户的对话历史
    getConversations(username) {
        return axios.get(`${API_BASE_URL}/conversations/${username}`);
    },

    //获取用户的上传文件记录
    getUploads(username) {
        return axios.get(`${API_BASE_URL}/uploads/${username}`);
    },

    //接收url
    receiveUrls(data) {
        return axios.post(`${API_BASE_URL}/urls`, data, 
           {
                headers: {
                    'Content-Type': 'application/json'
                }
           }
        );
    },

    //接收文件
    receiveFiles(formData) {
        return axios.post(`${API_BASE_URL}/files`, formData,
            {
                headers: {
                    'Content-Type': 'multipart/form-data'
                },
            }
        );
    },

    //接收图片
    receiveImages(formData) {
        return axios.post(`${API_BASE_URL}/images`, formData,
            {
                headers: {
                    'Content-Type': 'multipart/form-data'
                },
            }
        );
    },

    //移除上传的文件
    removeFile(fileName, userName) {
        return axios.delete(`${API_BASE_URL}/remove`, {data: { filename: fileName, username: userName }});
    },

    //发送聊天消息
    chat(data) {
        return axios.post(`${API_BASE_URL}/chat`, data);
    },
}
