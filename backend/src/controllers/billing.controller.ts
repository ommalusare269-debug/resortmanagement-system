import { Request, Response } from 'express';
import { prisma } from '../server';

export const getInvoices = async (req: Request, res: Response) => {
  try {
    const invoices = await prisma.invoice.findMany({
      include: {
        Booking: {
          include: { Customer: true }
        },
        Payments: true
      },
      orderBy: { InvoiceDate: 'desc' }
    });
    res.json(invoices);
  } catch (error) {
    res.status(500).json({ error: 'Internal server error' });
  }
};

export const generateInvoice = async (req: Request, res: Response): Promise<void> => {
  try {
    const { BookingID, Discount = 0 } = req.body;

    const booking = await prisma.booking.findUnique({
      where: { BookingID },
      include: {
        RoomAllocations: true,
        BookingServices: true
      }
    });

    if (!booking) {
      res.status(404).json({ error: 'Booking not found' });
      return;
    }

    // Calculate room charges
    let roomCharges = 0;
    booking.RoomAllocations.forEach(allocation => {
      const days = Math.ceil((allocation.CheckOutDate.getTime() - allocation.CheckInDate.getTime()) / (1000 * 3600 * 24));
      roomCharges += (days > 0 ? days : 1) * Number(allocation.Rate);
    });

    // Calculate service charges
    let serviceCharges = 0;
    booking.BookingServices.forEach(service => {
      serviceCharges += Number(service.Amount);
    });

    const totalAmount = roomCharges + serviceCharges;
    const grandTotal = totalAmount - Discount;

    const invoice = await prisma.invoice.create({
      data: {
        BookingID,
        InvoiceDate: new Date(),
        TotalAmount: totalAmount,
        Discount,
        GrandTotal: grandTotal
      }
    });

    res.status(201).json({ message: 'Invoice generated successfully', invoice });
  } catch (error) {
    console.error(error);
    res.status(500).json({ error: 'Internal server error' });
  }
};

export const recordPayment = async (req: Request, res: Response): Promise<void> => {
  try {
    const { InvoiceID, Amount, PaymentMode, TxnReference } = req.body;

    const payment = await prisma.payment.create({
      data: {
        InvoiceID,
        PaymentDate: new Date(),
        Amount,
        PaymentMode,
        TxnReference,
        Status: 'SUCCESS'
      }
    });

    res.status(201).json({ message: 'Payment recorded', payment });
  } catch (error) {
    console.error(error);
    res.status(500).json({ error: 'Internal server error' });
  }
};
