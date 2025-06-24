import { useState } from 'react';

export default function CommentForm({ postId, replyToId = null, onSubmit, loading }) {
  const [text, setText] = useState('');
  const [error, setError] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!text.trim()) {
      setError('Комментарий не может быть пустым');
      return;
    }
    setError('');
    await onSubmit({
      post_id: postId,
      reply_to_id: replyToId,
      text: text.trim(),
    });
    setText('');
  };

  return (
    <form onSubmit={handleSubmit} className="flex flex-col gap-2 mt-2">
      <textarea
        className="border rounded p-2 resize-none min-h-[40px] text-sm focus:outline-none focus:ring focus:border-blue-300"
        placeholder={replyToId ? 'Ответить...' : 'Добавить комментарий...'}
        value={text}
        onChange={e => setText(e.target.value)}
        maxLength={256}
        disabled={loading}
      />
      {error && <div className="text-xs text-red-500">{error}</div>}
      <div className="flex justify-end">
        <button
          type="submit"
          className="bg-blue-500 hover:bg-blue-600 text-white text-xs font-semibold py-1 px-3 rounded disabled:opacity-50"
          disabled={loading || !text.trim()}
        >
          {replyToId ? 'Ответить' : 'Комментировать'}
        </button>
      </div>
    </form>
  );
} 