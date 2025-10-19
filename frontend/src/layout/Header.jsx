import { useTranslation } from 'react-i18next';
import { Link } from 'react-router-dom';
import { useSelector } from 'react-redux';

import { LanguageSwitcher } from '../components/LanguageSwitcher.jsx';

export function Header() {
  const { t } = useTranslation();
  const cartItems = useSelector((state) => state.cart.items);
  const itemCount = cartItems.reduce((acc, item) => acc + item.quantity, 0);

  return (
    <header className="site-header">
      <div className="container">
        <Link to="/" className="logo" aria-label="Nakip home">
          Nakip
        </Link>
        <nav className="nav-links">
          <Link to="/" className="nav-link">
            {t('navigation.shop')}
          </Link>
          <Link to="/cart" className="nav-link">
            {t('navigation.cart')} ({itemCount})
          </Link>
        </nav>
        <LanguageSwitcher />
      </div>
    </header>
  );
}
