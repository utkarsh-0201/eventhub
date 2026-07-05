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

### Events
- `GET /api/events/`
  - List all events. Supports filtering by status with `?status=upcoming`.
- `POST /api/events/`
  - Create a new event.
  - Example JSON body:

```json
{
  "title": "Concert Night",
  "venue": "Downtown Hall",
  "date": "2026-08-15",
  "total_seats": 100,
  "available_seats": 100,
  "status": "upcoming"
}
```
- `GET /api/events/{id}/`
  - Retrieve details for a specific event.
- `DELETE /api/events/{id}/`
  - Remove an event.

### Reservations
- `GET /api/reservations/`
  - List all reservations. Supports filtering by event with `?event_id={id}`.
- `POST /api/reservations/`
  - Create a reservation for an event. Validates available seats and event status.
  - Example JSON body:

```json
{
  "event": 1,
  "attendee_name": "Jane Doe",
  "attendee_email": "jane@example.com",
  "seats_reserved": 2
}
```

- `GET /api/reservations/{id}/`
  - Retrieve a specific reservation.
- `DELETE /api/reservations/{id}/`
  - Remove a reservation.
- `POST /api/reservations/{id}/cancel/`
  - Cancel a reservation and restore the reserved seats back to the event.

## How to Run the Project

1. Create and activate a Python virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Apply database migrations:

```bash
python manage.py migrate
```

4. Start the development server:

```bash
python manage.py runserver
```

5. Open Postman or another API client and use the `http://127.0.0.1:8000/api/` endpoints.

## Design Decision

I chose to handle reservation creation inside a database transaction using `select_for_update()` on the related event. This ensures seat availability is checked and updated atomically, preventing race conditions when multiple reservation requests arrive concurrently.

## Notes

- `RequestLoggingMiddleware` is enabled in `eventhub/settings.py`.
- Reservation creation uses `select_for_update()` with a transaction to prevent race conditions on seat allocation.

## Screenshots

These screenshots show core API workflows using Postman:

- ![Postman screenshot showing event creation](postman%20screenshots/Event_Created.png) - Creating a new event.
- ![Postman screenshot showing seat reservation](postman%20screenshots/Event_Reservation.png) - Reserving seats for an event.
- ![Postman screenshot showing reservation cancellation](postman%20screenshots/Event_Reservation_Cancellation.png) - Cancelling a reservation and restoring seats.
- ![Postman screenshot showing overbooking validation](postman%20screenshots/Event_Overbooking.png) - Attempting to reserve more seats than are available.
