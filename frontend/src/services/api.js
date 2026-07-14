import axios from 'axios';

const API_URL = 'http://localhost:5000/api';

const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const getPrices = (params) => {
  return api.get('/prices', { params });
};

export const getEvents = (params) => {
  return api.get('/events', { params });
};

export const getCategories = () => {
  return api.get('/categories');
};

export const getStatistics = () => {
  return api.get('/statistics');
};

export const getImpacts = (params) => {
  return api.get('/impacts', { params });
};

export const getChangePoint = () => {
  return api.get('/change-point');
};

export default api;