import { Router } from 'express';
import { registerCustomer, login } from '../controllers/auth.controller';

const router = Router();

router.post('/register', registerCustomer);
router.post('/login', login);

export default router;
