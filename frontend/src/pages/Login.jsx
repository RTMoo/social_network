import { useForm } from 'react-hook-form';
import { yupResolver } from '@hookform/resolvers/yup';
import * as yup from 'yup';
import { useContext, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { authApi } from '../api';
import { AuthContext } from '../context/AuthContext';

const schema = yup.object().shape({
  email: yup.string().email('Введите корректный email').required('Email обязателен'),
  password: yup.string().required('Пароль обязателен'),
});

export default function Login() {
  const navigate = useNavigate();
  const [error, setError] = useState('');
  const { register, handleSubmit, formState: { errors, isSubmitting } } = useForm({
    resolver: yupResolver(schema),
  });

  const onSubmit = async (data) => {
    setError('');
    try {
      await authApi.login(data);
      navigate(0);
    } catch (e) {
      setError('Неверный email или пароль');
    }
  };

  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-gray-50">
      <form onSubmit={handleSubmit(onSubmit)} className="bg-white p-8 rounded shadow w-full max-w-md">
        <h2 className="text-2xl font-bold mb-6 text-center">Вход</h2>
        {error && <div className="mb-4 text-red-500 text-center">{error}</div>}
        <div className="mb-4">
          <label className="block mb-1">Email</label>
          <input type="email" {...register('email')} className="w-full border px-3 py-2 rounded" />
          {errors.email && <p className="text-red-500 text-sm mt-1">{errors.email.message}</p>}
        </div>
        <div className="mb-6">
          <label className="block mb-1">Пароль</label>
          <input type="password" {...register('password')} className="w-full border px-3 py-2 rounded" />
          {errors.password && <p className="text-red-500 text-sm mt-1">{errors.password.message}</p>}
        </div>
        <button type="submit" disabled={isSubmitting} className="w-full bg-blue-500 text-white py-2 rounded hover:bg-blue-600">Войти</button>
        <div className="mt-4 text-center">
          <a href="/register" className="text-blue-500 hover:underline">Нет аккаунта? Зарегистрируйтесь</a>
        </div>
      </form>
    </div>
  );
} 