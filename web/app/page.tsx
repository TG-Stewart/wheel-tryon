'use client';

import React, { useEffect, useRef, useState } from 'react';

export default function Page() {
  const API_BASE = process.env.NEXT_PUBLIC_API_BASE || 'http://localhost:8000';
  const canvasRef = useRef(null);
  const [carSrc, setCarSrc] = useState('');
  const [wheelSrc, setWheelSrc] = useState('');
  const [wheels, setWheels] = useState([]);

  async function handleCar(e) {
    const file = e.target.files[0];
    if (!file) return;
    setCarSrc(URL.createObjectURL(file));

    const fd = new FormData();
    fd.append('car', file);
    const res = await fetch(`${API_BASE}/detect-wheels`, { method: 'POST', body: fd });
    const data = await res.json();
    setWheels(data.wheels || []);
  }

  async function handleWheel(e) {
    const file = e.target.files[0];
    if (!file) return;
    setWheelSrc(URL.createObjectURL(file));
  }

  useEffect(() => {
    async function render() {
      if (!canvasRef.current || !carSrc) return;
      const canvas = canvasRef.current;
      const ctx = canvas.getContext('2d');

      const carImg = new Image();
      carImg.src = carSrc;
      await new Promise(r => carImg.onload = r);

      canvas.width = carImg.width;
      canvas.height = carImg.height;
      ctx.drawImage(carImg, 0, 0);

      if (!wheelSrc || wheels.length === 0) return;

      const wheelImg = new Image();
      wheelImg.src = wheelSrc;
      await new Promise(r => wheelImg.onload = r);

      wheels.forEach(w => {
        const size = 2 * w.r;
        ctx.drawImage(wheelImg, w.cx - size/2, w.cy - size/2, size, size);
      });
    }

    render();
  }, [carSrc, wheelSrc, wheels]);

  return (
    <div style={{ padding: 20 }}>
      <h1>Wheel Try-On (AI Positioning)</h1>
      <input type="file" accept="image/*" onChange={handleCar} />
      <br/><br/>
      <input type="file" accept="image/*" onChange={handleWheel} />
      <br/><br/>
      <canvas ref={canvasRef} style={{ maxWidth: '100%' }} />
    </div>
  );
}
