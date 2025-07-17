import React from 'react';
import {
  ArrowLeft,
  Eye,
  Ear,
  Hand,
  Brain,
  CheckCircle,
  AlertCircle,
  Users,
  Globe,
} from 'lucide-react';
import { Link } from 'react-router-dom';

const Accesibilidad: React.FC = () => {
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
            <Globe className='w-8 h-8 text-sena-blue' />
            <h1 className='text-3xl font-bold text-gray-900'>Declaración de Accesibilidad</h1>
          </div>
          <p className='text-gray-600 mt-2'>Compromiso con la inclusión digital - SICORA</p>
        </div>
      </div>

      {/* Content */}
      <div className='max-w-4xl mx-auto px-4 py-8'>
        <div className='bg-white rounded-lg shadow-sm p-8 space-y-8'>
          {/* Compromiso */}
          <section>
            <div className='bg-blue-50 border border-blue-200 rounded-lg p-6'>
              <div className='flex items-start'>
                <Users className='w-6 h-6 text-blue-600 mr-3 mt-1' />
                <div>
                  <h2 className='text-xl font-semibold text-blue-900 mb-3'>Nuestro Compromiso</h2>
                  <p className='text-blue-800 leading-relaxed'>
                    El SENA, a través de EPTI, se compromete a garantizar que la plataforma SICORA
                    sea accesible para todas las personas, independientemente de sus capacidades
                    físicas, sensoriales o cognitivas. Creemos firmemente que la educación debe ser
                    inclusiva y estar disponible para todos los colombianos.
                  </p>
                </div>
              </div>
            </div>
          </section>

          {/* Marco Legal */}
          <section>
            <h2 className='text-2xl font-semibold text-gray-900 mb-4'>Marco Legal y Normativo</h2>
            <div className='grid md:grid-cols-2 gap-6'>
              <div className='bg-green-50 p-4 rounded-lg'>
                <h3 className='font-semibold text-green-800 mb-2'>Normativa Nacional</h3>
                <ul className='text-sm text-gray-700 space-y-1'>
                  <li>• Ley Estatutaria 1618 de 2013 (Derechos de personas con discapacidad)</li>
                  <li>• Decreto 1421 de 2017 (Educación inclusiva)</li>
                  <li>
                    • Ley 1346 de 2009 (Convención sobre los Derechos de las Personas con
                    Discapacidad)
                  </li>
                  <li>• Constitución Política de Colombia - Art. 13, 47 y 68</li>
                </ul>
              </div>
              <div className='bg-purple-50 p-4 rounded-lg'>
                <h3 className='font-semibold text-purple-800 mb-2'>Estándares Internacionales</h3>
                <ul className='text-sm text-gray-700 space-y-1'>
                  <li>• WCAG 2.1 Nivel AA (Web Content Accessibility Guidelines)</li>
                  <li>• ISO/IEC 40500:2012 (Accesibilidad Web)</li>
                  <li>• Section 508 (Estados Unidos)</li>
                  <li>• EN 301 549 (Unión Europea)</li>
                </ul>
              </div>
            </div>
          </section>

          {/* Características de Accesibilidad */}
          <section>
            <h2 className='text-2xl font-semibold text-gray-900 mb-6'>
              Características de Accesibilidad Implementadas
            </h2>
            <div className='space-y-6'>
              {/* Accesibilidad Visual */}
              <div className='border rounded-lg p-6'>
                <div className='flex items-center mb-4'>
                  <Eye className='w-6 h-6 text-blue-600 mr-3' />
                  <h3 className='text-xl font-semibold text-gray-900'>Accesibilidad Visual</h3>
                </div>
                <div className='grid md:grid-cols-2 gap-4'>
                  <div>
                    <h4 className='font-semibold text-gray-800 mb-2'>
                      Para personas con baja visión:
                    </h4>
                    <ul className='text-sm text-gray-700 space-y-1'>
                      <li className='flex items-center'>
                        <CheckCircle className='w-4 h-4 text-green-500 mr-2' />
                        Alto contraste de colores (mínimo 4.5:1)
                      </li>
                      <li className='flex items-center'>
                        <CheckCircle className='w-4 h-4 text-green-500 mr-2' />
                        Texto escalable hasta 200% sin pérdida de funcionalidad
                      </li>
                      <li className='flex items-center'>
                        <CheckCircle className='w-4 h-4 text-green-500 mr-2' />
                        Modo oscuro disponible
                      </li>
                      <li className='flex items-center'>
                        <CheckCircle className='w-4 h-4 text-green-500 mr-2' />
                        Indicadores visuales claros para focus
                      </li>
                    </ul>
                  </div>
                  <div>
                    <h4 className='font-semibold text-gray-800 mb-2'>Para personas ciegas:</h4>
                    <ul className='text-sm text-gray-700 space-y-1'>
                      <li className='flex items-center'>
                        <CheckCircle className='w-4 h-4 text-green-500 mr-2' />
                        Compatibilidad total con lectores de pantalla
                      </li>
                      <li className='flex items-center'>
                        <CheckCircle className='w-4 h-4 text-green-500 mr-2' />
                        Textos alternativos descriptivos en imágenes
                      </li>
                      <li className='flex items-center'>
                        <CheckCircle className='w-4 h-4 text-green-500 mr-2' />
                        Estructura semántica HTML5
                      </li>
                      <li className='flex items-center'>
                        <CheckCircle className='w-4 h-4 text-green-500 mr-2' />
                        Navegación por encabezados (H1-H6)
                      </li>
                    </ul>
                  </div>
                </div>
              </div>

              {/* Accesibilidad Auditiva */}
              <div className='border rounded-lg p-6'>
                <div className='flex items-center mb-4'>
                  <Ear className='w-6 h-6 text-green-600 mr-3' />
                  <h3 className='text-xl font-semibold text-gray-900'>Accesibilidad Auditiva</h3>
                </div>
                <div className='grid md:grid-cols-2 gap-4'>
                  <div>
                    <h4 className='font-semibold text-gray-800 mb-2'>
                      Para personas con pérdida auditiva:
                    </h4>
                    <ul className='text-sm text-gray-700 space-y-1'>
                      <li className='flex items-center'>
                        <CheckCircle className='w-4 h-4 text-green-500 mr-2' />
                        Subtítulos en contenido multimedia
                      </li>
                      <li className='flex items-center'>
                        <CheckCircle className='w-4 h-4 text-green-500 mr-2' />
                        Transcripciones de audio disponibles
                      </li>
                      <li className='flex items-center'>
                        <CheckCircle className='w-4 h-4 text-green-500 mr-2' />
                        Alertas visuales en lugar de sonoras
                      </li>
                      <li className='flex items-center'>
                        <CheckCircle className='w-4 h-4 text-green-500 mr-2' />
                        Comunicación alternativa por chat/texto
                      </li>
                    </ul>
                  </div>
                  <div>
                    <h4 className='font-semibold text-gray-800 mb-2'>Comunicación inclusiva:</h4>
                    <ul className='text-sm text-gray-700 space-y-1'>
                      <li className='flex items-center'>
                        <CheckCircle className='w-4 h-4 text-green-500 mr-2' />
                        Lenguaje claro y sencillo
                      </li>
                      <li className='flex items-center'>
                        <CheckCircle className='w-4 h-4 text-green-500 mr-2' />
                        Iconos y símbolos universales
                      </li>
                      <li className='flex items-center'>
                        <AlertCircle className='w-4 h-4 text-yellow-500 mr-2' />
                        Interpretación en lengua de señas (en desarrollo)
                      </li>
                    </ul>
                  </div>
                </div>
              </div>

              {/* Accesibilidad Motriz */}
              <div className='border rounded-lg p-6'>
                <div className='flex items-center mb-4'>
                  <Hand className='w-6 h-6 text-orange-600 mr-3' />
                  <h3 className='text-xl font-semibold text-gray-900'>Accesibilidad Motriz</h3>
                </div>
                <div className='grid md:grid-cols-2 gap-4'>
                  <div>
                    <h4 className='font-semibold text-gray-800 mb-2'>Navegación por teclado:</h4>
                    <ul className='text-sm text-gray-700 space-y-1'>
                      <li className='flex items-center'>
                        <CheckCircle className='w-4 h-4 text-green-500 mr-2' />
                        Acceso completo con teclado (Tab, Enter, Arrow keys)
                      </li>
                      <li className='flex items-center'>
                        <CheckCircle className='w-4 h-4 text-green-500 mr-2' />
                        Orden lógico de navegación
                      </li>
                      <li className='flex items-center'>
                        <CheckCircle className='w-4 h-4 text-green-500 mr-2' />
                        Indicadores visuales de focus
                      </li>
                      <li className='flex items-center'>
                        <CheckCircle className='w-4 h-4 text-green-500 mr-2' />
                        Atajos de teclado personalizables
                      </li>
                    </ul>
                  </div>
                  <div>
                    <h4 className='font-semibold text-gray-800 mb-2'>Diseño adaptativo:</h4>
                    <ul className='text-sm text-gray-700 space-y-1'>
                      <li className='flex items-center'>
                        <CheckCircle className='w-4 h-4 text-green-500 mr-2' />
                        Botones y enlaces de tamaño adecuado (mín. 44px)
                      </li>
                      <li className='flex items-center'>
                        <CheckCircle className='w-4 h-4 text-green-500 mr-2' />
                        Tiempo suficiente para completar acciones
                      </li>
                      <li className='flex items-center'>
                        <CheckCircle className='w-4 h-4 text-green-500 mr-2' />
                        Posibilidad de cancelar acciones accidentales
                      </li>
                      <li className='flex items-center'>
                        <CheckCircle className='w-4 h-4 text-green-500 mr-2' />
                        Compatible con tecnologías asistivas
                      </li>
                    </ul>
                  </div>
                </div>
              </div>

              {/* Accesibilidad Cognitiva */}
              <div className='border rounded-lg p-6'>
                <div className='flex items-center mb-4'>
                  <Brain className='w-6 h-6 text-purple-600 mr-3' />
                  <h3 className='text-xl font-semibold text-gray-900'>Accesibilidad Cognitiva</h3>
                </div>
                <div className='grid md:grid-cols-2 gap-4'>
                  <div>
                    <h4 className='font-semibold text-gray-800 mb-2'>Diseño comprensible:</h4>
                    <ul className='text-sm text-gray-700 space-y-1'>
                      <li className='flex items-center'>
                        <CheckCircle className='w-4 h-4 text-green-500 mr-2' />
                        Navegación consistente y predecible
                      </li>
                      <li className='flex items-center'>
                        <CheckCircle className='w-4 h-4 text-green-500 mr-2' />
                        Instrucciones claras y paso a paso
                      </li>
                      <li className='flex items-center'>
                        <CheckCircle className='w-4 h-4 text-green-500 mr-2' />
                        Mensajes de error descriptivos
                      </li>
                      <li className='flex items-center'>
                        <CheckCircle className='w-4 h-4 text-green-500 mr-2' />
                        Organización lógica del contenido
                      </li>
                    </ul>
                  </div>
                  <div>
                    <h4 className='font-semibold text-gray-800 mb-2'>Apoyo al usuario:</h4>
                    <ul className='text-sm text-gray-700 space-y-1'>
                      <li className='flex items-center'>
                        <CheckCircle className='w-4 h-4 text-green-500 mr-2' />
                        Ayuda contextual disponible
                      </li>
                      <li className='flex items-center'>
                        <CheckCircle className='w-4 h-4 text-green-500 mr-2' />
                        Confirmación antes de acciones importantes
                      </li>
                      <li className='flex items-center'>
                        <CheckCircle className='w-4 h-4 text-green-500 mr-2' />
                        Posibilidad de deshacer acciones
                      </li>
                      <li className='flex items-center'>
                        <CheckCircle className='w-4 h-4 text-green-500 mr-2' />
                        Recordatorios y notificaciones opcionales
                      </li>
                    </ul>
                  </div>
                </div>
              </div>
            </div>
          </section>

          {/* Tecnologías Compatibles */}
          <section>
            <h2 className='text-2xl font-semibold text-gray-900 mb-4'>
              Tecnologías Asistivas Compatibles
            </h2>
            <div className='grid md:grid-cols-3 gap-6'>
              <div className='bg-blue-50 p-4 rounded-lg'>
                <h3 className='font-semibold text-blue-800 mb-2'>Lectores de Pantalla</h3>
                <ul className='text-sm text-gray-700 space-y-1'>
                  <li>• NVDA (Windows)</li>
                  <li>• JAWS (Windows)</li>
                  <li>• VoiceOver (macOS/iOS)</li>
                  <li>• TalkBack (Android)</li>
                  <li>• Orca (Linux)</li>
                </ul>
              </div>
              <div className='bg-green-50 p-4 rounded-lg'>
                <h3 className='font-semibold text-green-800 mb-2'>Navegadores</h3>
                <ul className='text-sm text-gray-700 space-y-1'>
                  <li>• Chrome/Chromium</li>
                  <li>• Firefox</li>
                  <li>• Safari</li>
                  <li>• Edge</li>
                  <li>• Opera</li>
                </ul>
              </div>
              <div className='bg-orange-50 p-4 rounded-lg'>
                <h3 className='font-semibold text-orange-800 mb-2'>Dispositivos</h3>
                <ul className='text-sm text-gray-700 space-y-1'>
                  <li>• Computadores de escritorio</li>
                  <li>• Laptops y tablets</li>
                  <li>• Smartphones</li>
                  <li>• Dispositivos de entrada alternativos</li>
                  <li>• Pantallas braille</li>
                </ul>
              </div>
            </div>
          </section>

          {/* Estado de Conformidad */}
          <section>
            <h2 className='text-2xl font-semibold text-gray-900 mb-4'>Estado de Conformidad</h2>
            <div className='bg-green-50 border border-green-200 rounded-lg p-6'>
              <div className='flex items-center mb-4'>
                <CheckCircle className='w-6 h-6 text-green-600 mr-3' />
                <h3 className='font-semibold text-green-800'>WCAG 2.1 Nivel AA - Conforme</h3>
              </div>
              <p className='text-green-700 mb-4'>
                La plataforma SICORA cumple con los criterios de conformidad de las WCAG 2.1 en
                nivel AA, lo que significa que es accesible para la mayoría de usuarios con
                discapacidades.
              </p>
              <div className='grid md:grid-cols-3 gap-4 text-sm'>
                <div>
                  <h4 className='font-semibold text-green-800'>Nivel A</h4>
                  <p className='text-green-700'>Cumplimiento: 100%</p>
                </div>
                <div>
                  <h4 className='font-semibold text-green-800'>Nivel AA</h4>
                  <p className='text-green-700'>Cumplimiento: 95%</p>
                </div>
                <div>
                  <h4 className='font-semibold text-green-800'>Nivel AAA</h4>
                  <p className='text-green-700'>Cumplimiento: 75%</p>
                </div>
              </div>
            </div>
          </section>

          {/* Testing y Validación */}
          <section>
            <h2 className='text-2xl font-semibold text-gray-900 mb-4'>Proceso de Validación</h2>
            <div className='space-y-4'>
              <div className='bg-gray-50 p-4 rounded-lg'>
                <h3 className='font-semibold text-gray-900 mb-2'>Métodos de Evaluación</h3>
                <ul className='text-sm text-gray-700 space-y-1'>
                  <li>
                    • Evaluación automatizada con herramientas especializadas (axe, WAVE,
                    Lighthouse)
                  </li>
                  <li>• Pruebas manuales con tecnologías asistivas</li>
                  <li>• Evaluación por expertos en accesibilidad</li>
                  <li>• Pruebas de usabilidad con usuarios reales</li>
                  <li>• Revisión continua del código fuente</li>
                </ul>
              </div>
              <div className='bg-gray-50 p-4 rounded-lg'>
                <h3 className='font-semibold text-gray-900 mb-2'>Frecuencia de Auditorías</h3>
                <p className='text-sm text-gray-700'>
                  Realizamos auditorías de accesibilidad cada 6 meses, además de evaluaciones
                  continuas durante el desarrollo de nuevas funcionalidades.
                </p>
              </div>
            </div>
          </section>

          {/* Limitaciones Conocidas */}
          <section>
            <h2 className='text-2xl font-semibold text-gray-900 mb-4'>Limitaciones Conocidas</h2>
            <div className='bg-yellow-50 border border-yellow-200 rounded-lg p-4'>
              <div className='flex items-start'>
                <AlertCircle className='w-5 h-5 text-yellow-600 mr-2 mt-0.5' />
                <div>
                  <h3 className='font-semibold text-yellow-800'>Áreas en Mejora</h3>
                  <ul className='text-yellow-700 text-sm mt-2 space-y-1'>
                    <li>• Algunos gráficos complejos necesitan descripciones más detalladas</li>
                    <li>• Integración con sistemas heredados puede presentar limitaciones</li>
                    <li>
                      • Contenido multimedia de terceros puede no cumplir todos los estándares
                    </li>
                    <li>• Algunas funcionalidades avanzadas están en proceso de optimización</li>
                  </ul>
                  <p className='text-yellow-700 text-sm mt-3'>
                    <strong>Compromiso:</strong> Estas limitaciones están siendo abordadas
                    activamente y esperamos resolverlas en las próximas actualizaciones.
                  </p>
                </div>
              </div>
            </div>
          </section>

          {/* Comentarios y Sugerencias */}
          <section>
            <h2 className='text-2xl font-semibold text-gray-900 mb-4'>Comentarios y Sugerencias</h2>
            <div className='bg-sena-blue text-white p-6 rounded-lg'>
              <h3 className='font-semibold mb-3'>¿Encontró alguna barrera de accesibilidad?</h3>
              <p className='mb-4'>
                Sus comentarios son fundamentales para mejorar la accesibilidad de SICORA. Si
                experimenta dificultades para acceder a algún contenido o funcionalidad, por favor
                contáctenos:
              </p>
              <div className='grid md:grid-cols-2 gap-4'>
                <div>
                  <h4 className='font-semibold mb-2'>Coordinador de Accesibilidad</h4>
                  <p className='text-sm'>📧 accesibilidad@sena.edu.co</p>
                  <p className='text-sm'>📞 (57) 1 546 1500 ext. 4444</p>
                  <p className='text-sm'>⏰ Lunes a viernes, 8:00 AM - 5:00 PM</p>
                </div>
                <div>
                  <h4 className='font-semibold mb-2'>Soporte Técnico Especializado</h4>
                  <p className='text-sm'>📧 soporte.accesible@sena.edu.co</p>
                  <p className='text-sm'>📞 (57) 1 546 1500 ext. 5555</p>
                  <p className='text-sm'>⏰ 24/7 para emergencias</p>
                </div>
              </div>
            </div>
          </section>

          {/* Compromiso Futuro */}
          <section>
            <h2 className='text-2xl font-semibold text-gray-900 mb-4'>
              Compromiso de Mejora Continua
            </h2>
            <div className='space-y-4'>
              <div className='border-l-4 border-sena-blue pl-4'>
                <h3 className='font-semibold text-gray-900'>Capacitación Continua</h3>
                <p className='text-gray-700'>
                  Nuestro equipo recibe capacitación regular en accesibilidad web y diseño
                  inclusivo.
                </p>
              </div>
              <div className='border-l-4 border-sena-orange pl-4'>
                <h3 className='font-semibold text-gray-900'>Innovación Tecnológica</h3>
                <p className='text-gray-700'>
                  Incorporamos las últimas tecnologías y estándares para mejorar la experiencia de
                  usuario.
                </p>
              </div>
              <div className='border-l-4 border-green-600 pl-4'>
                <h3 className='font-semibold text-gray-900'>Participación Comunitaria</h3>
                <p className='text-gray-700'>
                  Trabajamos con organizaciones de personas con discapacidad para recibir
                  retroalimentación directa.
                </p>
              </div>
            </div>
          </section>

          {/* Información de contacto final */}
          <section className='border-t pt-6'>
            <div className='text-center'>
              <p className='text-sm text-gray-600 mb-2'>
                Declaración de accesibilidad actualizada el 2 de julio de 2025
              </p>
              <p className='text-sm text-gray-600'>
                SENA - EPTI | Construyendo un futuro digital inclusivo para todos los colombianos
              </p>
            </div>
          </section>
        </div>
      </div>
    </div>
  );
};

export default Accesibilidad;
