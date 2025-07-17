import { SecureContactForm } from '../components/SecureContactForm';
import { SecureContactLink } from '../components/SecureContactLink';
import { DisclaimerBanner } from '../components/DisclaimerBanner';

/**
 * ContactPage - Página de contacto que demuestra mejores prácticas de seguridad
 * Alternativa moderna y segura a mailto: links tradicionales
 */

export function ContactPage() {
  return (
    <div className='min-h-screen bg-sena-neutral-50'>
      {/* Header */}
      <div className='bg-white border-b border-sena-neutral-200'>
        <div className='max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8'>
          <div className='text-center space-y-4'>
            <h1 className='text-3xl font-sena-heading font-bold text-sena-neutral-900'>
              📧 Contacto Seguro - Mejores Prácticas
            </h1>
            <p className='text-lg text-sena-neutral-600 max-w-2xl mx-auto'>
              Demostración de implementación segura de formularios de contacto, evitando los
              problemas de los enlace mailto tradicionales.
            </p>
          </div>
        </div>
      </div>

      <div className='max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-8'>
        {/* Disclaimer de demostración */}
        <DisclaimerBanner variant='card' />

        {/* Problema con mailto */}
        <div className='bg-red-50 border border-red-200 rounded-lg p-6'>
          <h2 className='text-xl font-sena-heading font-semibold text-red-800 mb-4'>
            ❌ Problema: Uso de mailto: con correos reales
          </h2>

          <div className='space-y-4 text-sm text-red-700'>
            <div>
              <h3 className='font-semibold'>🕷️ Harvesting de correos (Web Scraping)</h3>
              <p>
                Los bots escanean sitios web buscando patrones como{' '}
                <code>mailto:correo@dominio.com</code> para spam masivo y phishing.
              </p>
            </div>

            <div>
              <h3 className='font-semibold'>👁️ Exposición en código fuente</h3>
              <p>
                Las direcciones quedan visibles en el HTML, accesibles desde "Ver código fuente".
              </p>
            </div>

            <div>
              <h3 className='font-semibold'>📱 Problemas de usabilidad</h3>
              <p>Experiencia inconsistente: no todos tienen cliente de correo configurado.</p>
            </div>
          </div>

          {/* Ejemplo de mala práctica */}
          <div className='mt-4 bg-red-100 border border-red-300 rounded p-3'>
            <p className='text-xs text-red-600 font-mono'>
              {`<!-- MALA PRÁCTICA - Visible en código fuente -->`}
              <br />
              {`<a href="mailto:contacto@empresa.com">Contactar</a>`}
            </p>
          </div>
        </div>

        {/* Soluciones seguras */}
        <div className='grid grid-cols-1 lg:grid-cols-2 gap-8'>
          {/* Solución 1: Formulario seguro */}
          <div className='space-y-4'>
            <h2 className='text-xl font-sena-heading font-semibold text-sena-neutral-900'>
              ✅ Solución 1: Formulario Seguro
            </h2>
            <SecureContactForm compact />
          </div>

          {/* Solución 2: Enlaces ofuscados */}
          <div className='space-y-4'>
            <h2 className='text-xl font-sena-heading font-semibold text-sena-neutral-900'>
              ✅ Solución 2: Enlaces Ofuscados
            </h2>

            <div className='bg-white border border-sena-neutral-200 rounded-lg p-6 space-y-4'>
              <p className='text-sm text-sena-neutral-600'>
                Los correos se revelan solo cuando el usuario lo solicita:
              </p>

              <div className='space-y-3'>
                <SecureContactLink type='email' variant='button'>
                  📧 Mostrar Correo Demo
                </SecureContactLink>

                <SecureContactLink type='support' variant='button'>
                  💬 Mostrar Soporte
                </SecureContactLink>

                <SecureContactLink type='docs' variant='button'>
                  📚 Mostrar Documentación
                </SecureContactLink>
              </div>

              <div className='bg-sena-secondary-50 border border-sena-secondary-200 rounded p-3'>
                <p className='text-xs text-sena-neutral-600'>
                  <strong>🔒 Características de seguridad:</strong>
                </p>
                <ul className='text-xs text-sena-neutral-500 mt-1 space-y-1'>
                  <li>• Correos codificados en Base64</li>
                  <li>• Revelación solo bajo demanda del usuario</li>
                  <li>• Advertencias sobre funcionalidad demo</li>
                  <li>• No indexables por bots de scraping</li>
                </ul>
              </div>
            </div>
          </div>
        </div>

        {/* Estándares y recomendaciones */}
        <div className='bg-blue-50 border border-blue-200 rounded-lg p-6'>
          <h2 className='text-xl font-sena-heading font-semibold text-blue-800 mb-4'>
            📋 Estándares y Recomendaciones
          </h2>

          <div className='grid grid-cols-1 md:grid-cols-3 gap-6 text-sm'>
            <div>
              <h3 className='font-semibold text-blue-700 mb-2'>🛡️ OWASP</h3>
              <ul className='text-blue-600 space-y-1'>
                <li>• Evitar exposición de información sensible</li>
                <li>• Formularios con validación server-side</li>
                <li>• Medidas anti-spam (CAPTCHA)</li>
              </ul>
            </div>

            <div>
              <h3 className='font-semibold text-blue-700 mb-2'>🌐 W3C Guidelines</h3>
              <ul className='text-blue-600 space-y-1'>
                <li>• Importancia de privacidad del usuario</li>
                <li>• Interfaces de contacto controladas</li>
                <li>• Consideraciones de accesibilidad</li>
              </ul>
            </div>

            <div>
              <h3 className='font-semibold text-blue-700 mb-2'>📧 RFC 6068</h3>
              <ul className='text-blue-600 space-y-1'>
                <li>• Define estándar técnico de mailto:</li>
                <li>• No aborda implicaciones de seguridad</li>
                <li>• Uso público requiere precauciones</li>
              </ul>
            </div>
          </div>
        </div>

        {/* Implementación técnica */}
        <div className='bg-sena-neutral-100 border border-sena-neutral-300 rounded-lg p-6'>
          <h2 className='text-xl font-sena-heading font-semibold text-sena-neutral-900 mb-4'>
            🔧 Implementación Técnica
          </h2>

          <div className='space-y-4'>
            <div>
              <h3 className='font-semibold text-sena-neutral-800'>Ofuscación Base64:</h3>
              <pre className='bg-sena-neutral-200 rounded p-3 text-xs font-mono overflow-x-auto'>
                {`// Codificación segura
const correoReal = atob('ZGVtb0BlamVtcGxvLmxvY2Fs'); // "demo@ejemplo.local"

// Solo revelar cuando el usuario lo solicite
function revelarCorreo() {
  const elemento = document.getElementById('correo-ofuscado');
  elemento.innerHTML = \`<a href="mailto:\${correoReal}">\${correoReal}</a>\`;
}`}
              </pre>
            </div>

            <div>
              <h3 className='font-semibold text-sena-neutral-800'>Formulario con validación:</h3>
              <pre className='bg-sena-neutral-200 rounded p-3 text-xs font-mono overflow-x-auto'>
                {`// Procesamiento server-side seguro
app.post('/contacto', [
  body('email').isEmail().normalizeEmail(),
  body('message').isLength({ min: 10 }).trim(),
  // Protección anti-spam
  rateLimit({ windowMs: 15 * 60 * 1000, max: 5 })
], (req, res) => {
  // Procesar formulario de forma segura
});`}
              </pre>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default ContactPage;
