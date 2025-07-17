import React from 'react';
import { ArrowLeft, Shield, Users, FileText, AlertTriangle } from 'lucide-react';
import { Link } from 'react-router-dom';

const PoliticaPrivacidad: React.FC = () => {
  return (
    <div className='min-h-screen bg-gray-50'>
      {/* Header */}
      <div className='bg-white shadow-sm border-b'>
        <div className='max-w-4xl mx-auto px-4 py-6'>
          <Link
            to='/'
            className='inline-flex items-center text-sena-blue hover:text-sena-orange transition-colors mb-4'
          >
            <ArrowLeft className='w-5 h-5 mr-2' />
            Volver al inicio
          </Link>
          <div className='flex items-center space-x-3'>
            <Shield className='w-8 h-8 text-sena-blue' />
            <h1 className='text-3xl font-bold text-gray-900'>Política de Privacidad</h1>
          </div>
          <p className='text-gray-600 mt-2'>Última actualización: 2 de julio de 2025</p>
        </div>
      </div>

      {/* Content */}
      <div className='max-w-4xl mx-auto px-4 py-8'>
        <div className='bg-white rounded-lg shadow-sm p-8 space-y-8'>
          {/* Introducción */}
          <section>
            <h2 className='text-2xl font-semibold text-gray-900 mb-4 flex items-center'>
              <FileText className='w-6 h-6 mr-2 text-sena-blue' />
              Introducción
            </h2>
            <p className='text-gray-700 leading-relaxed'>
              EPTI (Equipo de Proyectos de Tecnología e Innovación) del SENA, en cumplimiento de la
              Ley 1581 de 2012 "Por la cual se dictan disposiciones generales para la protección de
              datos personales" y demás normas que la desarrollan, informa a los usuarios de la
              plataforma SICORA (Sistema de Información de Coordinación y Registro Académico) sobre
              el tratamiento de sus datos personales.
            </p>
          </section>

          {/* Responsable del Tratamiento */}
          <section>
            <h2 className='text-2xl font-semibold text-gray-900 mb-4'>
              Responsable del Tratamiento
            </h2>
            <div className='bg-gray-50 p-4 rounded-lg'>
              <p>
                <strong>Entidad:</strong> Servicio Nacional de Aprendizaje - SENA
              </p>
              <p>
                <strong>Equipo:</strong> EPTI - Equipo de Proyectos de Tecnología e Innovación
              </p>
              <p>
                <strong>Dirección:</strong> Calle 57 No. 8-69, Bogotá D.C., Colombia
              </p>
              <p>
                <strong>Teléfono:</strong> (57) 1 546 1500
              </p>
              <p>
                <strong>Correo electrónico:</strong> epti@sena.edu.co
              </p>
              <p>
                <strong>Página web:</strong> www.sena.edu.co
              </p>
            </div>
          </section>

          {/* Tipos de Datos */}
          <section>
            <h2 className='text-2xl font-semibold text-gray-900 mb-4'>
              Tipos de Datos Recolectados
            </h2>
            <div className='grid md:grid-cols-2 gap-6'>
              <div className='bg-blue-50 p-4 rounded-lg'>
                <h3 className='font-semibold text-sena-blue mb-2'>Datos de Identificación</h3>
                <ul className='text-sm text-gray-700 space-y-1'>
                  <li>• Número de documento de identidad</li>
                  <li>• Nombres y apellidos</li>
                  <li>• Fecha de nacimiento</li>
                  <li>• Lugar de nacimiento</li>
                  <li>• Nacionalidad</li>
                </ul>
              </div>
              <div className='bg-green-50 p-4 rounded-lg'>
                <h3 className='font-semibold text-green-700 mb-2'>Datos de Contacto</h3>
                <ul className='text-sm text-gray-700 space-y-1'>
                  <li>• Dirección de residencia</li>
                  <li>• Teléfono fijo y móvil</li>
                  <li>• Correo electrónico</li>
                  <li>• Ciudad y departamento</li>
                </ul>
              </div>
              <div className='bg-orange-50 p-4 rounded-lg'>
                <h3 className='font-semibold text-orange-700 mb-2'>Datos Académicos</h3>
                <ul className='text-sm text-gray-700 space-y-1'>
                  <li>• Nivel educativo</li>
                  <li>• Programa de formación</li>
                  <li>• Calificaciones</li>
                  <li>• Historial académico</li>
                  <li>• Certificaciones</li>
                </ul>
              </div>
              <div className='bg-purple-50 p-4 rounded-lg'>
                <h3 className='font-semibold text-purple-700 mb-2'>Datos Técnicos</h3>
                <ul className='text-sm text-gray-700 space-y-1'>
                  <li>• Dirección IP</li>
                  <li>• Cookies y datos de navegación</li>
                  <li>• Logs de sistema</li>
                  <li>• Información del dispositivo</li>
                </ul>
              </div>
            </div>
          </section>

          {/* Finalidades */}
          <section>
            <h2 className='text-2xl font-semibold text-gray-900 mb-4'>
              Finalidades del Tratamiento
            </h2>
            <div className='space-y-4'>
              <div className='border-l-4 border-sena-blue pl-4'>
                <h3 className='font-semibold text-gray-900'>Gestión Académica</h3>
                <p className='text-gray-700'>
                  Administrar procesos de inscripción, matrícula, evaluación y certificación de
                  programas de formación.
                </p>
              </div>
              <div className='border-l-4 border-sena-orange pl-4'>
                <h3 className='font-semibold text-gray-900'>Comunicación Institucional</h3>
                <p className='text-gray-700'>
                  Enviar información relevante sobre programas, eventos, cambios normativos y
                  comunicaciones oficiales.
                </p>
              </div>
              <div className='border-l-4 border-green-600 pl-4'>
                <h3 className='font-semibold text-gray-900'>Seguimiento y Mejora</h3>
                <p className='text-gray-700'>
                  Realizar seguimiento a egresados, estudios de satisfacción y mejora continua de
                  servicios.
                </p>
              </div>
              <div className='border-l-4 border-purple-600 pl-4'>
                <h3 className='font-semibold text-gray-900'>Cumplimiento Legal</h3>
                <p className='text-gray-700'>
                  Cumplir obligaciones legales, reportes estadísticos y requerimientos de
                  autoridades competentes.
                </p>
              </div>
            </div>
          </section>

          {/* Derechos del Titular */}
          <section>
            <h2 className='text-2xl font-semibold text-gray-900 mb-4 flex items-center'>
              <Users className='w-6 h-6 mr-2 text-sena-blue' />
              Derechos del Titular
            </h2>
            <p className='text-gray-700 mb-4'>
              Como titular de los datos personales, usted tiene derecho a:
            </p>
            <div className='grid md:grid-cols-2 gap-4'>
              <div className='bg-blue-50 p-4 rounded-lg'>
                <h3 className='font-semibold text-blue-800 mb-2'>Derechos de Acceso</h3>
                <ul className='text-sm text-gray-700 space-y-1'>
                  <li>• Conocer, actualizar y rectificar sus datos</li>
                  <li>• Solicitar prueba de autorización otorgada</li>
                  <li>• Ser informado sobre el uso dado a sus datos</li>
                </ul>
              </div>
              <div className='bg-green-50 p-4 rounded-lg'>
                <h3 className='font-semibold text-green-800 mb-2'>Derechos de Control</h3>
                <ul className='text-sm text-gray-700 space-y-1'>
                  <li>• Presentar quejas ante la SIC</li>
                  <li>• Revocar autorización y solicitar supresión</li>
                  <li>• Acceder de forma gratuita a sus datos</li>
                </ul>
              </div>
            </div>
          </section>

          {/* Procedimiento para ejercer derechos */}
          <section>
            <h2 className='text-2xl font-semibold text-gray-900 mb-4'>
              Procedimiento para Ejercer Derechos
            </h2>
            <div className='bg-gray-50 p-6 rounded-lg'>
              <h3 className='font-semibold text-gray-900 mb-3'>
                Para ejercer sus derechos, debe seguir estos pasos:
              </h3>
              <ol className='list-decimal list-inside space-y-2 text-gray-700'>
                <li>
                  Enviar solicitud escrita a: <strong>epti@sena.edu.co</strong>
                </li>
                <li>
                  Incluir: nombre completo, documento de identidad, dirección, teléfono y correo
                  electrónico
                </li>
                <li>Describir claramente el derecho que desea ejercer</li>
                <li>Anexar copia del documento de identidad</li>
                <li>Esperar respuesta en un término máximo de 15 días hábiles</li>
              </ol>
            </div>
          </section>

          {/* Medidas de Seguridad */}
          <section>
            <h2 className='text-2xl font-semibold text-gray-900 mb-4'>Medidas de Seguridad</h2>
            <div className='grid md:grid-cols-3 gap-4'>
              <div className='text-center p-4 border rounded-lg'>
                <Shield className='w-8 h-8 text-green-600 mx-auto mb-2' />
                <h3 className='font-semibold text-gray-900'>Técnicas</h3>
                <p className='text-sm text-gray-600'>
                  Encriptación, firewalls, autenticación segura
                </p>
              </div>
              <div className='text-center p-4 border rounded-lg'>
                <Users className='w-8 h-8 text-blue-600 mx-auto mb-2' />
                <h3 className='font-semibold text-gray-900'>Humanas</h3>
                <p className='text-sm text-gray-600'>
                  Capacitación, políticas de acceso, monitoreo
                </p>
              </div>
              <div className='text-center p-4 border rounded-lg'>
                <FileText className='w-8 h-8 text-purple-600 mx-auto mb-2' />
                <h3 className='font-semibold text-gray-900'>Administrativas</h3>
                <p className='text-sm text-gray-600'>
                  Procedimientos, auditorías, controles internos
                </p>
              </div>
            </div>
          </section>

          {/* Transferencias */}
          <section>
            <h2 className='text-2xl font-semibold text-gray-900 mb-4'>
              Transferencias Internacionales
            </h2>
            <div className='bg-yellow-50 border border-yellow-200 rounded-lg p-4'>
              <div className='flex items-start'>
                <AlertTriangle className='w-5 h-5 text-yellow-600 mr-2 mt-0.5' />
                <div>
                  <h3 className='font-semibold text-yellow-800'>Importante</h3>
                  <p className='text-yellow-700 text-sm mt-1'>
                    Los datos personales son almacenados y procesados en servidores ubicados en
                    Colombia. En caso de requerirse transferencias internacionales, se solicitará
                    autorización previa y se garantizará el mismo nivel de protección.
                  </p>
                </div>
              </div>
            </div>
          </section>

          {/* Contacto */}
          <section>
            <h2 className='text-2xl font-semibold text-gray-900 mb-4'>Contacto</h2>
            <div className='bg-sena-blue text-white p-6 rounded-lg'>
              <h3 className='font-semibold mb-3'>¿Preguntas sobre esta política?</h3>
              <p className='mb-2'>Contacte a nuestro equipo de protección de datos:</p>
              <p>
                <strong>Email:</strong> protecciondatos@sena.edu.co
              </p>
              <p>
                <strong>Teléfono:</strong> (57) 1 546 1500 ext. 11111
              </p>
              <p>
                <strong>Horario:</strong> Lunes a viernes, 8:00 AM - 5:00 PM
              </p>
            </div>
          </section>

          {/* Fecha de vigencia */}
          <section className='border-t pt-6'>
            <p className='text-sm text-gray-600'>
              Esta política de privacidad fue actualizada por última vez el 2 de julio de 2025 y
              está sujeta a modificaciones. Las actualizaciones serán publicadas en esta página con
              la fecha correspondiente.
            </p>
          </section>
        </div>
      </div>
    </div>
  );
};

export default PoliticaPrivacidad;
