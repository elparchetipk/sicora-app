import { useState } from 'react';
import { Button } from '../../components/Button';
import { ValidatedInput } from '../../components/ValidatedInput';
import { SecureFormDemo } from '../../components/examples/SecureFormDemo';
import {
  PlusIcon,
  MagnifyingGlassIcon,
  FunnelIcon,
  UserGroupIcon,
} from '@heroicons/react/24/outline';

export function UsuariosPage() {
  const [searchQuery, setSearchQuery] = useState('');
  const [showCreateForm, setShowCreateForm] = useState(false);

  // Mock data para demostración
  const usuarios = [
    {
      id: '1',
      name: 'María González Rodríguez',
      email: 'maria.gonzalez@sena.edu.co',
      role: 'admin',
      status: 'online',
      coordination: 'Administración Central',
    },
    {
      id: '2',
      name: 'Carlos Pérez Martínez',
      email: 'carlos.perez@sena.edu.co',
      role: 'instructor',
      status: 'online',
      coordination: 'CGMLTI',
    },
    {
      id: '3',
      name: 'Ana López Torres',
      email: 'ana.lopez@sena.edu.co',
      role: 'aprendiz',
      status: 'away',
      ficha: '2830024',
    },
  ];

  const getRoleBadge = (role: string) => {
    const roleStyles = {
      admin: 'bg-red-100 text-red-800',
      coordinador: 'bg-blue-100 text-blue-800',
      instructor: 'bg-green-100 text-green-800',
      aprendiz: 'bg-yellow-100 text-yellow-800',
      administrativo: 'bg-gray-100 text-gray-800',
    };

    const roleLabels = {
      admin: 'Administrador',
      coordinador: 'Coordinador',
      instructor: 'Instructor',
      aprendiz: 'Aprendiz',
      administrativo: 'Administrativo',
    };

    return (
      <span
        className={`px-2 py-1 text-xs font-medium rounded-full ${roleStyles[role as keyof typeof roleStyles]}`}
      >
        {roleLabels[role as keyof typeof roleLabels]}
      </span>
    );
  };

  return (
    <div className='space-y-6'>
      {/* Header */}
      <div className='flex justify-between items-center'>
        <div>
          <h1 className='text-2xl font-bold text-gray-900'>Gestión de Usuarios</h1>
          <p className='text-gray-600 mt-1'>
            Administrar instructores, aprendices y personal del SENA
          </p>
        </div>

        {/* ✅ Botón de acción principal a la derecha */}
        <div className='flex items-center space-x-3'>
          <Button variant='outline' size='sm'>
            <FunnelIcon className='w-4 h-4 mr-2' />
            Filtros
          </Button>
          <Button variant='primary' onClick={() => setShowCreateForm(!showCreateForm)}>
            <PlusIcon className='w-4 h-4 mr-2' />
            Nuevo Usuario
          </Button>
        </div>
      </div>

      {/* Barra de búsqueda */}
      <div className='bg-white p-6 rounded-lg shadow-md border border-gray-100'>
        <div className='flex items-center space-x-4'>
          <div className='flex-1'>
            <ValidatedInput
              label=''
              validationPattern='textoSeguro'
              placeholder='Buscar por nombre, email o cédula...'
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
            />
          </div>

          {/* ✅ Botón de búsqueda a la derecha */}
          <div className='flex items-end'>
            <Button variant='primary' size='md'>
              <MagnifyingGlassIcon className='w-4 h-4 mr-2' />
              Buscar
            </Button>
          </div>
        </div>
      </div>

      {/* Formulario de creación (condicional) */}
      {showCreateForm && (
        <div className='bg-white rounded-lg shadow-md border border-gray-100 p-6'>
          <h2 className='text-xl font-semibold text-gray-900 mb-6'>Crear Nuevo Usuario</h2>
          <SecureFormDemo />
        </div>
      )}

      {/* Lista de usuarios */}
      <div className='bg-white rounded-lg shadow-md border border-gray-100'>
        <div className='px-6 py-4 border-b border-gray-200'>
          <div className='flex items-center space-x-2'>
            <UserGroupIcon className='w-5 h-5 text-gray-500' />
            <h2 className='text-lg font-medium text-gray-900'>
              Usuarios Registrados ({usuarios.length})
            </h2>
          </div>
        </div>

        <div className='divide-y divide-gray-200'>
          {usuarios.map((usuario) => (
            <div key={usuario.id} className='p-6 hover:bg-gray-50'>
              <div className='flex items-center justify-between'>
                <div className='flex items-center space-x-4'>
                  {/* Avatar */}
                  <div className='w-12 h-12 bg-sena-primary-100 rounded-full flex items-center justify-center'>
                    <span className='text-sena-primary-700 font-semibold text-lg'>
                      {usuario.name
                        .split(' ')
                        .map((n) => n[0])
                        .join('')
                        .substring(0, 2)}
                    </span>
                  </div>

                  {/* Información del usuario */}
                  <div>
                    <h3 className='text-lg font-medium text-gray-900'>{usuario.name}</h3>
                    <p className='text-gray-600'>{usuario.email}</p>
                    <div className='flex items-center space-x-4 mt-1'>
                      {getRoleBadge(usuario.role)}
                      {usuario.coordination && (
                        <span className='text-sm text-gray-500'>{usuario.coordination}</span>
                      )}
                      {usuario.ficha && (
                        <span className='text-sm text-gray-500'>Ficha: {usuario.ficha}</span>
                      )}
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
                    Eliminar
                  </Button>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Paginación */}
      <div className='bg-white px-6 py-4 rounded-lg shadow-md border border-gray-100'>
        <div className='flex items-center justify-between'>
          <div className='text-sm text-gray-500'>Mostrando 1-3 de 3 usuarios</div>

          {/* ✅ Controles de paginación a la derecha */}
          <div className='flex items-center space-x-2'>
            <Button variant='outline' size='sm' disabled>
              Anterior
            </Button>
            <Button variant='outline' size='sm' disabled>
              Siguiente
            </Button>
          </div>
        </div>
      </div>
    </div>
  );
}

export default UsuariosPage;
