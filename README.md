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

## Screenshots
<img width="1917" height="887" alt="image" src="https://github.com/user-attachments/assets/6b7ab0a1-1966-498a-b747-b938bf56d99c" />
<img width="1918" height="906" alt="image" src="https://github.com/user-attachments/assets/9853905c-185d-42aa-8a73-6c4ae4826557" />
<img width="1919" height="905" alt="image" src="https://github.com/user-attachments/assets/5b335fe1-2a71-4ae2-84df-8355469d2b56" />



