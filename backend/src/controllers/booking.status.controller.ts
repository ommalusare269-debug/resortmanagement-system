import { Request, Response } from 'express';
import { prisma } from '../server';

export const updateBookingStatus = async (req: Request, res: Response) => {
  try {
    const { id } = req.params;
    const { Status } = req.body;
    
    const booking = await prisma.booking.update({
      where: { BookingID: parseInt(id) },
      data: { Status },
      include: {
        RoomAllocations: true,
        BookingServices: true,
        Invoices: true
      }
    });
    
    // Automatically generate invoice upon checkout if not exists
    if (Status === 'CHECKED_OUT' && booking.Invoices.length === 0) {
      let roomCharges = 0;
      booking.RoomAllocations.forEach(allocation => {
        // Calculate days between check-in and check-out
        const days = Math.ceil((new Date(booking.CheckOutDate).getTime() - new Date(booking.CheckInDate).getTime()) / (1000 * 3600 * 24));
        roomCharges += (days > 0 ? days : 1) * Number(allocation.Rate);
      });

      let serviceCharges = 0;
      booking.BookingServices.forEach(service => {
        serviceCharges += Number(service.Amount);
      });

      const totalAmount = roomCharges + serviceCharges;

      await prisma.invoice.create({
        data: {
          BookingID: booking.BookingID,
          InvoiceDate: new Date(),
          TotalAmount: totalAmount,
          Discount: 0,
          GrandTotal: totalAmount
        }
      });
    }

    // Automatically update physical Room status based on booking status
    if (Status === 'CHECKED_IN') {
      booking.RoomAllocations.forEach(async (allocation) => {
        await prisma.room.update({
          where: { RoomID: allocation.RoomID },
          data: { Status: 'OCCUPIED' }
        });
      });
    } else if (Status === 'CHECKED_OUT') {
      booking.RoomAllocations.forEach(async (allocation) => {
        await prisma.room.update({
          where: { RoomID: allocation.RoomID },
          data: { Status: 'AVAILABLE', CleaningStatus: 'Dirty' }
        });
      });
    }

    res.json({ message: 'Status updated' });
  } catch (error) {
    res.status(500).json({ error: 'Internal server error' });
  }
};
