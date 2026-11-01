# ecommerce-store — Full-Stack E-Commerce Platform (ALTA BUILDER 30 - Track A)

## 1. Problem Statement
Independent single-brand retailers and campus creators often struggle with high commissions on third-party marketplaces or clunky, unverified checkout flows on social media. **ecommerce-store** is a dedicated, full-stack e-commerce platform (Android Jetpack Compose client + REST API backend) that allows customers to seamlessly browse categorized products, manage a persistent cart, and complete verified digital payments via Razorpay (Test Mode), while giving store administrators complete role-based control over inventory, pricing, and order fulfillment.

## 2. User Roles
1. **Customer (`ROLE_CUSTOMER`):**
    - Can register, log in, browse products by category, search items, view detailed product pages, manage a persistent shopping cart, complete checkout via Razorpay test payments, and track past order history.
2. **Admin (`ROLE_ADMIN`):**
    - Has full access to the Admin Panel to create, update, and delete products, manage stock levels, view all customer orders, and update order fulfillment statuses.

## 3. MVP Features (Days 1–12 Must-Haves)
1. **JWT Authentication & Security:** Secure Signup and Login APIs with `bcrypt` password hashing and JWT bearer token middleware protecting private routes.
2. **Role-Based Access Control (RBAC):** Middleware separating Customer actions from Admin catalogue/order management endpoints.
3. **Product Catalogue with Categories & Search:** Paginated product listing supporting keyword search and category filtering.
4. **Product Detail View:** Rich product screen displaying high-res images, description, price, category, and real-time stock availability.
5. **Persistent Shopping Cart:** Cart state backed by the database/local persistence so items survive app restarts and screen refreshes.
6. **Order Placement & Order History:** Customer view of all completed orders with itemized totals, timestamps, and payment status.
7. **Admin Product & Order Dashboard:** Dedicated UI and CRUD endpoints for Admins to add, edit, and delete products and inspect orders.
8. **Heavy Feature (Days 11–12) — Verified Payment Gateway Integration:** End-to-end checkout using **Razorpay Test Mode**. Orders are confirmed only after cryptographic payment signature verification succeeds; failed or cancelled payments are gracefully handled and logged without deducting inventory.

## 4. Later Features (Post-MVP / Nice-to-Haves)
- **Product Reviews & Star Ratings:** Verified buyers can leave a 1–5 star rating and text review.
- **Wishlist / Saved Items:** Customers can bookmark products for later purchase.
- **Discount Coupons:** Promo code engine applying percentage or flat discounts at checkout.
- **Low-Stock Push Notifications:** Alerts for the Admin when a product's stock drops below 5 units.

## 5. Tech Stack
- **Client UI:** Kotlin, Jetpack Compose, Material 3, Retrofit2, OkHttp, Coil (Image Loading), Razorpay Checkout SDK (Android Studio).
- **Backend API:** Python FastAPI, SQLAlchemy ORM, Pydantic validation, JWT (`python-jose` + `passlib[bcrypt]`).
- **Database:** PostgreSQL (SQLite for local dev, Neon.tech / Supabase PostgreSQL for production).
- **Deployment:** Render / Railway (Backend API) + GitHub Releases APK & Web Preview.
-