import { Request, Response } from 'express';
import { prisma } from '../server';

export const createBooking = async (req: Request, res: Response): Promise<void> => {
  try {
    const { CustomerID, CheckInDate, CheckOutDate, NoOfGuests, RoomID } = req.body;

    if (!CustomerID || !CheckInDate || !CheckOutDate || !NoOfGuests || !RoomID) {
      res.status(400).json({ error: 'Missing required booking fields' });
      return;
    }

    const checkIn = new Date(CheckInDate);
    const checkOut = new Date(CheckOutDate);

    if (checkOut <= checkIn) {
      res.status(400).json({ error: 'Check-out date must be after check-in date' });
      return;
    }

    // 1. Check if the room is available for these dates
    const overlappingAllocations = await prisma.roomAllocation.findMany({
      where: {
        RoomID: RoomID,
        AND: [
          { CheckInDate: { lt: checkOut } },
          { CheckOutDate: { gt: checkIn } }
        ]
      }
    });

    if (overlappingAllocations.length > 0) {
      res.status(409).json({ error: 'Room is not available for selected dates' });
      return;
    }

    // 2. Fetch the room rate
    const room = await prisma.room.findUnique({
      where: { RoomID },
      include: { RoomType: true }
    });

    if (!room) {
      res.status(404).json({ error: 'Room not found' });
      return;
    }

    // 3. Create the Booking and Room Allocation inside a transaction
    const transaction = await prisma.$transaction(async (tx) => {
      const newBooking = await tx.booking.create({
        data: {
          CustomerID,
          CheckInDate: checkIn,
          CheckOutDate: checkOut,
          NoOfGuests,
          Status: 'CONFIRMED'
        }
      });

      const newAllocation = await tx.roomAllocation.create({
        data: {
          BookingID: newBooking.BookingID,
          RoomID: RoomID,
          CheckInDate: checkIn,
          CheckOutDate: checkOut,
          Rate: room.RoomType.Rate
        }
      });

      return { newBooking, newAllocation };
    });

    res.status(201).json({ 
      message: 'Booking created successfully', 
      booking: transaction.newBooking 
    });

  } catch (error) {
    console.error(error);
    res.status(500).json({ error: 'Internal server error' });
  }
};

export const getCustomerBookings = async (req: Request, res: Response): Promise<void> => {
  try {
    const { id } = req.params;
    const bookings = await prisma.booking.findMany({
      where: { CustomerID: parseInt(id) },
      include: {
        RoomAllocations: { include: { Room: { include: { RoomType: true } } } },
        BookingServices: { include: { Service: true } },
        Invoices: { include: { Payments: true } }
      },
      orderBy: { BookingDate: 'desc' }
    });
    res.json(bookings);
  } catch (error) {
    console.error(error);
    res.status(500).json({ error: 'Internal server error' });
  }
};

export const getAllBookings = async (req: Request, res: Response): Promise<void> => {
  try {
    const bookings = await prisma.booking.findMany({
      include: {
        Customer: true,
        RoomAllocations: { include: { Room: true } }
      },
      orderBy: { BookingDate: 'desc' }
    });
    res.json(bookings);
  } catch (error) {
    console.error(error);
    res.status(500).json({ error: 'Internal server error' });
  }
};
