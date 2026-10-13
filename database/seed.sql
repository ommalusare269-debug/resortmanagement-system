USE resort_management;

-- Note: Passwords are 'password123' hashed with bcrypt (salt rounds 10)
-- $2b$10$wY9aA.307xP592fT10h2v.H.Ew1K0L6o4N/5uH5l5QG9255sT9qC

-- 1. Insert STAFF (Admin, Accountant, Staff)
INSERT INTO STAFF (Name, Role, Phone, Email, PasswordHash, Salary) VALUES 
('System Admin', 'ADMIN', '1234567890', 'admin@resort.com', '$2b$10$wY9aA.307xP592fT10h2v.H.Ew1K0L6o4N/5uH5l5QG9255sT9qC', 80000.00),
('John Accountant', 'ACCOUNTANT', '0987654321', 'accountant@resort.com', '$2b$10$wY9aA.307xP592fT10h2v.H.Ew1K0L6o4N/5uH5l5QG9255sT9qC', 60000.00),
('Jane Staff', 'STAFF', '1122334455', 'staff@resort.com', '$2b$10$wY9aA.307xP592fT10h2v.H.Ew1K0L6o4N/5uH5l5QG9255sT9qC', 40000.00),
('Bob Security', 'STAFF', '5566778899', 'bob@resort.com', '$2b$10$wY9aA.307xP592fT10h2v.H.Ew1K0L6o4N/5uH5l5QG9255sT9qC', 35000.00),
('Alice Manager', 'ADMIN', '2233445566', 'alice@resort.com', '$2b$10$wY9aA.307xP592fT10h2v.H.Ew1K0L6o4N/5uH5l5QG9255sT9qC', 75000.00);

-- 2. Insert CUSTOMERS
INSERT INTO CUSTOMERS (Name, Phone, Email, Address, PasswordHash) VALUES 
('Test Customer', '9988776655', 'customer@test.com', '123 Test Ave', '$2b$10$wY9aA.307xP592fT10h2v.H.Ew1K0L6o4N/5uH5l5QG9255sT9qC'),
('Mark Johnson', '7766554433', 'mark@example.com', '456 Main St', '$2b$10$wY9aA.307xP592fT10h2v.H.Ew1K0L6o4N/5uH5l5QG9255sT9qC'),
('Sarah Williams', '3344556677', 'sarah@example.com', '789 Oak Ln', '$2b$10$wY9aA.307xP592fT10h2v.H.Ew1K0L6o4N/5uH5l5QG9255sT9qC');

-- 3. Insert ROOM_TYPES
INSERT INTO ROOM_TYPES (TypeName, Description, Capacity, Rate) VALUES 
('Standard', 'Basic room with essential amenities', 2, 100.00),
('Deluxe', 'Spacious room with better view', 2, 150.00),
('Premium', 'Luxury room with premium services', 2, 250.00),
('Family', 'Large room suitable for families', 4, 300.00),
('Suite', 'Top tier suite with living area', 4, 500.00);

-- 4. Insert ROOMS
INSERT INTO ROOMS (RoomTypeID, RoomNo, FloorNo, Status) VALUES 
(1, '101', 1, 'AVAILABLE'),
(1, '102', 1, 'AVAILABLE'),
(2, '201', 2, 'AVAILABLE'),
(2, '202', 2, 'AVAILABLE'),
(3, '301', 3, 'AVAILABLE'),
(4, '401', 4, 'AVAILABLE'),
(5, '501', 5, 'AVAILABLE');

-- 5. Insert SERVICES
INSERT INTO SERVICES (ServiceName, Description, Charge) VALUES 
('Spa', 'Full body relaxing massage', 50.00),
('Swimming Pool', 'Access to main pool', 20.00),
('Laundry', 'Per bag laundry service', 15.00),
('Room Service', 'In-room dining delivery fee', 10.00),
('Gym', '24/7 gym access', 25.00),
('Airport Pickup', 'One-way transfer from airport', 40.00);

-- Will generate bookings dynamically or in the application to keep dates relative, 
-- but we can add one past booking for demonstration.
INSERT INTO BOOKINGS (CustomerID, CheckInDate, CheckOutDate, NoOfGuests, Status) VALUES 
(1, DATE_SUB(CURDATE(), INTERVAL 10 DAY), DATE_SUB(CURDATE(), INTERVAL 7 DAY), 2, 'CHECKED_OUT');

INSERT INTO ROOM_ALLOCATIONS (BookingID, RoomID, CheckInDate, CheckOutDate, Rate) VALUES 
(1, 1, DATE_SUB(CURDATE(), INTERVAL 10 DAY), DATE_SUB(CURDATE(), INTERVAL 7 DAY), 100.00);

INSERT INTO INVOICES (BookingID, InvoiceDate, TotalAmount, Discount, GrandTotal) VALUES 
(1, DATE_SUB(CURDATE(), INTERVAL 7 DAY), 300.00, 0, 300.00);

INSERT INTO PAYMENTS (InvoiceID, PaymentDate, Amount, PaymentMode, TxnReference, Status) VALUES 
(1, DATE_SUB(CURDATE(), INTERVAL 7 DAY), 300.00, 'CARD', 'TXN123456', 'SUCCESS');
