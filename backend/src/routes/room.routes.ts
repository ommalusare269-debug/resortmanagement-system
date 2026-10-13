import { Router } from 'express';
import { getRoomTypes, createRoomType, updateRoomTypeDetails, getRooms, getAvailableRooms, createRoom, updateRoomCleaningStatus } from '../controllers/room.controller';
import { deleteRoom } from '../controllers/room.delete.controller';
import { updateRoomStatus } from '../controllers/room.status.controller';
import { authenticate, authorize } from '../middleware/auth';

const router = Router();

// Room Types
router.get('/types', getRoomTypes);
router.post('/types', authenticate, authorize(['ADMIN']), createRoomType);
router.put('/types/:id', authenticate, authorize(['ADMIN']), updateRoomTypeDetails);

// Rooms
router.get('/', getRooms);
router.get('/available', getAvailableRooms);
router.post('/', authenticate, authorize(['ADMIN']), createRoom);
router.put('/:id/status', authenticate, authorize(['ADMIN', 'STAFF']), updateRoomStatus);
router.put('/:id/cleaning', authenticate, authorize(['ADMIN', 'STAFF']), updateRoomCleaningStatus);
router.delete('/:id', authenticate, authorize(['ADMIN']), deleteRoom);

export default router;
