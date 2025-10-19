import { createAsyncThunk, createSlice } from '@reduxjs/toolkit';

import client from '../../api/client.js';

const ACCESS_KEY = 'nakip_access_token';
const REFRESH_KEY = 'nakip_refresh_token';

const initialState = {
  user: null,
  status: 'idle',
  error: null,
  accessToken: localStorage.getItem(ACCESS_KEY),
  refreshToken: localStorage.getItem(REFRESH_KEY),
};

export const login = createAsyncThunk('auth/login', async (credentials) => {
  const response = await client.post('/auth/token/', credentials);
  return response.data;
});

export const refresh = createAsyncThunk('auth/refresh', async (_, { getState }) => {
  const refreshToken = getState().auth.refreshToken;
  if (!refreshToken) {
    throw new Error('Missing refresh token');
  }
  const response = await client.post('/auth/token/refresh/', { refresh: refreshToken });
  return response.data;
});

export const fetchProfile = createAsyncThunk('auth/profile', async () => {
  const response = await client.get('/accounts/profile/');
  return response.data;
});

const authSlice = createSlice({
  name: 'auth',
  initialState,
  reducers: {
    logout: (state) => {
      state.user = null;
      state.accessToken = null;
      state.refreshToken = null;
      localStorage.removeItem(ACCESS_KEY);
      localStorage.removeItem(REFRESH_KEY);
    },
  },
  extraReducers: (builder) => {
    builder
      .addCase(login.pending, (state) => {
        state.status = 'loading';
      })
      .addCase(login.fulfilled, (state, action) => {
        state.status = 'succeeded';
        state.accessToken = action.payload.access;
        state.refreshToken = action.payload.refresh;
        localStorage.setItem(ACCESS_KEY, action.payload.access);
        localStorage.setItem(REFRESH_KEY, action.payload.refresh);
      })
      .addCase(login.rejected, (state, action) => {
        state.status = 'failed';
        state.error = action.error.message;
      })
      .addCase(refresh.fulfilled, (state, action) => {
        state.accessToken = action.payload.access;
        localStorage.setItem(ACCESS_KEY, action.payload.access);
      })
      .addCase(fetchProfile.fulfilled, (state, action) => {
        state.user = action.payload;
      });
  },
});

export const { logout } = authSlice.actions;

export default authSlice.reducer;
