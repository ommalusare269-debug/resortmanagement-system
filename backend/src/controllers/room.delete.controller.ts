import { Request, Response } from 'express';
import { prisma } from '../server';

export const deleteRoom = async (req: Request, res: Response) => {
  try {
    const { id } = req.params;
    await prisma.room.delete({
      where: { RoomID: parseInt(id) }
    });
    res.json({ message: 'Room deleted' });
  } catch (error) {
    res.status(500).json({ error: 'Cannot delete room' });
  }
};
