import { configureStore } from '@reduxjs/toolkit';

import authReducer from '../features/auth/authSlice.js';
import catalogReducer from '../features/catalog/catalogSlice.js';
import cartReducer from '../features/cart/cartSlice.js';

export const store = configureStore({
  reducer: {
    auth: authReducer,
    catalog: catalogReducer,
    cart: cartReducer,
  },
});
