import { cva } from 'class-variance-authority';

export const badgeVariants = cva(
  'inline-flex items-center rounded-full border px-2.5 py-0.5 text-xs font-semibold transition-colors focus:outline-none focus:ring-2 focus:ring-ring focus:ring-offset-2',
  {
    variants: {
      variant: {
        default: 'border-transparent bg-gray-100 text-gray-800 hover:bg-gray-200',
        primary: 'border-transparent bg-sena-primary text-white hover:bg-sena-primary/90',
        secondary: 'border-transparent bg-sena-secondary text-white hover:bg-sena-secondary/90',
        tertiary: 'border-transparent bg-sena-tertiary text-white hover:bg-sena-tertiary/90',
        success: 'border-transparent bg-green-100 text-green-800 hover:bg-green-200',
        warning: 'border-transparent bg-amber-100 text-amber-800 hover:bg-amber-200',
        danger: 'border-transparent bg-red-100 text-red-800 hover:bg-red-200',
        info: 'border-transparent bg-blue-100 text-blue-800 hover:bg-blue-200',
        outline: 'text-gray-700 border-gray-300 hover:bg-gray-50',
        'outline-primary': 'text-sena-primary border-sena-primary hover:bg-sena-light',
        'outline-success': 'text-green-600 border-green-300 hover:bg-green-50',
        'outline-warning': 'text-amber-600 border-amber-300 hover:bg-amber-50',
        'outline-danger': 'text-red-600 border-red-300 hover:bg-red-50',
      },
      size: {
        sm: 'px-2 py-0.5 text-xs',
        default: 'px-2.5 py-0.5 text-xs',
        lg: 'px-3 py-1 text-sm',
      },
      interactive: {
        true: 'cursor-pointer hover:scale-105 active:scale-95',
        false: 'cursor-default',
      },
    },
    defaultVariants: {
      variant: 'default',
      size: 'default',
      interactive: false,
    },
  }
);
