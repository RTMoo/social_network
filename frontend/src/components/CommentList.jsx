import React, { useState, useEffect } from 'react';
import { commentsApi, likesApi } from '../api';

export default function CommentList({ comments, onReply, currentUser, onDelete, onEdit, loading, level = 0 }) {
  const [replyTo, setReplyTo] = useState(null);
  const [editId, setEditId] = useState(null);
  const [editText, setEditText] = useState('');
  const [openReplies, setOpenReplies] = useState({});
  const [repliesCache, setRepliesCache] = useState({});
  const [repliesLoading, setRepliesLoading] = useState({});
  const [commentLikes, setCommentLikes] = useState({});
  const [likedByUser, setLikedByUser] = useState({});
  const [likeLoading, setLikeLoading] = useState({});

  useEffect(() => {
    const likes = {};
    const liked = {};
    comments.forEach(comment => {
      likes[comment.id] = comment.likes_count;
      liked[comment.id] = comment.is_liked_by_user;
    });
    setCommentLikes(likes);
    setLikedByUser(liked);
  }, [comments]);

  const handleEdit = (comment) => {
    setEditId(comment.id);
    setEditText(comment.text);
  };

  const handleEditSubmit = (e, comment) => {
    e.preventDefault();
    if (editText.trim()) {
      onEdit(comment.id, editText.trim());
      setEditId(null);
      setEditText('');
    }
  };

  const toggleReplies = async (id) => {
    // Если уже открыто — просто скрываем
    if (openReplies[id]) {
      setOpenReplies(prev => ({ ...prev, [id]: false }));
      return;
    }
    // Если уже есть в кэше — просто открываем
    if (repliesCache[id]) {
      setOpenReplies(prev => ({ ...prev, [id]: true }));
      return;
    }
    // Иначе делаем запрос
    setRepliesLoading(prev => ({ ...prev, [id]: true }));
    try {
      const res = await commentsApi.getCommentReplies(id);
      setRepliesCache(prev => ({ ...prev, [id]: res.data }));
      setOpenReplies(prev => ({ ...prev, [id]: true }));
    } catch {
      setRepliesCache(prev => ({ ...prev, [id]: [] }));
      setOpenReplies(prev => ({ ...prev, [id]: true }));
    } finally {
      setRepliesLoading(prev => ({ ...prev, [id]: false }));
    }
  };

  const handleLikeComment = async (commentId) => {
    if (likeLoading[commentId]) return;
    setLikeLoading(prev => ({ ...prev, [commentId]: true }));
    try {
      await likesApi.likeComment(commentId);
      setLikedByUser(prev => ({ ...prev, [commentId]: !prev[commentId] }));
      setCommentLikes(prev => ({
        ...prev,
        [commentId]: prev[commentId] + (likedByUser[commentId] ? -1 : 1)
      }));
    } catch {}
    setLikeLoading(prev => ({ ...prev, [commentId]: false }));
  };

  return (
    <div className="flex flex-col gap-4">
      {comments.map(comment => {
        const hasReplies = (comment.replies && comment.replies.length > 0) || repliesCache[comment.id]?.length > 0;
        const isOpen = openReplies[comment.id];
        const isLoading = repliesLoading[comment.id];
        const replies = repliesCache[comment.id] !== undefined ? repliesCache[comment.id] : comment.replies || [];
        return (
          <div key={comment.id} className="border-b pb-2">
            <div className="flex items-center gap-2 mb-1">
              <span className="font-semibold text-sm">{comment.author}</span>
              <span className="text-xs text-gray-400">{new Date(comment.created_at).toLocaleString('ru-RU')}</span>

            </div>
            {editId === comment.id ? (
              <form onSubmit={e => handleEditSubmit(e, comment)} className="flex gap-2 items-center">
                <input
                  className="border rounded p-1 text-sm flex-1"
                  value={editText}
                  onChange={e => setEditText(e.target.value)}
                  maxLength={256}
                  disabled={loading}
                />
                <button type="submit" className="text-blue-500 text-xs font-semibold" disabled={loading}>Сохранить</button>
                <button type="button" className="text-gray-400 text-xs" onClick={() => setEditId(null)}>Отмена</button>
              </form>
            ) : (
              <div className="text-sm whitespace-pre-line mb-1 break-words break-all">{comment.text}</div>
            )}
            <div className="flex gap-2 text-xs text-gray-500">
              <button type="button" onClick={() => setReplyTo(comment.id)} className="hover:underline">Ответить</button>
              {currentUser === comment.author && (
                <>
                  <button type="button" onClick={() => handleEdit(comment)} className="hover:underline">Редактировать</button>
                  <button type="button" onClick={() => onDelete(comment.id)} className="hover:underline text-red-400">Удалить</button>
                </>
              )}
              {/* Кнопка 'Ответы' только для первого уровня */}
              {level === 0 && (
                <button
                  type="button"
                  className="hover:underline text-blue-500"
                  onClick={() => toggleReplies(comment.id)}
                  disabled={isLoading}
                >
                  {isOpen ? 'Скрыть ответы' : `Ответы${hasReplies ? ` (${replies.length})` : ''}`}
                </button>
              )}
              {/* Кнопка лайка */}
              <button
                type="button"
                className="ml-2 focus:outline-none"
                onClick={() => handleLikeComment(comment.id)}
                disabled={likeLoading[comment.id]}
                title={likedByUser[comment.id] ? "Убрать лайк" : "Поставить лайк"}
              >
                <svg
                  xmlns="http://www.w3.org/2000/svg"
                  viewBox="0 0 24 24"
                  fill="currentColor"
                  className={`w-5 h-5 hover:scale-110 transition-transform inline ${likedByUser[comment.id] ? 'text-red-400' : 'text-gray-400'}`}
                >
                  <path d="M12 21.35l-1.45-1.32C5.4 15.36 2 12.28 2 8.5 2 5.42 4.42 3 7.5 3c1.74 0 3.41 0.81 4.5 2.09C13.09 3.81 14.76 3 16.5 3 19.58 3 22 5.42 22 8.5c0 3.78-3.4 6.86-8.55 11.54L12 21.35z" />
                </svg>
                <span className="ml-1">{commentLikes[comment.id] ?? 0}</span>
              </button>
            </div>
            {/* Ответы */}
            {isOpen && (
              <div className="ml-4 mt-2 border-l pl-2">
                {isLoading ? (
                  <div className="text-xs text-gray-400">Загрузка...</div>
                ) : replies.length > 0 ? (
                  <CommentList
                    comments={replies}
                    onReply={onReply}
                    currentUser={currentUser}
                    onDelete={onDelete}
                    onEdit={onEdit}
                    loading={loading}
                    level={level + 1}
                  />
                ) : (
                  <div className="text-xs text-gray-400">Нет ответов</div>
                )}
              </div>
            )}
            {/* Форма ответа */}
            {replyTo === comment.id && (
              <div className="ml-4 mt-2">
                {onReply && onReply(comment)}
                <button className="text-xs text-gray-400 mt-1" onClick={() => setReplyTo(null)}>Отмена</button>
              </div>
            )}
          </div>
        );
      })}
    </div>
  );
} 