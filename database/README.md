# Database

This directory contains the database schema and seed files for the Resort Management System.

## Requirements
- MySQL 8.0+

## Setup
To set up the database, you can run the following commands in your MySQL client or CLI:

```bash
# Log in to MySQL
mysql -u root -p

# Run schema script
mysql> source /path/to/resortmanagement-system/database/schema.sql;

# Run seed script
mysql> source /path/to/resortmanagement-system/database/seed.sql;
```

## Tables
The tables follow strict 3NF normalization as per the project requirements.

- `CUSTOMERS`
- `ROOM_TYPES`
- `ROOMS`
- `BOOKINGS`
- `ROOM_ALLOCATIONS`
- `SERVICES`
- `BOOKING_SERVICES`
- `STAFF`
- `INVOICES`
- `PAYMENTS`
