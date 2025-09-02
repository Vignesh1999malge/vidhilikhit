# FastAPI Authentication System

A simple and secure FastAPI application with JWT-based authentication system.

## Features

- User registration and authentication
- JWT token-based authentication
- Password hashing with bcrypt
- SQLAlchemy ORM with SQLite/PostgreSQL support
- Pydantic schemas for data validation
- CORS middleware enabled
- User management endpoints

## Project Structure

```
├── main.py          # FastAPI application and endpoints
├── models.py        # SQLAlchemy database models
├── schemas.py       # Pydantic schemas for validation
├── functions.py     # Authentication and utility functions
├── db.py           # Database configuration and session
├── requirements.txt # Python dependencies
├── env_example.txt  # Environment variables example
└── README.md       # This file
```

## Installation

1. Clone the repository:
```bash
git clone <your-repo-url>
cd vidhilikhit
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
```bash
cp env_example.txt .env
# Edit .env file with your configuration
```

## Usage

### Running the Application

```bash
python main.py
```

Or using uvicorn directly:
```bash
uvicorn main:app --reload
```

The API will be available at `http://localhost:8000`

### API Documentation

- Interactive API docs: `http://localhost:8000/docs`
- ReDoc documentation: `http://localhost:8000/redoc`

## API Endpoints

### Public Endpoints

- `POST /register` - User registration
- `POST /token` - User login (get access token)
- `GET /` - Welcome message

### Protected Endpoints (require authentication)

- `GET /users/me` - Get current user info
- `GET /users` - List all users
- `PUT /users/me` - Update current user
- `DELETE /users/me` - Delete current user account

## Authentication Flow

1. **Register**: Create a new user account
2. **Login**: Get JWT access token
3. **Use Token**: Include token in Authorization header for protected endpoints

### Example Usage

```bash
# Register a new user
curl -X POST "http://localhost:8000/register" \
     -H "Content-Type: application/json" \
     -d '{"email":"user@example.com","username":"testuser","password":"password123"}'

# Login to get token
curl -X POST "http://localhost:8000/token" \
     -H "Content-Type: application/x-www-form-urlencoded" \
     -d "username=testuser&password=password123"

# Use token for protected endpoint
curl -X GET "http://localhost:8000/users/me" \
     -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

## Database

The application uses SQLite by default. To use PostgreSQL:

1. Update `DATABASE_URL` in your `.env` file
2. Install PostgreSQL dependencies: `pip install psycopg2-binary`

## Security Features

- Password hashing with bcrypt
- JWT tokens with configurable expiration
- Protected endpoints with authentication middleware
- Input validation with Pydantic schemas

## Configuration

Key configuration options in `functions.py`:

- `SECRET_KEY`: JWT signing key (change in production!)
- `ALGORITHM`: JWT algorithm (HS256)
- `ACCESS_TOKEN_EXPIRE_MINUTES`: Token expiration time

## Development

### Adding New Models

1. Add model to `models.py`
2. Create corresponding schemas in `schemas.py`
3. Add endpoints in `main.py`

### Database Migrations

For production use, consider using Alembic for database migrations:

```bash
pip install alembic
alembic init alembic
# Configure alembic.ini and env.py
alembic revision --autogenerate -m "Initial migration"
alembic upgrade head
```

## Production Deployment

1. Change `SECRET_KEY` to a secure random string
2. Use environment variables for configuration
3. Set up proper database (PostgreSQL recommended)
4. Configure CORS origins appropriately
5. Use HTTPS in production
6. Set up proper logging and monitoring

## License

This project is open source and available under the MIT License.
