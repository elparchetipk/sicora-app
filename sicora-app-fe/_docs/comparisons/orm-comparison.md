# Comparación de ORMs - Multi-Stack Analysis

**Actualizado**: 15 de junio de 2025

## 🎯 Objetivo

Análisis comparativo de Object-Relational Mapping (ORM) implementations entre los 6 stacks del proyecto, usando UserService como caso de estudio.

## 🔍 ORMs por Stack

| Stack             | ORM/Query Builder    | Características Principales        |
| ----------------- | -------------------- | ---------------------------------- |
| **FastAPI**       | SQLAlchemy + Alembic | Mature, powerful, complex          |
| **Go**            | GORM                 | Simple, conventions, lightweight   |
| **Express.js**    | Prisma / TypeORM     | Type-safe, modern, auto-generation |
| **Next.js**       | Prisma               | Same as Express, React integration |
| **Spring Java**   | JPA + Hibernate      | Enterprise, annotations, mature    |
| **Spring Kotlin** | JPA + Hibernate      | Same as Java, Kotlin syntax        |

## 📊 Comparación Detallada

### **Definición de Entidades**

#### **FastAPI - SQLAlchemy**

```python
from sqlalchemy import Column, String, DateTime, Boolean
from sqlalchemy.dialects.postgresql import UUID
import uuid

class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String(255), unique=True, nullable=False)
    name = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
```

#### **Go - GORM**

```go
type User struct {
    ID        uuid.UUID `gorm:"type:uuid;primary_key;default:gen_random_uuid()"`
    Email     string    `gorm:"uniqueIndex;not null"`
    Name      string    `gorm:"not null"`
    IsActive  bool      `gorm:"default:true"`
    CreatedAt time.Time `gorm:"autoCreateTime"`
}
```

#### **Express.js - Prisma**

```typescript
// schema.prisma
model User {
  id        String   @id @default(uuid())
  email     String   @unique
  name      String
  isActive  Boolean  @default(true)
  createdAt DateTime @default(now())

  @@map("users")
}
```

#### **Spring Boot Java - JPA**

```java
@Entity
@Table(name = "users")
public class User {
    @Id
    @GeneratedValue(strategy = GenerationType.AUTO)
    private UUID id;

    @Column(unique = true, nullable = false)
    private String email;

    @Column(nullable = false)
    private String name;

    @Column(name = "is_active")
    private Boolean isActive = true;

    @CreationTimestamp
    private LocalDateTime createdAt;

    // Constructors, getters, setters...
}
```

#### **Spring Boot Kotlin - JPA**

```kotlin
@Entity
@Table(name = "users")
data class User(
    @Id
    @GeneratedValue(strategy = GenerationType.AUTO)
    val id: UUID = UUID.randomUUID(),

    @Column(unique = true, nullable = false)
    val email: String,

    @Column(nullable = false)
    val name: String,

    @Column(name = "is_active")
    val isActive: Boolean = true,

    @CreationTimestamp
    val createdAt: LocalDateTime = LocalDateTime.now()
)
```

### **Operaciones CRUD**

#### **Create - Crear Usuario**

**FastAPI**:

```python
def create_user(db: Session, user_data: UserCreate) -> User:
    db_user = User(**user_data.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
```

**Go**:

```go
func CreateUser(db *gorm.DB, userData CreateUserRequest) (*User, error) {
    user := User{
        Email: userData.Email,
        Name:  userData.Name,
    }
    result := db.Create(&user)
    return &user, result.Error
}
```

**Express.js**:

```typescript
async function createUser(userData: CreateUserDto): Promise<User> {
  return await prisma.user.create({
    data: userData,
  });
}
```

**Spring Java**:

```java
@Transactional
public User createUser(CreateUserDto userData) {
    User user = new User();
    user.setEmail(userData.getEmail());
    user.setName(userData.getName());
    return userRepository.save(user);
}
```

**Spring Kotlin**:

```kotlin
@Transactional
fun createUser(userData: CreateUserDto): User {
    val user = User(
        email = userData.email,
        name = userData.name
    )
    return userRepository.save(user)
}
```

## 📈 Análisis de Características

### **Migraciones**

| Stack         | Tool             | Comando                           | Auto-Generation |
| ------------- | ---------------- | --------------------------------- | --------------- |
| FastAPI       | Alembic          | `alembic revision --autogenerate` | ✅ Yes          |
| Go            | golang-migrate   | `migrate create -ext sql`         | ❌ Manual       |
| Express.js    | Prisma           | `prisma migrate dev`              | ✅ Yes          |
| Spring Java   | Flyway/Liquibase | `mvn flyway:migrate`              | ❌ Manual       |
| Spring Kotlin | Flyway/Liquibase | `./gradlew flywayMigrate`         | ❌ Manual       |

### **Query Building**

**Consulta compleja: Usuarios activos con email específico**

**FastAPI**:

```python
users = db.query(User).filter(
    User.is_active == True,
    User.email.ilike(f"%{search}%")
).order_by(User.created_at.desc()).limit(10).all()
```

**Go**:

```go
var users []User
db.Where("is_active = ? AND email ILIKE ?", true, "%"+search+"%").
   Order("created_at DESC").
   Limit(10).
   Find(&users)
```

**Express.js**:

```typescript
const users = await prisma.user.findMany({
  where: {
    isActive: true,
    email: {
      contains: search,
      mode: 'insensitive',
    },
  },
  orderBy: { createdAt: 'desc' },
  take: 10,
});
```

**Spring Java**:

```java
@Query("SELECT u FROM User u WHERE u.isActive = true AND LOWER(u.email) LIKE LOWER(CONCAT('%', :search, '%')) ORDER BY u.createdAt DESC")
Page<User> findActiveUsersByEmail(@Param("search") String search, Pageable pageable);
```

## 🎯 Criterios de Evaluación

### **Developer Experience**

1. **Learning Curve**: Facilidad de aprendizaje
2. **IDE Support**: Autocompletado, error detection
3. **Documentation**: Calidad y completitud
4. **Community**: Stack Overflow, GitHub issues

### **Performance**

1. **Query Efficiency**: N+1 problems, lazy loading
2. **Memory Usage**: Object overhead
3. **Startup Time**: Application boot time
4. **Runtime Performance**: Query execution speed

### **Features**

1. **Type Safety**: Compile-time error detection
2. **Schema Generation**: Auto-generation capabilities
3. **Migration Support**: Version control for DB schema
4. **Advanced Features**: Transactions, relationships, caching

## 📋 Resultados (Por Completar)

| Criterio       | FastAPI    | Go         | Express    | Next.js    | Java       | Kotlin     |
| -------------- | ---------- | ---------- | ---------- | ---------- | ---------- | ---------- |
| Learning Curve | ⭐⭐⭐     | ⭐⭐⭐⭐   | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐       | ⭐⭐⭐     |
| Type Safety    | ⭐⭐⭐     | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| Performance    | TBD        | TBD        | TBD        | TBD        | TBD        | TBD        |
| Features       | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐   | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |

_TBD: To Be Determined después de implementación completa_

## 🔄 Plan de Testing

1. **Implementar UserService** en todos los stacks
2. **Benchmarks de performance** para operaciones CRUD
3. **Análisis de memoria** durante ejecución
4. **Tiempo de desarrollo** por stack
5. **Encuesta a desarrolladores** sobre experience

## 📚 Recursos de Referencia

- [SQLAlchemy Docs](https://docs.sqlalchemy.org/)
- [GORM Docs](https://gorm.io/docs/)
- [Prisma Docs](https://www.prisma.io/docs/)
- [Spring Data JPA Docs](https://spring.io/projects/spring-data-jpa)

---

**Nota**: Este documento se actualiza conforme se implementan los stacks.
