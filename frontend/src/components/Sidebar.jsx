import { useContext, useState } from 'react';
import { NavLink, useNavigate } from 'react-router-dom';
import { AuthContext } from '../context/AuthContext';

// Иконки (простые SVG для примера)
const HomeIcon = () => <span>🏠</span>;
const SearchIcon = () => <span>🔍</span>;
const MessagesIcon = () => <span>💬</span>;
const NotificationsIcon = () => <span>❤️</span>;
const CreateIcon = () => <span>➕</span>;
const ProfileIcon = () => <span>👤</span>;
const FriendsIcon = () => <span>👥</span>;

export default function Sidebar() {
  const { user, logout } = useContext(AuthContext);
  const navigate = useNavigate();

  const navLinkClasses = ({ isActive }) =>
    `flex items-center gap-4 p-3 rounded-lg transition-colors duration-200 ${
      isActive ? 'bg-gray-200 font-bold' : 'hover:bg-gray-100'
    }`;

  const mobileNavLinkClasses = ({ isActive }) =>
    `flex flex-col items-center gap-1 p-2 rounded-lg transition-colors duration-200 ${
      isActive ? 'text-blue-600' : 'text-gray-600'
    }`;

  const handleLogout = async () => {
    await logout();
    navigate('/login');
  };

  return (
    <>
      {/* Десктопный навбар (lg и выше) */}
      <aside className="hidden lg:flex w-64 flex-shrink-0 border-r border-gray-200 bg-white h-screen sticky top-0 flex-col p-4">
        <div className="text-2xl font-bold mb-8">SocialNet</div>
        <nav className="flex flex-col gap-2">
          <NavLink to="/" className={navLinkClasses}>
            <HomeIcon />
            Главная
          </NavLink>
          <NavLink to="/search" className={navLinkClasses}>
            <SearchIcon />
            Поиск
          </NavLink>
          <NavLink to="/messages" className={navLinkClasses}>
            <MessagesIcon />
            Сообщения
          </NavLink>
          <NavLink to="/notifications" className={navLinkClasses}>
            <NotificationsIcon />
            Уведомления
          </NavLink>
          <NavLink to="/create" className={navLinkClasses}>
            <CreateIcon />
            Создать
          </NavLink>
          {user && (
            <NavLink to={`/profile/${user.username}`} className={navLinkClasses}>
              <ProfileIcon />
              Профиль
            </NavLink>
          )}
          {user && (
            <NavLink to="/friends" className={navLinkClasses}>
              <FriendsIcon />
              Друзья
            </NavLink>
          )}
        </nav>
        <div className="mt-auto">
          <button
            onClick={handleLogout}
            className="w-full flex items-center gap-3 p-3 rounded-lg text-red-600 bg-red-50 hover:bg-red-100 font-semibold transition-colors duration-200"
          >
            Выйти
          </button>
        </div>
      </aside>

      {/* Планшетный навбар (md-lg) - только иконки */}
      <aside className="hidden md:flex lg:hidden w-16 flex-shrink-0 border-r border-gray-200 bg-white h-screen sticky top-0 flex-col p-2">
        <div className="text-xl font-bold mb-8 text-center">SN</div>
        <nav className="flex flex-col gap-2">
          <NavLink to="/" className={navLinkClasses}>
            <HomeIcon />
          </NavLink>
          <NavLink to="/search" className={navLinkClasses}>
            <SearchIcon />
          </NavLink>
          <NavLink to="/messages" className={navLinkClasses}>
            <MessagesIcon />
          </NavLink>
          <NavLink to="/notifications" className={navLinkClasses}>
            <NotificationsIcon />
          </NavLink>
          <NavLink to="/create" className={navLinkClasses}>
            <CreateIcon />
          </NavLink>
          {user && (
            <NavLink to={`/profile/${user.username}`} className={navLinkClasses}>
              <ProfileIcon />
            </NavLink>
          )}
        </nav>
        <div className="mt-auto">
          <button
            onClick={handleLogout}
            className="w-full flex items-center justify-center p-3 rounded-lg text-red-600 bg-red-50 hover:bg-red-100 transition-colors duration-200"
            title="Выйти"
          >
            🚪
          </button>
        </div>
      </aside>

      {/* Мобильный нижний навбар (до md) */}
      <nav className="md:hidden fixed bottom-0 left-0 right-0 bg-white border-t border-gray-200 px-4 py-2 z-50">
        <div className="flex justify-around items-center">
          <NavLink to="/" className={mobileNavLinkClasses}>
            <HomeIcon />
            <span className="text-xs">Главная</span>
          </NavLink>
          <NavLink to="/search" className={mobileNavLinkClasses}>
            <SearchIcon />
            <span className="text-xs">Поиск</span>
          </NavLink>
          <NavLink to="/create" className={mobileNavLinkClasses}>
            <CreateIcon />
            <span className="text-xs">Создать</span>
          </NavLink>
          <NavLink to="/notifications" className={mobileNavLinkClasses}>
            <NotificationsIcon />
            <span className="text-xs">Уведомления</span>
          </NavLink>
          {user && (
            <NavLink to={`/profile/${user.username}`} className={mobileNavLinkClasses}>
              <ProfileIcon />
              <span className="text-xs">Профиль</span>
            </NavLink>
          )}
        </div>
      </nav>
    </>
  );
} 