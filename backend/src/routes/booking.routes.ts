import { Router } from 'express';
import { createBooking, getBookings, getCustomerBookings, getAllBookings } from '../controllers/booking.controller';
import { updateBookingStatus } from '../controllers/booking.status.controller';
import { authenticate, authorize } from '../middleware/auth';

const router = Router();

// Protect booking routes
router.put('/:id/status', authenticate, authorize(['ADMIN', 'STAFF', 'CUSTOMER']), updateBookingStatus);
router.post('/', authenticate, authorize(['CUSTOMER', 'ADMIN', 'STAFF']), createBooking);
router.get('/customer/:id', authenticate, getCustomerBookings);
router.get('/', authenticate, authorize(['ADMIN', 'STAFF', 'ACCOUNTANT']), getAllBookings);

export default router;
