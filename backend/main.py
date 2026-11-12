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
def root():
    return {"message": "Welcome to ecommerce-store API. Visit /docs for Swagger UI or /health for status."}

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