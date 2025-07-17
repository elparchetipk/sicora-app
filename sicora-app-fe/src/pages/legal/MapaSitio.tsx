import React from 'react';
import {
  ArrowLeft,
  Map,
  Home,
  Users,
  FileText,
  Settings,
  Shield,
  BookOpen,
  BarChart3,
} from 'lucide-react';
import { Link } from 'react-router-dom';

const MapaSitio: React.FC = () => {
  const secciones = [
    {
      titulo: 'Inicio',
      icono: Home,
      color: 'text-blue-600',
      bgColor: 'bg-blue-50',
      enlaces: [
        { nombre: 'Página Principal', ruta: '/', descripcion: 'Página de inicio de SICORA' },
        { nombre: 'Dashboard', ruta: '/dashboard', descripcion: 'Panel principal del usuario' },
        {
          nombre: 'Página de Demostración',
          ruta: '/demo',
          descripcion: 'Página de prueba y ejemplos',
        },
      ],
    },
    {
      titulo: 'Gestión Académica',
      icono: BookOpen,
      color: 'text-green-600',
      bgColor: 'bg-green-50',
      enlaces: [
        {
          nombre: 'Evaluaciones',
          ruta: '/evaluaciones',
          descripcion: 'Gestión de evaluaciones y calificaciones',
        },
        {
          nombre: 'Horarios',
          ruta: '/horarios',
          descripcion: 'Consulta y gestión de horarios académicos',
        },
        {
          nombre: 'Programas de Formación',
          ruta: '/programas',
          descripcion: 'Información sobre programas disponibles',
        },
        {
          nombre: 'Certificaciones',
          ruta: '/certificaciones',
          descripcion: 'Gestión de certificados y diplomas',
        },
      ],
    },
    {
      titulo: 'Gestión de Usuarios',
      icono: Users,
      color: 'text-purple-600',
      bgColor: 'bg-purple-50',
      enlaces: [
        {
          nombre: 'Usuarios',
          ruta: '/usuarios',
          descripcion: 'Administración de usuarios del sistema',
        },
        { nombre: 'Perfiles', ruta: '/perfiles', descripcion: 'Gestión de perfiles de usuario' },
        {
          nombre: 'Instructores',
          ruta: '/instructores',
          descripcion: 'Información de instructores',
        },
        { nombre: 'Estudiantes', ruta: '/estudiantes', descripcion: 'Gestión de estudiantes' },
      ],
    },
    {
      titulo: 'Reportes y Estadísticas',
      icono: BarChart3,
      color: 'text-orange-600',
      bgColor: 'bg-orange-50',
      enlaces: [
        {
          nombre: 'Reportes Académicos',
          ruta: '/reportes/academicos',
          descripcion: 'Reportes de rendimiento académico',
        },
        {
          nombre: 'Estadísticas Generales',
          ruta: '/reportes/estadisticas',
          descripcion: 'Estadísticas del sistema',
        },
        {
          nombre: 'Análisis de Datos',
          ruta: '/reportes/analisis',
          descripcion: 'Análisis avanzado de datos',
        },
        {
          nombre: 'Exportar Datos',
          ruta: '/reportes/exportar',
          descripcion: 'Exportación de información',
        },
      ],
    },
    {
      titulo: 'Configuración',
      icono: Settings,
      color: 'text-gray-600',
      bgColor: 'bg-gray-50',
      enlaces: [
        {
          nombre: 'Configuración General',
          ruta: '/configuracion',
          descripcion: 'Configuraciones del sistema',
        },
        {
          nombre: 'Preferencias de Usuario',
          ruta: '/configuracion/usuario',
          descripcion: 'Personalización de la cuenta',
        },
        {
          nombre: 'Notificaciones',
          ruta: '/configuracion/notificaciones',
          descripcion: 'Gestión de notificaciones',
        },
        {
          nombre: 'Seguridad',
          ruta: '/configuracion/seguridad',
          descripcion: 'Configuración de seguridad',
        },
      ],
    },
    {
      titulo: 'Información Legal',
      icono: Shield,
      color: 'text-red-600',
      bgColor: 'bg-red-50',
      enlaces: [
        {
          nombre: 'Política de Privacidad',
          ruta: '/legal/politica-privacidad',
          descripcion: 'Política de tratamiento de datos personales',
        },
        {
          nombre: 'Términos de Uso',
          ruta: '/legal/terminos-uso',
          descripcion: 'Términos y condiciones de uso',
        },
        {
          nombre: 'Declaración de Accesibilidad',
          ruta: '/legal/accesibilidad',
          descripcion: 'Compromiso con la accesibilidad web',
        },
        {
          nombre: 'Mapa del Sitio',
          ruta: '/legal/mapa-sitio',
          descripcion: 'Navegación completa del sitio',
        },
      ],
    },
    {
      titulo: 'Ayuda y Soporte',
      icono: FileText,
      color: 'text-indigo-600',
      bgColor: 'bg-indigo-50',
      enlaces: [
        {
          nombre: 'Centro de Ayuda',
          ruta: '/ayuda',
          descripcion: 'Preguntas frecuentes y documentación',
        },
        {
          nombre: 'Contacto',
          ruta: '/contacto',
          descripcion: 'Formulario de contacto y información',
        },
        {
          nombre: 'Soporte Técnico',
          ruta: '/soporte',
          descripcion: 'Asistencia técnica especializada',
        },
        { nombre: 'Tutoriales', ruta: '/tutoriales', descripcion: 'Guías paso a paso del sistema' },
      ],
    },
  ];

  return (
    <div className='min-h-screen bg-gray-50'>
      {/* Header */}
      <div className='bg-white shadow-sm border-b'>
        <div className='max-w-6xl mx-auto px-4 py-6'>
          <Link
            to='/'
            className='inline-flex items-center text-sena-blue hover:text-sena-orange transition-colors mb-4'
          >
            <ArrowLeft className='w-5 h-5 mr-2' />
            Volver al inicio
          </Link>
          <div className='flex items-center space-x-3'>
            <Map className='w-8 h-8 text-sena-blue' />
            <h1 className='text-3xl font-bold text-gray-900'>Mapa del Sitio</h1>
          </div>
          <p className='text-gray-600 mt-2'>Navegación completa de la plataforma SICORA</p>
        </div>
      </div>

      {/* Content */}
      <div className='max-w-6xl mx-auto px-4 py-8'>
        {/* Introducción */}
        <div className='bg-white rounded-lg shadow-sm p-6 mb-8'>
          <h2 className='text-xl font-semibold text-gray-900 mb-3'>¿Qué es SICORA?</h2>
          <p className='text-gray-700 leading-relaxed mb-4'>
            SICORA (Sistema de Información de Coordinación y Registro Académico) es la plataforma
            digital desarrollada por EPTI del SENA para facilitar la gestión académica,
            administrativa y de usuarios en los procesos de formación.
          </p>
          <div className='grid md:grid-cols-3 gap-4'>
            <div className='text-center p-4 bg-blue-50 rounded-lg'>
              <Users className='w-8 h-8 text-blue-600 mx-auto mb-2' />
              <h3 className='font-semibold text-gray-900'>+50,000</h3>
              <p className='text-sm text-gray-600'>Usuarios Registrados</p>
            </div>
            <div className='text-center p-4 bg-green-50 rounded-lg'>
              <BookOpen className='w-8 h-8 text-green-600 mx-auto mb-2' />
              <h3 className='font-semibold text-gray-900'>+1,000</h3>
              <p className='text-sm text-gray-600'>Programas de Formación</p>
            </div>
            <div className='text-center p-4 bg-orange-50 rounded-lg'>
              <BarChart3 className='w-8 h-8 text-orange-600 mx-auto mb-2' />
              <h3 className='font-semibold text-gray-900'>24/7</h3>
              <p className='text-sm text-gray-600'>Disponibilidad</p>
            </div>
          </div>
        </div>

        {/* Secciones del sitio */}
        <div className='space-y-8'>
          {secciones.map((seccion, index) => {
            const IconoComponente = seccion.icono;
            return (
              <div key={index} className='bg-white rounded-lg shadow-sm overflow-hidden'>
                <div className={`${seccion.bgColor} px-6 py-4 border-b`}>
                  <div className='flex items-center space-x-3'>
                    <IconoComponente className={`w-6 h-6 ${seccion.color}`} />
                    <h2 className='text-xl font-semibold text-gray-900'>{seccion.titulo}</h2>
                  </div>
                </div>
                <div className='p-6'>
                  <div className='grid md:grid-cols-2 gap-4'>
                    {seccion.enlaces.map((enlace, enlaceIndex) => (
                      <div
                        key={enlaceIndex}
                        className='border rounded-lg p-4 hover:bg-gray-50 transition-colors'
                      >
                        <Link to={enlace.ruta} className='block'>
                          <h3 className='font-semibold text-gray-900 hover:text-sena-blue transition-colors mb-1'>
                            {enlace.nombre}
                          </h3>
                          <p className='text-sm text-gray-600'>{enlace.descripcion}</p>
                          <div className='mt-2'>
                            <span className='text-xs text-gray-500 bg-gray-100 px-2 py-1 rounded'>
                              {enlace.ruta}
                            </span>
                          </div>
                        </Link>
                      </div>
                    ))}
                  </div>
                </div>
              </div>
            );
          })}
        </div>

        {/* Información adicional */}
        <div className='bg-white rounded-lg shadow-sm p-6 mt-8'>
          <h2 className='text-xl font-semibold text-gray-900 mb-4'>Información Adicional</h2>
          <div className='grid md:grid-cols-2 gap-6'>
            <div>
              <h3 className='font-semibold text-sena-blue mb-3'>Navegación Rápida</h3>
              <ul className='space-y-2 text-sm text-gray-700'>
                <li>• Use el menú principal para acceder a las secciones más importantes</li>
                <li>• Los enlaces de navegación siempre están disponibles en la parte superior</li>
                <li>• Utilice el buscador para encontrar contenido específico</li>
                <li>• El dashboard personaliza el contenido según su perfil</li>
              </ul>
            </div>
            <div>
              <h3 className='font-semibold text-sena-orange mb-3'>Accesibilidad</h3>
              <ul className='space-y-2 text-sm text-gray-700'>
                <li>• Navegación compatible con lectores de pantalla</li>
                <li>• Contraste mejorado para mejor visibilidad</li>
                <li>• Navegación por teclado disponible</li>
                <li>• Textos alternativos en todas las imágenes</li>
              </ul>
            </div>
          </div>
        </div>

        {/* Estructura técnica */}
        <div className='bg-gray-900 text-white rounded-lg p-6 mt-8'>
          <h2 className='text-xl font-semibold mb-4'>Estructura Técnica</h2>
          <div className='grid md:grid-cols-3 gap-6'>
            <div>
              <h3 className='font-semibold text-sena-orange mb-2'>Frontend</h3>
              <ul className='text-sm space-y-1'>
                <li>• React 18 + TypeScript</li>
                <li>• Tailwind CSS</li>
                <li>• Vite + SWC</li>
                <li>• React Router</li>
              </ul>
            </div>
            <div>
              <h3 className='font-semibold text-sena-orange mb-2'>Backend</h3>
              <ul className='text-sm space-y-1'>
                <li>• Arquitectura Multi-stack</li>
                <li>• APIs RESTful</li>
                <li>• Microservicios</li>
                <li>• Base de datos PostgreSQL</li>
              </ul>
            </div>
            <div>
              <h3 className='font-semibold text-sena-orange mb-2'>Infraestructura</h3>
              <ul className='text-sm space-y-1'>
                <li>• Docker containers</li>
                <li>• CI/CD automatizado</li>
                <li>• Monitoreo 24/7</li>
                <li>• Respaldos automatizados</li>
              </ul>
            </div>
          </div>
        </div>

        {/* Contacto y soporte */}
        <div className='bg-sena-blue text-white rounded-lg p-6 mt-8'>
          <h2 className='text-xl font-semibold mb-4'>¿Necesita Ayuda?</h2>
          <div className='grid md:grid-cols-2 gap-6'>
            <div>
              <h3 className='font-semibold mb-2'>Soporte Técnico</h3>
              <p className='text-sm mb-2'>Para problemas técnicos con la plataforma:</p>
              <p className='text-sm'>📧 soporte.sicora@sena.edu.co</p>
              <p className='text-sm'>📞 (57) 1 546 1500 ext. 2222</p>
            </div>
            <div>
              <h3 className='font-semibold mb-2'>Consultas Académicas</h3>
              <p className='text-sm mb-2'>Para consultas sobre programas y procesos:</p>
              <p className='text-sm'>📧 academico@sena.edu.co</p>
              <p className='text-sm'>📞 (57) 1 546 1500 ext. 3333</p>
            </div>
          </div>
        </div>

        {/* Última actualización */}
        <div className='text-center mt-8'>
          <p className='text-sm text-gray-600'>
            Mapa del sitio actualizado el 2 de julio de 2025 | SICORA v2.0
          </p>
        </div>
      </div>
    </div>
  );
};

export default MapaSitio;
