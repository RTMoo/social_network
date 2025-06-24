import React, { useState } from 'react';
import { commentsApi } from '../api';

export default function CommentList({ comments, onReply, currentUser, onDelete, onEdit, loading, level = 0 }) {
  const [replyTo, setReplyTo] = useState(null);
  const [editId, setEditId] = useState(null);
  const [editText, setEditText] = useState('');
  const [openReplies, setOpenReplies] = useState({});
  const [repliesCache, setRepliesCache] = useState({});
  const [repliesLoading, setRepliesLoading] = useState({});

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
              {comment.likes_count > 0 && (
                <span className="text-xs text-gray-500 ml-2">♥ {comment.likes_count}</span>
              )}
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
              <div className="text-sm whitespace-pre-line mb-1">{comment.text}</div>
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