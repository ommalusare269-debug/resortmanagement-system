import { Request, Response } from 'express';
import { prisma } from '../server';

export const deleteCustomer = async (req: Request, res: Response): Promise<void> => {
  try {
    const { id } = req.params;
    const customerId = parseInt(id);

    // Because we didn't specify onDelete: Cascade in the Prisma schema,
    // we must manually delete all dependent records in order to safely delete the customer.
    await prisma.$transaction(async (tx) => {
      // Find all bookings for this customer
      const bookings = await tx.booking.findMany({
        where: { CustomerID: customerId }
      });

      const bookingIds = bookings.map(b => b.BookingID);

      if (bookingIds.length > 0) {
        // Delete all payments related to invoices for these bookings
        const invoices = await tx.invoice.findMany({
          where: { BookingID: { in: bookingIds } }
        });
        const invoiceIds = invoices.map(i => i.InvoiceID);

        if (invoiceIds.length > 0) {
          await tx.payment.deleteMany({
            where: { InvoiceID: { in: invoiceIds } }
          });
        }

        // Delete invoices
        await tx.invoice.deleteMany({
          where: { BookingID: { in: bookingIds } }
        });

        // Delete booking services
        await tx.bookingService.deleteMany({
          where: { BookingID: { in: bookingIds } }
        });

        // Delete room allocations
        await tx.roomAllocation.deleteMany({
          where: { BookingID: { in: bookingIds } }
        });

        // Delete bookings
        await tx.booking.deleteMany({
          where: { CustomerID: customerId }
        });
      }

      // Finally, delete the customer
      await tx.customer.delete({
        where: { CustomerID: customerId }
      });
    });

    res.json({ message: 'Customer and all associated records deleted successfully' });
  } catch (error) {
    console.error(error);
    res.status(500).json({ error: 'Failed to delete customer' });
  }
};
