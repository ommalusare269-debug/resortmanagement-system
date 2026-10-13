import { Request, Response } from 'express';
import { prisma } from '../server';

export const getServices = async (req: Request, res: Response) => {
  try {
    const services = await prisma.service.findMany();
    res.json(services);
  } catch (error) {
    res.status(500).json({ error: 'Internal server error' });
  }
};

export const createService = async (req: Request, res: Response) => {
  try {
    const { ServiceName, Description, Charge } = req.body;
    const service = await prisma.service.create({
      data: { ServiceName, Description, Charge }
    });
    res.status(201).json(service);
  } catch (error) {
    res.status(500).json({ error: 'Internal server error' });
  }
};

export const addServiceToBooking = async (req: Request, res: Response): Promise<void> => {
  try {
    const { BookingID, ServiceID, Qty } = req.body;

    const service = await prisma.service.findUnique({ where: { ServiceID } });
    if (!service) {
      res.status(404).json({ error: 'Service not found' });
      return;
    }

    const Amount = Number(service.Charge) * Qty;

    const bookingService = await prisma.bookingService.create({
      data: {
        BookingID,
        ServiceID,
        Qty,
        Amount
      }
    });

    res.status(201).json({ message: 'Service added to booking', bookingService });
  } catch (error) {
    console.error(error);
    res.status(500).json({ error: 'Internal server error' });
  }
};

export const getServiceTasks = async (req: Request, res: Response) => {
  try {
    const tasks = await prisma.bookingService.findMany({
      include: {
        Service: true,
        Booking: {
          include: {
            Customer: true,
            RoomAllocations: {
              include: { Room: true }
            }
          }
        }
      },
      orderBy: { BookingServiceID: 'desc' }
    });
    res.json(tasks);
  } catch (error) {
    res.status(500).json({ error: 'Internal server error' });
  }
};

export const updateServiceTaskStatus = async (req: Request, res: Response) => {
  try {
    const { Status } = req.body;
    const task = await prisma.bookingService.update({
      where: { BookingServiceID: parseInt(req.params.id) },
      data: { Status }
    });
    res.json(task);
  } catch (error) {
    res.status(500).json({ error: 'Internal server error' });
  }
};
