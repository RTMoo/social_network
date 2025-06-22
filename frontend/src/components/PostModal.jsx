import { useEffect } from 'react';

export default function PostModal({ post, isOpen, onClose, backendUrl }) {
  useEffect(() => {
    const handleEscape = (e) => {
      if (e.key === 'Escape') {
        onClose();
      }
    };

    if (isOpen) {
      document.addEventListener('keydown', handleEscape);
      document.body.style.overflow = 'hidden';
    }

    return () => {
      document.removeEventListener('keydown', handleEscape);
      document.body.style.overflow = 'unset';
    };
  }, [isOpen, onClose]);

  const handleBackdropClick = (e) => {
    // Закрываем модальное окно только при клике на затемненную область
    if (e.target === e.currentTarget) {
      onClose();
    }
  };

  if (!isOpen || !post) return null;

  return (
    <div 
      className="fixed inset-0 bg-[#00000099] flex items-center justify-center z-50 p-4"
      onClick={handleBackdropClick}
    >
      <div className="bg-white rounded-lg max-w-2xl w-full max-h-[90vh] overflow-y-auto">
        {/* Заголовок модального окна */}
        <div className="flex justify-between items-center p-4 border-b">
          <h3 className="text-lg font-semibold">Публикация</h3>
          <button
            onClick={onClose}
            className="text-gray-500 hover:text-gray-700 text-2xl font-bold"
          >
            ×
          </button>
        </div>

        {/* Содержимое поста */}
        <div className="p-4">
          {/* Оригинальное изображение */}
          {post.image && (
            <div className="mb-4">
              <img
                src={`${backendUrl}${post.image}`}
                alt={post.title || 'Post image'}
                className="w-full h-auto rounded-lg"
              />
            </div>
          )}

          {/* Заголовок */}
          {post.title && (
            <h2 className="text-xl font-bold mb-2">{post.title}</h2>
          )}

          {/* Текст поста */}
          {post.content && (
            <p className="text-gray-700 whitespace-pre-line mb-4">{post.content}</p>
          )}

          {/* Метаинформация */}
          <div className="text-sm text-gray-500 border-t pt-4">
            <div className="flex justify-between items-center">
              <span>Автор: {post.author}</span>
              <span>Лайков: {post.likes_count || 0}</span>
            </div>
            {post.created_at && (
              <div className="mt-2">
                Опубликовано: {new Date(post.created_at).toLocaleDateString('ru-RU')}
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
} 