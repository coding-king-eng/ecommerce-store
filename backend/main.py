from auth import hash_password, verify_password
from security import create_access_token
from schemas import UserCreate, UserResponse, UserLogin, Token
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy import text
from database import engine, Base, get_db
from models import User
from schemas import UserCreate, UserResponse
from auth import hash_password
from schemas import UserCreate, UserResponse, UserLogin, Token, CategoryCreate, CategoryResponse
from models import User, Category, Product
from schemas import UserCreate, UserResponse, UserLogin, Token, CategoryCreate, CategoryResponse, ProductCreate, ProductResponse
from schemas import UserCreate, UserResponse, UserLogin, Token, CategoryCreate, CategoryResponse, ProductCreate, ProductResponse, ProductUpdate
from fastapi.responses import FileResponse
from pathlib import Path
from fastapi.responses import FileResponse
from pathlib import Path
from schemas import UserCreate, UserResponse, UserLogin, Token, CategoryCreate, CategoryResponse, ProductCreate, ProductResponse, ProductUpdate


Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="ecommerce-store REST API",
    description="Full-Stack E-Commerce Backend for ALTA Builder 30 (Track A)",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
@app.get("/")
def serve_frontend():
    return FileResponse(Path(__file__).parent / "index.html")

@app.get("/health")
def health_check(db: Session = Depends(get_db)):
    db.execute(text("SELECT 1"))
    return {
        "status": "OK",
        "database": "connected",
        "service": "ecommerce-store-backend"
    }

@app.post("/api/auth/signup", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def signup(user_data: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.email == user_data.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email is already registered with another account."
        )

    hashed_pwd = hash_password(user_data.password)

    new_user = User(
        name=user_data.name,
        email=user_data.email,
        password_hash=hashed_pwd,
        role=user_data.role
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user
@app.post("/api/auth/login", response_model=Token)
def login(credentials: UserLogin, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == credentials.email).first()
    if not user or not verify_password(credentials.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_access_token(data={"sub": user.email, "role": user.role})
    return {"access_token": access_token, "token_type": "bearer"}
@app.post("/api/categories", response_model=CategoryResponse, status_code=status.HTTP_201_CREATED)
def create_category(category_data: CategoryCreate, db: Session = Depends(get_db)):
    existing = db.query(Category).filter(Category.name == category_data.name).first()
    if existing:
        raise HTTPException(status_code=400, detail="Category already exists")

    new_category = Category(name=category_data.name, description=category_data.description)
    db.add(new_category)
    db.commit()
    db.refresh(new_category)
    return new_category

@app.get("/api/categories", response_model=list[CategoryResponse])
def get_categories(db: Session = Depends(get_db)):
    return db.query(Category).all()
@app.post("/api/products", response_model=ProductResponse, status_code=status.HTTP_201_CREATED)
def create_product(product_data: ProductCreate, db: Session = Depends(get_db)):
    # Verify category exists
    category = db.query(Category).filter(Category.id == product_data.category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")

    new_product = Product(
        name=product_data.name,
        description=product_data.description,
        price=product_data.price,
        stock=product_data.stock,
        category_id=product_data.category_id
    )
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return new_product

@app.get("/api/products", response_model=list[ProductResponse])
def get_products(
    category_id: int | None = None,
    search: str | None = None,
    db: Session = Depends(get_db)
):
    query = db.query(Product)

    # Filter by category if provided
    if category_id:
        query = query.filter(Product.category_id == category_id)

    # Search by product name (case-insensitive) if provided
    if search:
        query = query.filter(Product.name.ilike(f"%{search}%"))

    return query.all()
@app.get("/api/products/{product_id}", response_model=ProductResponse)
def get_product_by_id(product_id: int, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


@app.put("/api/products/{product_id}", response_model=ProductResponse)
def update_product(product_id: int, product_data: ProductUpdate, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    if product_data.category_id is not None:
        category = db.query(Category).filter(Category.id == product_data.category_id).first()
        if not category:
            raise HTTPException(status_code=404, detail="Category not found")
        product.category_id = product_data.category_id

    if product_data.name is not None:
        product.name = product_data.name
    if product_data.description is not None:
        product.description = product_data.description
    if product_data.price is not None:
        product.price = product_data.price
    if product_data.stock is not None:
        product.stock = product_data.stock

    db.commit()
    db.refresh(product)
    return product


@app.delete("/api/products/{product_id}", status_code=status.HTTP_200_OK)
def delete_product(product_id: int, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    db.delete(product)
    db.commit()
    return {"message": f"Product with id {product_id} has been deleted successfully"}
@app.post("/api/seed")
def seed_demo_data(db: Session = Depends(get_db)):
    """Automatically populates the store with categories and products if empty."""
    starter_cats = [
        {"name": "Tech & Gadgets", "description": "Premium electronics and accessories"},
        {"name": "Gaming Gear", "description": "Pro gaming peripherals and headsets"},
        {"name": "Instant Cravings", "description": "Quick snacks, coffee and beverages"},
        {"name": "Campus Essentials", "description": "Backpacks, bottles and daily gear"}
    ]

    cat_map = {}
    for c in starter_cats:
        existing = db.query(Category).filter(Category.name == c["name"]).first()
        if not existing:
            existing = Category(name=c["name"], description=c["description"])
            db.add(existing)
            db.commit()
            db.refresh(existing)
        cat_map[c["name"]] = existing.id

    if db.query(Product).count() <= 1:
        demo_products = [
            {
                "name": "Apple iPhone 16 Pro (Titanium)",
                "description": "A18 Pro chip, 48MP Pro camera system, 120Hz ProMotion OLED display |IMG|https://images.unsplash.com/photo-1695048133142-1a20484d2569?w=600&q=80",
                "price": 119900,
                "stock": 8,
                "category_id": cat_map["Tech & Gadgets"]
            },
            {
                "name": "Sony WH-1000XM5 ANC Headphones",
                "description": "Industry-leading noise cancellation, 30-hour battery life & crystal clear calls |IMG|https://images.unsplash.com/photo-1618366712010-f4ae9c647dcb?w=600&q=80",
                "price": 26990,
                "stock": 15,
                "category_id": cat_map["Tech & Gadgets"]
            },
            {
                "name": "RGB Mechanical Gaming Keyboard",
                "description": "Hot-swappable tactile switches, per-key RGB backlighting & aluminum frame |IMG|https://images.unsplash.com/photo-1595225476474-87563907a212?w=600&q=80",
                "price": 3499,
                "stock": 22,
                "category_id": cat_map["Gaming Gear"]
            },
            {
                "name": "Ultra-Light Wireless Gaming Mouse",
                "description": "26,000 DPI optical sensor, 58g ultra-lightweight honeycomb shell |IMG|https://images.unsplash.com/photo-1615663245857-ac93bb7c39e7?w=600&q=80",
                "price": 2199,
                "stock": 18,
                "category_id": cat_map["Gaming Gear"]
            },
            {
                "name": "Starbucks Frappuccino Cold Coffee",
                "description": "Chilled Arabica coffee blend with creamy milk, served ice cold in 10 mins |IMG|https://images.unsplash.com/photo-1461023058943-07fcbe16d735?w=600&q=80",
                "price": 280,
                "stock": 40,
                "category_id": cat_map["Instant Cravings"]
            },
            {
                "name": "Dark Chocolate Protein Energy Bar (Pack of 6)",
                "description": "20g protein per bar, zero added sugar, perfect for late-night coding |IMG|https://images.unsplash.com/photo-1622484211148-716598e04b1f?w=600&q=80",
                "price": 540,
                "stock": 35,
                "category_id": cat_map["Instant Cravings"]
            },
            {
                "name": "20000mAh 65W Fast-Charge Power Bank",
                "description": "Charges MacBook & phones at blazing speed with dual Type-C PD ports |IMG|https://images.unsplash.com/photo-1609091839311-d5365f9ff1c5?w=600&q=80",
                "price": 1899,
                "stock": 12,
                "category_id": cat_map["Tech & Gadgets"]
            },
            {
                "name": "Matte Black Insulated Tech Backpack",
                "description": "Water-resistant 16-inch laptop compartment with built-in USB charging port |IMG|https://images.unsplash.com/photo-1553062407-98eeb64c6a62?w=600&q=80",
                "price": 1599,
                "stock": 25,
                "category_id": cat_map["Campus Essentials"]
            }
        ]
        for p in demo_products:
            db.add(Product(**p))
        db.commit()

    return {"message": "Store stocked with products!"}