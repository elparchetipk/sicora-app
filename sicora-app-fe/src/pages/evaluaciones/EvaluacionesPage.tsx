import { useState } from 'react';
import { Button } from '../../components/Button';
import {
  ClipboardDocumentListIcon,
  PlusIcon,
  ChartBarIcon,
  CalendarDaysIcon,
  AcademicCapIcon,
} from '@heroicons/react/24/outline';

export function EvaluacionesPage() {
  const [activeTab, setActiveTab] = useState<'proyectos' | 'individuales' | 'reportes'>(
    'proyectos'
  );

  // Mock data para evaluaciones
  const evaluaciones = [
    {
      id: '1',
      title: 'Desarrollo de API REST',
      type: 'proyecto',
      instructor: 'Carlos Pérez',
      ficha: '2830024',
      fechaEntrega: '2025-07-15',
      estado: 'activa',
      estudiantes: 25,
      entregados: 18,
    },
    {
      id: '2',
      title: 'Evaluación React Hooks',
      type: 'individual',
      instructor: 'Ana López',
      ficha: '2830025',
      fechaEntrega: '2025-07-10',
      estado: 'calificando',
      estudiantes: 30,
      entregados: 30,
    },
    {
      id: '3',
      title: 'Proyecto Base de Datos',
      type: 'proyecto',
      instructor: 'María González',
      ficha: '2830024',
      fechaEntrega: '2025-07-20',
      estado: 'borrador',
      estudiantes: 25,
      entregados: 0,
    },
  ];

  const getStatusBadge = (estado: string) => {
    const statusStyles = {
      activa: 'bg-green-100 text-green-800',
      calificando: 'bg-yellow-100 text-yellow-800',
      borrador: 'bg-gray-100 text-gray-800',
      finalizada: 'bg-blue-100 text-blue-800',
    };

    const statusLabels = {
      activa: 'Activa',
      calificando: 'Calificando',
      borrador: 'Borrador',
      finalizada: 'Finalizada',
    };

    return (
      <span
        className={`px-2 py-1 text-xs font-medium rounded-full ${statusStyles[estado as keyof typeof statusStyles]}`}
      >
        {statusLabels[estado as keyof typeof statusLabels]}
      </span>
    );
  };

  const tabs = [
    { id: 'proyectos', label: 'Evaluación de Proyectos', icon: ClipboardDocumentListIcon },
    { id: 'individuales', label: 'Evaluaciones Individuales', icon: AcademicCapIcon },
    { id: 'reportes', label: 'Reportes', icon: ChartBarIcon },
  ];

  return (
    <div className='space-y-6'>
      {/* Header */}
      <div className='flex justify-between items-center'>
        <div>
          <h1 className='text-2xl font-bold text-gray-900'>Sistema de Evaluaciones</h1>
          <p className='text-gray-600 mt-1'>Gestión integral de evaluaciones de competencias</p>
        </div>

        {/* ✅ Acciones principales a la derecha */}
        <div className='flex items-center space-x-3'>
          <Button variant='outline' size='sm'>
            <ChartBarIcon className='w-4 h-4 mr-2' />
            Estadísticas
          </Button>
          <Button variant='primary'>
            <PlusIcon className='w-4 h-4 mr-2' />
            Nueva Evaluación
          </Button>
        </div>
      </div>

      {/* Estadísticas rápidas */}
      <div className='grid grid-cols-1 md:grid-cols-4 gap-6'>
        <div className='bg-white p-6 rounded-lg shadow-md border border-gray-100'>
          <div className='flex items-center'>
            <div className='w-12 h-12 bg-blue-100 rounded-lg flex items-center justify-center'>
              <ClipboardDocumentListIcon className='w-6 h-6 text-blue-600' />
            </div>
            <div className='ml-4'>
              <p className='text-2xl font-bold text-gray-900'>15</p>
              <p className='text-gray-600'>Evaluaciones Activas</p>
            </div>
          </div>
        </div>

        <div className='bg-white p-6 rounded-lg shadow-md border border-gray-100'>
          <div className='flex items-center'>
            <div className='w-12 h-12 bg-green-100 rounded-lg flex items-center justify-center'>
              <AcademicCapIcon className='w-6 h-6 text-green-600' />
            </div>
            <div className='ml-4'>
              <p className='text-2xl font-bold text-gray-900'>348</p>
              <p className='text-gray-600'>Entregas Recibidas</p>
            </div>
          </div>
        </div>

        <div className='bg-white p-6 rounded-lg shadow-md border border-gray-100'>
          <div className='flex items-center'>
            <div className='w-12 h-12 bg-yellow-100 rounded-lg flex items-center justify-center'>
              <CalendarDaysIcon className='w-6 h-6 text-yellow-600' />
            </div>
            <div className='ml-4'>
              <p className='text-2xl font-bold text-gray-900'>7</p>
              <p className='text-gray-600'>Pendientes Calificar</p>
            </div>
          </div>
        </div>

        <div className='bg-white p-6 rounded-lg shadow-md border border-gray-100'>
          <div className='flex items-center'>
            <div className='w-12 h-12 bg-purple-100 rounded-lg flex items-center justify-center'>
              <ChartBarIcon className='w-6 h-6 text-purple-600' />
            </div>
            <div className='ml-4'>
              <p className='text-2xl font-bold text-gray-900'>87.3%</p>
              <p className='text-gray-600'>Promedio General</p>
            </div>
          </div>
        </div>
      </div>

      {/* Tabs de navegación */}
      <div className='bg-white rounded-lg shadow-md border border-gray-100'>
        <div className='border-b border-gray-200'>
          <nav className='flex space-x-8 px-6'>
            {tabs.map((tab) => {
              const IconComponent = tab.icon;
              return (
                <button
                  key={tab.id}
                  onClick={() => setActiveTab(tab.id as 'proyectos' | 'individuales' | 'reportes')}
                  className={`flex items-center space-x-2 py-4 px-1 border-b-2 font-medium text-sm ${
                    activeTab === tab.id
                      ? 'border-sena-primary-500 text-sena-primary-600'
                      : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                  }`}
                >
                  <IconComponent className='w-5 h-5' />
                  <span>{tab.label}</span>
                </button>
              );
            })}
          </nav>
        </div>

        {/* Contenido de evaluaciones */}
        <div className='p-6'>
          <div className='space-y-4'>
            {evaluaciones.map((evaluacion) => (
              <div
                key={evaluacion.id}
                className='border border-gray-200 rounded-lg p-6 hover:bg-gray-50'
              >
                <div className='flex items-center justify-between'>
                  <div className='flex-1'>
                    <div className='flex items-center space-x-3 mb-2'>
                      <h3 className='text-lg font-medium text-gray-900'>{evaluacion.title}</h3>
                      {getStatusBadge(evaluacion.estado)}
                    </div>

                    <div className='grid grid-cols-2 md:grid-cols-4 gap-4 text-sm text-gray-600'>
                      <div>
                        <span className='font-medium'>Instructor:</span> {evaluacion.instructor}
                      </div>
                      <div>
                        <span className='font-medium'>Ficha:</span> {evaluacion.ficha}
                      </div>
                      <div>
                        <span className='font-medium'>Fecha entrega:</span>{' '}
                        {evaluacion.fechaEntrega}
                      </div>
                      <div>
                        <span className='font-medium'>Progreso:</span> {evaluacion.entregados}/
                        {evaluacion.estudiantes}
                      </div>
                    </div>

                    {/* Barra de progreso */}
                    <div className='mt-3'>
                      <div className='flex items-center justify-between text-sm text-gray-600 mb-1'>
                        <span>Entregas recibidas</span>
                        <span>
                          {Math.round((evaluacion.entregados / evaluacion.estudiantes) * 100)}%
                        </span>
                      </div>
                      <div className='w-full bg-gray-200 rounded-full h-2'>
                        <div
                          className='bg-sena-primary-600 h-2 rounded-full'
                          style={{
                            width: `${(evaluacion.entregados / evaluacion.estudiantes) * 100}%`,
                          }}
                        ></div>
                      </div>
                    </div>
                  </div>

                  {/* ✅ Acciones por evaluación a la derecha */}
                  <div className='flex items-center space-x-2 ml-6'>
                    <Button variant='ghost' size='sm'>
                      Ver Detalles
                    </Button>
                    <Button variant='ghost' size='sm'>
                      Calificar
                    </Button>
                    <Button variant='outline' size='sm'>
                      Editar
                    </Button>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Actividad reciente */}
      <div className='bg-white rounded-lg shadow-md border border-gray-100 p-6'>
        <h2 className='text-lg font-medium text-gray-900 mb-4'>
          Actividad Reciente en Evaluaciones
        </h2>

        <div className='space-y-3'>
          <div className='flex items-center space-x-4 p-3 bg-gray-50 rounded-lg'>
            <div className='w-8 h-8 bg-green-100 rounded-full flex items-center justify-center'>
              <ClipboardDocumentListIcon className='w-4 h-4 text-green-600' />
            </div>
            <div className='flex-1'>
              <p className='text-sm font-medium text-gray-900'>
                Nueva entrega recibida: "Desarrollo de API REST"
              </p>
              <p className='text-xs text-gray-500'>Ana López Torres - Hace 15 minutos</p>
            </div>
          </div>

          <div className='flex items-center space-x-4 p-3 bg-gray-50 rounded-lg'>
            <div className='w-8 h-8 bg-blue-100 rounded-full flex items-center justify-center'>
              <ChartBarIcon className='w-4 h-4 text-blue-600' />
            </div>
            <div className='flex-1'>
              <p className='text-sm font-medium text-gray-900'>
                Evaluación calificada: "React Hooks" - Nota: 4.2
              </p>
              <p className='text-xs text-gray-500'>Carlos Pérez - Hace 1 hora</p>
            </div>
          </div>

          <div className='flex items-center space-x-4 p-3 bg-gray-50 rounded-lg'>
            <div className='w-8 h-8 bg-yellow-100 rounded-full flex items-center justify-center'>
              <CalendarDaysIcon className='w-4 h-4 text-yellow-600' />
            </div>
            <div className='flex-1'>
              <p className='text-sm font-medium text-gray-900'>
                Recordatorio: "Proyecto Base de Datos" vence en 3 días
              </p>
              <p className='text-xs text-gray-500'>Sistema - Hace 2 horas</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default EvaluacionesPage;
