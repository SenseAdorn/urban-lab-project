import { createApp } from 'vue';
import App from './App.vue';
import router from './router'; 
import axios from 'axios';
// import 'bootstrap/dist/css/bootstrap.min.css';
// import './index.css';  // 确保你有在项目中创建了 Tailwind 的样式

// Set Axios base URL
axios.defaults.baseURL = 'http://127.0.0.1:5000'; // Replace with your backend server address

// Intercept requests to add Authorization header if token exists
axios.interceptors.request.use(
    (config) => {
        const token = localStorage.getItem('access_token'); // Retrieve token from local storage
        if (token) {
            config.headers['Authorization'] = `Bearer ${token}`; // Add token to headers
        }
        return config;
    },
    (error) => {
        return Promise.reject(error);
    }
);

const app = createApp(App);
app.use(router); 
app.mount('#app');
