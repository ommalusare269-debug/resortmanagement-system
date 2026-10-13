import { Router } from 'express';
import { prisma } from '../server';
import { authenticate, authorize } from '../middleware/auth';

const router = Router();

// Mark Attendance
router.post('/mark', authenticate, authorize(['ADMIN', 'STAFF']), async (req, res) => {
  try {
    const { StaffID, Date, Status } = req.body;
    
    // Use upsert to handle updates if they already marked for today
    const attendance = await prisma.attendance.upsert({
      where: {
        StaffID_Date: {
          StaffID,
          Date: new Date(Date)
        }
      },
      update: {
        Status
      },
      create: {
        StaffID,
        Date: new Date(Date),
        Status
      }
    });

    res.json(attendance);
  } catch (error) {
    console.error(error);
    res.status(500).json({ error: 'Server error' });
  }
});

// Get attendance for a date
router.get('/date/:date', authenticate, authorize(['ADMIN', 'STAFF']), async (req, res) => {
  try {
    const targetDate = new Date(req.params.date);
    const records = await prisma.attendance.findMany({
      where: {
        Date: targetDate
      },
      include: {
        Staff: {
          select: { Name: true, Department: true, Role: true }
        }
      }
    });
    res.json(records);
  } catch (error) {
    res.status(500).json({ error: 'Server error' });
  }
});

// Get attendance for a specific staff member
router.get('/staff/:staffId', authenticate, authorize(['ADMIN', 'STAFF']), async (req, res) => {
  try {
    const records = await prisma.attendance.findMany({
      where: {
        StaffID: parseInt(req.params.staffId)
      },
      orderBy: {
        Date: 'desc'
      }
    });
    res.json(records);
  } catch (error) {
    res.status(500).json({ error: 'Server error' });
  }
});

export default router;
