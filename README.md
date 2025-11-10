# Super Savers

#### Video Demo: <URL HERE>

## Description

Super Savers is a comprehensive Django-based e-commerce platform designed to connect farmers and vendors directly with customers, featuring a unique group buying system called "Pally" that enables users to purchase products together at discounted prices. The platform provides a full-featured online marketplace with product catalog management, shopping basket functionality, secure payment processing, order tracking, and vendor management capabilities. Built with Django 3.2.8, Bootstrap for responsive design, and jQuery for enhanced user interactions, Super Savers offers both traditional individual product purchases and innovative collaborative buying experiences.

The platform addresses the need for a more accessible and affordable way to purchase agricultural products and groceries by allowing customers to form buying groups. When multiple users join a "Pally" for a specific product, they can split the cost and quantity, making bulk purchases more affordable for individual consumers. This feature is particularly valuable in markets where bulk buying offers significant savings but individual consumers may not need or afford the full quantity.

## Project Structure and File Organization

The project follows Django's app-based architecture, with each application handling a specific domain of functionality. This modular approach ensures separation of concerns, making the codebase maintainable and scalable.

### Account Application (`account/`)

The account application manages user authentication, registration, and profile management. The core component is `models.py`, which defines a custom user model (`UserBase`) that extends Django's `AbstractBaseUser`. This design choice was made to incorporate delivery details directly into the user model, including phone number, postcode, address lines, and town/city information. By embedding delivery information in the user model rather than creating a separate profile model, we ensure that every user account has the necessary fields for order fulfillment without requiring additional joins.

The `views.py` file handles user registration with email activation, login, logout, dashboard access, and profile editing. The registration process includes email verification using token-based activation (`tokens.py`), which enhances security by ensuring users provide valid email addresses before accessing the platform. The `forms.py` file contains form definitions for registration and user editing, utilizing Django Crispy Forms for consistent Bootstrap styling.

### Store Application (`store/`)

The store application is the heart of the e-commerce platform, managing products, categories, and the innovative Pally group buying feature. The `models.py` file defines several key models: `Category` for product organization, `Product` for individual items, `Price` for flexible pricing with units and quantities, `Unit` for measurement standardization, and `Pally` for group buying functionality.

The `Product` model includes features such as seasonal status tracking, discount management, stock status, and automatic slug generation for SEO-friendly URLs. The `Pally` model is particularly sophisticated, tracking the author (creator), available slots, maximum slots, members, expiry dates, and pricing per slot. A custom manager (`PallyManager`) filters active Pallys that have available slots and haven't expired, ensuring users only see viable group buying opportunities.

The `views.py` file provides views for browsing products by category, viewing product details, searching products, and viewing Pally details. The search functionality uses Django's Q objects to search across product titles and descriptions, demonstrating efficient database querying.

### Basket Application (`basket/`)

The basket application implements shopping cart functionality using Django sessions rather than database storage. This design choice was made for performance and user experience reasons: session-based baskets allow users to add items without requiring authentication, and they're automatically cleared when sessions expire, reducing database clutter.

The `basket.py` file contains two classes: `Basket` for regular products and `PallyBasket` for group buying items. `PallyBasket` inherits from `Basket`, demonstrating object-oriented design principles and code reuse. Both classes implement methods for adding, updating, deleting, and calculating totals. The session-based approach requires careful management of session data, with methods ensuring proper serialization and deserialization of product information.

The `views.py` file handles AJAX requests for adding items to baskets, updating quantities, and removing items, providing a seamless user experience without page reloads. The `context_processors.py` file makes basket information available globally across templates, allowing the basket item count to be displayed in the navigation bar on every page.

### Orders Application (`orders/`)

The orders application manages order creation, tracking, and status management. The `models.py` file defines three models: `Order` for the main order record, `OrderItem` for individual product purchases, and `PallyOrderItem` for group buying purchases. This separation allows the system to handle both types of purchases within a single order while maintaining distinct tracking for each.

The order status system includes four states: "Not Yet Shipped", "Shipped", "Cancelled", and "Refunded", providing comprehensive order lifecycle management. The `views.py` file handles order creation from basket contents and provides order history for users. The `payment_confirmation` function updates order billing status when payments are verified, demonstrating integration with the payment system.

### Vendor Application (`vendor/`)

The vendor application provides a comprehensive dashboard for farmers and vendors to manage their businesses on the platform. The `models.py` file defines a `Vendor` model that creates a one-to-one relationship with users, allowing any user to become a vendor while maintaining separate customer and vendor identities.

The `views.py` file implements role-based access control using Django's `user_passes_test` decorator, ensuring only vendors can access vendor-specific views. The application provides functionality for vendor registration, product management (add, edit, delete), Pally management, and order fulfillment tracking. Vendors can view all their products, all active Pallys, and all orders (both regular and Pally orders) with status filtering.

The `forms.py` file contains forms for vendor registration and product creation, including file upload handling for product images. The vendor dashboard uses AdminLTE3 for a professional admin interface, providing vendors with a familiar and feature-rich management experience.

### Payment Application (`payment/`)

The payment application integrates Paystack, a popular payment gateway in Nigeria, for secure payment processing. The `views.py` file implements the payment flow, including payment form rendering, payment verification, and webhook handling for asynchronous payment confirmations.

The webhook implementation (`paystack_webhook`) uses cryptographic signature verification to ensure payment notifications are authentic, demonstrating security best practices. The `unique_order_key_gen.py` file generates unique order identifiers for tracking payments and orders. The payment flow supports both regular product purchases and Pally purchases, with the `order_placed` view handling post-payment processing including Pally activation and member addition.

### General Application (`general/`)

The general application handles static informational pages including About Us, Contact Us, Help Center, Promo/Discount information, and Terms & Conditions. The `views.py` file provides simple render views for these pages, while `forms.py` contains a contact form for customer inquiries. This separation keeps informational content organized and easily maintainable.

### Configuration (`config/`)

The `settings.py` file contains all Django configuration, including database settings, installed apps, middleware, template configuration, and third-party service integrations. Notable configurations include the custom user model specification (`AUTH_USER_MODEL`), session-based basket IDs, Paystack API keys, and email backend configuration. The project is configured for deployment on Heroku with SQLite for development and PostgreSQL support for production.

## Design Decisions and Rationale

Several key design decisions were made during development that significantly impact the platform's functionality and user experience.

**Custom User Model**: Instead of using Django's default User model with a separate Profile model, a custom `UserBase` model was created. This decision was made to integrate delivery information directly into the authentication system, reducing database queries and simplifying order processing. The trade-off is reduced flexibility if delivery requirements change significantly, but the current approach provides better performance and simpler code.

**Session-Based Baskets**: Shopping baskets are stored in Django sessions rather than the database. This allows unauthenticated users to add items to their cart, improving conversion rates. It also reduces database load and automatically handles basket cleanup. The main limitation is that baskets are lost if sessions expire, but this is acceptable given the benefits.

**Separate Pally and Regular Baskets**: While `PallyBasket` inherits from `Basket`, they use separate session keys. This separation was necessary because Pally items have different data structures (tracking slots rather than quantities) and require different processing logic. The inheritance relationship allows code reuse while maintaining distinct functionality.

**Paystack Integration**: Paystack was chosen as the payment gateway because it's widely used in Nigeria (where the platform appears to target based on currency symbols and business context) and provides robust webhook support for payment verification. The webhook implementation ensures payments are confirmed even if users close their browser before the redirect completes.

**Email Activation**: User accounts require email activation before they can log in. This prevents fake accounts, reduces spam, and ensures valid contact information for order communications. While this adds friction to registration, it significantly improves platform quality and security.

**Vendor Dashboard Separation**: Vendors access their management interface through a separate URL namespace (`/farmer/`) with role-based access control. This separation provides security (customers can't accidentally access vendor functions) and allows for different UI/UX optimized for vendor workflows versus customer shopping experiences.

The platform demonstrates a well-architected Django application with clear separation of concerns, thoughtful design decisions, and features that address real-world e-commerce needs while innovating with the group buying concept.


 *Readme was generated with the help of AI. Every other code was written without the use of AI*