# ToDo List - Aplicación de Gestión de Tareas

Una aplicación web full-stack para la gestión de tareas personales con sistema de autenticación JWT. Permite a los usuarios crear, editar, eliminar y organizar tareas con diferentes niveles de prioridad y fechas de vencimiento.

**Demo en vivo:** https://effulgent-praline-3c31f9.netlify.app

**API Backend:** https://proyect-todo.onrender.com

## Tabla de Contenidos

- [Características](#características)
- [Arquitectura del Sistema](#arquitectura-del-sistema)
- [Stack Tecnológico](#stack-tecnológico)
- [Estructura del Proyecto](#estructura-del-proyecto)
- [Instalación y Configuración Local](#instalación-y-configuración-local)
- [Variables de Entorno](#variables-de-entorno)
- [API Documentation](#api-documentation)
- [Despliegue en Producción](#despliegue-en-producción)

## Características

### Gestión de Tareas
- Crear tareas con título, descripción, prioridad y fecha de vencimiento
- Editar tareas existentes de forma individual
- Eliminar tareas
- Marcar tareas como completadas mediante checkbox
- Filtrado por estado: todas, pendientes o completadas
- Validación de fechas (no permite fechas pasadas)
- Organización por prioridad: baja, media, alta

## Arquitectura del Sistema

El proyecto sigue una arquitectura cliente-servidor con separación clara de responsabilidades:

```
┌─────────────────┐         ┌─────────────────┐         ┌─────────────────┐
│   React SPA     │  HTTPS  │   FastAPI       │   SQL   │   MySQL DB      │
│   (Netlify)     │ ──────> │   (Render)      │ ──────> │   (Railway)     │
│   Port: 443     │         │   Port: 443     │         │   Port: 3306    │
└─────────────────┘         └─────────────────┘         └─────────────────┘
     Frontend                    Backend                  Base de Datos
```

### Flujo de Autenticación

1. Usuario envía credenciales (email/password) al endpoint `/auth/login`
2. Backend valida credenciales contra la base de datos
3. Si son válidas, genera un JWT firmado con SECRET_KEY
4. Frontend almacena el token en localStorage
5. Todas las peticiones subsecuentes incluyen el token en el header `Authorization: Bearer <token>`
6. Backend valida el token en cada petición protegida

### Flujo de Operaciones CRUD

1. Usuario realiza una acción (crear, editar, eliminar tarea)
2. Frontend envía petición HTTP con el token JWT
3. Backend verifica el token y extrae el user_id
4. Backend ejecuta la operación solo sobre las tareas del usuario autenticado
5. Base de datos retorna el resultado
6. Backend responde con los datos actualizados
7. Frontend actualiza la interfaz sin recargar la página

## Stack Tecnológico

### Frontend
- **React 19.0.0** - Librería de JavaScript para construir interfaces de usuario
- **Vite 6.0.5** - Build tool y dev server de última generación
- **Axios 1.7.9** - Cliente HTTP para realizar peticiones al backend
- **Tailwind CSS 3.4.17** - Framework de CSS utility-first para estilos
- **Lucide React** - Librería de iconos moderna y ligera

### Backend
- **FastAPI** - Framework web moderno y de alto rendimiento para Python
- **Uvicorn** - Servidor ASGI de producción para aplicaciones Python
- **Pydantic** - Validación de datos y gestión de configuración
- **MySQL Connector Python** - Driver oficial para conectar con MySQL
- **bcrypt** - Librería para hashear contraseñas de forma segura
- **PyJWT** - Implementación de JSON Web Tokens para Python
- **python-dotenv** - Gestión de variables de entorno

### Base de Datos
- **MySQL 8.0** - Sistema de gestión de bases de datos relacional

### Infraestructura
- **Netlify** - Hosting y CI/CD para el frontend
- **Render** - Hosting para el backend API
- **Railway** - Hosting para la base de datos MySQL

## Estructura del Proyecto

```
proyect_todo/
│
├── Backend/
│   ├── __pycache__/              # Cache de Python (auto-generado)
│   ├── .venv/                    # Entorno virtual de Python
│   ├── BD/
│   │   └── schema.sql            # Definición de estructura de base de datos
│   ├── .env                      # Variables de entorno (no incluido en Git)
│   ├── auth_routes.py            # Endpoints de autenticación (login, register)
│   ├── config.py                 # Configuración de conexión a base de datos
│   ├── database.py               # Funciones de conexión a MySQL
│   ├── main.py                   # Punto de entrada de la aplicación FastAPI
│   ├── models.py                 # Modelos Pydantic para validación de datos
│   ├── requirements.txt          # Dependencias de Python
│   └── routes.py                 # Endpoints CRUD de tareas
│
├── Frontend/
│   ├── dist/                     # Build de producción (auto-generado)
│   ├── node_modules/             # Dependencias de Node (auto-generado)
│   ├── public/                   # Archivos estáticos públicos
│   ├── src/
│   │   ├── assets/               # Recursos como imágenes o fuentes
│   │   ├── components/
│   │   │   ├── Login.jsx         # Componente de inicio de sesión
│   │   │   ├── Register.jsx      # Componente de registro de usuario
│   │   │   ├── TaskForm.jsx      # Formulario para crear/editar tareas
│   │   │   ├── TaskItem.jsx      # Componente individual de tarea
│   │   │   └── TaskList.jsx      # Lista de tareas
│   │   ├── App.css               # Estilos específicos del componente App
│   │   ├── App.jsx               # Componente principal de la aplicación
│   │   ├── index.css             # Estilos globales y configuración de Tailwind
│   │   └── main.jsx              # Punto de entrada de React
│   ├── .env                      # Variables de entorno del frontend
│   ├── .gitignore                # Archivos ignorados por Git
│   ├── eslint.config.js          # Configuración de ESLint
│   ├── index.html                # HTML base de la aplicación
│   ├── package-lock.json         # Versiones exactas de dependencias
│   ├── package.json              # Dependencias y scripts de npm
│   ├── postcss.config.js         # Configuración de PostCSS
│   ├── tailwind.config.js        # Configuración personalizada de Tailwind
│   └── vite.config.js            # Configuración de Vite
│
└── README.md                     # Documentación del proyecto
```

### Descripción de Archivos Clave

#### Backend

**main.py**
- Punto de entrada de la API
- Configuración de CORS para permitir peticiones desde el frontend
- Definición de todos los endpoints HTTP
- Middleware de seguridad con HTTPBearer
- Manejo de dependencias con Depends()

**auth_routes.py**
- Lógica de autenticación y autorización
- Funciones de hashing de contraseñas con bcrypt
- Generación y validación de tokens JWT
- Endpoints de registro y login

**routes.py**
- Lógica de negocio para operaciones CRUD de tareas
- Validación de permisos (usuarios solo pueden acceder a sus propias tareas)
- Manejo de conversión de tipos de datos
- Logging detallado de operaciones

**models.py**
- Definición de modelos Pydantic para validación
- Task: Modelo completo de tarea con todos los campos
- TaskCreate: Modelo para crear nuevas tareas (solo campos requeridos)
- TaskUpdate: Modelo para actualizar tareas (todos los campos opcionales)
- User, UserCreate, UserLogin, UserResponse: Modelos relacionados con usuarios

**config.py**
- Configuración centralizada de la base de datos
- Carga de variables de entorno con dotenv
- Función helper para validar el puerto de la base de datos
- Diccionario DB_CONFIG con credenciales

**database.py**
- Función get_db_connection() para obtener conexión a MySQL
- Manejo de errores de conexión
- Logging de estado de conexión

**schema.sql**
- Definición de tablas users y tasks
- Configuración de claves primarias y foráneas
- Índices para optimizar consultas
- Valores por defecto y constraints

#### Frontend

**App.jsx**
- Componente raíz de la aplicación
- Gestión de estado global (usuario, tareas, filtros)
- Lógica de autenticación (verificar sesión, logout)
- Funciones para operaciones CRUD que se pasan a componentes hijos
- Enrutamiento simple entre vistas (login, register, tasks)

**Login.jsx / Register.jsx**
- Formularios de autenticación
- Validación de campos en el cliente
- Peticiones POST a endpoints de autenticación
- Almacenamiento de token y usuario en localStorage
- Manejo de errores y feedback visual

**TaskForm.jsx**
- Formulario para crear nuevas tareas
- Validación de campos (título requerido, fecha no puede ser pasada)
- Inputs para título, descripción, prioridad y fecha de vencimiento
- Limpieza del formulario después de enviar

**TaskList.jsx**
- Renderiza lista de componentes TaskItem
- Maneja el caso de lista vacía

**TaskItem.jsx**
- Representa una tarea individual
- Modo edición inline
- Checkbox para marcar como completada
- Botones de editar y eliminar
- Indicador visual de prioridad

## Instalación y Configuración Local

### Requisitos Previos

- Node.js versión 14 o superior
- Python versión 3.8 o superior
- MySQL versión 5.7 o superior
- Git

### 1. Clonar el Repositorio

```bash
git clone https://github.com/tu-usuario/proyect_todo.git
cd proyect_todo
```

### 2. Configuración del Backend

#### 2.1 Crear y Activar Entorno Virtual

**Windows:**
```bash
cd Backend
python -m venv .venv
.venv\Scripts\activate
```

**Linux/macOS:**
```bash
cd Backend
python3 -m venv .venv
source .venv/bin/activate
```

#### 2.2 Instalar Dependencias

```bash
pip install -r requirements.txt
```

#### 2.3 Configurar Base de Datos

Crear la base de datos en MySQL:

```bash
mysql -u root -p
```

Dentro de MySQL:
```sql
CREATE DATABASE todo_db;
EXIT;
```

Ejecutar el script de schema:
```bash
mysql -u root -p todo_db < BD/schema.sql
```

#### 2.4 Configurar Variables de Entorno

Crear archivo `.env` en la carpeta Backend:

```env
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=tu_contraseña_mysql
DB_NAME=todo_db
SECRET_KEY=una_clave_secreta_muy_larga_y_segura_de_al_menos_32_caracteres
```

#### 2.5 Ejecutar el Servidor Backend

```bash
uvicorn main:app --reload
```

El servidor estará disponible en `http://localhost:8000`

Para verificar que funciona, accede a `http://localhost:8000` y deberías ver:
```json
{"message": "Bienvenido a la API de ToDo"}
```

### 3. Configuración del Frontend

#### 3.1 Instalar Dependencias

Desde la raíz del proyecto:

```bash
cd Frontend
npm install
```

#### 3.2 Configurar Variables de Entorno

Crear archivo `.env` en la carpeta Frontend:

```env
VITE_API_URL=http://localhost:8000
```

#### 3.3 Ejecutar el Servidor de Desarrollo

```bash
npm run dev
```

El frontend estará disponible en `http://localhost:5173`

### 4. Verificar la Instalación

1. Abre `http://localhost:5173` en tu navegador
2. Regístrate con un nuevo usuario
3. Inicia sesión
4. Crea una tarea de prueba
5. Verifica que puedes editar, completar y eliminar tareas

## Variables de Entorno

### Backend (.env)

| Variable    | Descripción                    | Ejemplo                            | Requerido |
|-------------|--------------------------------|------------------------------------|-----------|
| DB_HOST     | Host de la base de datos MySQL | localhost o ballast.proxy.rlwy.net | Sí |
| DB_PORT     | Puerto de MySQL                | 3306                               | No (default: 3306) |
| DB_USER     | Usuario de MySQL               | root                               | Sí |
| DB_PASSWORD | Contraseña de MySQL            | tu_contraseña                      | Sí |
| DB_NAME     | Nombre de la base de datos     | todo_db                            | Sí |
| SECRET_KEY  | Clave para firmar tokens JWT   | clave_de_32_caracteres_minimo      | Sí |

### Frontend (.env)

| Variable     | Descripción         | Ejemplo                                                   |
|--------------|---------------------|-----------------------------------------------------------|
| VITE_API_URL | URL del backend API | http://localhost:8000 o https://proyect-todo.onrender.com |

**Nota de Seguridad:** Nunca subas archivos `.env` a control de versiones. Estos archivos ya están incluidos en `.gitignore`.

## API Documentation

Base URL (Producción): `https://proyect-todo.onrender.com`
Base URL (Local): `http://localhost:8000`

### Endpoints de Autenticación

#### POST /auth/register

Registra un nuevo usuario en el sistema.

**Request Body:**
```json
{
  "email": "usuario@ejemplo.com",
  "username": "nombreusuario",
  "password": "contraseña_segura"
}
```

**Response (201 Created):**
```json
{
  "id": 1,
  "email": "usuario@ejemplo.com",
  "username": "nombreusuario",
  "created_at": "2025-12-16T10:30:00",
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

**Errores:**
- 400: Email o username ya existe
- 500: Error interno del servidor

#### POST /auth/login

Autentica un usuario existente.

**Request Body:**
```json
{
  "email": "usuario@ejemplo.com",
  "password": "contraseña_segura"
}
```

**Response (200 OK):**
```json
{
  "id": 1,
  "email": "usuario@ejemplo.com",
  "username": "nombreusuario",
  "created_at": "2025-12-16T10:30:00",
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

**Errores:**
- 401: Email o contraseña incorrectos
- 500: Error interno del servidor

### Endpoints de Tareas

**Nota:** Todos los endpoints de tareas requieren autenticación mediante token JWT en el header:
```
Authorization: Bearer <tu_token_jwt>
```

#### GET /tasks

Obtiene todas las tareas del usuario autenticado.

**Query Parameters (opcionales):**
- `completed` (boolean): Filtra por estado de completado
  - `true`: Solo tareas completadas
  - `false`: Solo tareas pendientes
- `priority` (string): Filtra por prioridad
  - Valores: `low`, `medium`, `high`

**Ejemplos de URLs:**
- `/tasks` - Todas las tareas
- `/tasks?completed=false` - Solo pendientes
- `/tasks?priority=high` - Solo prioridad alta
- `/tasks?completed=true&priority=medium` - Completadas con prioridad media

**Response (200 OK):**
```json
[
  {
    "id": 1,
    "user_id": 1,
    "title": "Completar proyecto",
    "description": "Terminar el README y documentación",
    "completed": false,
    "priority": "high",
    "due_date": "2025-12-20",
    "created_at": "2025-12-16T10:30:00",
    "updated_at": "2025-12-16T10:30:00"
  }
]
```

**Errores:**
- 401: Token inválido o expirado
- 500: Error interno del servidor

#### POST /tasks

Crea una nueva tarea.

**Request Body:**
```json
{
  "title": "Nueva tarea",
  "description": "Descripción opcional",
  "priority": "medium",
  "due_date": "2025-12-25"
}
```

**Campos:**
- `title` (string, requerido): Título de la tarea
- `description` (string, opcional): Descripción detallada
- `priority` (string, opcional): Nivel de prioridad (default: "medium")
  - Valores permitidos: `low`, `medium`, `high`
- `due_date` (string, opcional): Fecha de vencimiento en formato YYYY-MM-DD

**Response (201 Created):**
```json
{
  "id": 2,
  "user_id": 1,
  "title": "Nueva tarea",
  "description": "Descripción opcional",
  "completed": false,
  "priority": "medium",
  "due_date": "2025-12-25",
  "created_at": "2025-12-16T11:00:00",
  "updated_at": "2025-12-16T11:00:00"
}
```

**Errores:**
- 401: Token inválido o expirado
- 422: Datos de entrada inválidos
- 500: Error interno del servidor

#### GET /tasks/{task_id}

Obtiene una tarea específica.

**Path Parameters:**
- `task_id` (integer): ID de la tarea

**Response (200 OK):**
```json
{
  "id": 1,
  "user_id": 1,
  "title": "Completar proyecto",
  "description": "Terminar el README y documentación",
  "completed": false,
  "priority": "high",
  "due_date": "2025-12-20",
  "created_at": "2025-12-16T10:30:00",
  "updated_at": "2025-12-16T10:30:00"
}
```

**Errores:**
- 401: Token inválido o expirado
- 404: Tarea no encontrada o no pertenece al usuario
- 500: Error interno del servidor

#### PUT /tasks/{task_id}

Actualiza una tarea existente.

**Path Parameters:**
- `task_id` (integer): ID de la tarea

**Request Body (todos los campos son opcionales):**
```json
{
  "title": "Título actualizado",
  "description": "Nueva descripción",
  "completed": true,
  "priority": "low",
  "due_date": "2025-12-30"
}
```

**Response (200 OK):**
```json
{
  "id": 1,
  "user_id": 1,
  "title": "Título actualizado",
  "description": "Nueva descripción",
  "completed": true,
  "priority": "low",
  "due_date": "2025-12-30",
  "created_at": "2025-12-16T10:30:00",
  "updated_at": "2025-12-16T12:00:00"
}
```

**Errores:**
- 401: Token inválido o expirado
- 404: Tarea no encontrada o no pertenece al usuario
- 422: Datos de entrada inválidos
- 500: Error interno del servidor

#### DELETE /tasks/{task_id}

Elimina una tarea.

**Path Parameters:**
- `task_id` (integer): ID de la tarea

**Response (200 OK):**
```json
{
  "message": "Tarea eliminada exitosamente"
}
```

**Errores:**
- 401: Token inválido o expirado
- 404: Tarea no encontrada o no pertenece al usuario
- 500: Error interno del servidor

## Despliegue en Producción

### 1. Base de Datos en Railway

#### 1.1 Crear Proyecto MySQL

1. Accede a https://railway.app
2. Crea un nuevo proyecto
3. Selecciona "Add MySQL"
4. Railway generará automáticamente las credenciales

#### 1.2 Ejecutar Schema

1. Ve a la pestaña "Data" o "Query"
2. Copia y pega el contenido de `BD/schema.sql`
3. Ejecuta el script

#### 1.3 Obtener Credenciales

Ve a la pestaña "Connect" y copia:
- MYSQL_HOST
- MYSQL_PORT
- MYSQL_USER
- MYSQL_PASSWORD
- MYSQL_DATABASE

### 2. Backend en Render

#### 2.1 Conectar Repositorio

1. Accede a https://render.com
2. Crea un nuevo "Web Service"
3. Conecta tu repositorio de GitHub
4. Selecciona la carpeta `Backend`

#### 2.2 Configurar Servicio

**Build Command:**
```bash
pip install -r requirements.txt
```

**Start Command:**
```bash
uvicorn main:app --host 0.0.0.0 --port $PORT
```

#### 2.3 Variables de Entorno

Añade todas las variables de entorno del backend:

```
DB_HOST=tu_host_railway
DB_PORT=tu_puerto_railway
DB_USER=tu_usuario_railway
DB_PASSWORD=tu_password_railway
DB_NAME=railway
SECRET_KEY=genera_una_clave_segura_de_32_caracteres_minimo
```

**Generar SECRET_KEY segura:**
```python
import secrets
print(secrets.token_urlsafe(32))
```

#### 2.4 Desplegar

Render desplegará automáticamente tu backend. La URL será algo como:
`https://tu-proyecto.onrender.com`

**Nota:** Render puede tardar 1-2 minutos en iniciar en el plan gratuito.

### 3. Frontend en Netlify

#### 3.1 Conectar Repositorio

1. Accede a https://netlify.com
2. Crea un nuevo sitio desde Git
3. Conecta tu repositorio de GitHub
4. Selecciona la carpeta `Frontend`

#### 3.2 Configurar Build

**Base Directory:**
```
Frontend
```

**Build Command:**
```bash
npm run build
```

**Publish Directory:**
```
Frontend/dist
```

#### 3.3 Variables de Entorno

Añade la variable de entorno:

```
VITE_API_URL=https://tu-proyecto.onrender.com
```

**Importante:** No incluyas barra diagonal final en la URL.

#### 3.4 Desplegar

Netlify construirá y desplegará tu frontend automáticamente. La URL será:
`https://tu-sitio.netlify.app`

#### 3.5 Configurar Dominio Personalizado (Opcional)

1. Ve a "Domain Settings"
2. Añade tu dominio personalizado
3. Configura los registros DNS según las instrucciones

### 4. Actualizar CORS en el Backend

Una vez desplegado el frontend, actualiza la configuración de CORS en `main.py`:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://tu-sitio.netlify.app",  # Tu URL de Netlify
        "http://localhost:5173",
        "http://localhost:3000"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

Haz commit y push para que Render redespliegue con la nueva configuración.

### 5. Verificación del Despliegue

1. Accede a tu URL de Netlify
2. Regístrate con un nuevo usuario
3. Crea, edita y elimina tareas
4. Verifica que los filtros funcionen
5. Cierra sesión y vuelve a iniciar

Si todo funciona correctamente, tu aplicación está en producción.

## Seguridad

### Implementaciones de Seguridad

**Autenticación JWT:**
- Tokens firmados con SECRET_KEY de 32+ caracteres
- Expiración configurable (actualmente 7 días)
- Validación en cada petición protegida
- Tokens no renovables automáticamente (mejora la seguridad)

**Contraseñas:**
- Hasheadas con bcrypt (algoritmo de hash adaptativo)
- Salt único para cada contraseña
- Nunca se almacenan en texto plano
- No se retornan en respuestas API

**Base de Datos:**
- Consultas parametrizadas para prevenir SQL Injection
- Validación de permisos en cada operación (usuarios solo acceden a sus datos)
- Índices para optimizar consultas
- Foreign Keys con ON DELETE CASCADE

**Validación de Datos:**
- Pydantic valida todos los datos de entrada
- FastAPI rechaza automáticamente peticiones malformadas
- Validación de tipos de datos en modelos
- Campos opcionales claramente definidos

**CORS:**
- Configurado para permitir solo orígenes específicos
- Credenciales habilitadas solo para orígenes permitidos
- No permite orígenes wildcard (*) en producción

### Mejores Prácticas Implementadas

1. Variables de entorno para datos sensibles (nunca hardcodeadas)
2. .gitignore configurado para excluir .env y archivos sensibles
3. Logging detallado para debugging sin exponer datos sensibles
4. Manejo de errores sin exponer información del sistema
5. Uso de HTTPS en producción (Netlify y Render lo proveen automáticamente)

### Optimizaciones Técnicas

**Performance:**
- Lazy loading de tareas
- Paginación en listas largas
- Compresión de respuestas HTTP
- CDN para assets estáticos
- Service Workers para PWA
- Optimización de imágenes

**DevOps:**
- CI/CD con GitHub Actions
- Tests automáticos pre-deploy
- Monitoreo con Sentry
- Logging centralizado
- Health checks y métricas
- Backup automático de base de datos

## Licencia

Este proyecto es de código abierto y está disponible bajo la Licencia MIT.

## Autor

Sara Valentina Diaz Rojas