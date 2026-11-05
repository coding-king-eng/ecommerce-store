# ecommerce-store — Core UI Wireframes (Day 2)

Below are the 4 low-fidelity screen wireframes designed for our Jetpack Compose Android client (`Login`, `Main Product List`, `Product Detail`, and `Admin Dashboard`).

---

## Screen 1: Login & Role Auth Screen (`AuthScreen.kt`)

+------------------------------------------+
|  9:41                           5G  100% |
+------------------------------------------+
|                                          |
|              [ Store Logo ]              |
|             ecommerce-store              |
|     Full-Stack Shopping Experience       |
|                                          |
|  Email Address                           |
|  +------------------------------------+  |
|  | shorya@example.com                 |  |
|  +------------------------------------+  |
|                                          |
|  Password                                |
|  +------------------------------------+  |
|  | ••••••••••••                   [👁] |  |
|  +------------------------------------+  |
|                                          |
|  +------------------------------------+  |
|  |             LOG IN                 |  |
|  +------------------------------------+  |
|                                          |
|      Don't have an account? Sign Up      |
|                                          |
|  --------------------------------------  |
|  Demo Quick-Fill: [Customer] | [Admin]   |
+------------------------------------------+

---

## Screen 2: Main Product Catalogue (`ProductListScreen.kt`)

+------------------------------------------+
|  ecommerce-store             [🛒 Cart (2)]|
+------------------------------------------+
|  [ 🔍 Search products...              ]  |
|                                          |
|  (All)  (Electronics)  (Apparel) (Books) |
+------------------------------------------+
|  +----------------+  +----------------+  |
|  |  [ Product 1 ] |  |  [ Product 2 ] |  |
|  |    Image       |  |    Image       |  |
|  +----------------+  +----------------+  |
|  Wireless Headset    Mechanical Keybd    |
|  ₹2,499   [+ Add]    ₹3,999   [+ Add]    |
|                                          |
|  +----------------+  +----------------+  |
|  |  [ Product 3 ] |  |  [ Product 4 ] |  |
|  |    Image       |  |    Image       |  |
|  +----------------+  +----------------+  |
|  USB-C Hub 7-in-1    Laptop Stand Alu    |
|  ₹1,299   [+ Add]    ₹899     [+ Add]    |
+------------------------------------------+
|  [🏠 Home]   [📦 Orders]   [👤 Profile]  |
+------------------------------------------+

---

## Screen 3: Product Detail Screen (`ProductDetailScreen.kt`)

+------------------------------------------+
|  [<- Back]        Product Details   [🛒] |
+------------------------------------------+
|  +------------------------------------+  |
|  |                                    |  |
|  |        Large Product Image         |  |
|  |            (Coil Async)            |  |
|  |                                    |  |
|  +------------------------------------+  |
|  Category: Electronics     [In Stock: 14]|
|                                          |
|  Pro Wireless ANC Headphones             |
|  ₹2,499.00                               |
|                                          |
|  Description:                            |
|  40mm dynamic drivers, 35-hour battery   |
|  life, USB-C fast charging, and low      |
|  latency mode for gaming & coding.       |
|                                          |
|  Quantity:  [-]  1  [+]                  |
|                                          |
|  +------------------------------------+  |
|  |       ADD TO CART  (₹2,499)        |  |
|  +------------------------------------+  |
+------------------------------------------+

---

## Screen 4: Admin Inventory & Order Dashboard (`AdminDashboardScreen.kt`)

+------------------------------------------+
|  Admin Panel                [+ New Item] |
+------------------------------------------+
|  [ Products (24) ]  |  [ Orders (12) ]   |
+------------------------------------------+
|  Total Revenue: ₹48,250  | Low Stock: 2  |
+------------------------------------------+
|  1. Pro Wireless Headphones              |
|     ₹2,499  •  Stock: 14                 |
|     [ ✏️ Edit ]          [ 🗑️ Delete ]   |
|  --------------------------------------  |
|  2. Mechanical Keyboard RGB              |
|     ₹3,999  •  Stock: 3 (LOW)            |
|     [ ✏️ Edit ]          [ 🗑️ Delete ]   |
|  --------------------------------------  |
|  3. USB-C Multiport Adapter              |
|     ₹1,299  •  Stock: 28                 |
|     [ ✏️ Edit ]          [ 🗑️ Delete ]   |
+------------------------------------------+