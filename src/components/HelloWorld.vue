<template>
  <div>
    <h1>Test API Connection</h1>
    <button @click="testApi">Test API</button>
    <p v-if="message">{{ message }}</p>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      message: '' // 用于显示 API 返回的结果
    };
  },
  methods: {
    async testApi() {
      try {
        // 测试连接 grants API
        const response = await axios.get('/grants');
        this.message = `API Response: ${response.data.length} grants found.`; // 成功后显示数据长度
      } catch (error) {
        this.message = `Error: ${error.message}`; // 失败后显示错误信息
      }
    }
  }
};
</script>

<style>
/* 可选样式 */
button {
  padding: 10px 20px;
  font-size: 16px;
  cursor: pointer;
}
</style>
