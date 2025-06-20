import { useContext } from 'react';
import { AuthContext } from '../context/AuthContext';
import { Link } from 'react-router-dom';

export default function Home() {
  const { user, logout } = useContext(AuthContext);

  return (
    <div className="min-h-screen bg-gray-50">
      <main className="flex flex-col items-center justify-center h-[80vh]">
        <h1 className="text-4xl font-bold mb-4">Добро пожаловать в SocialNetwork!</h1>
        <p className="text-lg text-gray-600">Общайтесь, делитесь, находите друзей.</p>
      </main>
    </div>
  );
} 