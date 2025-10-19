# Nakip E-commerce Platform

Nakip is a bilingual (English/Arabic) e-commerce experience built with a modern Django + React stack. The
backend exposes a secure and extensible API while the frontend provides a fast, responsive, and visually
appealing storefront.

## Project Structure

```
.
├── backend/                # Django REST API powering authentication, catalog and orders
│   ├── nakip_backend/      # Project configuration
│   └── apps/               # Domain driven Django apps (accounts, catalog, orders, core)
└── frontend/               # React + Vite single page application
    └── src/
        ├── features/       # Redux slices and page level components
        ├── layout/         # Shell components (header, footer, layout)
        ├── i18n/           # Translations with react-i18next
        └── styles/         # SCSS design system
```

## Key Features

- **Bilingual UI** with instant language toggling (LTR/RTL aware) on the frontend and translated catalog
  content in the backend using `django-modeltranslation`.
- **Responsive design** tuned for desktop, tablet, and mobile breakpoints using modern SCSS.
- **Authentication-ready API** including JWT endpoints, profile management, and registration flow.
- **Rich catalog** models with categories, products, media galleries, and user reviews.
- **Powerful search & filtering** powered by Django filters and Redux-driven client-side search helpers.
- **Shopping cart & checkout foundation** featuring cart management on the frontend and order creation with
  address handling on the backend.
- **SEO-friendly metadata** and clean URLs for product discovery.
- **Security best practices** including JWT authentication, configurable HTTPS enforcement, and CSRF-safe
  defaults.

## Backend (Django)

### Prerequisites

- Python 3.11+
- PostgreSQL 14+ (the default configuration falls back to SQLite for local development)

### Setup

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser  # optional: access Django admin
python manage.py runserver
```

Environment variables can be provided through a `.env` file. Common settings include:

```ini
DJANGO_SECRET_KEY=change-me
DJANGO_DEBUG=true
DB_ENGINE=django.db.backends.postgresql
DB_NAME=nakip
DB_USER=nakip
DB_PASSWORD=super-secret
DB_HOST=localhost
DB_PORT=5432
```

### API Highlights

- `POST /api/accounts/register/` – create a user account
- `POST /api/auth/token/` – obtain JWT access/refresh tokens
- `GET /api/catalog/products/` – list or filter products (`?search=`, `?min_price=`, etc.)
- `GET /api/catalog/products/{id}/` – product details including related images and reviews
- `POST /api/orders/` – create an order with shipping/billing addresses and line items (JWT required)

## Frontend (React + Vite)

### Prerequisites

- Node.js 18+

### Setup

```bash
cd frontend
npm install
npm run dev
```

The development server proxies API calls to `http://localhost:8000`, so ensure the Django server is running.

### State Management & Internationalisation

- Global state is orchestrated using Redux Toolkit slices under `src/features`.
- `react-i18next` powers runtime language switching with translation resources defined in `src/i18n`.
- RTL support is applied automatically when Arabic is active.

## Deployment Notes

- Configure CI to run Django tests (`python manage.py test`) and frontend checks (`npm run build`).
- For production, collect static files (`python manage.py collectstatic`) and build the React app (`npm run build`).
- Recommended hosting: AWS, Heroku, or any container-friendly platform. Use environment variables to point the
  frontend to the deployed API base URL.

## Contributing

1. Fork the repository and create a feature branch.
2. Ensure linting/tests pass.
3. Submit a pull request describing your changes.

Enjoy building delightful commerce experiences with Nakip! 🎉
