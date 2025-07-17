# Páginas Legales de SICORA

Este directorio contiene las páginas legales de la plataforma SICORA, desarrolladas en cumplimiento de la normativa colombiana y estándares internacionales de accesibilidad web.

## Páginas Incluidas

### 1. Política de Privacidad (`PoliticaPrivacidad.tsx`)

- **Cumplimiento**: Ley 1581 de 2012 (Ley de Habeas Data)
- **Contenido**: Tratamiento de datos personales, derechos del titular, procedimientos
- **Ruta**: `/legal/politica-privacidad`

### 2. Términos de Uso (`TerminosUso.tsx`)

- **Cumplimiento**: Marco legal colombiano, normativa institucional del SENA
- **Contenido**: Condiciones de uso, obligaciones del usuario, propiedad intelectual
- **Ruta**: `/legal/terminos-uso`

### 3. Mapa del Sitio (`MapaSitio.tsx`)

- **Propósito**: Navegación completa de la plataforma
- **Contenido**: Estructura del sitio, enlaces organizados por categorías
- **Ruta**: `/legal/mapa-sitio`

### 4. Declaración de Accesibilidad (`Accesibilidad.tsx`)

- **Cumplimiento**: WCAG 2.1 Nivel AA, Ley 1618 de 2013, Decreto 1421 de 2017
- **Contenido**: Características de accesibilidad, compromiso de inclusión digital
- **Ruta**: `/legal/accesibilidad`

## Marco Legal y Normativo

### Normativa Nacional

- **Ley 1581 de 2012**: Protección de datos personales (Habeas Data)
- **Decreto 1377 de 2013**: Reglamentario de la Ley 1581
- **Ley 1618 de 2013**: Derechos de personas con discapacidad
- **Decreto 1421 de 2017**: Educación inclusiva
- **Ley 1346 de 2009**: Convención sobre derechos de personas con discapacidad
- **Ley 1273 de 2009**: Protección de la información y delitos informáticos

### Estándares Internacionales

- **WCAG 2.1**: Web Content Accessibility Guidelines (Nivel AA)
- **ISO/IEC 40500:2012**: Accesibilidad web
- **Section 508**: Estándares de accesibilidad (Estados Unidos)
- **EN 301 549**: Estándares europeos de accesibilidad

## Características Técnicas

### Accesibilidad Web

- ✅ Compatibilidad con lectores de pantalla
- ✅ Navegación por teclado
- ✅ Alto contraste de colores (mínimo 4.5:1)
- ✅ Textos alternativos en imágenes
- ✅ Estructura semántica HTML5
- ✅ Escalabilidad de texto hasta 200%

### Diseño Responsivo

- ✅ Adaptación móvil, tablet y desktop
- ✅ Componentes escalables
- ✅ Tipografía SENA institucional
- ✅ Colores institucionales

### Integración con Router

```tsx
// Rutas configuradas en /src/router/index.tsx
<Route path='legal'>
  <Route path='politica-privacidad' element={<PoliticaPrivacidad />} />
  <Route path='terminos-uso' element={<TerminosUso />} />
  <Route path='mapa-sitio' element={<MapaSitio />} />
  <Route path='accesibilidad' element={<Accesibilidad />} />
</Route>
```

## Componentes de Apoyo

### DisclaimerBanner

- Aviso de exención de responsabilidad
- Configurable como banner, card o inline
- Opción dismissible

### LegalNavigation

- Navegación rápida a páginas legales
- Múltiples variantes de visualización
- Iconos y descripciones configurables

## Enlaces en Footer

Los enlaces legales están integrados en `InstitutionalFooter.tsx`:

- Política de Privacidad
- Términos de Uso
- Mapa del Sitio
- Accesibilidad

## Uso en la Aplicación

### Navegación desde cualquier página

```tsx
import { Link } from 'react-router-dom';

<Link to='/legal/politica-privacidad'>Política de Privacidad</Link>;
```

### Componente de navegación legal

```tsx
import { LegalNavigation } from '../components/LegalNavigation';

<LegalNavigation variant='grid' showIcons={true} showDescriptions={true} />;
```

## Mantenimiento y Actualizaciones

### Frecuencia de Revisión

- **Revisión legal**: Cada 6 meses
- **Actualización técnica**: Con cada release
- **Auditoría de accesibilidad**: Cada 6 meses

### Responsables

- **Contenido legal**: Oficina Jurídica SENA
- **Implementación técnica**: EPTI
- **Accesibilidad**: Coordinador de Accesibilidad

### Proceso de Actualización

1. Revisión de normativa vigente
2. Actualización de contenido
3. Validación legal
4. Pruebas de accesibilidad
5. Despliegue y comunicación

## Contacto para Consultas

### Consultas Legales

- **Email**: legal@sena.edu.co
- **Teléfono**: (57) 1 546 1500 ext. 1111

### Accesibilidad

- **Email**: accesibilidad@sena.edu.co
- **Teléfono**: (57) 1 546 1500 ext. 4444

### Soporte Técnico

- **Email**: soporte.sicora@sena.edu.co
- **Teléfono**: (57) 1 546 1500 ext. 2222

---

**Última actualización**: 2 de julio de 2025  
**Versión**: 1.0  
**Responsable**: EPTI - Equipo de Proyectos de Tecnología e Innovación
