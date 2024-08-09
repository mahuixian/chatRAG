<!-- eslint-disable vue/multi-word-component-names -->
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
import { EventBus } from '../bus';
import { api } from '../api';

export default {
  name: 'AppFooter',
  data() {
    return {
      input: '',
      username: localStorage.getItem('username') || ''
    };
  },
  methods: {
    async sendMessage() {
      if (this.input.trim() === '') return;

      //先将消息发送给事件总线
      EventBus.$emit('new-message', { type: 'user', content: { input: this.input} });

      //显示“等待中”
      const waitingMessage = { type: 'assistant', content: { reply: '助手正在思考...' }};
      EventBus.$emit('new-message', waitingMessage);

      const userInput = this.input;
      this.input = '';

      try {
        console.log('Sending message:', userInput);
        const response = await api.chat({ message: userInput,
            username: this.username
        });
        console.log('Message sent, response:', response.data);

        //用response替换“等待中”
        Object.assign(waitingMessage.content, response.data)

      } catch (error) {
        console.error('Error sending message:', error);
        waitingMessage.content.reply = '出现错误，请稍后重试。'
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
