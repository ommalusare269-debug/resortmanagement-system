import { Router } from 'express';
import { getServices, createService, addServiceToBooking, getServiceTasks, updateServiceTaskStatus } from '../controllers/service.controller';
import { deleteService } from '../controllers/service.delete.controller';
import { authenticate, authorize } from '../middleware/auth';

const router = Router();

router.delete('/:id', authenticate, authorize(['ADMIN']), deleteService);
router.get('/', getServices);
router.post('/', authenticate, authorize(['ADMIN']), createService);
router.post('/add-to-booking', authenticate, addServiceToBooking);

// Staff Tasks
router.get('/tasks', authenticate, authorize(['ADMIN', 'STAFF']), getServiceTasks);
router.put('/tasks/:id/status', authenticate, authorize(['ADMIN', 'STAFF']), updateServiceTaskStatus);

export default router;
