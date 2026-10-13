import { Router } from 'express';
import { getDashboardStats } from '../controllers/report.controller';
import { authenticate, authorize } from '../middleware/auth';

const router = Router();

router.get('/stats', authenticate, authorize(['ADMIN', 'ACCOUNTANT']), getDashboardStats);

export default router;
