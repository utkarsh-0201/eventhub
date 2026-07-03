# EventHub

EventHub is a backend API for a simplified event ticketing platform built with Django and Django REST Framework.

## Features

- Browse events
- Reserve seats with availability validation
- Cancel reservations and restore seat availability
- Safe reservation handling using database transactions and row locking
- Request logging middleware for incoming API calls

## Project Structure

- `eventhub/` - Django project configuration
- `events/` - main application containing models, serializers, views, and middleware
- `db.sqlite3` - default SQLite database file
- `requirements.txt` - Python dependencies

## Models

- `Event`
  - `title`, `venue`, `date`
  - `total_seats`, `available_seats`
  - `status` (`upcoming`, `ongoing`, `completed`, `cancelled`)

- `Reservation`
  - `event`, `attendee_name`, `attendee_email`
  - `seats_reserved`, `status` (`confirmed`, `cancelled`)

## API Endpoints

The DRF router exposes endpoints under `/api/`:

- `GET /api/events/`
- `POST /api/events/`
- `GET /api/events/{id}/`
- `PATCH /api/events/{id}/`
- `DELETE /api/events/{id}/`

- `GET /api/reservations/`
- `POST /api/reservations/`
- `GET /api/reservations/{id}/`
- `PATCH /api/reservations/{id}/`
- `DELETE /api/reservations/{id}/`
- `POST /api/reservations/{id}/cancel/`

## Middleware

- `events.middleware.RequestLoggingMiddleware`
  - logs request start and finish messages
  - records HTTP method, request path, and response status

## Setup

1. Create and activate a Python environment
2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Run migrations:

```bash
python manage.py migrate
```

4. Start the development server:

```bash
python manage.py runserver
```

## Notes

- `RequestLoggingMiddleware` is enabled in `eventhub/settings.py`.
- Reservation creation uses `select_for_update()` with a transaction to prevent race conditions on seat allocation.
