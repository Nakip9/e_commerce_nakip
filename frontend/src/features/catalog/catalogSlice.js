import { createAsyncThunk, createSlice } from '@reduxjs/toolkit';

import client from '../../api/client.js';

const initialState = {
  products: [],
  status: 'idle',
  error: null,
};

export const fetchProducts = createAsyncThunk('catalog/fetchProducts', async (params = {}) => {
  const response = await client.get('/catalog/products/', { params });
  return response.data.results || response.data;
});

export const fetchProductById = createAsyncThunk('catalog/fetchProductById', async (id) => {
  const response = await client.get(`/catalog/products/${id}/`);
  return response.data;
});

const catalogSlice = createSlice({
  name: 'catalog',
  initialState,
  reducers: {},
  extraReducers: (builder) => {
    builder
      .addCase(fetchProducts.pending, (state) => {
        state.status = 'loading';
      })
      .addCase(fetchProducts.fulfilled, (state, action) => {
        state.status = 'succeeded';
        state.products = action.payload;
      })
      .addCase(fetchProducts.rejected, (state, action) => {
        state.status = 'failed';
        state.error = action.error.message;
      })
      .addCase(fetchProductById.fulfilled, (state, action) => {
        const product = action.payload;
        const existing = state.products.find((item) => item.id === product.id);
        if (existing) {
          Object.assign(existing, product);
        } else {
          state.products.push(product);
        }
      });
  },
});

export default catalogSlice.reducer;
