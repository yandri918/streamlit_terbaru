# AgriSensa Vercel API

Flask API backend untuk AgriSensa. Deploy ke Vercel untuk mendukung cross-device authentication.

## Endpoints

- `POST /api/auth/simple-login` - Login
- `POST /api/auth/simple-register` - Register
- `POST /api/auth/log-activity` - Log activity
- `GET /api/auth/activities` - Get activities
- `GET /api/auth/users-list` - Get users

## Environment Variables

Set di Vercel:
- `DATABASE_URL` - PostgreSQL connection string
- `SECRET_KEY` - Flask secret
- `JWT_SECRET_KEY` - JWT secret
