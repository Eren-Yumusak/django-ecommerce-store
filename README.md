# Django E‑Commerce Store

A minimal Django e‑commerce application demonstrating a product catalog, shopping cart, guest + authenticated checkout workflow, and order processing. Built as a portfolio piece to showcase backend fundamentals, clean structure, and extensibility.

## Tech Stack
- Python / Django
- SQLite (dev) via default config in [`ecommerce/ecommerce/settings.py`](ecommerce/ecommerce/settings.py)
- Bootstrap 4 (UI)
- Vanilla JS cart logic (`static/js/cart.js`)
- Django Templating + Static & Media management
- JSON checkout endpoint: [`store.views.processOrder`](ecommerce/store/views.py)

## Key Features
- Product listing with images and pricing
- Session + user-associated cart (supports anonymous + authenticated flows)
- Dynamic cart quantity adjustments (client-side JS + server reconciliation)
- Guest checkout path (graceful upgrade if user registers later)
- Order + OrderItem persistence and shipping flag handling
- Media + static separation (`STATICFILES_DIRS`, `MEDIA_ROOT` in settings)
- Simple transaction integrity check in checkout (`total == order.get_cart_total`)

## Repository Structure (trimmed)
```
e-commerce/
  ecommerce/                 # Django project package
    ecommerce/               # (inner settings package)
      settings.py
      urls.py
    store/                   # Core app (products, orders, views)
      views.py
      templates/store/
    static/
      css/main.css
      js/cart.js
  README.md
  .gitignore
```

(If you still have a nested duplicate folder, flatten so only one "ecommerce" package exists.)

## How the Cart & Checkout Work
1. Browsing: Product data rendered in templates (e.g. `Main.html`).
2. Cart Updates: JS sends AJAX-like interactions to update local cart (for guests) or server session/db for authenticated users.
3. Checkout Submit: Frontend compiles form + cart state into JSON and posts to [`processOrder`](ecommerce/store/views.py).
4. Validation: `processOrder` re-calculates authoritative totals (`order.get_cart_total`) before marking `order.complete = True`.
5. Shipping: Conditional creation of `ShippingAddress` when `order.shipping` is true.

## Notable Code References
- Global settings & static/media config: [`ecommerce/ecommerce/settings.py`](ecommerce/ecommerce/settings.py)
- Order finalization endpoint: [`store.views.processOrder`](ecommerce/store/views.py)
- Core stylesheet: [`static/css/main.css`](ecommerce/static/css/main.css)

## Getting Started
```bash
git clone https://github.com/your-user/django-ecommerce-store.git
cd django-ecommerce-store

# (Optional) Create virtual environment
python -m venv venv
venv\Scripts\activate  # Windows

pip install -r requirements.txt  # (create one if not present)
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Visit: http://127.0.0.1:8000/

## Environment / Secrets
Create `.env` (or export vars) and override in `settings.py` if you later deploy:
```
SECRET_KEY=replace-this
DEBUG=False
ALLOWED_HOSTS=yourdomain.com
```
Do not commit real secrets.

## Testing (Add Later)
Potential directions:
- Model tests for Order / OrderItem totals
- View tests for cart + checkout
- Integration test simulating guest checkout flow

## Potential Enhancements (Talking Points)
- Replace SQLite with Postgres; add Docker.
- Payment integration (Stripe) in a `payments` app.
- Inventory tracking + low-stock signals.
- REST or GraphQL API layer (Django REST Framework).
- Caching layer for product listing (Redis).
- CI pipeline (GitHub Actions) + test coverage badge.
- Image optimization / S3 offloading.

## Why This Project
Demonstrates:
- Clean separation of concerns (views, templates, static assets)
- Secure server-side total validation (prevents client tampering)
- Support for both guest and authenticated user carts
- Extensible foundation for real commerce features

## Screenshots (Optional)
(Add screenshots of catalog, cart, checkout.)

## License
MIT (adjust if needed).

## Recruiter / Interview Notes
Discuss how you would:
- Introduce payments safely (idempotent webhooks)
- Harden security (CSRF everywhere except validated JSON endpoints)
- Scale static/media via CDN
- Add automated order confirmation emails

---
> Built as a demonstration project. Not production-secured.
