import { useForm } from 'react-hook-form';
import { yupResolver } from '@hookform/resolvers/yup';
import * as yup from 'yup';
import { useState, useRef } from 'react';
import { postsApi } from '../../api';

const schema = yup.object().shape({
  title: yup.string().max(128, 'Максимум 128 символов'),
  content: yup.string().max(2000, 'Максимум 2000 символов'),
  image: yup.mixed().required('Изображение обязательно'),
});

export default function CreatePostForm({ onSuccess }) {
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  const [imagePreview, setImagePreview] = useState(null);
  const imageInputRef = useRef(null);
  
  const { register, handleSubmit, formState: { errors, isSubmitting }, reset, setValue, watch } = useForm({
    resolver: yupResolver(schema),
  });

  const handleImageChange = (e) => {
    const file = e.target.files[0];
    if (file) {
      setValue('image', file);
      
      // Создаем превью изображения
      const reader = new FileReader();
      reader.onload = (e) => {
        setImagePreview(e.target.result);
      };
      reader.readAsDataURL(file);
    }
  };

  const onSubmit = async (data) => {
    setError('');
    setSuccess('');

    const formData = new FormData();
    formData.append('image', data.image);
    if (data.title) formData.append('title', data.title);
    if (data.content) formData.append('content', data.content);

    try {
      await postsApi.createPost(formData);
      setSuccess('Пост создан!');
      reset();
      setImagePreview(null);
      if (onSuccess) onSuccess();
    } catch (e) {
      console.error(e);
      setError('Ошибка при создании поста');
    }
  };

  return (
    <form onSubmit={handleSubmit(onSubmit)} className="bg-white p-6 rounded-lg shadow-md">
      <h3 className="text-xl font-bold mb-4">Создать пост</h3>
      
      {error && <div className="mb-4 text-red-500">{error}</div>}
      {success && <div className="mb-4 text-green-600">{success}</div>}

      {/* Загрузка изображения */}
      <div className="mb-4">
        <label className="block mb-2 font-medium">Изображение *</label>
        <div className="border-2 border-dashed border-gray-300 rounded-lg p-4 text-center">
          {imagePreview ? (
            <div className="space-y-2">
              <img src={imagePreview} alt="Preview" className="max-w-full h-64 object-cover mx-auto rounded" />
              <button
                type="button"
                onClick={() => {
                  setImagePreview(null);
                  setValue('image', null);
                  imageInputRef.current.value = '';
                }}
                className="text-red-500 hover:text-red-700"
              >
                Удалить изображение
              </button>
            </div>
          ) : (
            <div>
              <p className="text-gray-500 mb-2">Перетащите изображение сюда или нажмите для выбора</p>
              <button
                type="button"
                onClick={() => imageInputRef.current.click()}
                className="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600"
              >
                Выбрать файл
              </button>
            </div>
          )}
          <input
            type="file"
            ref={imageInputRef}
            onChange={handleImageChange}
            accept="image/*"
            className="hidden"
          />
        </div>
        {errors.image && <p className="text-red-500 text-sm mt-1">{errors.image.message}</p>}
      </div>

      {/* Заголовок */}
      <div className="mb-4">
        <label className="block mb-1 font-medium">Заголовок (необязательно)</label>
        <input
          type="text"
          {...register('title')}
          className="w-full border border-gray-300 px-3 py-2 rounded focus:outline-none focus:ring-2 focus:ring-blue-500"
          placeholder="Введите заголовок..."
        />
        {errors.title && <p className="text-red-500 text-sm mt-1">{errors.title.message}</p>}
      </div>

      {/* Содержание */}
      <div className="mb-6">
        <label className="block mb-1 font-medium">Содержание (необязательно)</label>
        <textarea
          {...register('content')}
          rows="4"
          className="w-full border border-gray-300 px-3 py-2 rounded resize-none focus:outline-none focus:ring-2 focus:ring-blue-500"
          placeholder="Расскажите что-нибудь..."
        />
        {errors.content && <p className="text-red-500 text-sm mt-1">{errors.content.message}</p>}
      </div>

      {/* Кнопка отправки */}
      <button
        type="submit"
        disabled={isSubmitting}
        className="w-full bg-blue-500 text-white py-2 px-4 rounded hover:bg-blue-600 disabled:opacity-50 disabled:cursor-not-allowed"
      >
        {isSubmitting ? 'Создание...' : 'Создать пост'}
      </button>
    </form>
  );
} 