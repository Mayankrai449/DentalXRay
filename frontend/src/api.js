import axios from 'axios';

const api = axios.create({
  baseURL: 'https://dentalxray-fre1.onrender.com',
  headers: { 'Content-Type': 'multipart/form-data' },
});

export default api;