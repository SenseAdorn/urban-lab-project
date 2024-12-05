<template>
  <div class="register-container">
    <div class="register-card">
      <h1>Register New User</h1>
      <form @submit.prevent="registerUser" class="register-form">
        <div class="form-group">
          <label for="username">Username</label>
          <input type="text" id="username" v-model="newUser.username" required />
        </div>

        <div class="form-group">
          <label for="password">Password</label>
          <input type="password" id="password" v-model="newUser.password" required />
        </div>

        <div class="form-group">
          <label for="role">Role</label>
          <select id="role" v-model="newUser.role">
            <option value="user">User</option>
            <option value="admin">Admin</option>
          </select>
        </div>

        <button type="submit" class="register-button">Register</button>
      </form>

      <p v-if="successMessage" class="success-message">{{ successMessage }}</p>
      <p v-if="errorMessage" class="error-message">{{ errorMessage }}</p>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      newUser: {
        username: '',
        password: '',
        role: 'user'
      },
      successMessage: '',
      errorMessage: ''
    };
  },
  methods: {
    async registerUser() {
      try {
        const token = localStorage.getItem('access_token');
        const response = await axios.post('http://127.0.0.1:5000/auth/register', this.newUser, {
          headers: {
            Authorization: `Bearer ${token}`
          }
        });
        this.successMessage = response.data.message;
        this.errorMessage = '';
      } catch (error) {
        this.successMessage = '';
        this.errorMessage = error.response?.data?.message || 'Registration failed';
      }
    }
  }
};
</script>

<style scoped>
body {
  font-family: Arial, sans-serif;
  margin:0;
  padding:0;
  background:#f7f9fa;
}

.register-container {
  display:flex;
  justify-content:center;
  align-items:center;
  height:100vh;
  background:#f7f9fa;
}

.register-card {
  background:#fff;
  padding:40px 30px;
  border-radius:8px;
  box-shadow:0 2px 6px rgba(0,0,0,0.1);
  max-width:350px;
  width:100%;
  box-sizing:border-box;
  text-align:center;
}

.register-card h1 {
  margin-bottom:30px;
  color:#2c3e50;
  font-size:24px;
}

.register-form {
  display:flex;
  flex-direction:column;
  gap:20px;
  margin-bottom:20px;
  text-align:left;
}

.form-group label {
  display:block;
  margin-bottom:8px;
  font-weight:bold;
  color:#34495e;
  font-size:14px;
}

.form-group input,
.form-group select {
  width:100%;
  padding:10px;
  border:1px solid #ccc;
  border-radius:4px;
  font-size:14px;
  box-sizing:border-box;
}

.form-group input:focus,
.form-group select:focus {
  border-color:#42b983;
  outline:none;
  box-shadow:0 0 2px rgba(66,185,131,0.5);
}

.register-button {
  background-color:#42b983;
  color:#fff;
  border:none;
  border-radius:4px;
  padding:10px 0;
  cursor:pointer;
  font-weight:bold;
  font-size:16px;
  transition: background-color 0.3s ease;
  width:100%;
}

.register-button:hover {
  background-color:#36a778;
}

.success-message {
  color: green;
  margin-top:10px;
  font-size:14px;
}

.error-message {
  color: red;
  margin-top:10px;
  font-size:14px;
}

@media (max-width: 400px) {
  .register-card {
    padding:20px 15px;
  }

  .register-card h1 {
    font-size:20px;
    margin-bottom:20px;
  }

  .form-group input,
  .form-group select {
    padding:8px;
  }

  .register-button {
    padding:8px 0;
    font-size:14px;
  }
}
</style>
