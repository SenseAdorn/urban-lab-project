<template>
  <div class="login-container">
    <div class="login-card">
      <h1>Login</h1>
      <form @submit.prevent="login" class="login-form">
        <div class="form-group">
          <label for="username">Username</label>
          <input type="text" id="username" v-model="username" required />
        </div>
        <div class="form-group">
          <label for="password">Password</label>
          <input type="password" id="password" v-model="password" required />
        </div>
        <button type="submit" class="login-button">Login</button>
        <p v-if="errorMessage" class="error-message">{{ errorMessage }}</p>
      </form>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      username: '',
      password: '',
      errorMessage: ''
    };
  },
  methods: {
    async login() {
      try {
        const response = await axios.post('http://127.0.0.1:5000/auth/login', {
          username: this.username,
          password: this.password
        });
        const token = response.data.access_token;
        localStorage.setItem('access_token', token); // Save token locally
        this.$router.push('/dashboard'); // Redirect to dashboard
      } catch (error) {
        this.errorMessage = 'Invalid username or password';
      }
    }
  }
};
</script>

<style scoped>
body {
  font-family: Arial, sans-serif;
  background: #f7f9fa;
  margin: 0;
  padding: 0;
  color: #333;
}

.login-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  background: #f7f9fa;
}

.login-card {
  background: #fff;
  padding: 40px 30px;
  border-radius: 8px;
  box-shadow: 0 2px 6px rgba(0,0,0,0.1);
  max-width: 350px;
  width: 100%;
  box-sizing: border-box;
  text-align: center;
}

.login-card h1 {
  margin-bottom: 30px;
  color: #2c3e50;
  font-size: 24px;
}

.login-form {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.form-group {
  text-align: left;
}

.form-group label {
  display: block;
  margin-bottom: 8px;
  font-weight: bold;
  color: #34495e;
}

.form-group input {
  width: 100%;
  padding: 10px;
  border: 1px solid #ccc;
  border-radius:4px;
  font-size:14px;
  box-sizing:border-box;
}

.form-group input:focus {
  border-color:#42b983;
  outline:none;
  box-shadow:0 0 2px rgba(66,185,131,0.5);
}

.login-button {
  background-color:#42b983;
  color:#fff;
  border:none;
  border-radius:4px;
  padding:10px 0;
  cursor:pointer;
  font-weight:bold;
  font-size:16px;
  transition: background-color 0.3s ease;
}

.login-button:hover {
  background-color:#36a778;
}

.error-message {
  color: red;
  margin-top:10px;
  font-size:14px;
}
</style>
