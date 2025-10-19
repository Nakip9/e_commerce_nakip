import placeholder from '../../assets/placeholder.svg';
import { useEffect } from 'react';
import { useTranslation } from 'react-i18next';
import { useDispatch, useSelector } from 'react-redux';
import { useParams } from 'react-router-dom';

import { addToCart } from '../cart/cartSlice.js';
import { fetchProductById } from './catalogSlice.js';

export function ProductDetailsPage() {
  const { id } = useParams();
  const dispatch = useDispatch();
  const { t } = useTranslation();
  const product = useSelector((state) => state.catalog.products.find((item) => String(item.id) === id));

  useEffect(() => {
    if (!product && id) {
      dispatch(fetchProductById(id));
    }
  }, [dispatch, id, product]);

  if (!product) {
    return <div className="loading">{t('messages.loading')}</div>;
  }

  return (
    <div className="page product-details">
      <div className="details-grid">
        <img src={product.image || placeholder} alt={product.name} className="product-image" />
        <div className="info">
          <h1>{product.name}</h1>
          <p className="price">{t('catalog.priceWithCurrency', { value: product.price })}</p>
          <p>{product.description}</p>
          <p className={product.stock > 0 ? 'in-stock' : 'out-of-stock'}>
            {product.stock > 0 ? t('catalog.inStock') : t('catalog.outOfStock')}
          </p>
          <button type="button" className="btn primary" onClick={() => dispatch(addToCart(product))}>
            {t('actions.addToCart')}
          </button>
        </div>
      </div>
      <section className="reviews">
        <h2>{t('catalog.customerReviews')}</h2>
        {product.reviews?.length ? (
          <ul>
            {product.reviews.map((review) => (
              <li key={review.id}>
                <strong>{review.user}</strong>
                <span>{'⭐'.repeat(review.rating)}</span>
                <p>{review.body}</p>
              </li>
            ))}
          </ul>
        ) : (
          <p>{t('catalog.noReviews')}</p>
        )}
      </section>
    </div>
  );
}
