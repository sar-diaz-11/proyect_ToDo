import { useState } from 'react';
import axios from 'axios';

const API_URL = 'https://proyect-todo.onrender.com';

function Register({ onRegisterSuccess, onGoToLogin }) {
  const [email, setEmail] = useState('');
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');

    if (password !== confirmPassword) {
      setError('Las contraseñas no coinciden');
      return;
    }

    if (password.length < 6) {
      setError('La contraseña debe tener al menos 6 caracteres');
      return;
    }

    setLoading(true);

    try {
      const response = await axios.post(`${API_URL}/auth/register`, {
        email,
        username,
        password
      });

      // Guardar token en localStorage
      localStorage.setItem('token', response.data.token);
      localStorage.setItem('user', JSON.stringify({
        id: response.data.id,
        email: response.data.email,
        username: response.data.username
      }));

      onRegisterSuccess(response.data);
    } catch (err) {
      setError(err.response?.data?.detail || 'Error al registrarse');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen py-12 px-4" style={{backgroundColor: '#E4DDCB'}}>
      <div className="max-w-md mx-auto">
        <div className="rounded-2xl shadow-2xl p-8" style={{backgroundColor: '#FFFFFF', borderTop: '6px solid #B46595'}}>
          <div className="text-center mb-8">
            <h1 className="text-4xl font-light mb-2" style={{color: '#4C042D', fontStyle: 'italic'}}>
              Registrarse
            </h1>
            <div className="h-1 w-20 mx-auto" style={{backgroundColor: '#B46595'}}></div>
          </div>

          {error && (
            <div className="mb-4 p-3 rounded-lg" style={{backgroundColor: '#FFE5E5', color: '#C41E3A', border: '1px solid #C41E3A'}}>
              {error}
            </div>
          )}

          <form onSubmit={handleSubmit} className="space-y-4">
            <div>
              <label className="block text-sm font-medium mb-2" style={{color: '#4C042D'}}>
                Email
              </label>
              <input
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                required
                className="w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2"
                style={{borderColor: '#B46595', color: '#4C042D'}}
              />
            </div>

            <div>
              <label className="block text-sm font-medium mb-2" style={{color: '#4C042D'}}>
                Nombre de usuario
              </label>
              <input
                type="text"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
                required
                className="w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2"
                style={{borderColor: '#B46595', color: '#4C042D'}}
              />
            </div>

            <div>
              <label className="block text-sm font-medium mb-2" style={{color: '#4C042D'}}>
                Contraseña
              </label>
              <input
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                required
                className="w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2"
                style={{borderColor: '#B46595', color: '#4C042D'}}
              />
            </div>

            <div>
              <label className="block text-sm font-medium mb-2" style={{color: '#4C042D'}}>
                Confirmar contraseña
              </label>
              <input
                type="password"
                value={confirmPassword}
                onChange={(e) => setConfirmPassword(e.target.value)}
                required
                className="w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2"
                style={{borderColor: '#B46595', color: '#4C042D'}}
              />
            </div>

            <button
              type="submit"
              disabled={loading}
              className="w-full py-2 rounded-lg font-medium transition-all duration-300 hover:shadow-lg"
              style={{
                backgroundColor: '#B46595',
                color: '#FFFFFF',
                opacity: loading ? 0.7 : 1,
                cursor: loading ? 'not-allowed' : 'pointer'
              }}
            >
              {loading ? 'Cargando...' : 'Registrarse'}
            </button>
          </form>

          <p className="text-center mt-6" style={{color: '#4C042D'}}>
            ¿Ya tienes cuenta?{' '}
            <button
              onClick={onGoToLogin}
              className="font-medium hover:underline"
              style={{color: '#B46595'}}
            >
              Inicia sesión aquí
            </button>
          </p>
        </div>
      </div>
    </div>
  );
}

export default Register;
