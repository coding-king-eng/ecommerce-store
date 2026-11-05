# ecommerce-store — Database Schema & Data Modelling (Day 2)

## 1. Entity-Relationship (ER) Diagram

erDiagram
    USERS ||--o{ CART_ITEMS : "maintains"
    USERS ||--o{ ORDERS : "places"
    CATEGORIES ||--o{ PRODUCTS : "categorizes"
    PRODUCTS ||--o{ CART_ITEMS : "added_to"
    ORDERS ||--|{ ORDER_ITEMS : "contains"
    PRODUCTS ||--o{ ORDER_ITEMS : "purchased_in"

    USERS {
        int id PK "Auto-increment Primary Key"
        string name "Full Name"
        string email UK "Unique Email for Login"
        string password_hash "Bcrypt Hashed Password"
        string role "CUSTOMER | ADMIN"
        datetime created_at "Registration Timestamp"
    }

    CATEGORIES {
        int id PK
        string name UK "e.g., Electronics, Apparel, Books"
        string slug UK
    }

    PRODUCTS {
        int id PK
        string title "Product Name"
        text description "Detailed Specs"
        decimal price "Unit Price in INR"
        int stock "Available Inventory Count"
        string image_url "Product Thumbnail/Banner URL"
        int category_id FK "References CATEGORIES(id)"
        datetime created_at
    }

    CART_ITEMS {
        int id PK
        int user_id FK "References USERS(id)"
        int product_id FK "References PRODUCTS(id)"
        int quantity "Must be >= 1 and <= product.stock"
    }

    ORDERS {
        int id PK
        int user_id FK "References USERS(id)"
        decimal total_amount "Total Order Value in INR"
        string payment_status "PENDING | PAID | FAILED"
        string razorpay_order_id "Razorpay Order Reference"
        string razorpay_payment_id "Verified Payment ID"
        datetime created_at
    }

    ORDER_ITEMS {
        int id PK
        int order_id FK "References ORDERS(id)"
        int product_id FK "References PRODUCTS(id)"
        int quantity "Quantity Purchased"
        decimal unit_price "Price Snapshot at Purchase Time"
    }

## 2. Key Relational Design Decisions
1. **Price Snapshot in `ORDER_ITEMS`:** Storing `unit_price` on `ORDER_ITEMS` ensures historical order totals remain accurate even if an Admin later changes a product's price in `PRODUCTS`.
2. **Persistent Cart (`CART_ITEMS`):** Linked directly to `user_id` so the user's cart survives app restarts or device switches.
3. **Payment Verification State (`ORDERS`):** Orders start as `PENDING` when initialized and only transition to `PAID` (with stock deduction) after Razorpay signature verification succeeds on Days 11–12.