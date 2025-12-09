import { useState, useEffect } from 'react';
import axios from 'axios';
import TaskForm from './components/TaskForm';
import TaskList from './components/TaskList';
import Login from './components/Login';
import Register from './components/Register';

const API_URL = 'https://proyect-todo.onrender.com';

function App() {
  const [tasks, setTasks] = useState([]);
  const [loading, setLoading] = useState(false);
  const [filter, setFilter] = useState('all');
  const [user, setUser] = useState(null);
  const [currentPage, setCurrentPage] = useState('login'); // 'tasks', 'login', 'register'

  // Verificar si hay usuario autenticado al cargar
  useEffect(() => {
    const storedUser = localStorage.getItem('user');
    const token = localStorage.getItem('token');
    
    if (storedUser && token) {
      try {
        setUser(JSON.parse(storedUser));
        setCurrentPage('tasks');
      } catch (error) {
        console.error('Error al cargar usuario:', error);
        localStorage.removeItem('user');
        localStorage.removeItem('token');
        setCurrentPage('login');
      }
    } else {
      setCurrentPage('login');
    }
  }, []);

  // Obtener tareas
  const fetchTasks = async () => {
    setLoading(true);
    try {
      const token = localStorage.getItem('token');
      const params = {};
      if (filter === 'completed') params.completed = true;
      if (filter === 'pending') params.completed = false;
  
      const response = await axios.get(`${API_URL}/tasks`, { 
        params,
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });
      setTasks(response.data);
    } catch (error) {
      console.error('Error al obtener tareas:', error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    if (user) {
      fetchTasks();
    }
  }, [filter, user]);

  // Agregar tarea
  const handleAddTask = async (taskData) => {
    try {
      const token = localStorage.getItem('token');
      const response = await axios.post(`${API_URL}/tasks`, taskData, {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });
      setTasks([response.data, ...tasks]);
    } catch (error) {
      console.error('Error al crear tarea:', error);
    }
  };

  // Actualizar tarea
  const handleUpdateTask = async (id, updates) => {
    try {
      const token = localStorage.getItem('token');
      const response = await axios.put(`${API_URL}/tasks/${id}`, updates, {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });
      setTasks(tasks.map(task => task.id === id ? response.data : task));
    } catch (error) {
      console.error('Error al actualizar tarea:', error);
    }
  };
    
  // Eliminar tarea
  const handleDeleteTask = async (id) => {
    try {
      const token = localStorage.getItem('token');
      await axios.delete(`${API_URL}/tasks/${id}`, {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });
      setTasks(tasks.filter(task => task.id !== id));
    } catch (error) {
      console.error('Error al eliminar tarea:', error);
    }
  };

  // Manejar login exitoso
  const handleLoginSuccess = (userData) => {
    setUser(userData);
    setCurrentPage('tasks');
  };

  // Manejar registro exitoso
  const handleRegisterSuccess = (userData) => {
    setUser(userData);
    setCurrentPage('tasks');
  };

  // Logout
  const handleLogout = () => {
    localStorage.removeItem('token');
    localStorage.removeItem('user');
    setUser(null);
    setTasks([]);
    setCurrentPage('login');
  };

  // Mostrar Login
  if (currentPage === 'login') {
    return <Login onLoginSuccess={handleLoginSuccess} onGoToRegister={() => setCurrentPage('register')} />;
  }

  // Mostrar Register
  if (currentPage === 'register') {
    return <Register onRegisterSuccess={handleRegisterSuccess} onGoToLogin={() => setCurrentPage('login')} />;
  }

  // Mostrar Tareas (solo si está autenticado)
  return (
    <div className="min-h-screen py-12 px-4" style={{backgroundColor: '#E4DDCB'}}>
      <div className="max-w-3xl mx-auto">
        <div className="rounded-2xl shadow-2xl p-8 md:p-10" style={{backgroundColor: '#FFFFFF', borderTop: '6px solid #B46595'}}>
          {/* Header con usuario y logout */}
          <div className="flex justify-between items-center mb-8">
            <div>
              <h1 className="text-5xl font-light" style={{color: '#4C042D', fontStyle: 'italic', letterSpacing: '1px'}}>
                Mi Lista de Tareas
              </h1>
              <p className="text-sm mt-2" style={{color: '#B46595'}}>
                Bienvenido, {user?.username}
              </p>
            </div>
            <button
              onClick={handleLogout}
              className="px-4 py-2 rounded-lg font-medium transition-all duration-300 hover:shadow-lg"
              style={{
                backgroundColor: '#E19FC7',
                color: '#4C042D',
                border: '2px solid #B46595'
              }}
            >
              Cerrar Sesión
            </button>
          </div>

          <div className="h-1 w-24 mb-4" style={{backgroundColor: '#B46595'}}></div>
          <p className="text-lg mb-8" style={{color: '#B46595'}}>
            Organiza tus tareas con elegancia
          </p>

          {/* Formulario para agregar tarea */}
          <TaskForm onAddTask={handleAddTask} />

          {/* Filtros */}
          <div className="flex gap-3 mb-8 justify-center flex-wrap">
            {['all', 'pending', 'completed'].map(f => (
              <button
                key={f}
                onClick={() => setFilter(f)}
                className="px-6 py-2 rounded-full font-medium transition-all duration-300 hover:shadow-lg"
                style={{
                  backgroundColor: filter === f ? '#B46595' : '#E19FC7',
                  color: filter === f ? '#FFFFFF' : '#4C042D',
                  border: filter === f ? '2px solid #840417' : '2px solid transparent'
                }}
              >
                {f === 'all' ? 'Todas' : f === 'pending' ? 'Pendientes' : 'Completadas'}
              </button>
            ))}
          </div>

          {/* Lista de tareas */}
          {loading ? (
            <div className="text-center py-12">
              <p style={{color: '#B46595', fontSize: '18px'}}>Cargando tareas...</p>
            </div>
          ) : tasks.length === 0 ? (
            <div className="text-center py-12">
              <p style={{color: '#B46595', fontSize: '18px'}}>No hay tareas. ¡Crea una nueva!</p>
            </div>
          ) : (
            <TaskList
              tasks={tasks}
              onUpdateTask={handleUpdateTask}
              onDeleteTask={handleDeleteTask}
            />
          )}
        </div>
      </div>
    </div>
  );
}

export default App;