import axios from 'axios';

const ACCESS_KEY = 'nakip_access_token';

const client = axios.create({
  baseURL: '/api'
});

client.interceptors.request.use((config) => {
  const token = localStorage.getItem(ACCESS_KEY);
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  const language = typeof document !== 'undefined' ? document.documentElement.lang || 'en' : 'en';
  config.headers['Accept-Language'] = language;
  return config;
});

export default client;
