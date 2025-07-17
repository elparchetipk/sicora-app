# 🔗 Especificación Técnica: Integración Frontend-Backend SICORA

## 📋 **RESUMEN EJECUTIVO**

Este documento detalla la integración técnica entre el frontend React de SICORA y los microservicios backend (Go + Python FastAPI), incluyendo patrones de comunicación, manejo de datos, autenticación y arquitectura de servicios.

---

## 🏗️ **ARQUITECTURA DE INTEGRACIÓN**

### **Patrón de Comunicación**

```
Frontend (React) ↔ API Gateway ↔ Microservicios (Go/Python)
                    ↓
                Load Balancer
                    ↓
            [UserService] [ScheduleService] [AttendanceService]
            [EvalinService] [KbService] [AIService] etc.
```

### **Tecnologías de Integración**

- **HTTP Client**: Axios con interceptors
- **State Management**: React Query + Zustand
- **Authentication**: JWT Tokens (Access + Refresh)
- **Real-time**: WebSockets (Socket.io)
- **File Upload**: Multipart form data
- **API Documentation**: OpenAPI/Swagger

---

## 🔐 **SISTEMA DE AUTENTICACIÓN**

### **JWT Token Management**

```typescript
interface AuthTokens {
  accessToken: string;
  refreshToken: string;
  expiresIn: number;
  tokenType: 'Bearer';
}

interface User {
  id: string;
  email: string;
  name: string;
  role: 'admin' | 'instructor' | 'aprendiz' | 'coordinador' | 'administrativo';
  permissions: string[];
  coordination?: string;
  ficha?: string;
}
```

### **Auth Flow Implementation**

```typescript
// services/auth.service.ts
class AuthService {
  async login(credentials: LoginCredentials): Promise<AuthResponse>;
  async refreshToken(): Promise<AuthTokens>;
  async logout(): Promise<void>;
  async getCurrentUser(): Promise<User>;
  async changePassword(data: ChangePasswordData): Promise<void>;
}

// hooks/useAuth.ts
export const useAuth = () => {
  const { user, isAuthenticated, login, logout } = useAuthStore();
  const { mutate: loginMutation } = useMutation(authService.login);
  // ... implementation
};
```

### **Protected Routes**

```typescript
// components/AuthGuard.tsx
interface AuthGuardProps {
  children: ReactNode;
  requiredRole?: UserRole;
  requiredPermissions?: string[];
}

export const AuthGuard: FC<AuthGuardProps> = ({
  children,
  requiredRole,
  requiredPermissions,
}) => {
  // Implementation with role/permission checking
};
```

---

## 🌐 **SERVICIOS API**

### **Base API Service**

```typescript
// services/api.base.ts
class BaseApiService {
  private axios: AxiosInstance;

  constructor(baseURL: string) {
    this.axios = axios.create({
      baseURL,
      timeout: 10000,
      headers: {
        'Content-Type': 'application/json',
      },
    });

    this.setupInterceptors();
  }

  private setupInterceptors() {
    // Request interceptor for auth tokens
    this.axios.interceptors.request.use();

    // Response interceptor for error handling
    this.axios.interceptors.response.use();
  }
}
```

### **UserService Integration**

```typescript
// services/user.service.ts
interface UserFilters {
  role?: UserRole;
  coordination?: string;
  status?: 'active' | 'inactive';
  search?: string;
}

interface PaginatedResponse<T> {
  data: T[];
  total: number;
  page: number;
  pageSize: number;
  totalPages: number;
}

class UserService extends BaseApiService {
  async getUsers(
    filters: UserFilters,
    pagination: Pagination
  ): Promise<PaginatedResponse<User>>;
  async getUserById(id: string): Promise<User>;
  async createUser(userData: CreateUserData): Promise<User>;
  async updateUser(id: string, userData: UpdateUserData): Promise<User>;
  async deleteUser(id: string): Promise<void>;
  async changeUserRole(id: string, role: UserRole): Promise<User>;
  async getUserPermissions(id: string): Promise<Permission[]>;
}
```

### **ScheduleService Integration**

```typescript
// services/schedule.service.ts
interface Schedule {
  id: string;
  title: string;
  instructorId: string;
  fichaId: string;
  roomId: string;
  startTime: Date;
  endTime: Date;
  dayOfWeek: number;
  competencyId?: string;
  status: 'active' | 'cancelled' | 'completed';
}

class ScheduleService extends BaseApiService {
  async getSchedules(filters: ScheduleFilters): Promise<Schedule[]>;
  async getScheduleById(id: string): Promise<Schedule>;
  async createSchedule(scheduleData: CreateScheduleData): Promise<Schedule>;
  async updateSchedule(
    id: string,
    scheduleData: UpdateScheduleData
  ): Promise<Schedule>;
  async deleteSchedule(id: string): Promise<void>;
  async getScheduleConflicts(scheduleData: ScheduleData): Promise<Conflict[]>;
  async getInstructorSchedule(
    instructorId: string,
    dateRange: DateRange
  ): Promise<Schedule[]>;
  async getRoomSchedule(
    roomId: string,
    dateRange: DateRange
  ): Promise<Schedule[]>;
}
```

### **AttendanceService Integration**

```typescript
// services/attendance.service.ts
interface AttendanceRecord {
  id: string;
  studentId: string;
  scheduleId: string;
  date: Date;
  status: 'present' | 'absent' | 'late' | 'justified';
  timeIn?: Date;
  timeOut?: Date;
  notes?: string;
}

class AttendanceService extends BaseApiService {
  async markAttendance(data: MarkAttendanceData): Promise<AttendanceRecord>;
  async getAttendanceByClass(
    scheduleId: string,
    date: Date
  ): Promise<AttendanceRecord[]>;
  async getStudentAttendance(
    studentId: string,
    dateRange: DateRange
  ): Promise<AttendanceRecord[]>;
  async generateAttendanceReport(
    filters: AttendanceFilters
  ): Promise<AttendanceReport>;
  async getAttendanceStats(
    filters: AttendanceFilters
  ): Promise<AttendanceStats>;
  async exportAttendance(
    filters: AttendanceFilters,
    format: 'xlsx' | 'pdf'
  ): Promise<Blob>;
}
```

### **EvaluationService Integration**

```typescript
// services/evaluation.service.ts
interface ProjectEvaluation {
  id: string;
  projectId: string;
  evaluatorId: string;
  criteria: EvaluationCriteria[];
  score: number;
  feedback: string;
  status: 'draft' | 'submitted' | 'approved';
  evaluatedAt: Date;
}

interface IndividualEvaluation {
  id: string;
  studentId: string;
  competencyId: string;
  evaluatorId: string;
  rubric: RubricItem[];
  score: number;
  level: 'basic' | 'intermediate' | 'advanced';
  feedback: string;
}

class EvaluationService extends BaseApiService {
  // Project Evaluation
  async getProjectEvaluations(
    filters: EvalFilters
  ): Promise<ProjectEvaluation[]>;
  async createProjectEvaluation(
    data: CreateProjectEvalData
  ): Promise<ProjectEvaluation>;
  async updateProjectEvaluation(
    id: string,
    data: UpdateProjectEvalData
  ): Promise<ProjectEvaluation>;

  // Individual Evaluation
  async getIndividualEvaluations(
    filters: EvalFilters
  ): Promise<IndividualEvaluation[]>;
  async createIndividualEvaluation(
    data: CreateIndividualEvalData
  ): Promise<IndividualEvaluation>;
  async getCompetencyEvaluations(
    competencyId: string
  ): Promise<IndividualEvaluation[]>;
}
```

### **AIService Integration**

```typescript
// services/ai.service.ts
interface AIRecommendation {
  type: 'learning_path' | 'content' | 'intervention';
  studentId: string;
  recommendation: string;
  confidence: number;
  reasoning: string;
}

interface ChatMessage {
  id: string;
  message: string;
  response: string;
  userId: string;
  timestamp: Date;
  context?: Record<string, any>;
}

class AIService extends BaseApiService {
  async getRecommendations(studentId: string): Promise<AIRecommendation[]>;
  async chatWithAI(
    message: string,
    context?: Record<string, any>
  ): Promise<string>;
  async analyzePerformance(studentId: string): Promise<PerformanceAnalysis>;
  async predictRisk(studentId: string): Promise<RiskPrediction>;
  async generateReport(type: string, filters: any): Promise<AIGeneratedReport>;
}
```

### **KnowledgeBaseService Integration**

```typescript
// services/kb.service.ts
interface KBDocument {
  id: string;
  title: string;
  content: string;
  category: string;
  tags: string[];
  version: number;
  createdAt: Date;
  updatedAt: Date;
}

interface SearchResult {
  document: KBDocument;
  score: number;
  highlights: string[];
}

class KBService extends BaseApiService {
  async searchDocuments(
    query: string,
    filters?: KBFilters
  ): Promise<SearchResult[]>;
  async getDocument(id: string): Promise<KBDocument>;
  async createDocument(data: CreateKBDocumentData): Promise<KBDocument>;
  async updateDocument(
    id: string,
    data: UpdateKBDocumentData
  ): Promise<KBDocument>;
  async deleteDocument(id: string): Promise<void>;
  async getCategories(): Promise<string[]>;
  async getPopularDocuments(): Promise<KBDocument[]>;
}
```

---

## 🔄 **GESTIÓN DE ESTADO**

### **Zustand Stores Structure**

```typescript
// stores/auth.store.ts
interface AuthState {
  user: User | null;
  tokens: AuthTokens | null;
  isAuthenticated: boolean;
  isLoading: boolean;

  // Actions
  login: (credentials: LoginCredentials) => Promise<void>;
  logout: () => void;
  refreshToken: () => Promise<void>;
  updateUser: (userData: Partial<User>) => void;
}

// stores/ui.store.ts
interface UIState {
  sidebarOpen: boolean;
  theme: 'light' | 'dark';
  notifications: Notification[];
  loading: Record<string, boolean>;

  // Actions
  toggleSidebar: () => void;
  setTheme: (theme: 'light' | 'dark') => void;
  addNotification: (notification: Notification) => void;
  removeNotification: (id: string) => void;
  setLoading: (key: string, loading: boolean) => void;
}

// stores/academic.store.ts
interface AcademicState {
  currentFicha: Ficha | null;
  schedules: Schedule[];
  attendanceRecords: AttendanceRecord[];

  // Actions
  setCurrentFicha: (ficha: Ficha) => void;
  updateSchedules: (schedules: Schedule[]) => void;
  markAttendance: (record: AttendanceRecord) => void;
}
```

### **React Query Integration**

```typescript
// hooks/queries/useUsers.ts
export const useUsers = (filters: UserFilters, pagination: Pagination) => {
  return useQuery({
    queryKey: ['users', filters, pagination],
    queryFn: () => userService.getUsers(filters, pagination),
    staleTime: 5 * 60 * 1000, // 5 minutes
    cacheTime: 10 * 60 * 1000, // 10 minutes
  });
};

export const useCreateUser = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: userService.createUser,
    onSuccess: () => {
      queryClient.invalidateQueries(['users']);
      toast.success('Usuario creado exitosamente');
    },
    onError: (error) => {
      toast.error('Error al crear usuario');
    },
  });
};

// hooks/queries/useSchedules.ts
export const useSchedules = (filters: ScheduleFilters) => {
  return useQuery({
    queryKey: ['schedules', filters],
    queryFn: () => scheduleService.getSchedules(filters),
    refetchInterval: 30000, // Refetch every 30 seconds
  });
};

export const useRealTimeSchedules = (filters: ScheduleFilters) => {
  const { data, ...query } = useSchedules(filters);

  useEffect(() => {
    const socket = io('/schedules');

    socket.on('schedule_updated', (updatedSchedule) => {
      queryClient.setQueryData(['schedules', filters], (old: Schedule[]) =>
        old.map((schedule) =>
          schedule.id === updatedSchedule.id ? updatedSchedule : schedule
        )
      );
    });

    return () => socket.disconnect();
  }, [filters]);

  return { data, ...query };
};
```

---

## 📊 **MANEJO DE DATOS EN TIEMPO REAL**

### **WebSocket Integration**

```typescript
// services/websocket.service.ts
class WebSocketService {
  private socket: Socket;

  connect(namespace: string) {
    this.socket = io(`${API_BASE_URL}/${namespace}`, {
      auth: { token: getAccessToken() },
    });

    this.socket.on('connect', () => {
      console.log('Connected to WebSocket');
    });

    this.socket.on('disconnect', () => {
      console.log('Disconnected from WebSocket');
    });
  }

  subscribe(event: string, callback: (data: any) => void) {
    this.socket.on(event, callback);
  }

  unsubscribe(event: string) {
    this.socket.off(event);
  }

  emit(event: string, data: any) {
    this.socket.emit(event, data);
  }
}

// hooks/useRealTime.ts
export const useRealTimeNotifications = () => {
  const { addNotification } = useUIStore();

  useEffect(() => {
    const wsService = new WebSocketService();
    wsService.connect('notifications');

    wsService.subscribe('new_notification', (notification) => {
      addNotification(notification);
    });

    return () => {
      wsService.unsubscribe('new_notification');
    };
  }, []);
};
```

---

## 📁 **MANEJO DE ARCHIVOS**

### **File Upload Service**

```typescript
// services/file.service.ts
interface UploadProgress {
  loaded: number;
  total: number;
  percentage: number;
}

class FileService extends BaseApiService {
  async uploadFile(
    file: File,
    onProgress?: (progress: UploadProgress) => void
  ): Promise<UploadedFile> {
    const formData = new FormData();
    formData.append('file', file);

    return this.axios.post('/files/upload', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
      onUploadProgress: (progressEvent) => {
        if (onProgress && progressEvent.total) {
          const progress = {
            loaded: progressEvent.loaded,
            total: progressEvent.total,
            percentage: Math.round(
              (progressEvent.loaded / progressEvent.total) * 100
            ),
          };
          onProgress(progress);
        }
      },
    });
  }

  async downloadFile(fileId: string): Promise<Blob>;
  async deleteFile(fileId: string): Promise<void>;
  async getFileInfo(fileId: string): Promise<FileInfo>;
}

// hooks/useFileUpload.ts
export const useFileUpload = () => {
  const [uploadProgress, setUploadProgress] = useState<UploadProgress | null>(
    null
  );
  const [isUploading, setIsUploading] = useState(false);

  const uploadFile = async (file: File) => {
    setIsUploading(true);
    try {
      const result = await fileService.uploadFile(file, setUploadProgress);
      return result;
    } finally {
      setIsUploading(false);
      setUploadProgress(null);
    }
  };

  return { uploadFile, uploadProgress, isUploading };
};
```

---

## 🔍 **BÚSQUEDA Y FILTROS**

### **Advanced Search Implementation**

```typescript
// components/SearchBar.tsx
interface SearchFilters {
  type: 'users' | 'schedules' | 'evaluations' | 'all';
  dateRange?: { start: Date; end: Date };
  status?: string[];
  tags?: string[];
  category?: string;
}

interface SearchResult {
  type: string;
  id: string;
  title: string;
  description: string;
  url: string;
  metadata: Record<string, any>;
}

// hooks/useSearch.ts
export const useSearch = () => {
  const [query, setQuery] = useState('');
  const [filters, setFilters] = useState<SearchFilters>({});
  const [results, setResults] = useState<SearchResult[]>([]);

  const { data, isLoading } = useQuery({
    queryKey: ['search', query, filters],
    queryFn: () => searchService.search(query, filters),
    enabled: query.length > 2,
    debounceMs: 300,
  });

  useEffect(() => {
    if (data) setResults(data);
  }, [data]);

  return { query, setQuery, filters, setFilters, results, isLoading };
};
```

---

## 📈 **ANALYTICS Y MÉTRICAS**

### **Analytics Service**

```typescript
// services/analytics.service.ts
interface UserAction {
  action: string;
  category: string;
  label?: string;
  value?: number;
  metadata?: Record<string, any>;
}

class AnalyticsService {
  trackPageView(page: string, user?: User) {
    // Google Analytics 4 implementation
    gtag('config', 'GA_MEASUREMENT_ID', {
      page_title: page,
      page_location: window.location.href,
      user_id: user?.id,
    });
  }

  trackUserAction(action: UserAction, user?: User) {
    gtag('event', action.action, {
      event_category: action.category,
      event_label: action.label,
      value: action.value,
      user_id: user?.id,
      custom_parameters: action.metadata,
    });
  }

  trackError(error: Error, context?: Record<string, any>) {
    // Sentry integration
    Sentry.captureException(error, {
      tags: context,
      user: getCurrentUser(),
    });
  }
}

// hooks/useAnalytics.ts
export const useAnalytics = () => {
  const { user } = useAuthStore();

  const trackPageView = useCallback(
    (page: string) => {
      analyticsService.trackPageView(page, user);
    },
    [user]
  );

  const trackAction = useCallback(
    (action: UserAction) => {
      analyticsService.trackUserAction(action, user);
    },
    [user]
  );

  return { trackPageView, trackAction };
};
```

---

## ⚡ **OPTIMIZACIÓN DE RENDIMIENTO**

### **Code Splitting y Lazy Loading**

```typescript
// Lazy loading of routes
const UserManagement = lazy(() => import('../pages/UserManagement'));
const ScheduleManagement = lazy(() => import('../pages/ScheduleManagement'));
const EvaluationSystem = lazy(() => import('../pages/EvaluationSystem'));

// Component lazy loading
const HeavyChart = lazy(() => import('../components/HeavyChart'));

// hooks/useLazyComponent.ts
export const useLazyComponent = <T>(
  importFn: () => Promise<{ default: ComponentType<T> }>
) => {
  const [Component, setComponent] = useState<ComponentType<T> | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<Error | null>(null);

  const loadComponent = useCallback(async () => {
    setLoading(true);
    try {
      const module = await importFn();
      setComponent(() => module.default);
    } catch (err) {
      setError(err as Error);
    } finally {
      setLoading(false);
    }
  }, [importFn]);

  return { Component, loading, error, loadComponent };
};
```

### **Caching Strategy**

```typescript
// utils/cache.ts
class CacheManager {
  private cache = new Map<
    string,
    { data: any; timestamp: number; ttl: number }
  >();

  set(key: string, data: any, ttl = 300000) {
    // 5 minutes default
    this.cache.set(key, {
      data,
      timestamp: Date.now(),
      ttl,
    });
  }

  get(key: string) {
    const item = this.cache.get(key);
    if (!item) return null;

    if (Date.now() - item.timestamp > item.ttl) {
      this.cache.delete(key);
      return null;
    }

    return item.data;
  }

  clear() {
    this.cache.clear();
  }
}

// Service worker for offline caching
// sw.js
self.addEventListener('fetch', (event) => {
  if (event.request.url.includes('/api/')) {
    event.respondWith(
      caches.open('api-cache').then((cache) => {
        return cache.match(event.request).then((response) => {
          if (response) {
            // Serve from cache
            fetch(event.request).then((fetchResponse) => {
              cache.put(event.request, fetchResponse.clone());
            });
            return response;
          }

          // Fetch and cache
          return fetch(event.request).then((fetchResponse) => {
            cache.put(event.request, fetchResponse.clone());
            return fetchResponse;
          });
        });
      })
    );
  }
});
```

---

## 🛡️ **SEGURIDAD Y VALIDACIÓN**

### **Input Validation with Zod**

```typescript
// schemas/user.schema.ts
import { z } from 'zod';

export const createUserSchema = z.object({
  name: z.string().min(2).max(100),
  email: z.string().email(),
  role: z.enum([
    'admin',
    'instructor',
    'aprendiz',
    'coordinador',
    'administrativo',
  ]),
  password: z
    .string()
    .min(8)
    .regex(/^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)/),
  coordination: z.string().optional(),
  ficha: z.string().optional(),
});

export type CreateUserData = z.infer<typeof createUserSchema>;

// hooks/useFormValidation.ts
export const useFormValidation = <T>(schema: z.ZodSchema<T>) => {
  const [errors, setErrors] = useState<Record<string, string>>({});

  const validate = (data: any): data is T => {
    try {
      schema.parse(data);
      setErrors({});
      return true;
    } catch (error) {
      if (error instanceof z.ZodError) {
        const errorMap = error.errors.reduce(
          (acc, err) => {
            const path = err.path.join('.');
            acc[path] = err.message;
            return acc;
          },
          {} as Record<string, string>
        );
        setErrors(errorMap);
      }
      return false;
    }
  };

  return { validate, errors };
};
```

### **XSS Protection**

```typescript
// utils/sanitize.ts
import DOMPurify from 'dompurify';

export const sanitizeHTML = (html: string): string => {
  return DOMPurify.sanitize(html);
};

export const sanitizeInput = (input: string): string => {
  return input.replace(/<script\b[^<]*(?:(?!<\/script>)<[^<]*)*<\/script>/gi, '');
};

// components/SafeHTML.tsx
interface SafeHTMLProps {
  html: string;
  className?: string;
}

export const SafeHTML: FC<SafeHTMLProps> = ({ html, className }) => {
  const sanitizedHTML = sanitizeHTML(html);

  return (
    <div
      className={className}
      dangerouslySetInnerHTML={{ __html: sanitizedHTML }}
    />
  );
};
```

---

## 🔒 **VALIDACIÓN Y SEGURIDAD FRONTEND**

### **Validaciones con REGEXP - Protección contra Ataques**

**REGLA CRÍTICA**: Todas las entradas de usuario deben ser validadas con patrones REGEXP robustos para prevenir ataques de inyección, XSS y otros vectores de ataque.

#### **📋 Patrones de Validación Institucional SENA**

```typescript
// Validaciones SENA - Patterns REGEXP seguros
export const VALIDATION_PATTERNS = {
  // Documento de identidad (solo números, 7-10 dígitos)
  cedula: /^[0-9]{7,10}$/,

  // Email institucional SENA (obligatorio dominio @sena.edu.co)
  emailSena: /^[a-zA-Z0-9._%+-]+@sena\.edu\.co$/,

  // Email general (RFC 5322 compliant, sin scripts)
  email:
    /^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?(?:\.[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)*$/,

  // Nombres (solo letras, espacios, acentos latinos, sin números ni símbolos)
  nombre: /^[a-zA-ZáéíóúÁÉÍÓÚñÑüÜ\s]{2,50}$/,

  // Código de ficha SENA (formato específico: 7 dígitos)
  fichaCode: /^[0-9]{7}$/,

  // Teléfono Colombia (formato +57 + 10 dígitos o 10 dígitos)
  telefono: /^(?:\+57\s?)?[0-9]{10}$/,

  // Contraseña segura (min 8 chars, mayús, minús, número, símbolo)
  password:
    /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$/,

  // Código de curso/competencia (letras y números, guiones permitidos)
  codigoCurso: /^[A-Z0-9-]{3,20}$/,

  // Texto libre seguro (sin scripts, tags HTML, ni caracteres peligrosos)
  textoSeguro: /^[a-zA-Z0-9áéíóúÁÉÍÓÚñÑüÜ\s.,;:()!?¿¡\-_]{0,500}$/,

  // URL segura (solo HTTPS, dominios permitidos)
  urlSegura:
    /^https:\/\/[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}(\/[a-zA-Z0-9._~:/?#[\]@!$&'()*+,;=-]*)?$/,

  // Código de centro de formación
  codigoCentro: /^[0-9]{4}$/,

  // GUID/UUID v4 (para IDs seguros)
  uuid: /^[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$/i,
} as const;

// Mensajes de error personalizados
export const VALIDATION_MESSAGES = {
  cedula: 'La cédula debe contener entre 7 y 10 dígitos',
  emailSena: 'Debe usar un email institucional @sena.edu.co',
  email: 'Formato de email inválido',
  nombre: 'Solo se permiten letras, espacios y acentos (2-50 caracteres)',
  fichaCode: 'El código de ficha debe tener exactamente 7 dígitos',
  telefono: 'Formato: +57 300 123 4567 o 300 123 4567',
  password: 'Mínimo 8 caracteres: mayúscula, minúscula, número y símbolo',
  codigoCurso: 'Formato inválido. Ej: TI-001, ADSO-2024',
  textoSeguro:
    'Texto contiene caracteres no permitidos o excede 500 caracteres',
  urlSegura: 'Solo se permiten URLs HTTPS válidas',
  codigoCentro: 'El código del centro debe tener 4 dígitos',
  uuid: 'Formato UUID inválido',
} as const;
```

#### **🛡️ Implementación de Validador Seguro**

```typescript
interface ValidationResult {
  isValid: boolean;
  message?: string;
  sanitizedValue?: string;
}

class SecureValidator {
  /**
   * Valida y sanitiza input usando REGEXP patterns
   */
  static validate(
    value: string,
    pattern: keyof typeof VALIDATION_PATTERNS,
    customMessage?: string
  ): ValidationResult {
    // Sanitización básica: trim y normalización
    const sanitizedValue = value.trim().normalize('NFD');

    // Verificación de longitud para prevenir ataques DoS
    if (sanitizedValue.length > 1000) {
      return {
        isValid: false,
        message: 'Entrada demasiado larga (máximo 1000 caracteres)',
      };
    }

    // Detección de intentos de inyección básicos
    const dangerousPatterns = [
      /<script[^>]*>/i,
      /javascript:/i,
      /vbscript:/i,
      /onload=/i,
      /onerror=/i,
      /eval\(/i,
      /document\./i,
      /window\./i,
      /'.*union.*select/i,
      /drop\s+table/i,
    ];

    const hasDangerousContent = dangerousPatterns.some((dp) =>
      dp.test(sanitizedValue)
    );
    if (hasDangerousContent) {
      return {
        isValid: false,
        message: 'Contenido potencialmente peligroso detectado',
      };
    }

    // Validación con pattern específico
    const regex = VALIDATION_PATTERNS[pattern];
    const isValid = regex.test(sanitizedValue);

    return {
      isValid,
      message: isValid
        ? undefined
        : customMessage || VALIDATION_MESSAGES[pattern],
      sanitizedValue: isValid ? sanitizedValue : undefined,
    };
  }

  /**
   * Validación específica para formularios SICORA
   */
  static validateSicoraUser(userData: {
    cedula: string;
    nombre: string;
    email: string;
    telefono?: string;
    fichaCode?: string;
  }): Record<string, ValidationResult> {
    return {
      cedula: this.validate(userData.cedula, 'cedula'),
      nombre: this.validate(userData.nombre, 'nombre'),
      email: this.validate(userData.email, 'emailSena'),
      ...(userData.telefono && {
        telefono: this.validate(userData.telefono, 'telefono'),
      }),
      ...(userData.fichaCode && {
        fichaCode: this.validate(userData.fichaCode, 'fichaCode'),
      }),
    };
  }
}
```

#### **🔍 Hook de Validación en Tiempo Real**

```typescript
import { useState, useCallback } from 'react';

interface UseValidationProps {
  pattern: keyof typeof VALIDATION_PATTERNS;
  customMessage?: string;
  debounceMs?: number;
}

export function useValidation({
  pattern,
  customMessage,
  debounceMs = 300,
}: UseValidationProps) {
  const [validationState, setValidationState] = useState<ValidationResult>({
    isValid: true,
  });
  const [isValidating, setIsValidating] = useState(false);

  const validateValue = useCallback(
    debounce((value: string) => {
      setIsValidating(true);
      const result = SecureValidator.validate(value, pattern, customMessage);
      setValidationState(result);
      setIsValidating(false);
    }, debounceMs),
    [pattern, customMessage, debounceMs]
  );

  return {
    ...validationState,
    isValidating,
    validate: validateValue,
    reset: () => setValidationState({ isValid: true }),
  };
}

// Utility function
function debounce<T extends (...args: any[]) => any>(
  func: T,
  wait: number
): (...args: Parameters<T>) => void {
  let timeout: NodeJS.Timeout;
  return (...args: Parameters<T>) => {
    clearTimeout(timeout);
    timeout = setTimeout(() => func(...args), wait);
  };
}
```

#### **📝 Componente de Input Validado**

```typescript
import { forwardRef, InputHTMLAttributes } from 'react';
import { useValidation } from '../hooks/useValidation';
import { cn } from '../utils/cn';

interface ValidatedInputProps extends Omit<InputHTMLAttributes<HTMLInputElement>, 'pattern'> {
  label: string;
  validationPattern: keyof typeof VALIDATION_PATTERNS;
  customMessage?: string;
  required?: boolean;
  onValidationChange?: (isValid: boolean, sanitizedValue?: string) => void;
}

export const ValidatedInput = forwardRef<HTMLInputElement, ValidatedInputProps>(
  ({
    label,
    validationPattern,
    customMessage,
    onValidationChange,
    className,
    ...props
  }, ref) => {
    const { isValid, message, isValidating, validate } = useValidation({
      pattern: validationPattern,
      customMessage
    });

    const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
      const value = e.target.value;
      validate(value);

      // Callback para el componente padre
      if (onValidationChange) {
        const result = SecureValidator.validate(value, validationPattern, customMessage);
        onValidationChange(result.isValid, result.sanitizedValue);
      }

      // Llamar onChange original si existe
      props.onChange?.(e);
    };

    return (
      <div className="space-y-2">
        <label className="block text-sm font-medium text-gray-700">
          {label}
          {props.required && <span className="text-red-500 ml-1">*</span>}
        </label>

        <div className="relative">
          <input
            ref={ref}
            {...props}
            onChange={handleChange}
            className={cn(
              'w-full px-4 py-2 border rounded-lg transition-colors',
              'focus:ring-2 focus:ring-sena-primary-500 focus:border-transparent',
              isValid
                ? 'border-gray-300'
                : 'border-red-500 bg-red-50',
              isValidating && 'border-yellow-300 bg-yellow-50',
              className
            )}
          />

          {isValidating && (
            <div className="absolute right-3 top-1/2 transform -translate-y-1/2">
              <div className="animate-spin h-4 w-4 border-2 border-yellow-500 border-t-transparent rounded-full" />
            </div>
          )}
        </div>

        {message && (
          <p className="text-sm text-red-600 flex items-center space-x-1">
            <span>⚠️</span>
            <span>{message}</span>
          </p>
        )}
      </div>
    );
  }
);
```

### **🚨 Prevención de Ataques Comunes**

#### **Cross-Site Scripting (XSS)**

```typescript
// Sanitización de contenido HTML
import DOMPurify from 'dompurify';

export function sanitizeHTML(dirty: string): string {
  return DOMPurify.sanitize(dirty, {
    ALLOWED_TAGS: ['b', 'i', 'em', 'strong', 'p', 'br'],
    ALLOWED_ATTR: [],
  });
}

// Escapar contenido para mostrar en UI
export function escapeHTML(text: string): string {
  const div = document.createElement('div');
  div.textContent = text;
  return div.innerHTML;
}
```

#### **SQL Injection Prevention (Frontend Validation)**

```typescript
// Validación adicional para prevenir intentos de SQL injection
export function validateSQLSafe(input: string): boolean {
  const sqlInjectionPatterns = [
    /('|(\\')|(;)|(\\)|(--)|(%27)|(%22)|(%2D%2D))/i,
    /(union|select|insert|update|delete|drop|create|alter|exec|execute)/i,
    /(script|javascript|vbscript|onload|onerror)/i,
  ];

  return !sqlInjectionPatterns.some((pattern) => pattern.test(input));
}
```

---

## 🐳 **CONTAINERIZACIÓN Y ENTORNO DE DESARROLLO**

### **📅 Cronograma de Implementación Docker**

#### **Fase 1: Desarrollo Local (Semana 3-4)**

```dockerfile
# Dockerfile.dev - Para desarrollo
FROM node:20-alpine

WORKDIR /app

# Instalar dependencias globales
RUN npm install -g pnpm

# Copiar archivos de dependencias
COPY package.json pnpm-lock.yaml ./

# Instalar dependencias
RUN pnpm install

# Copiar código fuente
COPY . .

# Exponer puerto de desarrollo
EXPOSE 5173

# Comando para desarrollo con hot reload
CMD ["pnpm", "dev", "--host", "0.0.0.0"]
```

#### **Devcontainer Configuration (.devcontainer/devcontainer.json)**

```json
{
  "name": "SICORA Frontend Development",
  "dockerComposeFile": "../docker-compose.dev.yml",
  "service": "frontend",
  "workspaceFolder": "/workspace",

  "customizations": {
    "vscode": {
      "extensions": [
        "ms-vscode.vscode-typescript-next",
        "bradlc.vscode-tailwindcss",
        "esbenp.prettier-vscode",
        "ms-vscode.vscode-eslint",
        "formulahendry.auto-rename-tag",
        "christian-kohler.path-intellisense",
        "ms-vscode.vscode-json"
      ],
      "settings": {
        "typescript.preferences.importModuleSpecifier": "relative",
        "editor.formatOnSave": true,
        "editor.defaultFormatter": "esbenp.prettier-vscode",
        "tailwindCSS.experimental.classRegex": [
          ["cn\\(([^)]*)\\)", "'([^']*)'"],
          ["clsx\\(([^)]*)\\)", "'([^']*)'"]
        ]
      }
    }
  },

  "forwardPorts": [5173, 3000],
  "postCreateCommand": "pnpm install",
  "remoteUser": "node"
}
```

#### **Docker Compose para Desarrollo (docker-compose.dev.yml)**

```yaml
version: '3.8'

services:
  frontend:
    build:
      context: .
      dockerfile: Dockerfile.dev
    container_name: sicora-frontend-dev
    ports:
      - '5173:5173'
      - '3000:3000' # Para Storybook
    volumes:
      - .:/workspace:cached
      - /workspace/node_modules
    environment:
      - NODE_ENV=development
      - VITE_API_URL=http://localhost:8080
      - VITE_BACKEND_GO_URL=http://localhost:8080
      - VITE_BACKEND_PYTHON_URL=http://localhost:8000
    depends_on:
      - backend-gateway
    networks:
      - sicora-dev

  # Simulación de backend para desarrollo
  backend-gateway:
    image: node:20-alpine
    container_name: sicora-backend-mock
    ports:
      - '8080:8080'
    volumes:
      - ./mock-backend:/app
    working_dir: /app
    command: npm start
    networks:
      - sicora-dev

networks:
  sicora-dev:
    driver: bridge
```

#### **Fase 2: Testing y CI/CD (Semana 5-6)**

```dockerfile
# Dockerfile.test - Para testing automatizado
FROM node:20-alpine AS test

WORKDIR /app

# Instalar dependencias
COPY package.json pnpm-lock.yaml ./
RUN npm install -g pnpm && pnpm install

# Copiar código fuente
COPY . .

# Ejecutar tests
RUN pnpm run test:ci
RUN pnpm run lint
RUN pnpm run type-check

# Build de producción para validar
RUN pnpm run build

# Stage final para artifact
FROM nginx:alpine AS production
COPY --from=test /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/nginx.conf
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
```

#### **Fase 3: Producción (Semana 7-8)**

```dockerfile
# Dockerfile.prod - Para producción optimizada
FROM node:20-alpine AS builder

WORKDIR /app

# Instalar dependencias de build
RUN npm install -g pnpm

# Copiar archivos de dependencias
COPY package.json pnpm-lock.yaml ./
RUN pnpm install --frozen-lockfile

# Copiar código fuente
COPY . .

# Build optimizado para producción
ENV NODE_ENV=production
RUN pnpm run build

# Stage de producción con nginx
FROM nginx:1.25-alpine AS production

# Copiar archivos estáticos
COPY --from=builder /app/dist /usr/share/nginx/html

# Configuración de nginx optimizada para SPA
COPY nginx.prod.conf /etc/nginx/nginx.conf

# Metadata
LABEL maintainer="SENA CGMLTI <desarrollo@sena.edu.co>"
LABEL version="1.0"
LABEL description="SICORA Frontend - React + Vite + TailwindCSS"

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD curl -f http://localhost/ || exit 1

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
```

### **🛠️ Scripts de Automatización**

#### **Makefile para gestión de contenedores**

```makefile
# Makefile para SICORA Frontend
.PHONY: dev build test deploy clean

# Desarrollo
dev:
	docker-compose -f docker-compose.dev.yml up --build

dev-detached:
	docker-compose -f docker-compose.dev.yml up -d --build

# Testing
test:
	docker build -f Dockerfile.test -t sicora-frontend:test .
	docker run --rm sicora-frontend:test

# Build de producción
build:
	docker build -f Dockerfile.prod -t sicora-frontend:latest .

# Deploy (según ambiente)
deploy-staging:
	docker build -f Dockerfile.prod -t sicora-frontend:staging .
	docker tag sicora-frontend:staging registry.sena.edu.co/sicora/frontend:staging
	docker push registry.sena.edu.co/sicora/frontend:staging

deploy-prod:
	docker build -f Dockerfile.prod -t sicora-frontend:prod .
	docker tag sicora-frontend:prod registry.sena.edu.co/sicora/frontend:latest
	docker push registry.sena.edu.co/sicora/frontend:latest

# Limpieza
clean:
	docker-compose -f docker-compose.dev.yml down -v
	docker system prune -f

# Logs
logs:
	docker-compose -f docker-compose.dev.yml logs -f frontend

# Acceso al contenedor
shell:
	docker-compose -f docker-compose.dev.yml exec frontend sh
```

### **📋 Cuándo Implementar Docker**

#### **Cronograma Recomendado:**

1. **Ahora (Semana 2)**: Configurar devcontainer básico para desarrollo
2. **Semana 3**: Docker compose completo para desarrollo local
3. **Semana 4**: Integración con backend via Docker networks
4. **Semana 5**: Dockerfile de testing para CI/CD
5. **Semana 6**: Dockerfile de producción optimizado
6. **Semana 7**: Deploy a staging con Docker
7. **Semana 8**: Deploy a producción

#### **Beneficios Inmediatos del Devcontainer:**

- Entorno de desarrollo consistente para todo el equipo
- Extensiones de VS Code preconfiguradas
- Configuración automática de linting y formatting
- Eliminación de problemas de "funciona en mi máquina"
- Integración automática con servicios de backend

#### **Preparación para Docker:**

- [x] Proyecto base funcional ✅
- [x] Scripts de build y test ✅
- [ ] Variables de entorno organizadas
- [ ] Configuración de nginx para SPA
- [ ] Health checks implementados
- [ ] Documentación de deployment

---

**NOTA IMPORTANTE**: La implementación de Docker debe hacerse gradualmente. Empezar con devcontainer esta semana, seguir con docker-compose la próxima, y culminar con producción en 2-3 semanas más.

---
