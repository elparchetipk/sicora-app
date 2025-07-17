import { Button } from '../components/Button';
import { HomeIcon } from '@heroicons/react/24/outline';

export function NotFoundPage() {
  return (
    <div className='min-h-screen bg-gray-50 flex flex-col justify-center'>
      <div className='max-w-md mx-auto text-center'>
        <div className='mb-8'>
          <div className='w-32 h-32 mx-auto bg-sena-primary-100 rounded-full flex items-center justify-center'>
            <span className='text-6xl font-bold text-sena-primary-600'>404</span>
          </div>
        </div>

        <h1 className='text-3xl font-bold text-gray-900 mb-4'>Página no encontrada</h1>

        <p className='text-gray-600 mb-8'>
          Lo sentimos, no pudimos encontrar la página que estás buscando. Verifica la URL o regresa
          al inicio.
        </p>

        {/* ✅ Botón de acción centrado (excepción a la regla en páginas de error) */}
        <div className='flex justify-center'>
          <Button variant='primary' onClick={() => (window.location.href = '/')}>
            <HomeIcon className='w-4 h-4 mr-2' />
            Volver al Inicio
          </Button>
        </div>
      </div>
    </div>
  );
}

export default NotFoundPage;
