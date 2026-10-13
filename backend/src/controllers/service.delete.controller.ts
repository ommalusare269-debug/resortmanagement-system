import { Request, Response } from 'express';
import { prisma } from '../server';

export const deleteService = async (req: Request, res: Response) => {
  try {
    const { id } = req.params;
    await prisma.service.delete({
      where: { ServiceID: parseInt(id) }
    });
    res.json({ message: 'Service deleted' });
  } catch (error) {
    res.status(500).json({ error: 'Cannot delete service' });
  }
};
