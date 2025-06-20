import { useForm } from 'react-hook-form';
import { yupResolver } from '@hookform/resolvers/yup';
import * as yup from 'yup';
import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { authApi } from '../api';

const schema = yup.object().shape({
  email: yup.string().email('Введите email, который вы указали при регистрации').required('Email обязателен'),
  code: yup.string().required('Код обязателен'),
});

export default function ConfirmCode() {
  const navigate = useNavigate();
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  const { register, handleSubmit, formState: { errors, isSubmitting }, setValue, getValues } = useForm({
    resolver: yupResolver(schema),
  });

  const onSubmit = async (data) => {
    setError('');
    setSuccess('');
    try {
      await authApi.confirmCode(data);
      setSuccess('Email подтверждён! Теперь вы можете войти.');
      setTimeout(() => navigate('/login'), 1500);
    } catch (e) {
      setError('Неверный код или email.');
    }
  };

  const resendCode = async () => {
    setError('');
    setSuccess('');
    const email = getValues('email');
    if (!email) {
      setError('Введите email для повторной отправки кода.');
      return;
    }
    try {
      await authApi.confirmCode({ email });
      setSuccess('Код повторно отправлен на email.');
    } catch (e) {
      setError('Ошибка при отправке кода.');
    }
  };

  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-gray-50">
      <form onSubmit={handleSubmit(onSubmit)} className="bg-white p-8 rounded shadow w-full max-w-md">
        <h2 className="text-2xl font-bold mb-6 text-center">Подтверждение email</h2>
        {error && <div className="mb-4 text-red-500 text-center">{error}</div>}
        {success && <div className="mb-4 text-green-600 text-center">{success}</div>}
        <div className="mb-4">
          <label className="block mb-1">Email</label>
          <input type="email" {...register('email')} className="w-full border px-3 py-2 rounded" />
          {errors.email && <p className="text-red-500 text-sm mt-1">{errors.email.message}</p>}
        </div>
        <div className="mb-6">
          <label className="block mb-1">Код подтверждения</label>
          <input type="text" {...register('code')} className="w-full border px-3 py-2 rounded" />
          {errors.code && <p className="text-red-500 text-sm mt-1">{errors.code.message}</p>}
        </div>
        <button type="submit" disabled={isSubmitting} className="w-full bg-blue-500 text-white py-2 rounded hover:bg-blue-600">Подтвердить</button>
        <button type="button" onClick={resendCode} className="w-full mt-3 bg-gray-200 text-gray-700 py-2 rounded hover:bg-gray-300">Отправить код повторно</button>
      </form>
    </div>
  );
} 