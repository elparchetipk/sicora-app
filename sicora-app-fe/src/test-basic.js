// Test básico para verificar si JavaScript se ejecuta
console.log('🔍 JavaScript básico funcionando');

// Verificar que el DOM root existe
const root = document.getElementById('root');
console.log('🔍 Root element:', root);

if (root) {
  root.innerHTML =
    '<h1 style="color: green; padding: 20px;">✅ JavaScript funcionando - DOM actualizado</h1>';
  console.log('🔍 DOM actualizado exitosamente');
} else {
  console.error('❌ No se encontró el elemento root');
}

// Verificar si hay errores en el navegador
window.addEventListener('error', (event) => {
  console.error('❌ Error capturado:', event.error);
});

window.addEventListener('unhandledrejection', (event) => {
  console.error('❌ Promise rechazada:', event.reason);
});
