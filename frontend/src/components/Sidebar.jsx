import { useContext, useState, useEffect, useRef } from 'react';
import { NavLink, useNavigate } from 'react-router-dom';
import { AuthContext } from '../context/AuthContext';
import { getNotifications } from '../api';
import { HiHome, HiSearch, HiChat, HiBell, HiPlus, HiUser, HiUsers, HiLogout } from 'react-icons/hi';

const HomeIcon = ({ className = '', size = 24 }) => <HiHome className={`text-black ${className}`} size={size} />;
const SearchIcon = ({ className = '', size = 24 }) => <HiSearch className={`text-black ${className}`} size={size} />;
const MessagesIcon = ({ className = '', size = 24 }) => <HiChat className={`text-black ${className}`} size={size} />;
const NotificationsIcon = ({ className = '', size = 24 }) => <HiBell className={`text-black ${className}`} size={size} />;
const CreateIcon = ({ className = '', size = 24 }) => <HiPlus className={`text-black ${className}`} size={size} />;
const ProfileIcon = ({ className = '', size = 24 }) => <HiUser className={`text-black ${className}`} size={size} />;
const FriendsIcon = ({ className = '', size = 24 }) => <HiUsers className={`text-black ${className}`} size={size} />;
const LogoutIcon = ({ className = '', size = 24 }) => <HiLogout className={`text-red-600 ${className}`} size={size} />

export default function Sidebar() {
  const { user, logout } = useContext(AuthContext);
  const navigate = useNavigate();
  const [unreadCount, setUnreadCount] = useState(0);
  const [showMore, setShowMore] = useState(false);
  const dropdownRef = useRef(null);

  const navLinkClasses = ({ isActive }) =>
    `flex items-center gap-4 p-3 rounded-lg transition-colors duration-200 ${isActive ? 'bg-gray-200 font-bold' : 'hover:bg-gray-100'
    }`;

  const mobileNavLinkClasses = ({ isActive }) =>
    `flex flex-col items-center gap-1 p-2 rounded-lg transition-colors duration-200 ${isActive ? 'text-blue-600' : 'text-gray-600'
    }`;

  const handleLogout = async () => {
    await logout();
    navigate('/login');
  };

  useEffect(() => {
    const loadUnreadCount = async () => {
      if (user) {
        try {
          const response = await getNotifications(false);
          setUnreadCount(response.data.length);
        } catch (error) {
          console.error('Ошибка загрузки количества уведомлений:', error);
        }
      }
    };
    loadUnreadCount();
  }, [user]);

  // Закрытие dropdown при клике вне
  useEffect(() => {
    const handleClickOutside = (e) => {
      if (dropdownRef.current && !dropdownRef.current.contains(e.target)) {
        setShowMore(false);
      }
    };
    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, []);

  return (
    <>
      {/* Десктоп */}
      <aside className="hidden lg:flex w-64 flex-shrink-0 border-r border-gray-200 bg-white h-screen fixed top-0 flex-col p-4">
        <div className="text-2xl font-bold mb-8">Romagram</div>
        <nav className="flex flex-col gap-2">
          <NavLink to="/" className={navLinkClasses}><HomeIcon size={30} />Главная</NavLink>
          <NavLink to="/search" className={navLinkClasses}><SearchIcon size={30} />Поиск</NavLink>
          <NavLink to="/messages" className={navLinkClasses}><MessagesIcon size={30} />Сообщения</NavLink>
          <NavLink to="/notifications" className={navLinkClasses}>
            <div className="flex items-center gap-4 relative">
              <NotificationsIcon size={30} />
              <span>Уведомления</span>
              {unreadCount > 0 && <span className="absolute -top-1 -right-1 bg-red-500 text-white text-xs rounded-full h-5 w-5 flex items-center justify-center">{unreadCount > 99 ? '99+' : unreadCount}</span>}
            </div>
          </NavLink>
          <NavLink to="/create" className={navLinkClasses}><CreateIcon size={30} />Создать</NavLink>
          {user && <NavLink to={`/profile/${user.username}`} className={navLinkClasses}><ProfileIcon size={30} />Профиль</NavLink>}
          {user && <NavLink to="/friends" className={navLinkClasses}><FriendsIcon size={30} />Друзья</NavLink>}
        </nav>
        <div className="mt-auto">
          <button onClick={handleLogout} className="w-full flex cursor-pointer items-center gap-3 p-3 rounded-lg text-red-600 bg-red-50 hover:bg-red-100 font-semibold transition-colors duration-200"><LogoutIcon size={30} />Выйти</button>
        </div>
      </aside>

      {/* Планшет */}
      <aside className="hidden md:flex lg:hidden w-16 flex-shrink-0 border-r border-gray-200 bg-white h-screen fixed top-0 flex-col p-2">
        <div className="text-xl font-bold mb-8 text-center">RM</div>
        <nav className="flex flex-col gap-2">
          <NavLink to="/" className={navLinkClasses}><HomeIcon size={27} /></NavLink>
          <NavLink to="/search" className={navLinkClasses}><SearchIcon size={27} /></NavLink>
          <NavLink to="/messages" className={navLinkClasses}><MessagesIcon size={27} /></NavLink>
          <NavLink to="/notifications" className={navLinkClasses}>
            <div className="relative">
              <NotificationsIcon size={27} />
              {unreadCount > 0 && <span className="absolute -top-1 -right-1 bg-red-500 text-white text-xs rounded-full h-4 w-4 flex items-center justify-center">{unreadCount > 9 ? '9+' : unreadCount}</span>}
            </div>
          </NavLink>
          <NavLink to="/create" className={navLinkClasses}><CreateIcon size={27} /></NavLink>
          {user && <NavLink to={`/profile/${user.username}`} className={navLinkClasses}><ProfileIcon size={27} /></NavLink>}
          {user && <NavLink to="/friends" className={navLinkClasses}><FriendsIcon size={27} /></NavLink>}
        </nav>
        <div className="mt-auto">
          <button onClick={handleLogout} className="w-full cursor-pointer flex items-center justify-center p-3 rounded-lg text-red-600 bg-red-50 hover:bg-red-100 transition-colors duration-200" title="Выйти"><LogoutIcon size={27} /></button>
        </div>
      </aside>

      {/* Мобильный нижний навбар */}
      <nav className="md:hidden fixed bottom-0 left-0 right-0 bg-white border-t border-gray-200 px-1 py-1 z-50">
        <div className="flex justify-around items-center">
          <NavLink to="/" className={mobileNavLinkClasses}><HomeIcon /><span className="text-[10px]">Главная</span></NavLink>
          <NavLink to="/search" className={mobileNavLinkClasses}><SearchIcon /><span className="text-[10px]">Поиск</span></NavLink>
          {user && <NavLink to={`/profile/${user.username}`} className={mobileNavLinkClasses} onClick={() => setShowMore(false)}><ProfileIcon />Профиль</NavLink>}
          <NavLink to="/create" className={mobileNavLinkClasses}><CreateIcon /><span className="text-[10px]">Создать</span></NavLink>

          {/* Dropdown "Ещё" */}
          <div className="relative" ref={dropdownRef}>
            <button onClick={() => setShowMore(!showMore)} className="flex flex-col items-center gap-0.5 p-1.5">
              <span className="text-lg font-bold">⋯</span>
              <span className="text-[10px]">Ещё</span>
            </button>
            {showMore && (
              <div className="absolute bottom-12 left-1/2 transform -translate-x-1/2 bg-white border border-gray-200 shadow-lg rounded-lg flex flex-col w-28">
                <NavLink to="/notifications" className={mobileNavLinkClasses} onClick={() => setShowMore(false)}>
                  <div className="relative">
                    <NotificationsIcon />
                    {unreadCount > 0 && <span className="absolute -top-1 -right-1 bg-red-500 text-white text-[10px] rounded-full h-3 w-3 flex items-center justify-center">{unreadCount > 9 ? '9+' : unreadCount}</span>}
                  </div>
                  <span className="text-[10px]">Уведомления</span>
                </NavLink>
                {user && <NavLink to="/friends" className={mobileNavLinkClasses} onClick={() => setShowMore(false)}><FriendsIcon />Друзья</NavLink>}
                {user && <NavLink to="/messages" className={mobileNavLinkClasses} onClick={() => setShowMore(false)}><MessagesIcon />Сообщения</NavLink>}
                <button onClick={handleLogout} className="w-full flex items-center justify-center p-1.5 rounded-lg text-red-600 hover:bg-red-50"><LogoutIcon />Выйти</button>
              </div>
            )}
          </div>
        </div>
      </nav>
    </>
  );
}
