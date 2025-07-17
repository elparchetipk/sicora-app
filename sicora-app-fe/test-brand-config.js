#!/usr/bin/env node

/**
 * Script de prueba para verificar las configuraciones de marca
 */

import path from 'path';
import fs from 'fs';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

// Función para leer archivos .env
function loadEnvFile(filePath) {
  if (!fs.existsSync(filePath)) {
    console.log(`❌ Archivo no encontrado: ${filePath}`);
    return {};
  }

  const content = fs.readFileSync(filePath, 'utf8');
  const vars = {};

  content.split('\n').forEach((line) => {
    line = line.trim();
    if (line && !line.startsWith('#')) {
      const [key, ...valueParts] = line.split('=');
      if (key && valueParts.length > 0) {
        vars[key.trim()] = valueParts
          .join('=')
          .trim()
          .replace(/^["']|["']$/g, '');
      }
    }
  });

  return vars;
}

// Configuraciones a probar
const configs = [
  { name: 'Development', file: '.env.development' },
  { name: 'Hostinger (EPTI)', file: '.env.hostinger' },
  { name: 'SENA', file: '.env.sena' },
];

console.log('🔍 Verificando configuraciones de marca...\n');

configs.forEach((config) => {
  console.log(`📋 ${config.name}:`);
  console.log(`   Archivo: ${config.file}`);

  const envVars = loadEnvFile(config.file);

  if (Object.keys(envVars).length === 0) {
    console.log('   ❌ No se pudieron leer las variables\n');
    return;
  }

  console.log(`   ✅ Variables cargadas:`);
  console.log(`      🏢 Organización: ${envVars.VITE_ORGANIZATION || 'No definida'}`);
  console.log(`      📛 Nombre: ${envVars.VITE_BRAND_NAME || 'No definido'}`);
  console.log(`      🎯 Target: ${envVars.VITE_BUILD_TARGET || 'No definido'}`);
  console.log(`      🖼️  Logo: ${envVars.VITE_SHOW_LOGO || 'No definido'}`);
  console.log(`      📧 Email: ${envVars.VITE_CONTACT_EMAIL || 'No definido'}`);
  console.log('');
});

console.log('✅ Verificación completada');
console.log('💡 Para probar cada configuración:');
console.log('   Development: pnpm run dev');
console.log('   Hostinger:   pnpm run build:hostinger');
console.log('   SENA:        pnpm run build:sena');
