import placeholder from '../../assets/placeholder.svg';
import { useTranslation } from 'react-i18next';
import { useSelector } from 'react-redux';
import { Link } from 'react-router-dom';

import { useSearch } from '../../hooks/useSearch.js';

export function ProductListPage() {
  const { t } = useTranslation();
  const { query, setQuery, filteredItems } = useSearch();
  const status = useSelector((state) => state.catalog.status);
  const error = useSelector((state) => state.catalog.error);

  if (status === 'loading') {
    return <div className="loading">{t('messages.loading')}</div>;
  }

  if (status === 'failed') {
    return <div className="error">{error}</div>;
  }

  return (
    <div className="page product-list">
      <div className="page-header">
        <h1>{t('catalog.featuredProducts')}</h1>
        <input
          type="search"
          value={query}
          onChange={(event) => setQuery(event.target.value)}
          placeholder={t('catalog.searchPlaceholder')}
          className="search-input"
        />
      </div>
      {filteredItems.length === 0 ? (
        <p className="empty-state">{t('catalog.noResults')}</p>
      ) : (
        <div className="grid">
          {filteredItems.map((product) => (
            <article key={product.id} className="product-card">
              <img src={product.image || placeholder} alt={product.name} loading="lazy" />
              <h2>{product.name}</h2>
              <p className="price">{t('catalog.priceWithCurrency', { value: product.price })}</p>
              <Link to={`/products/${product.id}`} className="btn">
                {t('actions.viewDetails')}
              </Link>
            </article>
          ))}
        </div>
      )}
    </div>
  );
}
