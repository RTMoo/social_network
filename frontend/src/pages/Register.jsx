import { useForm } from 'react-hook-form';
import { yupResolver } from '@hookform/resolvers/yup';
import * as yup from 'yup';
import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { authApi } from '../api';

const schema = yup.object().shape({
  email: yup.string().email('Введите корректный email').required('Email обязателен'),
  username: yup.string().required('Имя пользователя обязательно'),
  password: yup.string().min(6, 'Минимум 6 символов').required('Пароль обязателен'),
});

export default function Register() {
  const navigate = useNavigate();
  const [error, setError] = useState('');
  const { register, handleSubmit, formState: { errors, isSubmitting } } = useForm({
    resolver: yupResolver(schema),
  });

  const onSubmit = async (data) => {
    setError('');
    try {
      await authApi.register(data);
      navigate('/confirm');
    } catch (e) {
      setError('Ошибка регистрации. Возможно, email или username уже заняты.');
    }
  };

  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-gray-50">
      <form onSubmit={handleSubmit(onSubmit)} className="bg-white p-8 rounded shadow w-full max-w-md">
        <h2 className="text-2xl font-bold mb-6 text-center">Регистрация</h2>
        {error && <div className="mb-4 text-red-500 text-center">{error}</div>}
        <div className="mb-4">
          <label className="block mb-1">Email</label>
          <input type="email" {...register('email')} className="w-full border px-3 py-2 rounded" />
          {errors.email && <p className="text-red-500 text-sm mt-1">{errors.email.message}</p>}
        </div>
        <div className="mb-4">
          <label className="block mb-1">Имя пользователя</label>
          <input type="text" {...register('username')} className="w-full border px-3 py-2 rounded" />
          {errors.username && <p className="text-red-500 text-sm mt-1">{errors.username.message}</p>}
        </div>
        <div className="mb-6">
          <label className="block mb-1">Пароль</label>
          <input type="password" {...register('password')} className="w-full border px-3 py-2 rounded" />
          {errors.password && <p className="text-red-500 text-sm mt-1">{errors.password.message}</p>}
        </div>
        <button type="submit" disabled={isSubmitting} className="w-full bg-blue-500 text-white py-2 rounded hover:bg-blue-600">Зарегистрироваться</button>
        <div className="mt-4 text-center">
          <a href="/login" className="text-blue-500 hover:underline">Уже есть аккаунт? Войти</a>
        </div>
      </form>
    </div>
  );
} 