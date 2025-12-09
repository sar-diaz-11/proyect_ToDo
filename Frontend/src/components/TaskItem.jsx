import { useState } from 'react';

function TaskItem({ task, onUpdateTask, onDeleteTask }) {
  const [isEditing, setIsEditing] = useState(false);
  const [editTitle, setEditTitle] = useState(task.title);
  const [editDescription, setEditDescription] = useState(task.description || '');
  const [editPriority, setEditPriority] = useState(task.priority);
  const [editDueDate, setEditDueDate] = useState(task.due_date || '');

  const handleSave = () => {
    onUpdateTask(task.id, {
      title: editTitle,
      description: editDescription,
      priority: editPriority,
      due_date: editDueDate || null,
    });
    setIsEditing(false);
  };

  const getPriorityColor = (priority) => {
    switch (priority) {
      case 'high':
        return 'bg-red-100 text-red-800';
      case 'medium':
        return 'bg-yellow-100 text-yellow-800';
      case 'low':
        return 'bg-green-100 text-green-800';
      default:
        return 'bg-gray-100 text-gray-800';
    }
  };

  const getPriorityLabel = (priority) => {
    switch (priority) {
      case 'high':
        return 'Alta';
      case 'medium':
        return 'Media';
      case 'low':
        return 'Baja';
      default:
        return priority;
    }
  };

  if (isEditing) {
    return (
      <div className="p-6 rounded-xl border-2" style={{backgroundColor: '#F5F0E8', borderColor: '#E19FC7'}}>
        <input
          type="text"
          value={editTitle}
          onChange={(e) => setEditTitle(e.target.value)}
          className="w-full px-4 py-3 border rounded-lg mb-4 focus:outline-none focus:ring-2 transition"
          style={{borderColor: '#E19FC7', backgroundColor: '#FFFFFF', color: '#4C042D'}}
        />
        <textarea
          value={editDescription}
          onChange={(e) => setEditDescription(e.target.value)}
          className="w-full px-4 py-3 border rounded-lg mb-4 focus:outline-none focus:ring-2 transition"
          style={{borderColor: '#E19FC7', backgroundColor: '#FFFFFF', color: '#4C042D'}}
          rows="3"
        />
        <div className="grid grid-cols-2 gap-3 mb-6">
          <select
            value={editPriority}
            onChange={(e) => setEditPriority(e.target.value)}
            className="px-4 py-3 border rounded-lg focus:outline-none focus:ring-2 transition"
            style={{borderColor: '#E19FC7', backgroundColor: '#FFFFFF', color: '#4C042D'}}
          >
            <option value="low">Baja</option>
            <option value="medium">Media</option>
            <option value="high">Alta</option>
          </select>
          <input
            type="date"
            value={editDueDate}
            onChange={(e) => setEditDueDate(e.target.value)}
            className="px-4 py-3 border rounded-lg focus:outline-none focus:ring-2 transition"
            style={{borderColor: '#E19FC7', backgroundColor: '#FFFFFF', color: '#4C042D'}}
          />
        </div>
        <div className="flex gap-3">
          <button
            onClick={handleSave}
            className="flex-1 py-3 rounded-lg transition-all duration-300 text-white font-medium hover:shadow-md"
            style={{backgroundColor: '#B46595'}}
          >
            Guardar
          </button>
          <button
            onClick={() => setIsEditing(false)}
            className="flex-1 py-3 rounded-lg transition-all duration-300 font-medium border-2 hover:bg-opacity-10"
            style={{borderColor: '#E19FC7', color: '#4C042D', backgroundColor: 'transparent'}}
          >
            Cancelar
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className={`p-4 rounded-lg border-l-4 ${task.completed ? 'bg-gray-100 border-gray-400' : 'bg-white border-indigo-500'}`}>
      <div className="flex items-start gap-3">
        <input
          type="checkbox"
          checked={task.completed}
          onChange={(e) => onUpdateTask(task.id, { completed: e.target.checked })}
          className="mt-1 w-5 h-5 text-indigo-600 rounded focus:ring-2 focus:ring-indigo-500 cursor-pointer"
        />
        <div className="flex-1">
          <h3 className={`font-semibold text-lg ${task.completed ? 'line-through text-gray-500' : 'text-gray-800'}`}>
            {task.title}
          </h3>
          {task.description && (
            <p className={`text-sm mt-1 ${task.completed ? 'text-gray-400' : 'text-gray-600'}`}>
              {task.description}
            </p>
          )}
          <div className="flex gap-2 mt-2 flex-wrap">
            <span className={`text-xs font-medium px-2 py-1 rounded ${getPriorityColor(task.priority)}`}>
              {getPriorityLabel(task.priority)}
            </span>
            {task.due_date && (
              <span className="text-xs text-gray-500 px-2 py-1 bg-gray-100 rounded">
                📅 {new Date(task.due_date).toLocaleDateString('es-ES')}
              </span>
            )}
          </div>
        </div>
        <div className="flex gap-3 flex-shrink-0">
          <button
            onClick={() => setIsEditing(true)}
            className="px-4 py-2 rounded-lg transition-all duration-300 text-sm font-medium border-2 hover:bg-opacity-10"
            style={{borderColor: '#B46595', color: '#B46595', backgroundColor: 'transparent'}}
          >
            Editar
          </button>
          <button
            onClick={() => onDeleteTask(task.id)}
            className="px-4 py-2 rounded-lg transition-all duration-300 text-sm font-medium border-2 hover:bg-opacity-10"
            style={{borderColor: '#840417', color: '#840417', backgroundColor: 'transparent'}}
          >
            Eliminar
          </button>
        </div>
      </div>
    </div>
  );
}

export default TaskItem;