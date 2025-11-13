# SellnService API Documentation

A Django REST Framework application for managing units, services, sales, and real-time chat functionality.

## 🚀 Features

- User authentication with JWT tokens
- Email verification system
- Password reset functionality
- Units, Services, and Sales management
- Real-time chat with WebSocket support
- Admin content management (Privacy Policy, Terms & Conditions, About Us)
- Media file uploads

## 📋 Table of Contents

- [Getting Started](#getting-started)
- [API Endpoints](#api-endpoints)
  - [Authentication & JWT](#authentication--jwt)
  - [User Management](#user-management)
  - [Units](#units)
  - [Services](#services)
  - [Sales](#sales)
  - [Public Information](#public-information)
  - [Admin - Content Management](#admin---content-management)
  - [Chat System](#chat-system)
- [WebSocket](#websocket)

## 🔧 Getting Started

### Installation

```bash
# Clone the repository
git clone <repository-url>
cd SellnService

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Run the development server
python manage.py runserver
```

### Base URL
```
http://localhost:8000
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
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc..."
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
**Description:** Register a new user account

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "password123",
  "password2": "password123",
  "first_name": "John",
  "last_name": "Doe",
  "phone_number": "+1234567890"
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
    "phone_number": "+1234567890",
    "is_verified": false
  }
}
```

---

#### Login
```http
POST /api/users/login/
```
**Permission:** AllowAny  
**Description:** User login

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
    "last_name": "Doe"
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

---

#### Verify Email
```http
POST /api/users/verify-email/
```
**Permission:** AllowAny  
**Description:** Verify email address with OTP code

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
    "is_verified": true
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

---

#### Forgot Password
```http
POST /api/users/forgot-password/
```
**Permission:** AllowAny  
**Description:** Request password reset OTP

**Request Body:**
```json
{
  "email": "user@example.com"
}
```

---

#### Verify Reset OTP
```http
POST /api/users/verify-reset-otp/
```
**Permission:** AllowAny  
**Description:** Verify password reset OTP code

**Request Body:**
```json
{
  "email": "user@example.com",
  "otp_code": "123456"
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

---

#### Get User Profile
```http
GET /api/users/profile/
```
**Permission:** IsAuthenticated  
**Description:** Get current user profile

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
  "phone_number": "+1234567890",
  "profile_pic": "/media/profile_pics/user.jpg",
  "is_verified": true
}
```

---

#### Update Profile
```http
PUT /api/users/profile/update/
PATCH /api/users/profile/update/
```
**Permission:** IsAuthenticated  
**Description:** Update user profile

**Headers:**
```
Authorization: Bearer <access_token>
```

**Request Body:**
```json
{
  "first_name": "John",
  "last_name": "Doe",
  "phone_number": "+1234567890"
}
```

---

#### Change Password
```http
POST /api/users/profile/change-password/
```
**Permission:** IsAuthenticated  
**Description:** Change user password

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

---

### 🏢 Units

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

**POST Request Body:**
```json
{
  "name": "Unit Name",
  "description": "Unit description",
  "location": "Unit location",
  "status": "available"
}
```

---

#### Get/Update/Delete Unit
```http
GET /api/main/units/<id>/
PUT /api/main/units/<id>/
PATCH /api/main/units/<id>/
DELETE /api/main/units/<id>/
```
**Permission:** IsAuthenticated  
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

**POST Request Body:**
```json
{
  "unit": 1,
  "name": "Service Name",
  "description": "Service description",
  "price": "99.99"
}
```

---

#### Get/Update/Delete Service
```http
GET /api/main/services/<id>/
PUT /api/main/services/<id>/
PATCH /api/main/services/<id>/
DELETE /api/main/services/<id>/
```
**Permission:** IsAuthenticated  
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
**Description:** List all user's sales or create a new sale (marks unit as sold)

**Headers:**
```
Authorization: Bearer <access_token>
```

**POST Request Body:**
```json
{
  "unit": 1,
  "buyer_name": "Buyer Name",
  "sale_price": "1000.00",
  "sale_date": "2025-11-13"
}
```

---

#### Get/Update/Delete Sale
```http
GET /api/main/sales/<id>/
PUT /api/main/sales/<id>/
PATCH /api/main/sales/<id>/
DELETE /api/main/sales/<id>/
```
**Permission:** IsAuthenticated  
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
  "title": "Privacy Policy",
  "content": "Privacy policy content...",
  "effective_date": "2025-11-13"
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
  "title": "Terms and Conditions",
  "content": "Terms content...",
  "effective_date": "2025-11-13"
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
  "title": "About Us",
  "content": "About us content...",
  "mission": "Our mission...",
  "vision": "Our vision..."
}
```

---

### 🔐 Admin - Content Management

#### Privacy Policy Management

**List All Privacy Policies**
```http
GET /api/main/admin/privacy-policy/
```
**Permission:** IsAdminUser

**Create Privacy Policy**
```http
POST /api/main/admin/privacy-policy/
```
**Permission:** IsAdminUser

**Get/Update/Delete Privacy Policy**
```http
GET /api/main/admin/privacy-policy/<id>/
PUT /api/main/admin/privacy-policy/<id>/
PATCH /api/main/admin/privacy-policy/<id>/
DELETE /api/main/admin/privacy-policy/<id>/
```
**Permission:** IsAdminUser

---

#### Terms & Conditions Management

**List All Terms**
```http
GET /api/main/admin/terms-and-conditions/
```
**Permission:** IsAdminUser

**Create Terms**
```http
POST /api/main/admin/terms-and-conditions/
```
**Permission:** IsAdminUser

**Get/Update/Delete Terms**
```http
GET /api/main/admin/terms-and-conditions/<id>/
PUT /api/main/admin/terms-and-conditions/<id>/
PATCH /api/main/admin/terms-and-conditions/<id>/
DELETE /api/main/admin/terms-and-conditions/<id>/
```
**Permission:** IsAdminUser

---

#### About Us Management

**List All About Us Entries**
```http
GET /api/main/admin/about-us/
```
**Permission:** IsAdminUser

**Create About Us**
```http
POST /api/main/admin/about-us/
```
**Permission:** IsAdminUser

**Get/Update/Delete About Us**
```http
GET /api/main/admin/about-us/<id>/
PUT /api/main/admin/about-us/<id>/
PATCH /api/main/admin/about-us/<id>/
DELETE /api/main/admin/about-us/<id>/
```
**Permission:** IsAdminUser

---

### 💬 Chat System

#### List Chat Rooms
```http
GET /api/chat/rooms/
```
**Permission:** IsAuthenticated  
**Description:** List all active chat rooms for the user (users see their rooms, admins see rooms they manage)

**Headers:**
```
Authorization: Bearer <access_token>
```

**Response:**
```json
[
  {
    "id": 1,
    "subject": "Chat subject",
    "user": {
      "id": 2,
      "email": "user@example.com",
      "first_name": "John"
    },
    "admin": {
      "id": 1,
      "email": "admin@example.com",
      "first_name": "Admin"
    },
    "is_active": true,
    "created_at": "2025-11-13T10:00:00Z",
    "updated_at": "2025-11-13T10:30:00Z",
    "unread_count": 3
  }
]
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
  "subject": "Discussion about Unit #123",
  "related_type": "unit",
  "related_id": 123
}
```

**Note:** `related_type` can be: `unit`, `service`, or `sell`

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
[
  {
    "id": 1,
    "chat_room": 1,
    "sender": {
      "id": 1,
      "email": "user@example.com",
      "first_name": "John"
    },
    "message": "Hello, how can I help?",
    "timestamp": "2025-11-13T10:00:00Z",
    "is_read": true
  }
]
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
  "message": "Hello, I need help with my unit"
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

### Chat WebSocket Connection
```
ws://localhost:8000/ws/chat/<room_id>/
```
**Description:** Real-time chat WebSocket connection for a specific chat room

**Authentication:** WebSocket connection is authenticated via Django session or token

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
    "first_name": "John"
  },
  "timestamp": "2025-11-13T10:00:00Z"
}
```

---

## 🔑 Authentication

Most endpoints require JWT authentication. Include the access token in the Authorization header:

```
Authorization: Bearer <access_token>
```

### Permission Levels:
- **AllowAny**: No authentication required
- **IsAuthenticated**: Requires valid JWT token
- **IsAdminUser**: Requires admin/staff privileges

---

## 📁 Media Files

Profile pictures and other media files are served from:
```
http://localhost:8000/media/<file_path>
```

**Note:** Media serving is only available in DEBUG mode.

---

## 🛠️ Admin Panel

Django admin interface is available at:
```
http://localhost:8000/admin/
```

---

## 📝 Notes

- OTP codes expire after 15 minutes
- Email verification is required for new users
- Units are automatically marked as "sold" when a sale is created
- Chat rooms can be deactivated by admins
- WebSocket connections use Django Channels for real-time communication

---

## 🧪 Testing

To run tests:
```bash
python manage.py test
```

---

## 📞 Support

For issues or questions, please contact the development team.

---

**Last Updated:** November 13, 2025
