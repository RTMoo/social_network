import { useLocation } from 'react-router-dom';
import Sidebar from './Sidebar';

export default function MainLayout({ children }) {
  const location = useLocation();

  // Страница сообщений
  const isMessagesPage = location.pathname.startsWith('/messages');

  return (
    <div className="flex bg-gray-50 min-h-screen">
      {/* Сайдбар показываем только если мы НЕ на странице сообщений */}
      {!isMessagesPage && (
        <Sidebar />
      )}

      <main
        className={`flex-1 ${!isMessagesPage ? 'lg:ml-64 md:ml-16' : ''}`}
      >
        {children}
      </main>
    </div>
  );
}
