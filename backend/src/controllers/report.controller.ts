import { Request, Response } from 'express';
import { prisma } from '../server';

export const getDashboardStats = async (req: Request, res: Response) => {
  try {
    const customersCount = await prisma.customer.count();
    const roomsCount = await prisma.room.count();
    
    const revenueResult = await prisma.payment.aggregate({
      _sum: { Amount: true },
      where: { Status: 'SUCCESS' }
    });

    const activeBookings = await prisma.booking.count({
      where: { Status: { in: ['CONFIRMED', 'CHECKED_IN'] } }
    });

    res.json({
      totalCustomers: customersCount,
      totalRooms: roomsCount,
      activeBookings,
      totalRevenue: revenueResult._sum.Amount || 0
    });
  } catch (error) {
    res.status(500).json({ error: 'Internal server error' });
  }
};
