<template>
  <div class="history">
    <div v-for="(message, index) in messages" :key="index" :class="['message', message.type]">
      <template v-if="message.type === 'user'">
        <div class="user-message">
          <span class="message-content">{{ message.content.input }}</span>
          <!-- <span class="message-id"> ：用户</span> -->
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
import { EventBus } from '../bus';

export default {
  name: 'Content',
  data() {
    return {
      messages: []
    };
  },
  created() {
    EventBus.$on('new-message', message => {
      this.messages.push(message);
    });
    EventBus.$on('new-input', input => {
      this.messages.push({ type: 'user', content: input });
    });
  }
};
</script>

<style scoped>
.history {
  padding: 10px;
}

.message {
  margin-bottom: 10px;
}

.user-message {
  display: flex;
  justify-content: flex-end; /* 用户消息靠右对齐 */
  align-items: center;
}

.user-message .message-content {
  max-width: 50%; /* 最大宽度限制 */
  word-wrap: break-word; /* 长文本自动换行 */
  padding: 8px 12px; /* 文字内容的内边距 */
  background-color: #eaecec; /* 背景颜色 */
  border-radius: 10px; /* 圆角 */
}

.user-message .message-id {
  margin-left: 10px; /* 添加左边距 */
  font-weight: bold;
}

.assistant-message { 
  display: flex;
  justify-content: flex-start; 
  align-items: flex-start;
}

.message-prefix {
  flex: 5%; 
  font-weight: bold;
  align-self: flex-start; 
}

.assistant-content {
  flex: 95%; 
  word-wrap: break-word; /* 长文本自动换行 */
  background-color: #f8f9fa; /* 背景颜色 */
  border-radius: 10px; /* 圆角 */
  align-items: flex-start;
}

</style>
