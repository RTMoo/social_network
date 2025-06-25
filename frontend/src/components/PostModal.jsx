import { useEffect, useState, useContext } from 'react';
import { AuthContext } from '../context/AuthContext';
import { commentsApi, postsApi, likesApi } from '../api';
import CommentList from './CommentList';
import CommentForm from './CommentForm';
import { useForm } from 'react-hook-form';

export default function PostModal({ post, isOpen, onClose, backendUrl, setPosts, posts }) {
  const { user } = useContext(AuthContext);
  const [comments, setComments] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [replyTo, setReplyTo] = useState(null);
  const [postLikes, setPostLikes] = useState(post?.likes_count || 0);
  const [likeLoading, setLikeLoading] = useState(false);
  const [likedByUser, setLikedByUser] = useState(!!post?.is_liked_by_user);
  const { register, handleSubmit, formState: { errors, isSubmitting }, reset, setValue } = useForm({
    defaultValues: { title: post?.title || '', content: post?.content || '' }
  });
  const [editMode, setEditMode] = useState(false);

  useEffect(() => {
    if (isOpen && post?.id) {
      fetchComments();
    }
    setPostLikes(post?.likes_count || 0);
    setLikedByUser(!!post?.is_liked_by_user);
    reset({ title: post?.title || '', content: post?.content || '' });
    // eslint-disable-next-line
  }, [isOpen, post?.id, post?.is_liked_by_user, post, reset]);

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

  const handleLikePost = async () => {
    if (!post?.id || likeLoading) return;
    setLikeLoading(true);
    try {
      await likesApi.likePost(post.id);
      setLikedByUser(prev => !prev);
      setPostLikes(prev => prev + (likedByUser ? -1 : 1));
    } catch {}
    setLikeLoading(false);
  };

  const handleDeletePost = async () => {
    if (!window.confirm('Вы уверены, что хотите удалить этот пост?')) return;
    try {
      const res = await postsApi.deletePost(post.id);
      if (res.status === 204 && setPosts) {
        setPosts(posts => posts.filter(p => p.id !== post.id));
      }
      onClose();
    } catch (e) {
      setError('Ошибка при удалении поста');
    }
  };

  const onEditPost = async (data) => {
    try {
      await postsApi.updatePost(post.id, data);
      setEditMode(false);
      Object.assign(post, data); // временно обновим локально
    } catch (e) {
      setError('Ошибка при редактировании поста');
    }
  };

  if (!isOpen || !post) return null;

  return (
    <div className="fixed inset-0 bg-[#00000099] flex items-center justify-center z-50 p-2 sm:p-4" onClick={handleBackdropClick}>
      <div className="bg-white rounded-lg w-full max-w-[1440px] max-h-[95vh] flex flex-col md:flex-row overflow-hidden shadow-2xl">
        {/* Левая часть: изображение (60% на десктопе, 100% на мобиле) */}
        <div
          className="w-full md:w-[60%] h-[220px] sm:h-[300px] md:h-[720px] flex items-center justify-center bg-black"
          style={{ minWidth: 0 }}
        >
          {post.image ? (
            <img
              src={`${backendUrl}${post.image}`}
              alt={post.title || 'Post image'}
              className="object-contain w-full h-full max-w-full max-h-full bg-black"
            />
          ) : (
            <div className="w-full h-full flex items-center justify-center text-white text-4xl">Нет изображения</div>
          )}
        </div>
        {/* Правая часть: комментарии (40% на десктопе, 100% на мобиле) */}
        <div className="w-full md:w-[40%] flex flex-col bg-white border-l" style={{ minWidth: 0 }}>
          {/* Верх: заголовок и кнопка закрытия */}
          <div className="flex justify-between items-center p-3 sm:p-4 border-b">
            <h3 className="text-lg font-semibold">Публикация</h3>
            <button
              onClick={onClose}
              className="text-gray-500 hover:text-gray-700 text-2xl font-bold"
            >
              ×
            </button>
          </div>
          {/* Комментарии */}
          <div className="flex-1 px-2 sm:px-4 py-2 overflow-y-auto min-h-[120px] max-h-[220px] sm:max-h-[320px] md:max-h-[420px]">
            <h4 className="font-semibold mb-2">Комментарии</h4>
            {error && <div className="text-xs text-red-500 mb-2">{error}</div>}
            {loading ? (
              <div className="text-gray-400 text-sm">Загрузка...</div>
            ) : (
              <CommentList
                comments={comments}
                onReply={handleReply}
                currentUser={user?.username}
                onDelete={handleDelete}
                onEdit={handleEdit}
                loading={loading}
              />
            )}
          </div>
          {/* Форма добавления комментария */}
          <div className="px-2 sm:px-4 pb-4 border-t">
            <CommentForm
              postId={post.id}
              onSubmit={handleAddComment}
              loading={loading}
            />
          </div>
          {/* Информация о посте и кнопки управления */}
          <div className="p-2 sm:p-4 border-t bg-gray-50">
            {editMode ? (
              <form onSubmit={handleSubmit(onEditPost)} className="mb-2">
                <input
                  {...register('title', { maxLength: 128 })}
                  className="block w-full mb-2 border rounded px-2 py-1"
                  placeholder="Заголовок"
                  disabled={isSubmitting}
                />
                <textarea
                  {...register('content', { maxLength: 2000 })}
                  className="block w-full mb-2 border rounded px-2 py-1"
                  placeholder="Текст"
                  rows={3}
                  disabled={isSubmitting}
                />
                <div className="flex gap-2">
                  <button type="submit" className="bg-blue-500 text-white px-4 py-1 rounded" disabled={isSubmitting}>
                    Сохранить
                  </button>
                  <button type="button" className="bg-gray-200 px-4 py-1 rounded" onClick={() => setEditMode(false)} disabled={isSubmitting}>
                    Отмена
                  </button>
                </div>
                {(errors.title || errors.content) && (
                  <div className="text-red-500 text-xs mt-1">
                    {errors.title?.message || errors.content?.message}
                  </div>
                )}
              </form>
            ) : (
              <div className="mb-2">
                {post.title && <h2 className="text-xl font-bold mb-2">{post.title}</h2>}
                {post.content && <p className="text-gray-700 whitespace-pre-line mb-2">{post.content}</p>}
              </div>
            )}
            <div className="flex flex-wrap justify-between items-center text-sm text-gray-500">
              <div>
                Автор: {post.author}
                {post.created_at && (
                  <span className="ml-4">Опубликовано: {new Date(post.created_at).toLocaleDateString('ru-RU')}</span>
                )}
              </div>
              <div className="flex items-center gap-2 mt-2 md:mt-0">
                <button
                  onClick={handleLikePost}
                  className="focus:outline-none"
                  disabled={likeLoading}
                  title={likedByUser ? 'Убрать лайк' : 'Поставить лайк'}
                >
                  <svg
                    xmlns="http://www.w3.org/2000/svg"
                    viewBox="0 0 24 24"
                    fill="currentColor"
                    className={`w-6 h-6 hover:scale-110 transition-transform ${likedByUser ? 'text-red-500' : 'text-gray-400'}`}
                  >
                    <path d="M12 21.35l-1.45-1.32C5.4 15.36 2 12.28 2 8.5 2 5.42 4.42 3 7.5 3c1.74 0 3.41 0.81 4.5 2.09C13.09 3.81 14.76 3 16.5 3 19.58 3 22 5.42 22 8.5c0 3.78-3.4 6.86-8.55 11.54L12 21.35z" />
                  </svg>
                  <span>{postLikes}</span>
                </button>
                {user?.username === post.author && !editMode && (
                  <>
                    <button
                      onClick={() => setEditMode(true)}
                      className="ml-2 px-3 py-1 bg-blue-100 text-blue-700 rounded hover:bg-blue-200"
                    >
                      ✏️ Редактировать
                    </button>
                    <button
                      onClick={handleDeletePost}
                      className="ml-2 px-3 py-1 bg-red-100 text-red-700 rounded hover:bg-red-200"
                    >
                      🗑️ Удалить
                    </button>
                  </>
                )}
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
} 