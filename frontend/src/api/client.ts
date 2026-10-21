import axios from 'axios';
import type { DashboardResponse, PredictionInput, PredictionResult } from '../types';

const api = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL ?? 'http://127.0.0.1:8000',
});

export const getDashboard = async () => (await api.get<DashboardResponse>('/api/dashboard')).data;

export const getMetrics = async () => (await api.get('/api/metrics')).data;

export const getOptions = async () => (await api.get('/api/options')).data;

export const getRecords = async (params?: Record<string, string | number | undefined>) =>
  (await api.get('/api/records', { params })).data;

export const predictEmission = async (payload: PredictionInput) =>
  (await api.post<PredictionResult>('/api/predict', payload)).data;

export const uploadCsv = async (file: File) => {
  const formData = new FormData();
  formData.append('file', file);
  return (await api.post('/api/predict/batch', formData)).data;
};

export const getRecyclingMethods = async () => (await api.get('/api/recycling-methods')).data;

export const getResearch = async () => (await api.get('/api/research')).data;
