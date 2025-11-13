# SellnService - Vehicle Management & Service Platform

A comprehensive Django REST Framework application for vehicle fleet management, featuring unit tracking, service scheduling, sales management, and real-time chat communication with WebSocket support.

## 🚀 Key Features

- **User Authentication & Security**
  - JWT-based authentication with token rotation
  - Email verification with OTP
  - Password reset with secure OTP codes
  - Token blacklisting for logout
  
- **Vehicle (Unit) Management**
  - Complete vehicle tracking with VIN validation
  - Multiple status tracking (Active, Sold, In Service, Inactive)
  - Vehicle details: brand, model, year, mileage, location
  - Image uploads for vehicles
  
- **Service Management**
  - Schedule and track vehicle services
  - Service status workflow (Scheduled → In Progress → Completed)
  - Cost tracking and service history
  - Appointment scheduling
  
- **Sales Management**
  - Record vehicle sales with buyer information
  - Automatic unit status updates on sale
  - Payment method tracking
  - Sales history and reporting
  
- **Real-time Chat System**
  - WebSocket-based live messaging
  - User-to-Admin communication channels
  - Chat rooms linked to specific units, services, or sales
  - Message read status tracking
  - Unread message counters
  
- **Admin Content Management**
  - Privacy Policy management
  - Terms & Conditions versioning
  - About Us content
  
- **Media Management**
  - Profile picture uploads
  - Vehicle image storage
  - Secure media file serving

## 🏗️ Project Structure

```
SellnService/
├── SellsAndServices/          # Main project configuration
│   ├── settings.py            # Django settings with JWT & Channels config
│   ├── urls.py                # Root URL configuration
│   ├── asgi.py                # ASGI config for WebSocket support
│   └── wsgi.py                # WSGI config for HTTP
├── users/                     # User authentication & management
│   ├── models.py              # CustomUser, EmailVerificationToken, PasswordResetOTP
│   ├── views.py               # Registration, login, profile management
│   ├── serializers.py         # User data serialization
│   └── urls.py                # User endpoints
├── main/                      # Core business logic
│   ├── models.py              # Unit, Service, Sell models
│   ├── views.py               # CRUD operations for units/services/sales
│   ├── serializers.py         # Business model serialization
│   └── urls.py                # Main API endpoints
├── chats/                     # Real-time chat functionality
│   ├── models.py              # ChatRoom, ChatMessage
│   ├── consumers.py           # WebSocket consumer
│   ├── routing.py             # WebSocket URL routing
│   ├── views.py               # Chat REST API
│   └── urls.py                # Chat endpoints
├── admin/                     # Content management
│   ├── models.py              # PrivacyPolicy, TermsAndConditions, AboutUs
│   ├── views.py               # Admin-only content CRUD
│   └── urls.py                # Admin endpoints
├── media/                     # User-uploaded files
│   └── profile_pics/          # Profile pictures
├── db.sqlite3                 # SQLite database
├── manage.py                  # Django management script
└── requirements.txt           # Python dependencies
```

## 📋 Technology Stack

### Backend Framework
- **Django 5.2.8** - Web framework
- **Django REST Framework 3.16.1** - REST API toolkit
- **Django Channels 4.3.1** - WebSocket support
- **Daphne 4.2.1** - ASGI server

### Authentication & Security
- **djangorestframework-simplejwt 5.5.1** - JWT authentication
- **cryptography 46.0.3** - Encryption utilities

### Real-time Communication
- **channels-redis 4.3.0** - Channel layer backend
- **redis 7.0.1** - In-memory data store
- **autobahn 25.10.2** - WebSocket protocol

### File Handling
- **Pillow 12.0.0** - Image processing

### Environment Management
- **python-dotenv 1.2.1** - Environment variable management

## 🔧 Getting Started

### Prerequisites
- Python 3.8+
- Redis server (for WebSocket channel layers)
- SMTP server access (for email verification)

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/nadeemmaahmud/sellingaapp.git
cd SellnService
```

2. **Create virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Configure environment variables**
Create a `.env` file in the project root:
```env
SECRET_KEY=your-secret-key-here
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
DEFAULT_FROM_EMAIL=your-email@gmail.com
```

5. **Run database migrations**
```bash
python manage.py migrate
```

6. **Create superuser**
```bash
python manage.py createsuperuser
```

7. **Run the development server**
```bash
# For HTTP only
python manage.py runserver

# For WebSocket support (recommended)
daphne -b 0.0.0.0 -p 8000 SellsAndServices.asgi:application
```

### Base URL
```
http://localhost:8000
```

### Admin Panel
```
http://localhost:8000/admin/
```


---

## 📡 API Endpoints

### 🔐 Authentication & JWT

#### Obtain Token Pair
```http
POST /api/token/
```
**Permission:** AllowAny  
**Description:** Obtain access and refresh JWT tokens

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "password123"
}
```

**Response:**
```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

**Token Lifetime:**
- Access Token: 1 hour
- Refresh Token: 7 days
- Tokens rotate on refresh with automatic blacklisting

---

#### Refresh Token
```http
POST /api/token/refresh/
```
**Permission:** AllowAny  
**Description:** Refresh the access token

**Request Body:**
```json
{
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

**Response:**
```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."  // New refresh token (rotation enabled)
}
```

---

#### Verify Token
```http
POST /api/token/verify/
```
**Permission:** AllowAny  
**Description:** Verify if a token is valid

**Request Body:**
```json
{
  "token": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

---

### 👤 User Management

#### Register User
```http
POST /api/users/register/
```
**Permission:** AllowAny  
**Description:** Register a new user account. Users are created as inactive until email verification.

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "password123",
  "password2": "password123",
  "first_name": "John",
  "last_name": "Doe",
  "phone": "+1234567890"
}
```

**Response:**
```json
{
  "message": "User registered successfully. Please check your email for the verification code.",
  "user": {
    "id": 1,
    "email": "user@example.com",
    "first_name": "John",
    "last_name": "Doe",
    "phone": "+1234567890",
    "is_verified": false,
    "is_active": false
  }
}
```

**Note:** A 6-digit OTP is sent to the user's email, valid for 15 minutes.

---

#### Login
```http
POST /api/users/login/
```
**Permission:** AllowAny  
**Description:** User login (requires verified and active account)

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "password123"
}
```

**Response:**
```json
{
  "message": "Login successful",
  "user": {
    "id": 1,
    "email": "user@example.com",
    "first_name": "John",
    "last_name": "Doe",
    "profile_pic": "/media/profile_pics/user.jpg"
  },
  "tokens": {
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc...",
    "access": "eyJ0eXAiOiJKV1QiLCJhbGc..."
  }
}
```

---

#### Logout
```http
POST /api/users/logout/
```
**Permission:** IsAuthenticated  
**Description:** Logout user and blacklist refresh token

**Headers:**
```
Authorization: Bearer <access_token>
```

**Request Body:**
```json
{
  "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

**Response:**
```json
{
  "message": "Logout successful"
}
```

---

#### Verify Email
```http
POST /api/users/verify-email/
```
**Permission:** AllowAny  
**Description:** Verify email address with OTP code. Activates the user account.

**Request Body:**
```json
{
  "email": "user@example.com",
  "otp_code": "123456"
}
```

**Response:**
```json
{
  "message": "Email verified successfully! You can now login.",
  "user": {
    "id": 1,
    "email": "user@example.com",
    "is_verified": true,
    "is_active": true
  },
  "tokens": {
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc...",
    "access": "eyJ0eXAiOiJKV1QiLCJhbGc..."
  }
}
```

---

#### Resend Verification Email
```http
POST /api/users/resend-verification/
```
**Permission:** AllowAny  
**Description:** Resend email verification OTP

**Request Body:**
```json
{
  "email": "user@example.com"
}
```

**Response:**
```json
{
  "message": "Verification code has been resent to your email"
}
```

---

#### Forgot Password
```http
POST /api/users/forgot-password/
```
**Permission:** AllowAny  
**Description:** Request password reset OTP (sent via email)

**Request Body:**
```json
{
  "email": "user@example.com"
}
```

**Response:**
```json
{
  "message": "Password reset code has been sent to your email"
}
```

---

#### Verify Reset OTP
```http
POST /api/users/verify-reset-otp/
```
**Permission:** AllowAny  
**Description:** Verify password reset OTP code (does not reset password)

**Request Body:**
```json
{
  "email": "user@example.com",
  "otp_code": "123456"
}
```

**Response:**
```json
{
  "message": "OTP verified successfully. You can now reset your password."
}
```

---

#### Reset Password
```http
POST /api/users/reset-password/
```
**Permission:** AllowAny  
**Description:** Reset password with verified OTP

**Request Body:**
```json
{
  "email": "user@example.com",
  "otp_code": "123456",
  "new_password": "newpassword123",
  "confirm_password": "newpassword123"
}
```

**Response:**
```json
{
  "message": "Password has been reset successfully. You can now login with your new password."
}
```

---

#### Get User Profile
```http
GET /api/users/profile/
```
**Permission:** IsAuthenticated  
**Description:** Get current user profile information

**Headers:**
```
Authorization: Bearer <access_token>
```

**Response:**
```json
{
  "id": 1,
  "email": "user@example.com",
  "first_name": "John",
  "last_name": "Doe",
  "phone": "+1234567890",
  "date_of_birth": "1990-01-01",
  "address": "123 Main St",
  "zip_code": "12345",
  "profile_pic": "/media/profile_pics/user.jpg",
  "is_verified": true,
  "is_active": true,
  "date_joined": "2025-11-01T10:00:00Z"
}
```

---

#### Update Profile
```http
PUT /api/users/profile/update/
PATCH /api/users/profile/update/
```
**Permission:** IsAuthenticated  
**Description:** Update user profile (supports multipart/form-data for image upload)

**Headers:**
```
Authorization: Bearer <access_token>
Content-Type: multipart/form-data  (if uploading profile_pic)
```

**Request Body (Form Data):**
```json
{
  "first_name": "John",
  "last_name": "Doe",
  "phone": "+1234567890",
  "date_of_birth": "1990-01-01",
  "address": "123 Main St",
  "zip_code": "12345",
  "profile_pic": <file>  // Optional image file
}
```

---

#### Change Password
```http
POST /api/users/profile/change-password/
```
**Permission:** IsAuthenticated  
**Description:** Change user password (requires old password)

**Headers:**
```
Authorization: Bearer <access_token>
```

**Request Body:**
```json
{
  "old_password": "oldpassword123",
  "new_password": "newpassword123",
  "confirm_password": "newpassword123"
}
```

**Response:**
```json
{
  "message": "Password changed successfully"
}
```

---

### 🚗 Units (Vehicles)

#### List/Create Units
```http
GET /api/main/units/
POST /api/main/units/
```
**Permission:** IsAuthenticated  
**Description:** List all user's units or create a new unit

**Headers:**
```
Authorization: Bearer <access_token>
```

**GET Response:**
```json
{
  "count": 10,
  "next": "http://localhost:8000/api/main/units/?page=2",
  "previous": null,
  "results": [
    {
      "id": 1,
      "vin": "1HGBH41JXMN109186",
      "brand": "Honda",
      "model": "Accord",
      "year": "2021",
      "mileage": 15000,
      "date_of_purchase": "2021-01-15",
      "location": "New York",
      "status": "active",
      "additional_info": "Well maintained vehicle",
      "image": "/media/unit_images/honda.jpg",
      "created_at": "2025-11-01T10:00:00Z",
      "updated_at": "2025-11-13T14:30:00Z"
    }
  ]
}
```

**POST Request Body (multipart/form-data):**
```json
{
  "vin": "1HGBH41JXMN109186",
  "brand": "Honda",
  "model": "Accord",
  "year": "2021",
  "mileage": 15000,
  "date_of_purchase": "2021-01-15",
  "location": "New York",
  "status": "active",
  "additional_info": "Well maintained vehicle",
  "image": <file>  // Optional
}
```

**Status Options:** `active`, `sold`, `in_service`, `inactive`

**Validation:** VIN must be exactly 17 characters

---

#### Get/Update/Delete Unit
```http
GET /api/main/units/<id>/
PUT /api/main/units/<id>/
PATCH /api/main/units/<id>/
DELETE /api/main/units/<id>/
```
**Permission:** IsAuthenticated (Owner only)  
**Description:** Retrieve, update, or delete a specific unit

**Headers:**
```
Authorization: Bearer <access_token>
```

---

### 🛠️ Services

#### List/Create Services
```http
GET /api/main/services/
POST /api/main/services/
```
**Permission:** IsAuthenticated  
**Description:** List services (optionally filter by unit_id) or create a new service

**Headers:**
```
Authorization: Bearer <access_token>
```

**Query Parameters:**
- `unit_id` (optional): Filter services by unit ID

**GET Response:**
```json
{
  "count": 5,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 1,
      "unit": {
        "id": 1,
        "vin": "1HGBH41JXMN109186",
        "brand": "Honda",
        "model": "Accord"
      },
      "description": "Oil change and tire rotation",
      "location": "AutoCare Center",
      "appointment": "2025-11-20",
      "completion_date": null,
      "cost": "150.00",
      "status": "scheduled",
      "past_history": false,
      "created_at": "2025-11-13T10:00:00Z",
      "updated_at": "2025-11-13T10:00:00Z"
    }
  ]
}
```

**POST Request Body:**
```json
{
  "unit": 1,
  "description": "Oil change and tire rotation",
  "location": "AutoCare Center",
  "appointment": "2025-11-20",
  "cost": "150.00",
  "status": "scheduled",
  "past_history": false
}
```

**Status Options:** `scheduled`, `in_progress`, `completed`, `cancelled`

---

#### Get/Update/Delete Service
```http
GET /api/main/services/<id>/
PUT /api/main/services/<id>/
PATCH /api/main/services/<id>/
DELETE /api/main/services/<id>/
```
**Permission:** IsAuthenticated (Owner only)  
**Description:** Retrieve, update, or delete a specific service

**Headers:**
```
Authorization: Bearer <access_token>
```

---

### 💰 Sales

#### List/Create Sales
```http
GET /api/main/sales/
POST /api/main/sales/
```
**Permission:** IsAuthenticated  
**Description:** List all user's sales or create a new sale (automatically marks unit as "sold")

**Headers:**
```
Authorization: Bearer <access_token>
```

**GET Response:**
```json
{
  "count": 3,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 1,
      "unit": {
        "id": 1,
        "vin": "1HGBH41JXMN109186",
        "brand": "Honda",
        "model": "Accord"
      },
      "sale_price": "18500.00",
      "sale_date": "2025-11-10",
      "buyer_name": "Jane Smith",
      "buyer_email": "jane@example.com",
      "buyer_phone": "+1234567890",
      "payment_method": "Bank Transfer",
      "notes": "Sold in excellent condition",
      "created_at": "2025-11-10T15:00:00Z",
      "updated_at": "2025-11-10T15:00:00Z"
    }
  ]
}
```

**POST Request Body:**
```json
{
  "unit": 1,
  "sale_price": "18500.00",
  "sale_date": "2025-11-10",
  "buyer_name": "Jane Smith",
  "buyer_email": "jane@example.com",
  "buyer_phone": "+1234567890",
  "payment_method": "Bank Transfer",
  "notes": "Sold in excellent condition"
}
```

**Note:** Creating a sale automatically updates the unit's status to "sold"

---

#### Get/Update/Delete Sale
```http
GET /api/main/sales/<id>/
PUT /api/main/sales/<id>/
PATCH /api/main/sales/<id>/
DELETE /api/main/sales/<id>/
```
**Permission:** IsAuthenticated (Owner only)  
**Description:** Retrieve, update, or delete a specific sale

**Headers:**
```
Authorization: Bearer <access_token>
```


---

### 📄 Public Information

#### Get Privacy Policy
```http
GET /api/main/privacy-policy/
```
**Permission:** AllowAny  
**Description:** Get the latest privacy policy

**Response:**
```json
{
  "id": 1,
  "content": "Privacy policy content...",
  "effective_date": "2025-11-13",
  "created_at": "2025-11-01T10:00:00Z",
  "updated_at": "2025-11-13T14:00:00Z"
}
```

---

#### Get Terms & Conditions
```http
GET /api/main/terms-and-conditions/
```
**Permission:** AllowAny  
**Description:** Get the latest terms and conditions

**Response:**
```json
{
  "id": 1,
  "content": "Terms and conditions content...",
  "effective_date": "2025-11-13",
  "created_at": "2025-11-01T10:00:00Z",
  "updated_at": "2025-11-13T14:00:00Z"
}
```

---

#### Get About Us
```http
GET /api/main/about-us/
```
**Permission:** AllowAny  
**Description:** Get about us information

**Response:**
```json
{
  "id": 1,
  "content": "About us content...",
  "created_at": "2025-11-01T10:00:00Z",
  "updated_at": "2025-11-13T14:00:00Z"
}
```

---

### 🔐 Admin - Content Management

All admin endpoints require `IsAdminUser` permission (staff/superuser).

#### Privacy Policy Management

**List All Privacy Policies**
```http
GET /api/admin/privacy-policy/
```
**Permission:** IsAdminUser  
**Description:** List all privacy policy versions

---

**Create Privacy Policy**
```http
POST /api/admin/privacy-policy/
```
**Permission:** IsAdminUser

**Request Body:**
```json
{
  "content": "Privacy policy content...",
  "effective_date": "2025-11-13"
}
```

---

**Get/Update/Delete Privacy Policy**
```http
GET /api/admin/privacy-policy/<id>/
PUT /api/admin/privacy-policy/<id>/
PATCH /api/admin/privacy-policy/<id>/
DELETE /api/admin/privacy-policy/<id>/
```
**Permission:** IsAdminUser

---

#### Terms & Conditions Management

**List All Terms**
```http
GET /api/admin/terms-and-conditions/
```
**Permission:** IsAdminUser

---

**Create Terms**
```http
POST /api/admin/terms-and-conditions/
```
**Permission:** IsAdminUser

**Request Body:**
```json
{
  "content": "Terms and conditions content...",
  "effective_date": "2025-11-13"
}
```

---

**Get/Update/Delete Terms**
```http
GET /api/admin/terms-and-conditions/<id>/
PUT /api/admin/terms-and-conditions/<id>/
PATCH /api/admin/terms-and-conditions/<id>/
DELETE /api/admin/terms-and-conditions/<id>/
```
**Permission:** IsAdminUser

---

#### About Us Management

**List All About Us Entries**
```http
GET /api/admin/about-us/
```
**Permission:** IsAdminUser

---

**Create About Us**
```http
POST /api/admin/about-us/
```
**Permission:** IsAdminUser

**Request Body:**
```json
{
  "content": "About us content..."
}
```

---

**Get/Update/Delete About Us**
```http
GET /api/admin/about-us/<id>/
PUT /api/admin/about-us/<id>/
PATCH /api/admin/about-us/<id>/
DELETE /api/admin/about-us/<id>/
```
**Permission:** IsAdminUser

---

### 💬 Chat System

The chat system enables real-time communication between users and admins. Chat rooms can be linked to specific units, services, or sales.

#### List Chat Rooms
```http
GET /api/chat/rooms/
```
**Permission:** IsAuthenticated  
**Description:** List chat rooms (users see their rooms, admins see rooms they manage)

**Headers:**
```
Authorization: Bearer <access_token>
```

**Response:**
```json
{
  "count": 2,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 1,
      "user": {
        "id": 2,
        "email": "user@example.com",
        "first_name": "John",
        "last_name": "Doe"
      },
      "admin": {
        "id": 1,
        "email": "admin@example.com",
        "first_name": "Admin"
      },
      "content_type": "main.unit",
      "object_id": 5,
      "subject": "Discussion about Honda Accord",
      "is_active": true,
      "created_at": "2025-11-13T10:00:00Z",
      "updated_at": "2025-11-13T10:30:00Z",
      "unread_count": 3
    }
  ]
}
```

---

#### Create Chat Room
```http
POST /api/chat/rooms/create/
```
**Permission:** IsAdminUser  
**Description:** Create a new chat room (admin only)

**Headers:**
```
Authorization: Bearer <access_token>
```

**Request Body:**
```json
{
  "user_id": 2,
  "subject": "Discussion about Unit #5",
  "content_type": "unit",
  "object_id": 5
}
```

**Content Type Options:**
- `unit` - Link to a Unit
- `service` - Link to a Service
- `sell` - Link to a Sale

**Note:** The system prevents duplicate chat rooms for the same user and related object.

---

#### Get Chat Room Details
```http
GET /api/chat/rooms/<id>/
```
**Permission:** IsAuthenticated  
**Description:** Get details of a specific chat room

**Headers:**
```
Authorization: Bearer <access_token>
```

---

#### Update Chat Room
```http
PATCH /api/chat/rooms/<id>/
```
**Permission:** IsAdminUser  
**Description:** Update chat room (e.g., activate/deactivate)

**Headers:**
```
Authorization: Bearer <access_token>
```

**Request Body:**
```json
{
  "is_active": false
}
```

---

#### List Messages
```http
GET /api/chat/messages/?chat_room_id=<room_id>
```
**Permission:** IsAuthenticated  
**Description:** List all messages in a chat room

**Headers:**
```
Authorization: Bearer <access_token>
```

**Query Parameters:**
- `chat_room_id` (required): The chat room ID

**Response:**
```json
{
  "count": 10,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 1,
      "chat_room": 1,
      "sender": {
        "id": 1,
        "email": "user@example.com",
        "first_name": "John"
      },
      "message": "Hello, I have a question about my vehicle",
      "timestamp": "2025-11-13T10:00:00Z",
      "is_read": true
    },
    {
      "id": 2,
      "chat_room": 1,
      "sender": {
        "id": 2,
        "email": "admin@example.com",
        "first_name": "Admin"
      },
      "message": "Hello! How can I help you?",
      "timestamp": "2025-11-13T10:05:00Z",
      "is_read": false
    }
  ]
}
```

---

#### Create Message
```http
POST /api/chat/messages/create/
```
**Permission:** IsAuthenticated  
**Description:** Send a new message in a chat room

**Headers:**
```
Authorization: Bearer <access_token>
```

**Request Body:**
```json
{
  "chat_room": 1,
  "message": "Hello, I need help with my vehicle service"
}
```

**Response:**
```json
{
  "id": 3,
  "chat_room": 1,
  "sender": {
    "id": 2,
    "email": "user@example.com",
    "first_name": "John"
  },
  "message": "Hello, I need help with my vehicle service",
  "timestamp": "2025-11-13T10:10:00Z",
  "is_read": false
}
```

---

#### Mark Messages as Read
```http
POST /api/chat/messages/mark-read/
```
**Permission:** IsAuthenticated  
**Description:** Mark all unread messages in a chat room as read

**Headers:**
```
Authorization: Bearer <access_token>
```

**Request Body:**
```json
{
  "chat_room_id": 1
}
```

**Response:**
```json
{
  "message": "5 messages marked as read"
}
```

---

#### Get Unread Message Count
```http
GET /api/chat/messages/unread-count/
```
**Permission:** IsAuthenticated  
**Description:** Get total unread message count across all chat rooms

**Headers:**
```
Authorization: Bearer <access_token>
```

**Response:**
```json
{
  "unread_count": 12
}
```

---

## 🔌 WebSocket

### Real-time Chat WebSocket Connection

**Endpoint:**
```
ws://localhost:8000/ws/chat/<room_id>/
```

**Description:** Establish real-time WebSocket connection for a specific chat room

**Authentication:** WebSocket connections are authenticated via Django session or JWT token

**Connecting:**
```javascript
const chatSocket = new WebSocket(
    'ws://localhost:8000/ws/chat/1/'
);

chatSocket.onopen = function(e) {
    console.log('WebSocket connection established');
};

chatSocket.onmessage = function(e) {
    const data = JSON.parse(e.data);
    console.log('Message received:', data);
};

chatSocket.onerror = function(e) {
    console.error('WebSocket error:', e);
};

chatSocket.onclose = function(e) {
    console.log('WebSocket connection closed');
};
```

**Sending Messages:**
```javascript
chatSocket.send(JSON.stringify({
    'message': 'Hello, this is a real-time message'
}));
```

**Message Format (Send):**
```json
{
  "message": "Hello, this is a real-time message"
}
```

**Message Format (Receive):**
```json
{
  "type": "chat_message",
  "message": "Hello, this is a real-time message",
  "sender": {
    "id": 1,
    "email": "user@example.com",
    "first_name": "John",
    "last_name": "Doe"
  },
  "timestamp": "2025-11-13T10:00:00Z",
  "message_id": 123,
  "is_read": false
}
```

**WebSocket Features:**
- Real-time message delivery
- Automatic message persistence
- Sender information included
- Support for multiple concurrent connections
- Graceful error handling

---

## 🔑 Authentication & Security

### JWT Token Authentication

Most endpoints require JWT authentication. Include the access token in the Authorization header:

```http
Authorization: Bearer <access_token>
```

### Token Configuration
- **Access Token Lifetime:** 1 hour
- **Refresh Token Lifetime:** 7 days
- **Token Rotation:** Enabled (new refresh token on each refresh)
- **Blacklisting:** Enabled (invalidates old tokens on logout/refresh)
- **Algorithm:** HS256

### Permission Levels
1. **AllowAny** - No authentication required (public endpoints)
2. **IsAuthenticated** - Requires valid JWT token
3. **IsAdminUser** - Requires admin/staff privileges

### Security Features
- Password validation (length, complexity, common passwords)
- Email verification required for account activation
- OTP expiration (15 minutes)
- Secure password reset flow
- Token blacklisting on logout
- CSRF protection
- Session security middleware

---

## 📁 Media Files

Profile pictures and vehicle images are served from:
```
http://localhost:8000/media/<file_path>
```

**Supported Upload Directories:**
- `/media/profile_pics/` - User profile pictures
- `/media/unit_images/` - Vehicle images

**Note:** Media file serving is only available when `DEBUG=True` (development mode). For production, configure a proper media server (e.g., Nginx, S3).

**File Upload:**
- Use `multipart/form-data` content type
- Supported formats: JPG, PNG, GIF
- Image processing via Pillow library

---

## 🛠️ Admin Panel

Django admin interface provides a web-based administrative interface for managing:
- Users and permissions
- Units (vehicles)
- Services and appointments
- Sales records
- Chat rooms and messages
- Content management (Privacy Policy, Terms, About Us)

**Access URL:**
```
http://localhost:8000/admin/
```

**Credentials:** Use superuser account created during setup

---

## � Database Schema

### Core Models

**CustomUser**
- Custom user model with email authentication
- Fields: email, first_name, last_name, phone, address, date_of_birth, zip_code, profile_pic
- Verification: is_verified, is_active, is_staff

**Unit (Vehicle)**
- VIN (17 characters, unique)
- Brand, model, year, mileage
- Status: active, sold, in_service, inactive
- Location, image, purchase date

**Service**
- Linked to Unit
- Status: scheduled, in_progress, completed, cancelled
- Appointment date, completion date, cost
- Service description and location

**Sell (Sale)**
- Linked to Unit
- Sale price, date, buyer information
- Payment method, notes

**ChatRoom**
- User-to-Admin communication
- Linked to Unit/Service/Sell via GenericForeignKey
- Subject, active status

**ChatMessage**
- Linked to ChatRoom
- Message content, sender, timestamp
- Read status tracking

**EmailVerificationToken & PasswordResetOTP**
- 6-digit OTP codes
- 15-minute expiration
- One-time use

---

## 🧪 Testing

Run the test suite:
```bash
# Run all tests
python manage.py test

# Run tests for specific app
python manage.py test users
python manage.py test main
python manage.py test chats

# Run with verbosity
python manage.py test --verbosity=2

# Run specific test class
python manage.py test users.tests.UserRegistrationTests
```

---

## 🚀 Deployment

### Production Checklist

1. **Environment Variables**
   - Set `DEBUG=False`
   - Use strong `SECRET_KEY`
   - Configure production database (PostgreSQL recommended)
   - Set proper `ALLOWED_HOSTS`

2. **Static & Media Files**
   - Configure static file serving
   - Set up media file storage (S3, CDN)
   - Run `python manage.py collectstatic`

3. **Database**
   - Migrate to PostgreSQL or MySQL
   - Run migrations: `python manage.py migrate`
   - Create superuser

4. **Security**
   - Enable HTTPS
   - Configure CORS headers
   - Set secure cookie settings
   - Configure CSP headers

5. **WebSocket Support**
   - Configure Redis for channel layers
   - Update `CHANNEL_LAYERS` in settings
   - Use production ASGI server (Daphne/Uvicorn)

6. **Email Configuration**
   - Configure production SMTP server
   - Set up email templates
   - Test email delivery

### Example Production Settings

```python
# settings.py (production)
DEBUG = False
ALLOWED_HOSTS = ['yourdomain.com', 'www.yourdomain.com']

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('DB_NAME'),
        'USER': os.getenv('DB_USER'),
        'PASSWORD': os.getenv('DB_PASSWORD'),
        'HOST': os.getenv('DB_HOST'),
        'PORT': os.getenv('DB_PORT', '5432'),
    }
}

# Redis Channel Layer
CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            "hosts": [(os.getenv('REDIS_HOST', '127.0.0.1'), 6379)],
        },
    },
}

# Static & Media
STATIC_ROOT = BASE_DIR / 'staticfiles'
MEDIA_URL = 'https://your-cdn.com/media/'
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
```

### Running in Production

```bash
# Using Daphne (ASGI server)
daphne -b 0.0.0.0 -p 8000 SellsAndServices.asgi:application

# Using Gunicorn + Daphne
gunicorn SellsAndServices.wsgi:application --bind 0.0.0.0:8000
daphne -b 0.0.0.0 -p 8001 SellsAndServices.asgi:application

# Using Docker
docker-compose up -d
```

---

## 📝 API Response Pagination

API responses use Django REST Framework's pagination:

**Default Page Size:** 10 items per page

**Response Format:**
```json
{
  "count": 50,
  "next": "http://localhost:8000/api/main/units/?page=2",
  "previous": null,
  "results": [...]
}
```

**Query Parameters:**
- `page=<number>` - Page number (starts at 1)

---

## 🔍 Common Use Cases

### 1. User Registration Flow
1. Register → `POST /api/users/register/`
2. Receive OTP via email
3. Verify email → `POST /api/users/verify-email/`
4. Account activated, receive JWT tokens

### 2. Password Reset Flow
1. Request reset → `POST /api/users/forgot-password/`
2. Receive OTP via email
3. Verify OTP → `POST /api/users/verify-reset-otp/`
4. Reset password → `POST /api/users/reset-password/`

### 3. Vehicle Management Flow
1. Add vehicle → `POST /api/main/units/`
2. Schedule service → `POST /api/main/services/`
3. Complete service → `PATCH /api/main/services/<id>/` (status: completed)
4. Sell vehicle → `POST /api/main/sales/` (unit status auto-updated to "sold")

### 4. Chat Communication Flow
1. Admin creates chat room → `POST /api/chat/rooms/create/`
2. User/Admin connects via WebSocket → `ws://localhost:8000/ws/chat/<room_id>/`
3. Send messages in real-time
4. Alternative: Use REST API → `POST /api/chat/messages/create/`
5. Mark messages as read → `POST /api/chat/messages/mark-read/`

---

## 📞 Support & Contributing

### Reporting Issues
If you encounter bugs or have feature requests, please open an issue on the GitHub repository.

### Contributing
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Write tests
5. Submit a pull request

### Contact
- **Repository:** https://github.com/nadeemmaahmud/sellingaapp
- **Developer:** Nadeem Mahmud

---

## 📄 License

This project is proprietary software. All rights reserved.

---

## 🔄 Changelog

### Version 1.0.0 (Current)
- Initial release
- User authentication with JWT
- Email verification system
- Vehicle (Unit) management
- Service scheduling and tracking
- Sales management
- Real-time chat with WebSocket
- Admin content management
- Media file uploads

---

**Last Updated:** November 14, 2025  
**Django Version:** 5.2.8  
**DRF Version:** 3.16.1  
**Channels Version:** 4.3.1
