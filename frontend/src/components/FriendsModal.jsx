import { useEffect, useState } from 'react';
import * as friendshipsApi from '../api/endpoints/friendships';

export default function FriendsModal({ open, onClose, user }) {
  const [tab, setTab] = useState('friends');
  const [friends, setFriends] = useState([]);
  const [requests, setRequests] = useState([]);
  const [sentRequests, setSentRequests] = useState([]);
  const [loading, setLoading] = useState(false);
  const [actionLoading, setActionLoading] = useState({});
  const [error, setError] = useState('');

  useEffect(() => {
    if (open) {
      fetchFriends();
      fetchRequests();
      fetchSentRequests();
    }
  }, [open]);

  const fetchFriends = async () => {
    setLoading(true);
    setError('');
    try {
      const res = await friendshipsApi.getFriends(user.username);
      setFriends(res.data);
    } catch (e) {
      setError('Ошибка загрузки друзей');
    } finally {
      setLoading(false);
    }
  };

  const fetchRequests = async () => {
    setLoading(true);
    setError('');
    try {
      const res = await friendshipsApi.getReceivedRequests();
      setRequests(res.data);
    } catch (e) {
      setError('Ошибка загрузки запросов');
    } finally {
      setLoading(false);
    }
  };

  const fetchSentRequests = async () => {
    setLoading(true);
    setError('');
    try {
      const res = await friendshipsApi.getSentRequests();
      setSentRequests(res.data);
    } catch (e) {
      setError('Ошибка загрузки отправленных запросов');
    } finally {
      setLoading(false);
    }
  };

  const handleDeleteFriend = async (username) => {
    setActionLoading((prev) => ({ ...prev, [username]: true }));
    try {
      await friendshipsApi.deleteFriend(username);
      await fetchFriends();
    } catch (e) {
      setError('Ошибка при удалении друга');
    } finally {
      setActionLoading((prev) => ({ ...prev, [username]: false }));
    }
  };

  const handleAccept = async (username) => {
    setActionLoading((prev) => ({ ...prev, [username]: true }));
    try {
      await friendshipsApi.acceptFriendRequest(username);
      await fetchRequests();
      await fetchFriends();
    } catch (e) {
      setError('Ошибка при принятии запроса');
    } finally {
      setActionLoading((prev) => ({ ...prev, [username]: false }));
    }
  };

  const handleReject = async (username) => {
    setActionLoading((prev) => ({ ...prev, [username]: true }));
    try {
      await friendshipsApi.rejectFriendRequest(username);
      await fetchRequests();
    } catch (e) {
      setError('Ошибка при отклонении запроса');
    } finally {
      setActionLoading((prev) => ({ ...prev, [username]: false }));
    }
  };

  if (!open) return null;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black bg-opacity-40">
      <div className="bg-white rounded-lg shadow-lg w-full max-w-md p-6 relative">
        <button onClick={onClose} className="absolute top-2 right-2 text-gray-400 hover:text-gray-700 text-2xl">×</button>
        <div className="flex mb-4 border-b">
          <button
            className={`flex-1 py-2 font-bold ${tab === 'friends' ? 'border-b-2 border-blue-500 text-blue-600' : 'text-gray-500'}`}
            onClick={() => setTab('friends')}
          >
            Друзья
          </button>
          <button
            className={`flex-1 py-2 font-bold ${tab === 'requests' ? 'border-b-2 border-blue-500 text-blue-600' : 'text-gray-500'}`}
            onClick={() => setTab('requests')}
          >
            Запросы
          </button>
          <button
            className={`flex-1 py-2 font-bold ${tab === 'sent' ? 'border-b-2 border-blue-500 text-blue-600' : 'text-gray-500'}`}
            onClick={() => setTab('sent')}
          >
            Мои запросы
          </button>
        </div>
        {error && <div className="text-red-500 text-center mb-2">{error}</div>}
        {loading ? (
          <div className="text-center text-gray-500 py-8">Загрузка...</div>
        ) : tab === 'friends' ? (
          friends.length > 0 ? (
            <ul className="divide-y">
              {friends.map((f) => (
                <li key={f.username} className="flex items-center justify-between py-2">
                  <span>{f.first_name || f.username}</span>
                  <button
                    onClick={() => handleDeleteFriend(f.username)}
                    disabled={actionLoading[f.username]}
                    className="px-3 py-1 bg-red-100 text-red-700 rounded hover:bg-red-200 disabled:opacity-50"
                  >
                    {actionLoading[f.username] ? '...' : 'Удалить'}
                  </button>
                </li>
              ))}
            </ul>
          ) : (
            <div className="text-center text-gray-400 py-8">Нет друзей</div>
          )
        ) : tab === 'requests' ? (
          requests.length > 0 ? (
            <ul className="divide-y">
              {requests.map((r) => (
                <li key={r.username} className="flex items-center justify-between py-2">
                  <span>{r.first_name || r.username}</span>
                  <div className="flex gap-2">
                    <button
                      onClick={() => handleAccept(r.username)}
                      disabled={actionLoading[r.username]}
                      className="px-3 py-1 bg-green-100 text-green-700 rounded hover:bg-green-200 disabled:opacity-50"
                    >
                      {actionLoading[r.username] ? '...' : 'Принять'}
                    </button>
                    <button
                      onClick={() => handleReject(r.username)}
                      disabled={actionLoading[r.username]}
                      className="px-3 py-1 bg-yellow-100 text-yellow-700 rounded hover:bg-yellow-200 disabled:opacity-50"
                    >
                      {actionLoading[r.username] ? '...' : 'Отклонить'}
                    </button>
                  </div>
                </li>
              ))}
            </ul>
          ) : (
            <div className="text-center text-gray-400 py-8">Нет входящих запросов</div>
          )
        ) : (
          sentRequests.length > 0 ? (
            <ul className="divide-y">
              {sentRequests.map((s) => (
                <li key={s.username} className="flex items-center justify-between py-2">
                  <span>{s.first_name || s.username}</span>
                  <button
                    onClick={() => handleReject(s.username)}
                    disabled={actionLoading[s.username]}
                    className="px-3 py-1 bg-yellow-100 text-yellow-700 rounded hover:bg-yellow-200 disabled:opacity-50"
                  >
                    {actionLoading[s.username] ? '...' : 'Отменить'}
                  </button>
                </li>
              ))}
            </ul>
          ) : (
            <div className="text-center text-gray-400 py-8">Нет отправленных запросов</div>
          )
        )}
      </div>
    </div>
  );
} 