# 📝 ToDo List - Aplicación de Gestión de Tareas

Una aplicación web moderna y elegante para gestionar tus tareas diarias. Construida con React, FastAPI y MySQL.

## 🎨 Características

✅ **Crear tareas** con título, descripción, prioridad y fecha de vencimiento
✅ **Editar tareas** en tiempo real
✅ **Eliminar tareas** de forma segura
✅ **Marcar como completadas** con checkbox
✅ **Filtrar tareas** (Todas, Pendientes, Completadas)
✅ **Validación de fechas** - No permite fechas pasadas
✅ **Diseño elegante** con paleta de colores sofisticada
✅ **Interfaz responsiva** - Funciona en desktop y móvil

## 🛠️ Tecnologías

### Frontend
- **React 19** - Librería de UI
- **Vite** - Bundler rápido
- **Tailwind CSS** - Estilos
- **Axios** - Cliente HTTP

### Backend
- **FastAPI** - Framework web Python
- **Uvicorn** - Servidor ASGI
- **MySQL Connector** - Conexión a BD
- **Pydantic** - Validación de datos

### Base de Datos
- **MySQL** - Base de datos relacional

## 📁 Estructura del Proyecto

proyect_todo/ 
|    ├── Frontend/ 
|    |    ├── src/ 
|    |    ├── components/ 
|    |    |    ├── TaskForm.jsx
|    |    |    ├── TaskList.jsx
|    |    |    └── TaskItem.jsx
|    |    ├── App.jsx
|    |    ├── index.css 
|    └── main.jsx 
|    ├── package.json
|    ├── vite.config.js
|    └── tailwind.config.js 
|    |
|    ├── Backend/
|    ├── main.py
|    ├── config.py
|    ├── models.py
|    ├── database.py
|    ├── routes.py
|    ├── requirements.txt
|    ├── .env
|    |    └── BD/
|    |        └── schema.sql 
└── README.md


## 🚀 Instalación Local

### Requisitos
- Python 3.8+
- Node.js 14+
- MySQL 5.7+

### Backend

1. **Clonar el repositorio**
```bash
git clone [https://github.com/tu-usuario/proyect_todo.git](https://github.com/tu-usuario/proyect_todo.git)
cd proyect_todo/Backend

Crear entorno virtual
bash
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac
Instalar dependencias
bash
pip install -r requirements.txt
Configurar variables de entorno Crea un archivo .env en la carpeta Backend:
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=tu_contraseña
DB_NAME=todo_db
Crear base de datos
bash
mysql -u root -p < Backend/BD/schema.sql
Ejecutar servidor
bash
uvicorn main:app --reload
El backend estará disponible en http://localhost:8000

Frontend
Navegar a la carpeta Frontend
bash
cd Frontend
Instalar dependencias
bash
npm install
Ejecutar servidor de desarrollo
bash
npm run dev
El frontend estará disponible en http://localhost:5173

📚 API Endpoints
GET /tasks
Obtiene todas las tareas

Parámetros opcionales:
completed (boolean): Filtrar por estado
priority (string): Filtrar por prioridad (low, medium, high)
POST /tasks
Crea una nueva tarea

Body:
json
{
  "title": "Mi tarea",
  "description": "Descripción opcional",
  "priority": "medium",
  "due_date": "2025-12-31"
}
GET /tasks/{id}
Obtiene una tarea específica

PUT /tasks/{id}
Actualiza una tarea

Body: Mismo formato que POST (todos los campos son opcionales)
DELETE /tasks/{id}
Elimina una tarea

🎨 Paleta de Colores
Dust Veil: #E4DDCB (Fondo claro)
Blush of Sin: #E19FC7 (Acentos suaves)
Forbidden Rose: #B46595 (Elementos destacados)
Enchanted Wine: #4C042D (Texto principal)
Crimson Curse: #840417 (Botones/acciones)
Nocturnal Ink: #130E12 (Fondos oscuros)
🌐 Despliegue
Frontend - Netlify
Conecta tu repositorio de GitHub a Netlify
Configura el comando de build: npm run build
Configura el directorio de publicación: dist
Agrega variable de entorno: VITE_API_URL=https://tu-backend.onrender.com
Backend - Render
Conecta tu repositorio de GitHub a Render
Configura el comando de inicio: uvicorn main:app --host 0.0.0.0
Agrega variables de entorno desde Railway
Base de Datos - Railway
Crea un servicio MySQL en Railway
Ejecuta el script schema.sql en tu BD
Obtén las credenciales y úsalas en Render
📝 Variables de Entorno
Backend (.env)
DB_HOST=tu_host_railway
DB_USER=tu_usuario
DB_PASSWORD=tu_contraseña
DB_NAME=railway
Frontend (.env.local)
VITE_API_URL=https://tu-backend.onrender.com
🤝 Contribuir
Las contribuciones son bienvenidas. Por favor:

Fork el proyecto
Crea una rama para tu feature (git checkout -b feature/AmazingFeature)
Commit tus cambios (git commit -m 'Add some AmazingFeature')
Push a la rama (git push origin feature/AmazingFeature)
Abre un Pull Request