import { BrowserRouter } from 'react-router-dom';
import { AppRouter } from './router';
import { useUserStore } from './stores/userStore';
import { useEffect } from 'react';

/**
 * SICORA - Sistema de Información de Coordinación Académica
 * Frontend con React 19 + Vite + TailwindCSS
 * Diseño institucional SENA 2024 - Manual de Identidad
 *
 * App principal con React Router y Zustand
 */

function App() {
  const { initializeUser } = useUserStore();

  useEffect(() => {
    // Inicializar usuario demo al cargar la aplicación
    initializeUser();
  }, [initializeUser]);

  return (
    <BrowserRouter>
      <AppRouter />
    </BrowserRouter>
  );
}

export default App;
