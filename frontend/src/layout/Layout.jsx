import { Outlet } from 'react-router-dom';

import { Header } from './Header.jsx';
import { Footer } from './Footer.jsx';

export function Layout({ children }) {
  return (
    <div className="app-container">
      <Header />
      <main className="main-content">{children ?? <Outlet />}</main>
      <Footer />
    </div>
  );
}
