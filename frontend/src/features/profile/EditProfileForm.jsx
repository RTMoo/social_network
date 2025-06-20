import { useForm } from 'react-hook-form';
import { yupResolver } from '@hookform/resolvers/yup';
import * as yup from 'yup';
import { useState } from 'react';
import { profilesApi } from '../../api';

// Список стран (ISO 3166-1 alpha-2 + название)
const COUNTRIES = [
    { code: 'null', name: 'Не указано' },
    { code: 'RU', name: 'Россия' },
    { code: 'US', name: 'США' },
    { code: 'DE', name: 'Германия' },
    { code: 'FR', name: 'Франция' },
    { code: 'GB', name: 'Великобритания' },
    { code: 'CN', name: 'Китай' },
    { code: 'JP', name: 'Япония' },
    { code: 'IT', name: 'Италия' },
    { code: 'ES', name: 'Испания' },
    { code: 'UA', name: 'Украина' },
    { code: 'BY', name: 'Беларусь' },
    { code: 'KZ', name: 'Казахстан' },
    { code: 'TR', name: 'Турция' },
    { code: 'PL', name: 'Польша' },
    // ... можно добавить остальные страны по необходимости
];

const schema = yup.object().shape({
    first_name: yup.string().max(32, 'Максимум 32 символа'),
    last_name: yup.string().max(32, 'Максимум 32 символа'),
    bio: yup.string().max(512, 'Максимум 512 символов'),
    country: yup
    .string()
    .nullable()
    .test('is-null-or-length-2', 'Выберите страну', value => {
      return value === 'null' || value.length === 2;
    }),
    birth_date: yup.date().nullable().typeError('Введите корректную дату'),
});

export default function EditProfileForm({ initial, onSuccess }) {
    const [error, setError] = useState('');
    const [success, setSuccess] = useState('');
    const { register, handleSubmit, formState: { errors, isSubmitting }, reset } = useForm({
        resolver: yupResolver(schema),
        defaultValues: initial,
    });

    const onSubmit = async (data) => {
        setError('');
        setSuccess('');
        // Преобразуем 'null' в null для country и форматируем дату
        const sendData = {
            ...data,
            country: data.country === 'null' ? null : data.country,
            birth_date: data.birth_date ? new Date(data.birth_date).toISOString().split('T')[0] : null,
        };
        try {
            await profilesApi.updateProfile(sendData);
            setSuccess('Профиль обновлён!');
            if (onSuccess) onSuccess();
            reset(sendData);
        } catch (e) {
            console.log(e)
            setError('Ошибка при обновлении профиля');
        }
    };

    return (
        <form onSubmit={handleSubmit(onSubmit)} className="bg-white p-6 rounded shadow mt-6">
            <h3 className="text-xl font-bold mb-4">Редактировать профиль</h3>
            {error && <div className="mb-2 text-red-500">{error}</div>}
            {success && <div className="mb-2 text-green-600">{success}</div>}
            <div className="mb-4">
                <label className="block mb-1">Имя</label>
                <input type="text" {...register('first_name')} className="w-full border px-3 py-2 rounded" />
                {errors.first_name && <p className="text-red-500 text-sm mt-1">{errors.first_name.message}</p>}
            </div>
            <div className="mb-4">
                <label className="block mb-1">Фамилия</label>
                <input type="text" {...register('last_name')} className="w-full border px-3 py-2 rounded" />
                {errors.last_name && <p className="text-red-500 text-sm mt-1">{errors.last_name.message}</p>}
            </div>
            <div className="mb-4">
                <label className="block mb-1">О себе</label>
                <textarea 
                    {...register('bio')} 
                    className="w-full border px-3 py-2 rounded resize-none" 
                    rows="3"
                    placeholder="Расскажите о себе..."
                />
                {errors.bio && <p className="text-red-500 text-sm mt-1">{errors.bio.message}</p>}
            </div>
            <div className="mb-4">
                <label className="block mb-1">Страна</label>
                <select {...register('country')} className="w-full border px-3 py-2 rounded">
                    {COUNTRIES.map(c => (
                        <option key={c.code} value={c.code}>{c.name}</option>
                    ))}
                </select>
                {errors.country && <p className="text-red-500 text-sm mt-1">{errors.country.message}</p>}
            </div>
            <div className="mb-6">
                <label className="block mb-1">Дата рождения</label>
                <input type="date" {...register('birth_date')} className="w-full border px-3 py-2 rounded" />
                {errors.birth_date && <p className="text-red-500 text-sm mt-1">{errors.birth_date.message}</p>}
            </div>
            <button type="submit" disabled={isSubmitting} className="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600">Сохранить</button>
        </form>
    );
} 