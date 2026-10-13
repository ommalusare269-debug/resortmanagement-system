import { Request, Response } from 'express';
import { prisma } from '../server';

export const updateRoomStatus = async (req: Request, res: Response) => {
  try {
    const { id } = req.params;
    const { Status } = req.body;
    
    await prisma.room.update({
      where: { RoomID: parseInt(id) },
      data: { Status }
    });
    
    res.json({ message: 'Room status updated' });
  } catch (error) {
    res.status(500).json({ error: 'Cannot update room status' });
  }
};
