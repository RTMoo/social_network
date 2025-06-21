import { BrowserRouter as Router, Routes, Route, useLocation, useNavigate } from 'react-router-dom';
import { AuthProvider, AuthContext } from './context/AuthContext';
import { useContext, useEffect } from 'react';
import Home from './pages/Home';
import Login from './pages/Login';
import Register from './pages/Register';
import ConfirmCode from './pages/ConfirmCode';
import Profile from './pages/Profile';
import EditProfilePage from './pages/EditProfilePage';
import CreatePost from './pages/CreatePost';
import MainLayout from './components/MainLayout';

function App() {
  const { user, loading } = useContext(AuthContext);
  const location = useLocation();
  const navigate = useNavigate();
  const noLayoutRoutes = ['/login', '/register', '/confirm-code'];
  const showLayout = user && !noLayoutRoutes.includes(location.pathname);

  // Глобальный редирект после логина
  useEffect(() => {
    if (user && noLayoutRoutes.includes(location.pathname)) {
      navigate('/');
    }
  }, [user, location.pathname, navigate]);

  if (loading) {
    return <div>Загрузка...</div>;
  }

  return (
    <>
      {showLayout ? (
        <MainLayout>
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/profile/:username" element={<Profile />} />
            <Route path="/profile/:username/edit" element={<EditProfilePage />} />
            <Route path="/create" element={<CreatePost />} />
            {/* Другие маршруты внутри MainLayout */}
          </Routes>
        </MainLayout>
      ) : (
        <Routes>
          <Route path="/login" element={<Login />} />
          <Route path="/register" element={<Register />} />
          <Route path="/confirm-code" element={<ConfirmCode />} />
          {/* Если пользователь не авторизован и пытается зайти на другие страницы, можно добавить редирект на /login */}
          <Route path="*" element={user ? <Home/> : <Login/>} />
        </Routes>
      )}
    </>
  );
}

export default function AppWrapper() {
  return (
    <Router>
      <AuthProvider>
        <App />
      </AuthProvider>
    </Router>
  );
}
