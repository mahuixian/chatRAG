<template>
  <div class="footer">
    <el-input
      placeholder="请输入你的需求"
      v-model="input"
      class="footer-input">
      <span slot="suffix" class="icon-wrapper" @click="sendMessage">
        <i class="el-input__icon el-icon-s-promotion"></i>
      </span>
    </el-input>
  </div>
</template>

<script>
import axios from 'axios';
import { EventBus } from '../bus';

export default {
  name: 'Footer',
  data() {
    return {
      input: '',
      username: localStorage.getItem('username') || ''
    };
  },
  methods: {
    async sendMessage() {
      if (this.input.trim() === '') return;

      try {
        console.log('Sending message:', this.input);
        const response = await axios.post('http://127.0.0.1:5000/api/chat', 
          { message: this.input,
            username: this.username
          }
        );
        console.log('Message sent, response:', response.data);

        // 向事件总线发送消息，包括用户输入和后端返回的消息
        EventBus.$emit('new-message', { type: 'user', content: { input: this.input, username: this.username } });
        EventBus.$emit('new-message', { type: 'assistant', content: response.data });

        // 清空输入框内容
        this.input = '';
      } catch (error) {
        console.error('Error sending message:', error);
      }
    }
  }
};
</script>

<style scoped>
.footer {
  width: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
}

.footer-input {
  width: 100%;
}

.footer-input input {
  width: calc(100% - 30px); /* 留出图标宽度的空间 */
  padding: 10px;
  font-size: 16px;
  border: 1px solid rgba(179, 230, 231, 0.3);
  border-radius: 25px;
  box-sizing: border-box;
}

.footer-input input:focus {
  outline: none;
  box-shadow: 0 0 5px rgba(81, 203, 238, 1);
  background-color: rgba(255, 255, 255, 0.9);
}

.icon-wrapper {
  cursor: pointer;
}

.el-input__icon {
  cursor: pointer;
}
</style>
