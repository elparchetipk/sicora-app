import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { StrictMode } from 'react';
import { createRoot } from 'react-dom/client';
import './index.css';
// import AppDebug from './AppDebug.tsx';
// import AppRouterTest from './AppRouterTest.tsx';
// import AppLayoutTest from './AppLayoutTest.tsx';
import AppRouterSimplifiedTest from './AppRouterSimplifiedTest.tsx';

// Crear QueryClient
const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      retry: 1,
      refetchOnWindowFocus: false,
    },
  },
});

console.log('🔍 main.tsx cargado - Usando AppRouterSimplifiedTest');

createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <QueryClientProvider client={queryClient}>
      <AppRouterSimplifiedTest />
    </QueryClientProvider>
  </StrictMode>
);
