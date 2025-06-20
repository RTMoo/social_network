import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Home from './pages/Home';
import Login from './pages/Login';
import Register from './pages/Register';
import ConfirmCode from './pages/ConfirmCode';
import Profile from './pages/Profile';
import { AuthProvider, AuthContext } from './context/AuthContext';
import { useContext } from 'react';

function AppRoutes() {
  const { loading } = useContext(AuthContext);
  if (loading) {
    return <div className="flex items-center justify-center min-h-screen">Загрузка...</div>;
  }
  return (
    <Routes>
      <Route path="/" element={<Home />} />
      <Route path="/login" element={<Login />} />
      <Route path="/register" element={<Register />} />
      <Route path="/confirm" element={<ConfirmCode />} />
      <Route path="/profile/:username" element={<Profile />} />
    </Routes>
  );
}

export default function App() {
  return (
    <AuthProvider>
      <Router>
        <AppRoutes />
      </Router>
    </AuthProvider>
  );
}
