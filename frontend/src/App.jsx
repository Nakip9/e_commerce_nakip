import { Suspense, useEffect } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { Route, Routes } from 'react-router-dom';

import { Layout } from './layout/Layout.jsx';
import { ProductListPage } from './features/catalog/ProductListPage.jsx';
import { ProductDetailsPage } from './features/catalog/ProductDetailsPage.jsx';
import { CartPage } from './features/cart/CartPage.jsx';
import { fetchProducts } from './features/catalog/catalogSlice.js';
import { fetchProfile } from './features/auth/authSlice.js';

export default function App() {
  const dispatch = useDispatch();
  const catalogStatus = useSelector((state) => state.catalog.status);
  const accessToken = useSelector((state) => state.auth.accessToken);

  useEffect(() => {
    if (catalogStatus === 'idle') {
      dispatch(fetchProducts());
    }
  }, [dispatch, catalogStatus]);

  useEffect(() => {
    if (accessToken) {
      dispatch(fetchProfile());
    }
  }, [dispatch, accessToken]);

  return (
    <Suspense fallback={<div className="loading">Loading...</div>}>
      <Layout>
        <Routes>
          <Route path="/" element={<ProductListPage />} />
          <Route path="/products/:id" element={<ProductDetailsPage />} />
          <Route path="/cart" element={<CartPage />} />
        </Routes>
      </Layout>
    </Suspense>
  );
}
