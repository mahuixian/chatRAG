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
          <span class="message-content">{{ message.content.reply }}</span>
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
  justify-content: flex-start; /* 助手消息靠左对齐 */
  align-items: flex-start; /* 助手消息垂直顶部对齐 */
}

.message-prefix {
  flex: 10%; /* 设置助手前缀占据的宽度 */
  font-weight: bold;
  align-self: flex-start; /* 助手前缀垂直顶部对齐 */
}

.assistant-content {
  flex: 90%; /* 设置助手内容占据的宽度 */
  word-wrap: break-word; /* 长文本自动换行 */
  padding: 8px 12px; /* 文字内容的内边距 */
  background-color: #f8f9fa; /* 背景颜色 */
  border-radius: 10px; /* 圆角 */
}


</style>
