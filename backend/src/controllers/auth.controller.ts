import { Request, Response } from 'express';
import bcrypt from 'bcrypt';
import { prisma } from '../server';
import { generateToken } from '../utils/jwt';

export const registerCustomer = async (req: Request, res: Response): Promise<void> => {
  try {
    const { Name, Phone, Email, Address, Password } = req.body;

    if (!Name || !Phone || !Email || !Password) {
      res.status(400).json({ error: 'Missing required fields' });
      return;
    }

    const existingUser = await prisma.customer.findUnique({ where: { Email } });
    if (existingUser) {
      res.status(409).json({ error: 'Email already exists' });
      return;
    }

    const PasswordHash = await bcrypt.hash(Password, 10);

    const newCustomer = await prisma.customer.create({
      data: {
        Name,
        Phone,
        Email,
        Address,
        PasswordHash,
      },
    });

    res.status(201).json({ message: 'Customer registered successfully', customerId: newCustomer.CustomerID });
  } catch (error) {
    console.error(error);
    res.status(500).json({ error: 'Internal server error' });
  }
};

export const login = async (req: Request, res: Response): Promise<void> => {
  try {
    const { Email, Password, Role } = req.body;

    if (!Email || !Password || !Role) {
      res.status(400).json({ error: 'Email, Password, and Role are required' });
      return;
    }

    if (Role === 'CUSTOMER') {
      const customer = await prisma.customer.findUnique({ where: { Email } });
      if (!customer) {
        res.status(401).json({ error: 'Invalid credentials' });
        return;
      }
      const isMatch = await bcrypt.compare(Password, customer.PasswordHash);
      if (!isMatch) {
        res.status(401).json({ error: 'Invalid credentials' });
        return;
      }
      const token = generateToken({ id: customer.CustomerID, role: 'CUSTOMER' });
      res.json({ token, user: { id: customer.CustomerID, name: customer.Name, role: 'CUSTOMER' } });
    } else {
      // ADMIN, ACCOUNTANT, STAFF
      const staff = await prisma.staff.findUnique({ where: { Email } });
      if (!staff || staff.Role !== Role) {
        res.status(401).json({ error: 'Invalid credentials or role' });
        return;
      }
      const isMatch = await bcrypt.compare(Password, staff.PasswordHash);
      if (!isMatch) {
        res.status(401).json({ error: 'Invalid credentials' });
        return;
      }
      const token = generateToken({ id: staff.StaffID, role: staff.Role });
      res.json({ token, user: { id: staff.StaffID, name: staff.Name, role: staff.Role } });
    }
  } catch (error) {
    console.error(error);
    res.status(500).json({ error: 'Internal server error' });
  }
};
