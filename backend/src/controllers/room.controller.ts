import { Request, Response } from 'express';
import { prisma } from '../server';

export const getRoomTypes = async (req: Request, res: Response) => {
  try {
    const roomTypes = await prisma.roomType.findMany();
    res.json(roomTypes);
  } catch (error) {
    res.status(500).json({ error: 'Internal server error' });
  }
};

export const createRoomType = async (req: Request, res: Response) => {
  try {
    const { TypeName, Description, Capacity, Rate } = req.body;
    const roomType = await prisma.roomType.create({
      data: { TypeName, Description, Capacity, Rate }
    });
    res.status(201).json(roomType);
  } catch (error) {
    res.status(500).json({ error: 'Internal server error' });
  }
};

export const getRooms = async (req: Request, res: Response) => {
  try {
    const rooms = await prisma.room.findMany({ include: { RoomType: true } });
    res.json(rooms);
  } catch (error) {
    res.status(500).json({ error: 'Internal server error' });
  }
};

export const getAvailableRooms = async (req: Request, res: Response) => {
  try {
    // Basic available check (no dates given)
    const rooms = await prisma.room.findMany({
      where: { Status: 'AVAILABLE' },
      include: { RoomType: true }
    });
    res.json(rooms);
  } catch (error) {
    res.status(500).json({ error: 'Internal server error' });
  }
};

export const createRoom = async (req: Request, res: Response) => {
  try {
    const { RoomTypeID, RoomNo, FloorNo, Status } = req.body;
    const room = await prisma.room.create({
      data: { RoomTypeID, RoomNo, FloorNo, Status }
    });
    res.status(201).json(room);
  } catch (error) {
    res.status(500).json({ error: 'Internal server error' });
  }
};

export const updateRoomTypeDetails = async (req: Request, res: Response) => {
  try {
    const { Rate, Capacity } = req.body;
    
    // Only update fields that were actually provided
    const data: any = {};
    if (Rate !== undefined) data.Rate = parseFloat(Rate);
    if (Capacity !== undefined) data.Capacity = parseInt(Capacity);

    const roomType = await prisma.roomType.update({
      where: { RoomTypeID: parseInt(req.params.id) },
      data
    });
    res.json(roomType);
  } catch (error) {
    res.status(500).json({ error: 'Internal server error' });
  }
};

export const updateRoomCleaningStatus = async (req: Request, res: Response) => {
  try {
    const { CleaningStatus } = req.body;
    const room = await prisma.room.update({
      where: { RoomID: parseInt(req.params.id) },
      data: { CleaningStatus }
    });
    res.json(room);
  } catch (error) {
    res.status(500).json({ error: 'Internal server error' });
  }
};
