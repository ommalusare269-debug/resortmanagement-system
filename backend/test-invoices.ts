async function test() {
  const loginRes = await fetch('http://localhost:5000/api/auth/login', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      Email: 'admin@resort.com',
      Password: 'password123',
      Role: 'ADMIN'
    })
  });
  
  const loginData = await loginRes.json();
  const token = loginData.token;
  
  if (!token) return;

  const res = await fetch('http://localhost:5000/api/billing/invoices', {
    headers: { Authorization: `Bearer ${token}` }
  });
  
  const text = await res.text();
  console.log(text);
}

test();
