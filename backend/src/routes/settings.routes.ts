import { Router } from 'express';
import { PrismaClient } from '@prisma/client';

const router = Router();
const prisma = new PrismaClient();

// Get all settings
router.get('/', async (req, res) => {
  try {
    const settings = await prisma.setting.findMany();
    const settingsMap = settings.reduce((acc: any, curr: any) => {
      acc[curr.Key] = curr.Value;
      return acc;
    }, {});
    res.json(settingsMap);
  } catch (err: any) {
    res.status(500).json({ error: err.message });
  }
});

// Update settings (bulk)
router.post('/', async (req, res) => {
  try {
    const updates = Object.entries(req.body).map(([key, value]) => {
      return prisma.setting.upsert({
        where: { Key: key },
        update: { Value: String(value) },
        create: { Key: key, Value: String(value) }
      });
    });

    await prisma.$transaction(updates);
    res.json({ message: 'Settings updated successfully' });
  } catch (err: any) {
    res.status(500).json({ error: err.message });
  }
});

export default router;
