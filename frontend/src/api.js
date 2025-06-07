import axios from 'axios';

const api = axios.create({
  baseURL: 'https://dentalxray-production.up.railway.app',
  headers: { 'Content-Type': 'multipart/form-data' },
});

export default api;