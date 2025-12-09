import { useState } from 'react';

function TaskForm({ onAddTask }) {
  const [title, setTitle] = useState('');
  const [description, setDescription] = useState('');
  const [priority, setPriority] = useState('medium');
  const [dueDate, setDueDate] = useState('');
  const [dateError, setDateError] = useState('');

  const handleDateChange = (e) => {
    const selectedDate = e.target.value;
    const today = new Date().toISOString().split('T')[0];
    
    if (selectedDate && selectedDate < today) {
      setDateError('La fecha no puede ser anterior a hoy');
      setDueDate('');
    } else {
      setDateError('');
      setDueDate(selectedDate);
    }
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!title.trim()) return;

    onAddTask({
      title,
      description,
      priority,
      due_date: dueDate || null,
    });

    setTitle('');
    setDescription('');
    setPriority('medium');
    setDueDate('');
  };

  return (
    <form onSubmit={handleSubmit} className="p-8 rounded-xl mb-8" style={{backgroundColor: '#F5F0E8', border: '2px solid #E19FC7'}}>
      <h2 className="text-2xl font-light mb-6" style={{color: '#4C042D', fontStyle: 'italic'}}>Nueva Tarea</h2>
      
      <div className="mb-5">
        <label className="block font-medium mb-2" style={{color: '#4C042D'}}>Título *</label>
        <input
          type="text"
          value={title}
          onChange={(e) => setTitle(e.target.value)}
          placeholder="¿Qué necesitas hacer?"
          className="w-full px-4 py-3 border rounded-lg focus:outline-none focus:ring-2 transition"
          style={{borderColor: '#E19FC7', backgroundColor: '#FFFFFF', color: '#4C042D', focusRingColor: '#B46595'}}
          required
        />
      </div>

      <div className="mb-5">
        <label className="block font-medium mb-2" style={{color: '#4C042D'}}>Descripción</label>
        <textarea
          value={description}
          onChange={(e) => setDescription(e.target.value)}
          placeholder="Detalles adicionales (opcional)"
          className="w-full px-4 py-3 border rounded-lg focus:outline-none focus:ring-2 transition"
          style={{borderColor: '#E19FC7', backgroundColor: '#FFFFFF', color: '#4C042D'}}
          rows="4"
        />
      </div>

      <div className="grid grid-cols-2 gap-4 mb-6">
        <div>
          <label className="block font-medium mb-2" style={{color: '#4C042D'}}>Prioridad</label>
          <select
            value={priority}
            onChange={(e) => setPriority(e.target.value)}
            className="w-full px-4 py-3 border rounded-lg focus:outline-none focus:ring-2 transition"
            style={{borderColor: '#E19FC7', backgroundColor: '#FFFFFF', color: '#4C042D'}}
          >
            <option value="low">Baja</option>
            <option value="medium">Media</option>
            <option value="high">Alta</option>
          </select>
        </div>

        <div>
          <label className="block font-medium mb-2" style={{color: '#4C042D'}}>Fecha de vencimiento</label>
          <input
            type="date"
            value={dueDate}
            onChange={handleDateChange}
            min={new Date().toISOString().split('T')[0]}
            className="w-full px-4 py-3 border rounded-lg focus:outline-none focus:ring-2 transition"
            style={{borderColor: dateError ? '#840417' : '#E19FC7', backgroundColor: '#FFFFFF', color: '#4C042D'}}
          />
          {dateError && (
            <p className="text-sm mt-2 font-medium" style={{color: '#840417'}}>
              ⚠️ {dateError}
            </p>
          )}
        </div>
      </div>

      <button
        type="submit"
        className="w-full font-medium py-3 rounded-lg transition-all duration-300 hover:shadow-lg text-white"
        style={{backgroundColor: '#840417'}}
      >
        + Agregar Tarea
      </button>
    </form>
  );
}

export default TaskForm;