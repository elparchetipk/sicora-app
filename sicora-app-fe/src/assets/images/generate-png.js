// Simple PNG pixel data
const w = 256,
  h = 256;
const canvas = document.createElement('canvas');
canvas.width = w;
canvas.height = h;
const ctx = canvas.getContext('2d');

// Fondo circular
ctx.fillStyle = '#E6F4D7';
ctx.beginPath();
ctx.arc(w / 2, h / 2, w / 2, 0, Math.PI * 2);
ctx.fill();

// Cabeza
ctx.fillStyle = '#39A900';
ctx.beginPath();
ctx.arc(w / 2, h * 0.4, w / 4, 0, Math.PI * 2);
ctx.fill();

// Cuerpo
ctx.beginPath();
ctx.moveTo(w / 2, h * 0.55);
ctx.bezierCurveTo(w * 0.3, h * 0.55, w * 0.2, h * 0.7, w * 0.2, h);
ctx.lineTo(w * 0.8, h);
ctx.bezierCurveTo(w * 0.8, h * 0.7, w * 0.7, h * 0.55, w / 2, h * 0.55);
ctx.fill();

// Convertir a base64
const dataUrl = canvas.toDataURL('image/png');
console.log(dataUrl);
