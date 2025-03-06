# Booking App

### Setup Instructions

1. Clone the repo:
git clone https://github.com/raj10amit/booking.git cd booking_app


2. Install dependencies:
pip install -r requirements.txt

3. Run migrations:
python manage.py migrate


4. Import CSV data:
python manage.py import_csv

5. Run the server:
python manage.py runserver


6. API Endpoints:
- Book item: `/api/book/ -d member_id=<id>&item_id=<id>`
  /api/book/ -d "member_id=1&item_id=2"
- Cancel booking: `/api/cancel/?booking_id=<id>`
  /api/cancel/?booking_id=1"
