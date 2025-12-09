import { useState, useEffect } from 'react';
import axios from 'axios';
import TaskForm from './components/TaskForm';
import TaskList from './components/TaskList';

const API_URL = 'http://localhost:8000';

axios.get(`${API_URL}/tasks`)

function App() {
  const [tasks, setTasks] = useState([]);
  const [loading, setLoading] = useState(false);
  const [filter, setFilter] = useState('all');

  // Obtener tareas
  const fetchTasks = async () => {
    setLoading(true);
    try {
      const params = {};
      if (filter === 'completed') params.completed = true;
      if (filter === 'pending') params.completed = false;

      const response = await axios.get(`${API_URL}/tasks`, { params });
      setTasks(response.data);
    } catch (error) {
      console.error('Error al obtener tareas:', error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchTasks();
  }, [filter]);

  // Agregar tarea
  const handleAddTask = async (taskData) => {
    try {
      const response = await axios.post(`${API_URL}/tasks`, taskData);
      setTasks([response.data, ...tasks]);
    } catch (error) {
      console.error('Error al crear tarea:', error);
    }
  };

  // Actualizar tarea
  const handleUpdateTask = async (id, updates) => {
    try {
      const response = await axios.put(`${API_URL}/tasks/${id}`, updates);
      setTasks(tasks.map(task => task.id === id ? response.data : task));
    } catch (error) {
      console.error('Error al actualizar tarea:', error);
    }
  };

  // Eliminar tarea
  const handleDeleteTask = async (id) => {
    try {
      await axios.delete(`${API_URL}/tasks/${id}`);
      setTasks(tasks.filter(task => task.id !== id));
    } catch (error) {
      console.error('Error al eliminar tarea:', error);
    }
  };

  return (
    <div className="min-h-screen py-12 px-4" style={{backgroundColor: '#E4DDCB'}}>
      <div className="max-w-3xl mx-auto">
        <div className="rounded-2xl shadow-2xl p-8 md:p-10" style={{backgroundColor: '#FFFFFF', borderTop: '6px solid #B46595'}}>
          <div className="text-center mb-10">
            <h1 className="text-5xl font-light mb-2" style={{color: '#4C042D', fontStyle: 'italic', letterSpacing: '1px'}}>
              Mi Lista de Tareas
            </h1>
            <div className="h-1 w-24 mx-auto mb-4" style={{backgroundColor: '#B46595'}}></div>
            <p className="text-lg" style={{color: '#B46595'}}>
              Organiza tus tareas con elegancia
            </p>
          </div>

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