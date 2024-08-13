// import axios from 'axios';

// const API_BASE_URL = 'http://127.0.0.1:8000/api';

// export const api = {
//     //登录接口
//     login(data) {
//         return axios.post(`${API_BASE_URL}/login`, data);
//     },

//     //获取用户的对话历史
//     getConversations(username) {
//         return axios.get(`${API_BASE_URL}/conversations/${username}`);
//     },

//     //获取用户的上传文件记录
//     getUploads(username) {
//         return axios.get(`${API_BASE_URL}/uploads/${username}`);
//     },

//     //上传url或文件
//     uploadData(data, type) {
//         let header = {};

//         if (type === 'url') {
//             header['Content-Type'] = 'application/json';
//         } else {
//             header['Content-Type'] = 'multipart/form-data';
//         }
//         console.log(header)
//         return axios.post(`${API_BASE_URL}/uploadfile`, data, { headers: header });
//     },

//     //移除上传的文件
//     removeFile(data) {
//         return axios.delete(`${API_BASE_URL}/remove`, {data: data});
//     },

//     //发送聊天消息
//     chat(data) {
//         return axios.post(`${API_BASE_URL}/chat`, data);
//     },
// }

import axios from 'axios';

const API_BASE_URL = 'http://127.0.0.1:8000/api';

export const api = {
    // 登录接口
    async login(data) {
        try {
            const response = await axios.post(`${API_BASE_URL}/login`, data);
            return response;
        } catch (error) {
            console.error('Error logging in:', error);
            throw error;
        }
    },

    // 获取用户的对话历史
    async getConversations(username) {
        try {
            const response = await axios.get(`${API_BASE_URL}/conversations/${username}`);
            return response;
        } catch (error) {
            console.error('Error fetching conversations:', error);
            throw error;
        }
    },

    // 获取用户的上传文件记录
    async getUploads(username) {
        try {
            const response = await axios.get(`${API_BASE_URL}/uploads/${username}`);
            return response;
        } catch (error) {
            console.error('Error fetching uploads:', error);
            throw error;
        }
    },

    // 上传 URL 或文件
    async uploadData(data, type) {
        let headers = {};

        if (type === 'url') {
            headers['Content-Type'] = 'application/json';
        } else {
            headers['Content-Type'] = 'multipart/form-data';
        }

        try {
            const response = await axios.post(`${API_BASE_URL}/uploadfile`, data, { headers });
            return response;
        } catch (error) {
            console.error('Error uploading data:', error);
            throw error;
        }
    },

    // 移除上传的文件
    async removeFile(data) {
        try {
            const response = await axios.delete(`${API_BASE_URL}/remove`, { data: data });
            return response;
        } catch (error) {
            console.error('Error removing file:', error);
            throw error;
        }
    },

    // 发送聊天消息
    async chat(data) {
        try {
            const response = await axios.post(`${API_BASE_URL}/chat`, data);
            return response;
        } catch (error) {
            console.error('Error sending chat message:', error);
            throw error;
        }
    },
};
