import { useEffect, useState, useContext } from 'react';
import { AuthContext } from '../context/AuthContext';
import { commentsApi } from '../api';
import CommentList from './CommentList';
import CommentForm from './CommentForm';

export default function PostModal({ post, isOpen, onClose, backendUrl }) {
  const { user } = useContext(AuthContext);
  const [comments, setComments] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [replyTo, setReplyTo] = useState(null);

  useEffect(() => {
    if (isOpen && post?.id) {
      fetchComments();
    }
    // eslint-disable-next-line
  }, [isOpen, post?.id]);

  const fetchComments = async () => {
    setLoading(true);
    setError('');
    try {
      const res = await commentsApi.getPostComments(post.id);
      setComments(buildCommentTree(res.data));
    } catch (e) {
      setError('Ошибка загрузки комментариев');
    } finally {
      setLoading(false);
    }
  };

  function buildCommentTree(list) {
    const map = {};
    const roots = [];
    list.forEach(c => (map[c.id] = { ...c, replies: [] }));
    list.forEach(c => {
      if (c.reply_to_id) {
        map[c.reply_to_id]?.replies.push(map[c.id]);
      } else {
        roots.push(map[c.id]);
      }
    });
    return roots;
  }

  const handleAddComment = async (data) => {
    setLoading(true);
    try {
      await commentsApi.createComment(data);
      await fetchComments();
      setReplyTo(null);
    } catch (e) {
      setError('Ошибка при добавлении комментария');
    } finally {
      setLoading(false);
    }
  };

  const handleDelete = async (commentId) => {
    setLoading(true);
    try {
      await commentsApi.deleteComment(commentId);
      await fetchComments();
    } catch (e) {
      setError('Ошибка при удалении комментария');
    } finally {
      setLoading(false);
    }
  };

  const handleEdit = async (commentId, text) => {
    setLoading(true);
    try {
      await commentsApi.updateComment(commentId, { text });
      await fetchComments();
    } catch (e) {
      setError('Ошибка при редактировании комментария');
    } finally {
      setLoading(false);
    }
  };

  const handleReply = (comment) => (
    <CommentForm
      postId={post.id}
      replyToId={comment.id}
      onSubmit={handleAddComment}
      loading={loading}
    />
  );

  const handleBackdropClick = (e) => {
    if (e.target === e.currentTarget) {
      onClose();
    }
  };

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

  if (!isOpen || !post) return null;

  return (
    <div 
      className="fixed inset-0 bg-[#00000099] flex items-center justify-center z-50 p-4"
      onClick={handleBackdropClick}
    >
      <div className="bg-white rounded-lg w-full max-w-[1440px] max-h-[90vh] flex flex-col md:flex-row overflow-hidden shadow-2xl">
        {/* Левая часть: изображение */}
        <div className="w-full md:w-[1080px] h-[300px] md:h-[720px] flex items-center justify-center bg-black">
          {post.image ? (
            <img
              src={`${backendUrl}${post.image}`}
              alt={post.title || 'Post image'}
              className="object-contain w-full h-full max-w-[1080px] max-h-[720px] bg-black"
            />
          ) : (
            <div className="w-full h-full flex items-center justify-center text-white text-4xl">Нет изображения</div>
          )}
        </div>
        {/* Правая часть: комментарии и инфо */}
        <div className="w-full md:w-[360px] h-[420px] md:h-[720px] flex flex-col bg-white border-l">
          {/* Заголовок и кнопка закрытия */}
          <div className="flex justify-between items-center p-4 border-b">
            <h3 className="text-lg font-semibold">Публикация</h3>
            <button
              onClick={onClose}
              className="text-gray-500 hover:text-gray-700 text-2xl font-bold"
            >
              ×
            </button>
          </div>
          {/* Информация о посте */}
          <div className="p-4 pb-0 border-b">
            {post.title && (
              <h2 className="text-xl font-bold mb-2">{post.title}</h2>
            )}
            {post.content && (
              <p className="text-gray-700 whitespace-pre-line mb-2">{post.content}</p>
            )}
            <div className="text-sm text-gray-500 border-t pt-2">
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
          {/* Комментарии */}
          <div className="flex-1 px-4 py-2 overflow-y-auto min-h-[120px] max-h-[320px] md:max-h-[420px]">
            <h4 className="font-semibold mb-2">Комментарии</h4>
            {error && <div className="text-xs text-red-500 mb-2">{error}</div>}
            {loading ? (
              <div className="text-gray-400 text-sm">Загрузка...</div>
            ) : (
              <>
                <CommentList
                  comments={comments}
                  onReply={handleReply}
                  currentUser={user?.username}
                  onDelete={handleDelete}
                  onEdit={handleEdit}
                  loading={loading}
                />
              </>
            )}
          </div>
          {/* Форма добавления комментария */}
          <div className="px-4 pb-4 border-t">
            <CommentForm
              postId={post.id}
              onSubmit={handleAddComment}
              loading={loading}
            />
          </div>
        </div>
      </div>
    </div>
  );
} 