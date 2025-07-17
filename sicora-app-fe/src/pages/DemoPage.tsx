import { useState } from 'react';
import { Button } from '../components/Button';
import { DisclaimerBanner } from '../components/DisclaimerBanner';
import { LegalNavigation } from '../components/LegalNavigation';
import { useUserStore } from '../stores/userStore';
import { useNavigate, useLocation } from 'react-router-dom';

/**
 * Demo Page - Página que muestra las funcionalidades de SICORA
 * Incluye el contenido original del App.tsx como demo
 */

// Tipos de usuario para demo
type UserRole = 'admin' | 'instructor' | 'aprendiz' | 'coordinador' | 'administrativo';

interface DemoUser {
  id: string;
  name: string;
  email: string;
  role: UserRole;
  avatar: string;
  status: 'online' | 'offline' | 'away' | 'busy';
  coordination?: string;
  ficha?: string;
}

// Datos de demostración de usuario
const demoUsers: Record<UserRole, DemoUser> = {
  admin: {
    id: '1',
    name: 'María González Rodríguez',
    email: 'maria.gonzalez@sena.edu.co',
    role: 'admin',
    avatar: '',
    status: 'online',
    coordination: 'Administración Central',
  },
  instructor: {
    id: '2',
    name: 'Carlos Pérez Martínez',
    email: 'carlos.perez@sena.edu.co',
    role: 'instructor',
    avatar: '',
    status: 'online',
    coordination: 'CGMLTI',
  },
  aprendiz: {
    id: '3',
    name: 'Ana López Torres',
    email: 'ana.lopez@sena.edu.co',
    role: 'aprendiz',
    avatar: '',
    status: 'online',
    ficha: '2830024',
  },
  coordinador: {
    id: '4',
    name: 'Roberto Silva Vega',
    email: 'roberto.silva@sena.edu.co',
    role: 'coordinador',
    avatar: '',
    status: 'online',
    coordination: 'CGMLTI',
  },
  administrativo: {
    id: '5',
    name: 'Elena Ruiz Morales',
    email: 'elena.ruiz@sena.edu.co',
    role: 'administrativo',
    avatar: '',
    status: 'online',
    coordination: 'Gestión Académica',
  },
};

export function DemoPage() {
  const navigate = useNavigate();
  const location = useLocation();
  const { user, setUser } = useUserStore();
  const [layoutDemo, setLayoutDemo] = useState<'demo' | 'navigation'>('demo');

  const handleRoleChange = (role: UserRole) => {
    const demoUser = demoUsers[role];
    setUser({
      id: demoUser.id,
      name: demoUser.name,
      email: demoUser.email,
      role: demoUser.role,
      avatar: demoUser.avatar,
      status: demoUser.status,
      coordination: demoUser.coordination,
      ficha: demoUser.ficha,
    });
  };

  const handleNavigateDemo = (href: string) => {
    navigate(href);
  };

  const renderContent = () => (
    <>
      {/* Aviso de Exención de Responsabilidad */}
      <DisclaimerBanner variant='card' dismissible={true} className='mb-8' />

      {/* Navegación Legal */}
      <div className='mb-8'>
        <LegalNavigation variant='grid' showIcons={true} showDescriptions={true} />
      </div>

      {/* Demo de Navegación por React Router */}
      <div className='text-center mb-8'>
        <h2 className='text-3xl font-sena-heading font-bold text-gray-900 mb-4'>
          🚀 ¡SICORA con React Router + Layout Institucional SENA!
        </h2>
        <p className='text-lg font-sena-body text-gray-600 mb-6 max-w-2xl mx-auto'>
          Sistema completo con React Router v6, Zustand y layout institucional inspirado en
          SofiaPlus
        </p>

        {/* Información de la Ubicación Actual */}
        <div className='bg-sena-primary-50 p-4 rounded-lg border border-sena-primary-200 mb-8'>
          <div className='flex items-center justify-center space-x-2 text-sena-primary-700'>
            <span className='text-xl'>📍</span>
            <span className='font-sena-body font-medium'>
              Ruta actual:{' '}
              <code className='bg-white px-2 py-1 rounded font-sena-mono text-sm'>
                {location.pathname}
              </code>
            </span>
          </div>
        </div>

        {/* Selector de Tipo de Demo */}
        <div className='bg-white p-6 rounded-lg shadow-md border border-gray-100 mb-6'>
          <h3 className='text-lg font-sena-heading font-semibold text-gray-900 mb-4'>
            🎛️ Tipo de Demo
          </h3>
          <div className='flex flex-wrap justify-center gap-3 mb-4'>
            <Button
              variant={layoutDemo === 'demo' ? 'primary' : 'outline'}
              size='sm'
              onClick={() => setLayoutDemo('demo')}
            >
              Demo Sistema
            </Button>
            <Button
              variant={layoutDemo === 'navigation' ? 'primary' : 'outline'}
              size='sm'
              onClick={() => setLayoutDemo('navigation')}
            >
              Demo Navegación
            </Button>
          </div>
        </div>

        {/* Demo de Navegación */}
        {layoutDemo === 'navigation' && (
          <div className='bg-white p-6 rounded-lg shadow-md border border-gray-100 mb-8'>
            <h3 className='text-lg font-sena-heading font-semibold text-gray-900 mb-4'>
              🧭 Navegación por React Router
            </h3>
            <div className='grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-3'>
              <Button
                variant='outline'
                size='sm'
                onClick={() => handleNavigateDemo('/')}
                className='flex flex-col items-center space-y-1 py-3'
              >
                <span>🏠</span>
                <span>Dashboard</span>
              </Button>
              <Button
                variant='outline'
                size='sm'
                onClick={() => handleNavigateDemo('/usuarios')}
                className='flex flex-col items-center space-y-1 py-3'
              >
                <span>👥</span>
                <span>Usuarios</span>
              </Button>
              <Button
                variant='outline'
                size='sm'
                onClick={() => handleNavigateDemo('/horarios')}
                className='flex flex-col items-center space-y-1 py-3'
              >
                <span>📅</span>
                <span>Horarios</span>
              </Button>
              <Button
                variant='outline'
                size='sm'
                onClick={() => handleNavigateDemo('/evaluaciones')}
                className='flex flex-col items-center space-y-1 py-3'
              >
                <span>📊</span>
                <span>Evaluaciones</span>
              </Button>
              <Button
                variant='outline'
                size='sm'
                onClick={() => handleNavigateDemo('/asistencia')}
                className='flex flex-col items-center space-y-1 py-3'
              >
                <span>✅</span>
                <span>Asistencia</span>
              </Button>
              <Button
                variant='outline'
                size='sm'
                onClick={() => handleNavigateDemo('/ia')}
                className='flex flex-col items-center space-y-1 py-3'
              >
                <span>🤖</span>
                <span>IA</span>
              </Button>
              <Button
                variant='outline'
                size='sm'
                onClick={() => handleNavigateDemo('/reportes')}
                className='flex flex-col items-center space-y-1 py-3'
              >
                <span>📈</span>
                <span>Reportes</span>
              </Button>
              <Button
                variant='outline'
                size='sm'
                onClick={() => handleNavigateDemo('/configuracion')}
                className='flex flex-col items-center space-y-1 py-3'
              >
                <span>⚙️</span>
                <span>Config</span>
              </Button>
            </div>
            <p className='text-sm text-gray-600 font-sena-body mt-4'>
              <strong>Navegación activa:</strong> Haz clic en cualquier módulo para navegar
            </p>
          </div>
        )}

        {/* Selector de Roles para Demo */}
        {layoutDemo === 'demo' && (
          <div className='bg-white p-6 rounded-lg shadow-md border border-gray-100 mb-8'>
            <h3 className='text-lg font-sena-heading font-semibold text-gray-900 mb-4'>
              🎭 Cambiar Rol de Usuario (Demo)
            </h3>
            <div className='flex flex-wrap justify-center gap-3'>
              {Object.entries(demoUsers).map(([role]) => (
                <Button
                  key={role}
                  variant={user?.role === role ? 'primary' : 'outline'}
                  size='md'
                  onClick={() => handleRoleChange(role as UserRole)}
                  className='flex items-center space-x-2'
                >
                  <span>
                    {role === 'admin' && '👑'}
                    {role === 'instructor' && '👨‍🏫'}
                    {role === 'aprendiz' && '🎓'}
                    {role === 'coordinador' && '📋'}
                    {role === 'administrativo' && '🏢'}
                  </span>
                  <span className='capitalize'>{role}</span>
                </Button>
              ))}
            </div>
            {user && (
              <div className='mt-4 text-sm text-gray-600 font-sena-body'>
                <strong>Usuario actual:</strong> {user.name} ({user.role})
                {user.coordination && <span> - {user.coordination}</span>}
                {user.ficha && <span> - Ficha: {user.ficha}</span>}
              </div>
            )}
          </div>
        )}
      </div>

      {/* Características del Sistema */}
      <div className='grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8'>
        <div className='bg-white p-6 rounded-lg shadow-md border border-gray-100'>
          <div className='w-12 h-12 bg-blue-100 rounded-lg flex items-center justify-center mx-auto mb-4'>
            <span className='text-2xl'>🛣️</span>
          </div>
          <h3 className='text-lg font-sena-heading font-semibold text-gray-900 mb-2'>
            React Router v6
          </h3>
          <p className='text-gray-600 font-sena-body text-sm'>
            Navegación moderna con rutas anidadas, breadcrumbs automáticos y URLs limpias
          </p>
        </div>

        <div className='bg-white p-6 rounded-lg shadow-md border border-gray-100'>
          <div className='w-12 h-12 bg-purple-100 rounded-lg flex items-center justify-center mx-auto mb-4'>
            <span className='text-2xl'>🏪</span>
          </div>
          <h3 className='text-lg font-sena-heading font-semibold text-gray-900 mb-2'>
            Zustand Store
          </h3>
          <p className='text-gray-600 font-sena-body text-sm'>
            Estado global persistente con LocalStorage para usuario y configuraciones
          </p>
        </div>

        <div className='bg-white p-6 rounded-lg shadow-md border border-gray-100'>
          <div className='w-12 h-12 bg-green-100 rounded-lg flex items-center justify-center mx-auto mb-4'>
            <span className='text-2xl'>⚡</span>
          </div>
          <h3 className='text-lg font-sena-heading font-semibold text-gray-900 mb-2'>
            React Query
          </h3>
          <p className='text-gray-600 font-sena-body text-sm'>
            Gestión eficiente de datos del servidor con cache automático y refetching
          </p>
        </div>

        <div className='bg-white p-6 rounded-lg shadow-md border border-gray-100'>
          <div className='w-12 h-12 bg-sena-primary-100 rounded-lg flex items-center justify-center mx-auto mb-4'>
            <span className='text-2xl'>🏛️</span>
          </div>
          <h3 className='text-lg font-sena-heading font-semibold text-gray-900 mb-2'>
            Layout Institucional
          </h3>
          <p className='text-gray-600 font-sena-body text-sm'>
            Header, footer, navegación y búsqueda institucional inspirados en SofiaPlus
          </p>
        </div>

        <div className='bg-white p-6 rounded-lg shadow-md border border-gray-100'>
          <div className='w-12 h-12 bg-yellow-100 rounded-lg flex items-center justify-center mx-auto mb-4'>
            <span className='text-2xl'>🔒</span>
          </div>
          <h3 className='text-lg font-sena-heading font-semibold text-gray-900 mb-2'>
            Validación REGEXP
          </h3>
          <p className='text-gray-600 font-sena-body text-sm'>
            Sistema de validación seguro con patrones REGEXP para prevenir ataques
          </p>
        </div>

        <div className='bg-white p-6 rounded-lg shadow-md border border-gray-100'>
          <div className='w-12 h-12 bg-red-100 rounded-lg flex items-center justify-center mx-auto mb-4'>
            <span className='text-2xl'>🎨</span>
          </div>
          <h3 className='text-lg font-sena-heading font-semibold text-gray-900 mb-2'>
            Identidad SENA
          </h3>
          <p className='text-gray-600 font-sena-body text-sm'>
            Colores, tipografías y componentes alineados con el manual de identidad SENA 2024
          </p>
        </div>
      </div>

      {/* Tecnologías utilizadas */}
      <div className='mt-16'>
        <h3 className='text-lg font-sena-heading font-semibold text-gray-900 mb-6 text-center'>
          Stack Tecnológico SICORA Frontend
        </h3>
        <div className='flex flex-wrap justify-center gap-4'>
          <span className='px-3 py-1 bg-blue-100 text-blue-800 text-sm font-sena-mono rounded-md'>
            React 19
          </span>
          <span className='px-3 py-1 bg-purple-100 text-purple-800 text-sm font-sena-mono rounded-md'>
            TypeScript 5.7
          </span>
          <span className='px-3 py-1 bg-green-100 text-green-800 text-sm font-sena-mono rounded-md'>
            Vite 7.0
          </span>
          <span className='px-3 py-1 bg-cyan-100 text-cyan-800 text-sm font-sena-mono rounded-md'>
            TailwindCSS 3.5
          </span>
          <span className='px-3 py-1 bg-indigo-100 text-indigo-800 text-sm font-sena-mono rounded-md'>
            React Router v6
          </span>
          <span className='px-3 py-1 bg-orange-100 text-orange-800 text-sm font-sena-mono rounded-md'>
            Zustand
          </span>
          <span className='px-3 py-1 bg-pink-100 text-pink-800 text-sm font-sena-mono rounded-md'>
            React Query
          </span>
          <span className='px-3 py-1 bg-yellow-100 text-yellow-800 text-sm font-sena-mono rounded-md'>
            Docker + DevContainer
          </span>
        </div>
      </div>
    </>
  );

  return <div className='container mx-auto px-4 py-8'>{renderContent()}</div>;
}

export default DemoPage;
