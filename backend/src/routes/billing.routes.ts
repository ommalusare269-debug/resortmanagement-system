import { Router } from 'express';
import { generateInvoice, recordPayment, getInvoices } from '../controllers/billing.controller';
import { authenticate, authorize } from '../middleware/auth';

const router = Router();

router.get('/invoices', authenticate, authorize(['ADMIN', 'ACCOUNTANT']), getInvoices);
router.post('/invoice', authenticate, authorize(['ADMIN', 'ACCOUNTANT']), generateInvoice);
router.post('/payment', authenticate, authorize(['ADMIN', 'ACCOUNTANT', 'CUSTOMER']), recordPayment);

export default router;
