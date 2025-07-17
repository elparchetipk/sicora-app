import { useUserStore } from '../stores/userStore';
import { Button } from '../components/Button';
import { BRAND_CONFIG, IS_SENA_BUILD } from '../config/brand';
import {
  UserGroupIcon,
  CalendarDaysIcon,
  ChartBarIcon,
  CogIcon,
  AcademicCapIcon,
  ClipboardDocumentListIcon,
  PresentationChartLineIcon,
} from '@heroicons/react/24/outline';

export function Dashboard() {
  const { user } = useUserStore();

  const dashboardCards = [
    {
      title: 'Demo Sistema',
      description: 'Ver demos de React Router, componentes y funcionalidades',
      icon: PresentationChartLineIcon,
      href: '/demo',
      color: 'purple',
      available: ['admin', 'coordinador', 'instructor', 'aprendiz', 'administrativo'],
    },
    {
      title: 'Gestión de Usuarios',
      description: 'Administrar instructores, aprendices y personal administrativo',
      icon: UserGroupIcon,
      href: '/usuarios',
      color: 'sena-primary',
      available: ['admin', 'coordinador'],
    },
    {
      title: 'Horarios Académicos',
      description: 'Programar y gestionar horarios de clases y actividades',
      icon: CalendarDaysIcon,
      href: '/horarios',
      color: 'blue',
      available: ['admin', 'coordinador', 'instructor'],
    },
    {
      title: 'Evaluaciones',
      description: 'Crear y gestionar evaluaciones de competencias',
      icon: ClipboardDocumentListIcon,
      href: '/evaluaciones',
      color: 'green',
      available: ['admin', 'coordinador', 'instructor'],
    },
    {
      title: 'Asistencia',
      description: 'Control y seguimiento de asistencia',
      icon: AcademicCapIcon,
      href: '/asistencia',
      color: 'purple',
      available: ['admin', 'coordinador', 'instructor'],
    },
    {
      title: 'Inteligencia Artificial',
      description: 'Asistente IA y análisis predictivo',
      icon: ChartBarIcon,
      href: '/ia',
      color: 'orange',
      available: ['admin', 'coordinador', 'instructor'],
    },
    {
      title: 'Reportes',
      description: 'Reportes y estadísticas del sistema',
      icon: ChartBarIcon,
      href: '/reportes',
      color: 'indigo',
      available: ['admin', 'coordinador'],
    },
    {
      title: 'Configuración',
      description: 'Configuración del sistema y parámetros',
      icon: CogIcon,
      href: '/configuracion',
      color: 'gray',
      available: ['admin'],
    },
  ];

  const availableCards = dashboardCards.filter((card) =>
    card.available.includes(user?.role || 'aprendiz')
  );

  const getWelcomeMessage = () => {
    const hour = new Date().getHours();
    let timeGreeting = 'Buenos días';

    if (hour >= 12 && hour < 18) {
      timeGreeting = 'Buenas tardes';
    } else if (hour >= 18) {
      timeGreeting = 'Buenas noches';
    }

    return `${timeGreeting}, ${user?.name || 'Usuario'}`;
  };

  const getRoleDisplay = () => {
    const roleMap = {
      admin: 'Administrador',
      coordinador: 'Coordinador Académico',
      instructor: 'Instructor',
      aprendiz: 'Aprendiz',
      administrativo: 'Personal Administrativo',
    };

    return roleMap[user?.role || 'aprendiz'];
  };

  return (
    <div className='space-y-8'>
      {/* Header de bienvenida */}
      <div className='bg-gradient-to-r from-sena-primary-600 to-sena-primary-700 rounded-lg p-8 text-white'>
        <h1 className='text-3xl font-bold mb-2'>{getWelcomeMessage()}</h1>
        <p className='text-sena-primary-100 text-lg'>
          {getRoleDisplay()} -{' '}
          {IS_SENA_BUILD ? user?.coordination || 'SENA CGMLTI' : BRAND_CONFIG.organizationFull}
        </p>
        {user?.ficha && IS_SENA_BUILD && (
          <p className='text-sena-primary-200 text-sm mt-1'>Ficha de Formación: {user.ficha}</p>
        )}
        {!IS_SENA_BUILD && (
          <p className='text-sena-primary-200 text-sm mt-1'>{BRAND_CONFIG.description}</p>
        )}
      </div>

      {/* Estadísticas rápidas */}
      <div className='grid grid-cols-1 md:grid-cols-3 gap-6'>
        <div className='bg-white p-6 rounded-lg shadow-md border border-gray-100'>
          <div className='flex items-center'>
            <div className='w-12 h-12 bg-blue-100 rounded-lg flex items-center justify-center'>
              <UserGroupIcon className='w-6 h-6 text-blue-600' />
            </div>
            <div className='ml-4'>
              <p className='text-2xl font-bold text-gray-900'>1,247</p>
              <p className='text-gray-600'>Usuarios Activos</p>
            </div>
          </div>
        </div>

        <div className='bg-white p-6 rounded-lg shadow-md border border-gray-100'>
          <div className='flex items-center'>
            <div className='w-12 h-12 bg-green-100 rounded-lg flex items-center justify-center'>
              <CalendarDaysIcon className='w-6 h-6 text-green-600' />
            </div>
            <div className='ml-4'>
              <p className='text-2xl font-bold text-gray-900'>89</p>
              <p className='text-gray-600'>Clases Programadas</p>
            </div>
          </div>
        </div>

        <div className='bg-white p-6 rounded-lg shadow-md border border-gray-100'>
          <div className='flex items-center'>
            <div className='w-12 h-12 bg-purple-100 rounded-lg flex items-center justify-center'>
              <ChartBarIcon className='w-6 h-6 text-purple-600' />
            </div>
            <div className='ml-4'>
              <p className='text-2xl font-bold text-gray-900'>95.2%</p>
              <p className='text-gray-600'>Asistencia Promedio</p>
            </div>
          </div>
        </div>
      </div>

      {/* Módulos disponibles */}
      <div>
        <h2 className='text-2xl font-bold text-gray-900 mb-6'>Módulos Disponibles</h2>

        <div className='grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6'>
          {availableCards.map((card) => {
            const IconComponent = card.icon;

            return (
              <div
                key={card.href}
                className='bg-white p-6 rounded-lg shadow-md border border-gray-100 hover:shadow-lg transition-shadow'
              >
                <div className='flex items-start justify-between mb-4'>
                  <div
                    className={`w-12 h-12 bg-${card.color}-100 rounded-lg flex items-center justify-center`}
                  >
                    <IconComponent className={`w-6 h-6 text-${card.color}-600`} />
                  </div>
                </div>

                <h3 className='text-lg font-semibold text-gray-900 mb-2'>{card.title}</h3>

                <p className='text-gray-600 text-sm mb-4 line-clamp-2'>{card.description}</p>

                {/* ✅ Botón de acción a la derecha siguiendo guías UX/UI */}
                <div className='flex justify-end'>
                  <Button
                    variant='primary'
                    size='sm'
                    onClick={() => (window.location.href = card.href)}
                  >
                    Acceder
                  </Button>
                </div>
              </div>
            );
          })}
        </div>
      </div>

      {/* Actividad reciente */}
      <div className='bg-white rounded-lg shadow-md border border-gray-100 p-6'>
        <h2 className='text-xl font-semibold text-gray-900 mb-4'>Actividad Reciente</h2>

        <div className='space-y-4'>
          <div className='flex items-center space-x-4 p-3 bg-gray-50 rounded-lg'>
            <div className='w-8 h-8 bg-blue-100 rounded-full flex items-center justify-center'>
              <UserGroupIcon className='w-4 h-4 text-blue-600' />
            </div>
            <div className='flex-1'>
              <p className='text-sm font-medium text-gray-900'>
                Nuevo usuario registrado: Ana López Torres
              </p>
              <p className='text-xs text-gray-500'>Hace 2 horas</p>
            </div>
          </div>

          <div className='flex items-center space-x-4 p-3 bg-gray-50 rounded-lg'>
            <div className='w-8 h-8 bg-green-100 rounded-full flex items-center justify-center'>
              <CalendarDaysIcon className='w-4 h-4 text-green-600' />
            </div>
            <div className='flex-1'>
              <p className='text-sm font-medium text-gray-900'>
                Horario actualizado para Ficha 2830024
              </p>
              <p className='text-xs text-gray-500'>Hace 4 horas</p>
            </div>
          </div>

          <div className='flex items-center space-x-4 p-3 bg-gray-50 rounded-lg'>
            <div className='w-8 h-8 bg-purple-100 rounded-full flex items-center justify-center'>
              <ClipboardDocumentListIcon className='w-4 h-4 text-purple-600' />
            </div>
            <div className='flex-1'>
              <p className='text-sm font-medium text-gray-900'>
                Nueva evaluación creada: Desarrollo Web Frontend
              </p>
              <p className='text-xs text-gray-500'>Ayer</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default Dashboard;
