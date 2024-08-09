<template>
  <div class="history" ref="history">
    <div v-for="(message, index) in messages" :key="index" :class="['message', message.type]">
      <template v-if="message.type === 'user'">
        <div class="user-message">
          <span class="message-content">{{ message.content.input }}</span>
        </div>
      </template>
      <template v-else-if="message.type === 'assistant'">
        <div class="assistant-message">
          <span class="message-prefix">助手：</span>
          <span class="assistant-content">{{ message.content.reply }}</span>
        </div>
      </template>
    </div>
  </div>
</template>

<script>
// import axios from 'axios';
import { EventBus } from '../bus';
import { api } from '../api';

export default {
  name: 'AppContent',
  data() {
    return {
      messages: []
    };
  },
  created() {
    this.loadConversations();
    EventBus.$on('new-message', message => {
      this.messages.push(message);
      this.scrollToBottom();
    });
  },

  watch: {
    messages() {
      this.$nextTick(() => {
        this.scrollToBottom();
      });
    }
  },

  methods: {
    async loadConversations() {
      try {
        const username = localStorage.getItem('username');
        const response = await api.getConversations(username);
        const conversations = response.data;

        console.log(conversations);
        //将API返回的数据添加到message
        conversations.forEach(element => {
          const messageContent = JSON.parse(element.message).content;
          const replyContent = JSON.parse(element.reply) !== null ? JSON.parse(element.reply).content : null;

          console.log(messageContent, replyContent);
          this.messages.push(
            { type: 'user', content: { input: messageContent }},
            { type: 'assistant', content: { reply: replyContent !== null ? replyContent : "回复出错，请稍后重试。"}}
          );
        });
        this.scrollToBottom();
      } catch (error) {
        console.error('Error loading conversations:', error)
      }
    },
    scrollToBottom() {
      this.$nextTick(() => {
        const history = this.$refs.history;
        history.scrollTop = history.scrollHeight;
      });
    }
  }
};
</script>

<style scoped>
.history {
  height: 80vh;
  overflow-y: auto;
  padding: 10px;
  scrollbar-width: thin;
  scrollbar-color: #a1c4fd #cfd9df; 
  border-radius: 10px;
}

.history::-webkit-scrollbar {
  width: 8px;
}

.history::-webkit-scrollbar-thumb {
  background: linear-gradient(to bottom, #a1c4fd, #c2e9fb); 
  border-radius: 10px;
}

.history::-webkit-scrollbar-thumb:hover {
  background: linear-gradient(to bottom, #89cff0, #76c7e0);
}

.message {
  margin-bottom: 10px;
  opacity: 0;
  transform: translateY(10px);
  animation: slideIn 0.3s forwards;
}

@keyframes slideIn {
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.user-message {
  display: flex;
  justify-content: flex-end;
  align-items: center;
}

.user-message .message-content {
  max-width: 50%; 
  word-wrap: break-word; 
  padding: 8px 12px; 
  background-color: #eaecec; 
  border-radius: 10px; 
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  transition: transform 0.3s ease-in-out;
}

.user-message .message-content:hover {
  transform: scale(1.02);
}

.assistant-message { 
  display: flex;
  align-items: flex-start;
}

.message-prefix {
  margin-right: 8px;
  white-space: nowrap;
  font-weight: bold;
}

.assistant-content {
  max-width: 80%;
  word-wrap: break-word;
  padding: 8px 12px;
  background-color: aliceblue;
  border-radius: 10px;
  flex-shrink: 1;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  transition: transform 0.3s ease-in-out;
}

.assistant-content:hover {
  transform: scale(1.02);
}
</style>
