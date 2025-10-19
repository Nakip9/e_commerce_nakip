import { useState } from 'react';
import { useTranslation } from 'react-i18next';
import { useDispatch, useSelector } from 'react-redux';

import client from '../../api/client.js';
import { clearCart, removeFromCart, updateQuantity } from './cartSlice.js';

const initialAddress = {
  line1: '',
  line2: '',
  city: '',
  state: '',
  postal_code: '',
  country: '',
  phone_number: '',
};

export function CartPage() {
  const { t } = useTranslation();
  const dispatch = useDispatch();
  const items = useSelector((state) => state.cart.items);
  const isAuthenticated = useSelector((state) => Boolean(state.auth.accessToken));
  const subtotal = items.reduce((acc, item) => acc + item.price * item.quantity, 0);

  const [shippingAddress, setShippingAddress] = useState({ ...initialAddress });
  const [billingAddress, setBillingAddress] = useState({ ...initialAddress });
  const [shippingMethod, setShippingMethod] = useState('standard');
  const [status, setStatus] = useState('idle');
  const [error, setError] = useState(null);
  const [orderId, setOrderId] = useState(null);

  const shippingCost = shippingMethod === 'express' ? 15 : 0;
  const total = subtotal + shippingCost;

  const handleAddressChange = (event, type) => {
    const { name, value } = event.target;
    if (type === 'shipping') {
      setShippingAddress((prev) => ({ ...prev, [name]: value }));
    } else {
      setBillingAddress((prev) => ({ ...prev, [name]: value }));
    }
  };

  const handleCheckout = async (event) => {
    event.preventDefault();
    if (!isAuthenticated) {
      setError(t('cart.loginRequired'));
      return;
    }
    if (items.length === 0) {
      setError(t('cart.empty'));
      return;
    }

    setStatus('loading');
    setError(null);
    setOrderId(null);

    try {
      const payload = {
        shipping_cost: shippingCost,
        items: items.map((item) => ({
          product: item.id,
          quantity: item.quantity,
        })),
        shipping_address: shippingAddress,
        billing_address: billingAddress,
      };
      const response = await client.post('/orders/', payload);
      setOrderId(response.data.id);
      setStatus('succeeded');
      setShippingAddress({ ...initialAddress });
      setBillingAddress({ ...initialAddress });
      dispatch(clearCart());
    } catch (checkoutError) {
      setStatus('failed');
      const apiMessage = checkoutError.response?.data?.detail || checkoutError.response?.data?.non_field_errors?.[0];
      setError(apiMessage || checkoutError.message);
    }
  };

  return (
    <div className="page cart-page">
      <h1>{t('cart.title')}</h1>
      {items.length === 0 ? (
        <p>{t('cart.empty')}</p>
      ) : (
        <div className="cart-table">
          <table>
            <thead>
              <tr>
                <th>{t('cart.product')}</th>
                <th>{t('cart.price')}</th>
                <th>{t('cart.quantity')}</th>
                <th>{t('cart.total')}</th>
                <th />
              </tr>
            </thead>
            <tbody>
              {items.map((item) => (
                <tr key={item.id}>
                  <td>{item.name}</td>
                  <td>{t('catalog.priceWithCurrency', { value: item.price })}</td>
                  <td>
                    <input
                      type="number"
                      min={1}
                      value={item.quantity}
                      onChange={(event) =>
                        dispatch(updateQuantity({ id: item.id, quantity: Number(event.target.value) }))
                      }
                    />
                  </td>
                  <td>{t('catalog.priceWithCurrency', { value: item.price * item.quantity })}</td>
                  <td>
                    <button type="button" className="link" onClick={() => dispatch(removeFromCart(item.id))}>
                      {t('actions.remove')}
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
          <div className="summary">
            <p>
              <strong>{t('cart.subtotal')}:</strong> {t('catalog.priceWithCurrency', { value: subtotal })}
            </p>
            <p>
              <strong>{t('cart.shipping')}:</strong> {t('catalog.priceWithCurrency', { value: shippingCost })}
            </p>
            <p>
              <strong>{t('cart.total')}:</strong> {t('catalog.priceWithCurrency', { value: total })}
            </p>
          </div>
        </div>
      )}

      {items.length > 0 && (
        <form className="checkout-form" onSubmit={handleCheckout}>
          <h2>{t('cart.checkout')}</h2>
          <div className="form-grid">
            <fieldset>
              <legend>{t('cart.shippingAddress')}</legend>
              <AddressFields
                values={shippingAddress}
                onChange={(event) => handleAddressChange(event, 'shipping')}
                t={t}
              />
            </fieldset>
            <fieldset>
              <legend>{t('cart.billingAddress')}</legend>
              <AddressFields
                values={billingAddress}
                onChange={(event) => handleAddressChange(event, 'billing')}
                t={t}
              />
            </fieldset>
          </div>

          <div className="form-row">
            <label htmlFor="shipping-method">{t('cart.shippingMethod')}</label>
            <select
              id="shipping-method"
              value={shippingMethod}
              onChange={(event) => setShippingMethod(event.target.value)}
            >
              <option value="standard">{t('cart.standardShipping')}</option>
              <option value="express">{t('cart.expressShipping')}</option>
            </select>
          </div>

          <div className="form-row">
            <label htmlFor="payment-method">{t('cart.paymentMethod')}</label>
            <select id="payment-method" defaultValue="card">
              <option value="card">{t('cart.creditCard')}</option>
              <option value="paypal">{t('cart.paypal')}</option>
              <option value="cod">{t('cart.cashOnDelivery')}</option>
            </select>
          </div>

          {error && <p className="error">{error}</p>}
          {orderId && <p className="success">{t('cart.orderSuccess', { orderId })}</p>}

          <button type="submit" className="btn primary" disabled={status === 'loading'}>
            {status === 'loading' ? t('cart.processing') : t('cart.proceedToCheckout')}
          </button>
        </form>
      )}
    </div>
  );
}

function AddressFields({ values, onChange, t }) {
  return (
    <div className="address-fields">
      <label>
        {t('cart.addressLine1')}
        <input name="line1" value={values.line1} onChange={onChange} required />
      </label>
      <label>
        {t('cart.addressLine2')}
        <input name="line2" value={values.line2} onChange={onChange} />
      </label>
      <label>
        {t('cart.city')}
        <input name="city" value={values.city} onChange={onChange} required />
      </label>
      <label>
        {t('cart.state')}
        <input name="state" value={values.state} onChange={onChange} />
      </label>
      <label>
        {t('cart.postalCode')}
        <input name="postal_code" value={values.postal_code} onChange={onChange} required />
      </label>
      <label>
        {t('cart.country')}
        <input name="country" value={values.country} onChange={onChange} required />
      </label>
      <label>
        {t('cart.phoneNumber')}
        <input name="phone_number" value={values.phone_number} onChange={onChange} />
      </label>
    </div>
  );
}
