import { useContext } from 'react';
import { AuthContext } from '../context/AuthContext';
import { Link } from 'react-router-dom';

export default function Home() {
  const { user, logout } = useContext(AuthContext);

  return (
    <div className="min-h-screen bg-gray-50">
      <header className="flex items-center justify-between px-6 py-4 bg-white shadow">
        <Link to="/" className="text-2xl font-bold text-blue-600">SocialNetwork</Link>
        <nav>
          {user ? (
            <div className="flex items-center gap-4">
              <Link to={`/profile/${user.username}`} className="text-gray-700 hover:text-blue-600">Профиль</Link>
              <button onClick={logout} className="px-4 py-2 bg-red-500 text-white rounded hover:bg-red-600">Выйти</button>
            </div>
          ) : (
            <div className="flex items-center gap-4">
              <Link to="/login" className="px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600">Вход</Link>
              <Link to="/register" className="px-4 py-2 bg-gray-200 text-gray-700 rounded hover:bg-gray-300">Регистрация</Link>
            </div>
          )}
        </nav>
      </header>
      <main className="flex flex-col items-center justify-center h-[80vh]">
        <h1 className="text-4xl font-bold mb-4">Добро пожаловать в SocialNetwork!</h1>
        <p className="text-lg text-gray-600">Общайтесь, делитесь, находите друзей.</p>
      </main>
    </div>
  );
} 