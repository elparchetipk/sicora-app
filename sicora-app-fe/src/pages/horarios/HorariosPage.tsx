import { useState } from 'react';
import { Button } from '../../components/Button';
import {
  CalendarDaysIcon,
  PlusIcon,
  ChevronLeftIcon,
  ChevronRightIcon,
  ClockIcon,
} from '@heroicons/react/24/outline';

export function HorariosPage() {
  const [currentDate] = useState(new Date());
  const [viewMode, setViewMode] = useState<'week' | 'month'>('week');

  // Mock data para horarios
  const horarios = [
    {
      id: '1',
      title: 'Programación Backend',
      instructor: 'Carlos Pérez',
      ficha: '2830024',
      ambiente: 'Lab 101',
      startTime: '08:00',
      endTime: '12:00',
      date: '2025-07-01',
      color: 'blue',
    },
    {
      id: '2',
      title: 'Base de Datos',
      instructor: 'María González',
      ficha: '2830024',
      ambiente: 'Lab 102',
      startTime: '14:00',
      endTime: '18:00',
      date: '2025-07-01',
      color: 'green',
    },
    {
      id: '3',
      title: 'Frontend React',
      instructor: 'Ana López',
      ficha: '2830025',
      ambiente: 'Lab 103',
      startTime: '08:00',
      endTime: '12:00',
      date: '2025-07-02',
      color: 'purple',
    },
  ];

  const formatDate = (date: Date) => {
    return date.toLocaleDateString('es-CO', {
      weekday: 'long',
      year: 'numeric',
      month: 'long',
      day: 'numeric',
    });
  };

  const getWeekDays = (date: Date) => {
    const start = new Date(date);
    start.setDate(start.getDate() - start.getDay() + 1); // Lunes

    const days = [];
    for (let i = 0; i < 5; i++) {
      // Solo días laborales
      const day = new Date(start);
      day.setDate(start.getDate() + i);
      days.push(day);
    }
    return days;
  };

  const weekDays = getWeekDays(currentDate);

  return (
    <div className='space-y-6'>
      {/* Header */}
      <div className='flex justify-between items-center'>
        <div>
          <h1 className='text-2xl font-bold text-gray-900'>Horarios Académicos</h1>
          <p className='text-gray-600 mt-1'>Gestión y programación de horarios de clase</p>
        </div>

        {/* ✅ Acciones principales a la derecha */}
        <div className='flex items-center space-x-3'>
          <Button
            variant={viewMode === 'week' ? 'primary' : 'outline'}
            size='sm'
            onClick={() => setViewMode('week')}
          >
            Semana
          </Button>
          <Button
            variant={viewMode === 'month' ? 'primary' : 'outline'}
            size='sm'
            onClick={() => setViewMode('month')}
          >
            Mes
          </Button>
          <Button variant='primary'>
            <PlusIcon className='w-4 h-4 mr-2' />
            Nueva Clase
          </Button>
        </div>
      </div>

      {/* Navegación de fecha */}
      <div className='bg-white p-6 rounded-lg shadow-md border border-gray-100'>
        <div className='flex items-center justify-between'>
          <Button variant='outline' size='sm'>
            <ChevronLeftIcon className='w-4 h-4 mr-1' />
            Anterior
          </Button>

          <div className='text-center'>
            <h2 className='text-lg font-semibold text-gray-900'>{formatDate(currentDate)}</h2>
            <p className='text-sm text-gray-500'>
              Semana del {weekDays[0].getDate()} al {weekDays[4].getDate()}
            </p>
          </div>

          <Button variant='outline' size='sm'>
            Siguiente
            <ChevronRightIcon className='w-4 h-4 ml-1' />
          </Button>
        </div>
      </div>

      {/* Vista de calendario semanal */}
      <div className='bg-white rounded-lg shadow-md border border-gray-100 overflow-hidden'>
        <div className='p-6 border-b border-gray-200'>
          <div className='flex items-center space-x-2'>
            <CalendarDaysIcon className='w-5 h-5 text-gray-500' />
            <h2 className='text-lg font-medium text-gray-900'>Programación Semanal</h2>
          </div>
        </div>

        {/* Grilla de horarios */}
        <div className='overflow-x-auto'>
          <table className='w-full'>
            <thead className='bg-gray-50'>
              <tr>
                <th className='px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider'>
                  Hora
                </th>
                {weekDays.map((day) => (
                  <th
                    key={day.toISOString()}
                    className='px-6 py-3 text-center text-xs font-medium text-gray-500 uppercase tracking-wider'
                  >
                    <div>{day.toLocaleDateString('es-CO', { weekday: 'short' })}</div>
                    <div className='text-sm font-normal text-gray-900'>{day.getDate()}</div>
                  </th>
                ))}
              </tr>
            </thead>
            <tbody className='bg-white divide-y divide-gray-200'>
              {Array.from({ length: 10 }, (_, i) => {
                // 10 horas: 6 AM - 6 PM
                const hour = i + 6;
                const timeSlot = `${hour.toString().padStart(2, '0')}:00`;

                return (
                  <tr key={timeSlot} className='hover:bg-gray-50'>
                    <td className='px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900'>
                      {timeSlot}
                    </td>
                    {weekDays.map((day) => {
                      // Buscar horarios para este día y hora
                      const dayHorarios = horarios.filter(
                        (h) =>
                          h.date === day.toISOString().split('T')[0] &&
                          parseInt(h.startTime.split(':')[0]) <= hour &&
                          parseInt(h.endTime.split(':')[0]) > hour
                      );

                      return (
                        <td
                          key={day.toISOString()}
                          className='px-6 py-4 whitespace-nowrap text-sm text-gray-500'
                        >
                          {dayHorarios.map((horario) => (
                            <div
                              key={horario.id}
                              className={`p-2 rounded-lg bg-${horario.color}-100 border border-${horario.color}-200 mb-1`}
                            >
                              <div className={`font-medium text-${horario.color}-800 text-xs`}>
                                {horario.title}
                              </div>
                              <div className={`text-${horario.color}-600 text-xs`}>
                                {horario.instructor}
                              </div>
                              <div className={`text-${horario.color}-600 text-xs`}>
                                {horario.ambiente} - {horario.ficha}
                              </div>
                            </div>
                          ))}
                        </td>
                      );
                    })}
                  </tr>
                );
              })}
            </tbody>
          </table>
        </div>
      </div>

      {/* Lista de horarios del día */}
      <div className='bg-white rounded-lg shadow-md border border-gray-100'>
        <div className='p-6 border-b border-gray-200'>
          <h2 className='text-lg font-medium text-gray-900'>Horarios de Hoy</h2>
        </div>

        <div className='divide-y divide-gray-200'>
          {horarios.slice(0, 2).map((horario) => (
            <div key={horario.id} className='p-6 hover:bg-gray-50'>
              <div className='flex items-center justify-between'>
                <div className='flex items-center space-x-4'>
                  <div className={`w-4 h-4 bg-${horario.color}-500 rounded-full`}></div>

                  <div>
                    <h3 className='text-lg font-medium text-gray-900'>{horario.title}</h3>
                    <div className='flex items-center space-x-4 mt-1 text-sm text-gray-600'>
                      <div className='flex items-center space-x-1'>
                        <ClockIcon className='w-4 h-4' />
                        <span>
                          {horario.startTime} - {horario.endTime}
                        </span>
                      </div>
                      <span>Instructor: {horario.instructor}</span>
                      <span>Ambiente: {horario.ambiente}</span>
                      <span>Ficha: {horario.ficha}</span>
                    </div>
                  </div>
                </div>

                {/* ✅ Acciones por fila a la derecha */}
                <div className='flex items-center space-x-2'>
                  <Button variant='ghost' size='sm'>
                    Ver
                  </Button>
                  <Button variant='ghost' size='sm'>
                    Editar
                  </Button>
                  <Button variant='ghost' size='sm' className='text-red-600 hover:text-red-700'>
                    Cancelar
                  </Button>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}

export default HorariosPage;
