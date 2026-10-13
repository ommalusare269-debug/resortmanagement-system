import { Router } from 'express';
import bcrypt from 'bcrypt';
import { prisma } from '../server';
import { authenticate, authorize } from '../middleware/auth';

const router = Router();

// Get all staff
router.get('/', authenticate, authorize(['ADMIN']), async (req, res) => {
  try {
    const staff = await prisma.staff.findMany({
      select: {
        StaffID: true,
        Name: true,
        Role: true,
        Department: true,
        Phone: true,
        Email: true,
        Salary: true,
      }
    });
    res.json(staff);
  } catch (error) {
    res.status(500).json({ error: 'Server error' });
  }
});

// Update staff department
router.put('/:id/department', authenticate, authorize(['ADMIN']), async (req, res) => {
  try {
    const { Department } = req.body;
    const staffId = parseInt(req.params.id);
    const updated = await prisma.staff.update({
      where: { StaffID: staffId },
      data: { Department }
    });
    res.json(updated);
  } catch (error) {
    res.status(500).json({ error: 'Server error' });
  }
});

// Create new staff
router.post('/', authenticate, authorize(['ADMIN']), async (req, res) => {
  try {
    const { Name, Email, Phone, Role, Department, Salary, Password } = req.body;
    
    const existing = await prisma.staff.findUnique({ where: { Email } });
    if (existing) return res.status(400).json({ error: 'Email already exists' });
    
    const PasswordHash = await bcrypt.hash(Password, 10);
    
    const staff = await prisma.staff.create({
      data: {
        Name,
        Email,
        Phone,
        Role,
        Department,
        Salary: parseFloat(Salary),
        PasswordHash
      }
    });
    
    res.status(201).json(staff);
  } catch (error) {
    res.status(500).json({ error: 'Server error' });
  }
});

// Delete staff
router.delete('/:id', authenticate, authorize(['ADMIN']), async (req, res) => {
  try {
    await prisma.staff.delete({
      where: { StaffID: parseInt(req.params.id) }
    });
    res.json({ message: 'Deleted successfully' });
  } catch (error) {
    res.status(500).json({ error: 'Server error' });
  }
});

export default router;
