import { useNavigate } from 'react-router-dom';
import CreatePostForm from '../features/posts/CreatePostForm';

export default function CreatePost() {
  const navigate = useNavigate();

  const handleSuccess = () => {
    // Перенаправляем на главную страницу после создания поста
    navigate('/');
  };

  return (
    <div className="max-w-2xl mx-auto py-8 px-4">
      <h1 className="text-3xl font-bold mb-8 text-center">Создать новый пост</h1>
      <CreatePostForm onSuccess={handleSuccess} />
    </div>
  );
} 