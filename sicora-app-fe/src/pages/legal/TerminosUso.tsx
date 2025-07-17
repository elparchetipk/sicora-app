import React from 'react';
import { ArrowLeft, FileText, AlertCircle, Scale, Users, Shield } from 'lucide-react';
import { Link } from 'react-router-dom';

const TerminosUso: React.FC = () => {
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
            <Scale className='w-8 h-8 text-sena-blue' />
            <h1 className='text-3xl font-bold text-gray-900'>Términos de Uso</h1>
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
            <p className='text-gray-700 leading-relaxed mb-4'>
              Los presentes Términos de Uso regulan el acceso y utilización de la plataforma SICORA
              (Sistema de Información de Coordinación y Registro Académico), desarrollada por EPTI
              (Equipo de Proyectos de Tecnología e Innovación) del SENA (Servicio Nacional de
              Aprendizaje).
            </p>
            <div className='bg-blue-50 border border-blue-200 rounded-lg p-4'>
              <div className='flex items-start'>
                <AlertCircle className='w-5 h-5 text-blue-600 mr-2 mt-0.5' />
                <div>
                  <h3 className='font-semibold text-blue-800'>Aceptación de Términos</h3>
                  <p className='text-blue-700 text-sm mt-1'>
                    Al acceder y utilizar esta plataforma, usted acepta estar sujeto a estos
                    términos y condiciones, así como a todas las leyes y regulaciones aplicables en
                    Colombia.
                  </p>
                </div>
              </div>
            </div>
          </section>

          {/* Definiciones */}
          <section>
            <h2 className='text-2xl font-semibold text-gray-900 mb-4'>Definiciones</h2>
            <div className='space-y-4'>
              <div className='bg-gray-50 p-4 rounded-lg'>
                <h3 className='font-semibold text-gray-900'>SENA</h3>
                <p className='text-gray-700 text-sm'>
                  Servicio Nacional de Aprendizaje, establecimiento público nacional adscrito al
                  Ministerio del Trabajo de Colombia.
                </p>
              </div>
              <div className='bg-gray-50 p-4 rounded-lg'>
                <h3 className='font-semibold text-gray-900'>EPTI</h3>
                <p className='text-gray-700 text-sm'>
                  Equipo de Proyectos de Tecnología e Innovación del SENA, responsable del
                  desarrollo y mantenimiento de SICORA.
                </p>
              </div>
              <div className='bg-gray-50 p-4 rounded-lg'>
                <h3 className='font-semibold text-gray-900'>SICORA</h3>
                <p className='text-gray-700 text-sm'>
                  Sistema de Información de Coordinación y Registro Académico, plataforma digital
                  para la gestión académica del SENA.
                </p>
              </div>
              <div className='bg-gray-50 p-4 rounded-lg'>
                <h3 className='font-semibold text-gray-900'>Usuario</h3>
                <p className='text-gray-700 text-sm'>
                  Persona natural que accede y utiliza la plataforma SICORA en cualquier modalidad
                  (estudiante, instructor, administrativo).
                </p>
              </div>
            </div>
          </section>

          {/* Uso Autorizado */}
          <section>
            <h2 className='text-2xl font-semibold text-gray-900 mb-4 flex items-center'>
              <Users className='w-6 h-6 mr-2 text-sena-blue' />
              Uso Autorizado de la Plataforma
            </h2>
            <div className='grid md:grid-cols-2 gap-6'>
              <div className='bg-green-50 p-4 rounded-lg'>
                <h3 className='font-semibold text-green-800 mb-2'>Usos Permitidos</h3>
                <ul className='text-sm text-gray-700 space-y-1'>
                  <li>• Gestión de procesos académicos autorizados</li>
                  <li>• Consulta de información personal y académica</li>
                  <li>• Comunicación institucional oficial</li>
                  <li>• Acceso a recursos educativos disponibles</li>
                  <li>• Participación en evaluaciones y actividades</li>
                </ul>
              </div>
              <div className='bg-red-50 p-4 rounded-lg'>
                <h3 className='font-semibold text-red-800 mb-2'>Usos Prohibidos</h3>
                <ul className='text-sm text-gray-700 space-y-1'>
                  <li>• Acceso no autorizado a datos de terceros</li>
                  <li>• Uso comercial de la información</li>
                  <li>• Alteración de datos o funcionalidades</li>
                  <li>• Distribución de contenido inapropiado</li>
                  <li>• Actividades que violen la ley colombiana</li>
                </ul>
              </div>
            </div>
          </section>

          {/* Obligaciones del Usuario */}
          <section>
            <h2 className='text-2xl font-semibold text-gray-900 mb-4'>Obligaciones del Usuario</h2>
            <div className='space-y-4'>
              <div className='border-l-4 border-sena-blue pl-4'>
                <h3 className='font-semibold text-gray-900'>Veracidad de la Información</h3>
                <p className='text-gray-700'>
                  Proporcionar información veraz, completa y actualizada en todos los formularios y
                  procesos.
                </p>
              </div>
              <div className='border-l-4 border-sena-orange pl-4'>
                <h3 className='font-semibold text-gray-900'>Confidencialidad</h3>
                <p className='text-gray-700'>
                  Mantener la confidencialidad de sus credenciales de acceso y no compartirlas con
                  terceros.
                </p>
              </div>
              <div className='border-l-4 border-green-600 pl-4'>
                <h3 className='font-semibold text-gray-900'>Uso Responsable</h3>
                <p className='text-gray-700'>
                  Utilizar la plataforma de manera responsable, respetando los derechos de otros
                  usuarios.
                </p>
              </div>
              <div className='border-l-4 border-purple-600 pl-4'>
                <h3 className='font-semibold text-gray-900'>Cumplimiento Normativo</h3>
                <p className='text-gray-700'>
                  Cumplir con todas las normas institucionales del SENA y la legislación colombiana
                  aplicable.
                </p>
              </div>
            </div>
          </section>

          {/* Propiedad Intelectual */}
          <section>
            <h2 className='text-2xl font-semibold text-gray-900 mb-4'>Propiedad Intelectual</h2>
            <div className='bg-yellow-50 border border-yellow-200 rounded-lg p-6'>
              <h3 className='font-semibold text-yellow-800 mb-3'>Derechos de Autor</h3>
              <p className='text-yellow-700 mb-4'>
                Todo el contenido de la plataforma SICORA, incluyendo pero no limitado a textos,
                gráficos, logos, iconos, imágenes, clips de audio, descargas digitales,
                compilaciones de datos y software, es propiedad del SENA o de sus proveedores de
                contenido.
              </p>
              <div className='bg-yellow-100 p-4 rounded-lg'>
                <h4 className='font-semibold text-yellow-800 mb-2'>Licencia de Uso</h4>
                <p className='text-yellow-700 text-sm'>
                  El SENA otorga una licencia limitada, no exclusiva, intransferible y revocable
                  para usar la plataforma únicamente para los fines educativos y administrativos
                  autorizados.
                </p>
              </div>
            </div>
          </section>

          {/* Privacidad */}
          <section>
            <h2 className='text-2xl font-semibold text-gray-900 mb-4 flex items-center'>
              <Shield className='w-6 h-6 mr-2 text-sena-blue' />
              Privacidad y Protección de Datos
            </h2>
            <p className='text-gray-700 mb-4'>
              El tratamiento de datos personales se rige por nuestra
              <Link
                to='/legal/politica-privacidad'
                className='text-sena-blue hover:text-sena-orange font-semibold'
              >
                {' '}
                Política de Privacidad
              </Link>
              , en cumplimiento de la Ley 1581 de 2012 y demás normativa aplicable.
            </p>
            <div className='grid md:grid-cols-2 gap-4'>
              <div className='bg-blue-50 p-4 rounded-lg'>
                <h3 className='font-semibold text-blue-800 mb-2'>Compromiso Institucional</h3>
                <p className='text-sm text-gray-700'>
                  El SENA se compromete a proteger la privacidad y confidencialidad de los datos
                  personales de todos los usuarios de la plataforma.
                </p>
              </div>
              <div className='bg-green-50 p-4 rounded-lg'>
                <h3 className='font-semibold text-green-800 mb-2'>Derechos del Titular</h3>
                <p className='text-sm text-gray-700'>
                  Los usuarios pueden ejercer sus derechos de acceso, rectificación, cancelación y
                  oposición según la normativa vigente.
                </p>
              </div>
            </div>
          </section>

          {/* Responsabilidades y Limitaciones */}
          <section>
            <h2 className='text-2xl font-semibold text-gray-900 mb-4'>
              Responsabilidades y Limitaciones
            </h2>
            <div className='space-y-4'>
              <div className='bg-red-50 border border-red-200 rounded-lg p-4'>
                <h3 className='font-semibold text-red-800 mb-2'>Exención de Responsabilidad</h3>
                <p className='text-red-700 text-sm'>
                  El SENA no será responsable por daños directos, indirectos, incidentales,
                  especiales o consecuenciales que puedan surgir del uso o la imposibilidad de uso
                  de la plataforma, incluyendo pero no limitado a la pérdida de datos, interrupción
                  del negocio o pérdida de beneficios.
                </p>
              </div>
              <div className='bg-orange-50 border border-orange-200 rounded-lg p-4'>
                <h3 className='font-semibold text-orange-800 mb-2'>Disponibilidad del Servicio</h3>
                <p className='text-orange-700 text-sm'>
                  Aunque nos esforzamos por mantener la plataforma disponible 24/7, no garantizamos
                  que el servicio será ininterrumpido, seguro o libre de errores. Pueden ocurrir
                  interrupciones por mantenimiento, actualizaciones o causas de fuerza mayor.
                </p>
              </div>
            </div>
          </section>

          {/* Suspensión y Terminación */}
          <section>
            <h2 className='text-2xl font-semibold text-gray-900 mb-4'>Suspensión y Terminación</h2>
            <div className='bg-gray-50 p-6 rounded-lg'>
              <h3 className='font-semibold text-gray-900 mb-3'>
                El SENA se reserva el derecho de:
              </h3>
              <ul className='list-disc list-inside space-y-2 text-gray-700'>
                <li>
                  Suspender o terminar el acceso de cualquier usuario que viole estos términos
                </li>
                <li>Modificar, suspender o descontinuar la plataforma en cualquier momento</li>
                <li>Investigar y tomar medidas legales por uso indebido de la plataforma</li>
                <li>Cooperar con autoridades competentes en investigaciones legales</li>
              </ul>
            </div>
          </section>

          {/* Legislación Aplicable */}
          <section>
            <h2 className='text-2xl font-semibold text-gray-900 mb-4'>
              Legislación Aplicable y Jurisdicción
            </h2>
            <div className='bg-sena-blue text-white p-6 rounded-lg'>
              <h3 className='font-semibold mb-3'>Marco Legal</h3>
              <p className='mb-4'>
                Estos términos se rigen por las leyes de la República de Colombia, incluyendo:
              </p>
              <ul className='list-disc list-inside space-y-1 text-sm'>
                <li>Ley 119 de 1994 (Reestructuración del SENA)</li>
                <li>Ley 1581 de 2012 (Protección de Datos Personales)</li>
                <li>Ley 1273 de 2009 (Delitos Informáticos)</li>
                <li>Decreto 1377 de 2013 (Reglamentario de la Ley 1581)</li>
                <li>Código Civil y Comercial de Colombia</li>
              </ul>
              <p className='mt-4 text-sm'>
                <strong>Jurisdicción:</strong> Los tribunales competentes de Bogotá D.C., Colombia,
                tendrán jurisdicción exclusiva para resolver cualquier disputa relacionada con estos
                términos.
              </p>
            </div>
          </section>

          {/* Modificaciones */}
          <section>
            <h2 className='text-2xl font-semibold text-gray-900 mb-4'>Modificaciones</h2>
            <div className='bg-yellow-50 border border-yellow-200 rounded-lg p-4'>
              <div className='flex items-start'>
                <AlertCircle className='w-5 h-5 text-yellow-600 mr-2 mt-0.5' />
                <div>
                  <h3 className='font-semibold text-yellow-800'>Actualizaciones de Términos</h3>
                  <p className='text-yellow-700 text-sm mt-1'>
                    El SENA se reserva el derecho de modificar estos términos en cualquier momento.
                    Las modificaciones entrarán en vigencia inmediatamente después de su publicación
                    en la plataforma. El uso continuado después de las modificaciones constituye
                    aceptación de los nuevos términos.
                  </p>
                </div>
              </div>
            </div>
          </section>

          {/* Contacto */}
          <section>
            <h2 className='text-2xl font-semibold text-gray-900 mb-4'>Contacto y Consultas</h2>
            <div className='grid md:grid-cols-2 gap-6'>
              <div className='bg-sena-blue text-white p-4 rounded-lg'>
                <h3 className='font-semibold mb-2'>Soporte Técnico</h3>
                <p className='text-sm'>Email: soporte.sicora@sena.edu.co</p>
                <p className='text-sm'>Teléfono: (57) 1 546 1500 ext. 2222</p>
                <p className='text-sm'>Horario: 8:00 AM - 8:00 PM</p>
              </div>
              <div className='bg-sena-orange text-white p-4 rounded-lg'>
                <h3 className='font-semibold mb-2'>Consultas Legales</h3>
                <p className='text-sm'>Email: legal@sena.edu.co</p>
                <p className='text-sm'>Teléfono: (57) 1 546 1500 ext. 1111</p>
                <p className='text-sm'>Horario: 8:00 AM - 5:00 PM</p>
              </div>
            </div>
          </section>

          {/* Fecha de vigencia */}
          <section className='border-t pt-6'>
            <p className='text-sm text-gray-600'>
              Estos términos de uso fueron actualizados por última vez el 2 de julio de 2025. La
              versión más reciente estará siempre disponible en esta página.
            </p>
          </section>
        </div>
      </div>
    </div>
  );
};

export default TerminosUso;
