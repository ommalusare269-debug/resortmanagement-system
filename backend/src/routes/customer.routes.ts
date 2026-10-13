import { Router } from 'express';
import { getCustomers } from '../controllers/customer.controller';
import { deleteCustomer } from '../controllers/customer.delete.controller';
import { authenticate, authorize } from '../middleware/auth';

const router = Router();

router.delete('/:id', authenticate, authorize(['ADMIN']), deleteCustomer);
router.get('/', authenticate, authorize(['ADMIN', 'STAFF']), getCustomers);

export default router;
