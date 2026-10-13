import jwt from 'jsonwebtoken';

async function test() {
  const token = jwt.sign({ id: 4, role: 'CUSTOMER' }, 'resort_super_secret_key_2026_for_dev_only', { expiresIn: '1d' });
  
  const res = await fetch('http://localhost:5000/api/billing/payment', {
    method: 'POST',
    headers: { 
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${token}` 
    },
    body: JSON.stringify({
        InvoiceID: 1,
        Amount: 100,
        PaymentMode: 'CARD',
        TxnReference: 'DEMO'
    })
  });
  
  const text = await res.text();
  console.log('Payment Res:', text);
}

test();
