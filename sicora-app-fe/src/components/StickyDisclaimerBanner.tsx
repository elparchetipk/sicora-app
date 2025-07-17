import { useState, useEffect } from 'react';
import { cn } from '../utils/cn';
import { IS_SENA_BUILD, BRAND_CONFIG } from '../config/brand';
import { SecureContactLink } from './SecureContactLink';

/**
 * StickyDisclaimerBanner - Banner pegajoso de disclaimer para máxima visibilidad
 * Se muestra en la parte superior de la aplicación para EPTI OneVision
 */

interface StickyDisclaimerBannerProps {
  /** Clase CSS adicional */
  className?: string;
}

export function StickyDisclaimerBanner({ className }: StickyDisclaimerBannerProps) {
  const [isDismissed, setIsDismissed] = useState(false);
  const [isMinimized, setIsMinimized] = useState(false);

  // Solo mostrar en builds de EPTI (no SENA)
  if (IS_SENA_BUILD) return null;

  useEffect(() => {
    // Verificar si el usuario ya había cerrado el banner (localStorage)
    const dismissed = localStorage.getItem('epti-disclaimer-dismissed');
    if (dismissed === 'true') {
      setIsDismissed(true);
    }
  }, []);

  const handleDismiss = () => {
    setIsDismissed(true);
    localStorage.setItem('epti-disclaimer-dismissed', 'true');
  };

  const handleMinimize = () => {
    setIsMinimized(!isMinimized);
  };

  if (isDismissed) return null;

  return (
    <div
      className={cn(
        'sticky top-0 z-50 bg-sena-naranja border-b-2 border-sena-naranja-light shadow-sm',
        className
      )}
    >
      <div className='max-w-7xl mx-auto px-4 sm:px-6 lg:px-8'>
        <div
          className={cn('transition-all duration-300 ease-in-out', isMinimized ? 'py-2' : 'py-4')}
        >
          <div className='flex items-center justify-between'>
            {/* Contenido principal */}
            <div className='flex items-center space-x-3 flex-1'>
              <div className='flex-shrink-0'>
                <div className='w-8 h-8 bg-sena-secondary-100 rounded-full flex items-center justify-center'>
                  <span className='text-sena-secondary-600 text-lg font-bold'>⚠</span>
                </div>
              </div>

              <div className='flex-1'>
                {!isMinimized ? (
                  <div className='space-y-1'>
                    <h3 className='text-sena-neutral-700 font-sena-heading font-bold text-sm sm:text-base'>
                      🔒 {BRAND_CONFIG.name} - Entorno de Demostración
                    </h3>
                    <p className='text-sena-neutral-600 text-xs sm:text-sm font-sena-body'>
                      <strong>IMPORTANTE:</strong> Todos los datos son sintéticos y ficticios. No
                      representan información real. El código se proporciona "tal como está" sin
                      garantías.
                    </p>
                  </div>
                ) : (
                  <div className='flex items-center space-x-2'>
                    <span className='text-sena-neutral-700 font-sena-heading font-bold text-sm'>
                      🔒 Datos Sintéticos
                    </span>
                    <span className='text-sena-neutral-600 text-xs'>Solo demostración</span>
                  </div>
                )}
              </div>
            </div>

            {/* Controles */}
            <div className='flex items-center space-x-2 ml-4'>
              {/* Botón minimizar/maximizar */}
              <button
                onClick={handleMinimize}
                className='w-6 h-6 bg-sena-secondary-200 hover:bg-sena-secondary-300 rounded-full flex items-center justify-center transition-colors'
                title={isMinimized ? 'Expandir' : 'Minimizar'}
              >
                <span className='text-sena-neutral-700 text-xs'>{isMinimized ? '↕' : '−'}</span>
              </button>

              {/* Botón cerrar */}
              <button
                onClick={handleDismiss}
                className='w-6 h-6 bg-sena-secondary-200 hover:bg-sena-secondary-300 rounded-full flex items-center justify-center transition-colors'
                title='Cerrar aviso'
              >
                <span className='text-sena-neutral-700 text-xs'>×</span>
              </button>
            </div>
          </div>

          {/* Enlaces adicionales (solo cuando no está minimizado) */}
          {!isMinimized && (
            <div className='mt-3 flex flex-wrap gap-4 text-xs'>
              <a
                href={BRAND_CONFIG.docsUrl}
                className='text-sena-neutral-700 hover:text-sena-neutral-900 underline transition-colors'
              >
                📚 Documentación
              </a>
              <a
                href={BRAND_CONFIG.supportUrl}
                className='text-sena-neutral-700 hover:text-sena-neutral-900 underline transition-colors'
              >
                💬 Soporte
              </a>
              <SecureContactLink type='email' variant='link' className='text-xs'>
                📧 Contacto
              </SecureContactLink>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

export default StickyDisclaimerBanner;
