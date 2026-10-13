# Lumiere Resort Management System

A completely functional, database-driven Resort Management System built on a modern MERN-style stack (MySQL, Express, React, Node.js, Prisma).

## Architecture & Tech Stack
- **Frontend**: React 18, TypeScript, Tailwind CSS 3, Recharts, React Router
- **Backend**: Node.js, Express, TypeScript, JWT Authentication, bcrypt
- **Database**: MySQL, Prisma ORM
- **Roles**: CUSTOMER, ADMIN, ACCOUNTANT, STAFF

## Features & Modules Implemented

### 1. Authentication Module
- Role-based login system for Customers, Admins, Accountants, and Staff.
- Password hashing using `bcrypt`.
- JWT-based protected API routes and frontend PrivateRoutes.
- Live new customer registration.

### 2. Beautiful Dashboards
- **Admin**: Features interactive `recharts` graphs plotting real-time revenue and occupancy data.
- **Customer**: A stunning, modern hotel landing page showing featured premium rooms and instant booking access.
- **Accountant/Staff**: Highly restricted, role-based dashboards focusing on exact job functions.

### 3. Room Management
- Admin can instantly add physical rooms, assign them to floors and Room Types (e.g., Deluxe, Suite).
- Room data displays dynamically with pricing logic calculated from the database.
- Admin can delete un-booked rooms.

### 4. Interactive Booking Engine
- Customers can pick Check-In/Check-Out dates, select their Guest count, and create a reservation with an instant Price Preview.
- The Node.js backend handles strict **Overlap Prevention** (customers cannot book a room that is already occupied during their requested dates).
- Admins and Staff can change Booking Status in real-time (`CONFIRMED`, `CHECKED_IN`, `CHECKED_OUT`).

### 5. Services Module
- Admin can create Resort Services (e.g., Spa Massage, Pool Access, Airport Transfer).
- Customers can browse available services and instantly add them to their Active Booking!

### 6. Billing & Payments
- Full auto-generation of Invoices calculating Room Stay duration (`$Rate * Days`) + Added Services.
- Customers can view their invoice dynamically inside their Bookings dashboard and simulate a Card Payment.
- Payment status reflects instantly for the Accountant in the `AdminInvoices` screen.

### 7. Real-Time Reporting
- The `AdminReports` module calculates Occupancy Rate, Total Revenue, and Active Bookings directly from the SQL engine and displays it visually.

## Database Structure (Strict 3NF)
The schema strictly follows the requirements:
- `CUSTOMERS` (CustomerID, Name, Address, Phone, Email)
- `STAFF` (StaffID, Name, Role, Phone, Email)
- `ROOM_TYPES` (RoomTypeID, TypeName, Description, Rate, Capacity)
- `ROOMS` (RoomID, RoomNo, RoomTypeID, FloorNo, Status)
- `BOOKINGS` (BookingID, CustomerID, BookingDate, CheckInDate, CheckOutDate, NoOfGuests, Status)
- `ROOM_ALLOCATIONS` (AllocationID, BookingID, RoomID)
- `SERVICES` (ServiceID, ServiceName, Description, Charge)
- `BOOKING_SERVICES` (BookingServiceID, BookingID, ServiceID, Qty, Amount)
- `INVOICES` (InvoiceID, BookingID, InvoiceDate, TotalAmount, Discount, GrandTotal)
- `PAYMENTS` (PaymentID, InvoiceID, PaymentDate, Amount, PaymentMode, Status, TxnReference)

## How to Run

1. Clone or download this project.
2. Ensure you have MySQL running locally.
3. Add your MySQL password to `backend/.env`.
4. In the `backend` folder, run `npm install` and then `npm run dev`.
5. In the `frontend` folder, run `npm install` and then `npm run dev`.

Enjoy the beautiful, fully functional Lumiere Resort!
