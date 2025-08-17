import React, { useState, useEffect, useRef } from 'react';
import { useAuth } from '../context/AuthContext';
import { getChats, getChatMessages } from '../api/endpoints/chats';
import { useParams, useNavigate } from 'react-router-dom';
import { backendUrl } from '../constants';
import { HiArrowLeft } from 'react-icons/hi';
import { ipUrl } from '../constants';

const Messages = () => {
  const { user } = useAuth();
  const [chats, setChats] = useState([]);
  const [selectedChat, setSelectedChat] = useState(null);
  const [messages, setMessages] = useState([]);
  const [newMessage, setNewMessage] = useState('');
  const [loading, setLoading] = useState(false);
  const [ws, setWs] = useState(null);
  const [wsConnected, setWsConnected] = useState(false);
  const [mobileView, setMobileView] = useState('list'); // 'list' или 'chat'

  const messagesEndRef = useRef(null);
  const inputRef = useRef(null);
  const { chat_id } = useParams();
  const navigate = useNavigate();

  const scrollToBottom = () => messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  useEffect(() => scrollToBottom(), [messages]);

  // Загрузка чатов
  useEffect(() => {
    const loadChats = async () => {
      try {
        setLoading(true);
        const response = await getChats();
        setChats(response.data);
        if (chat_id) {
          const found = response.data.find(chat => String(chat.chat_id) === String(chat_id));
          if (found) {
            setSelectedChat(found);
            setMobileView('chat');
          }
        }
      } catch (error) {
        console.error('Ошибка загрузки чатов:', error);
      } finally {
        setLoading(false);
      }
    };
    loadChats();
  }, [chat_id]);

  // WebSocket
  useEffect(() => {
    if (selectedChat) {
      // Закрываем предыдущее подключение
      if (ws) {
        ws.close();
      }

      const wsUrl = `ws://${ipUrl}/ws/chat/${selectedChat.chat_id}/`;
      const websocket = new WebSocket(wsUrl);

      websocket.onopen = () => setWsConnected(true);
      websocket.onmessage = (event) => setMessages(prev => [...prev, JSON.parse(event.data)]);
      websocket.onerror = () => setWsConnected(false);
      websocket.onclose = () => setWsConnected(false);

      setWs(websocket);
      return () => websocket.close();
    }
  }, [selectedChat]);

  // Загрузка сообщений
  useEffect(() => {
    if (selectedChat) {
      const loadMessages = async () => {
        try {
          const response = await getChatMessages(selectedChat.chat_id);
          setMessages(response.data);
        } catch (error) {
          console.error('Ошибка загрузки сообщений:', error);
        }
      };
      loadMessages();
    }
  }, [selectedChat]);

  const sendMessage = () => {
    if (newMessage.trim() && ws?.readyState === WebSocket.OPEN) {
      ws.send(JSON.stringify({ text: newMessage }));
      setNewMessage('');
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  };

  const formatTime = (timestamp) => new Date(timestamp).toLocaleTimeString('ru-RU', { hour: '2-digit', minute: '2-digit' });
  const formatDate = (timestamp) => {
    const date = new Date(timestamp);
    const today = new Date();
    const yesterday = new Date(today); yesterday.setDate(today.getDate() - 1);
    if (date.toDateString() === today.toDateString()) return 'Сегодня';
    if (date.toDateString() === yesterday.toDateString()) return 'Вчера';
    return date.toLocaleDateString('ru-RU');
  };

  // Мобильная кнопка назад
  const handleBack = () => {
    setMobileView('list');
    setSelectedChat(null);
  };

  // ======= Рендер ==========
  return (
    <div className="flex h-screen bg-gray-100">

      {/* --- Список чатов --- */}
      {/* --- Список чатов --- */}
      <div className={`
  bg-white border-r border-gray-200
  ${mobileView === 'chat' ? 'hidden md:block' : 'block'}
  w-full sm:w-full md:w-56 lg:w-64 flex-shrink-0
  flex flex-col
`}>
        <div className="sticky top-0 z-10 p-4 border-b border-gray-200 bg-white font-semibold text-lg">
          Чаты
        </div>
        <div className="flex-1 overflow-y-auto">
          {loading ? (
            <div className="p-4 text-center text-gray-500">Загрузка чатов...</div>
          ) : chats.length === 0 ? (
            <div className="p-4 text-center text-gray-500">Нет чатов</div>
          ) : (
            chats.map(chat => (
              <div
                key={chat.chat_id}
                className={`flex items-center p-4 cursor-pointer hover:bg-gray-50 transition-colors ${selectedChat?.chat_id === chat.chat_id ? 'bg-blue-50 border-r-2 border-blue-600' : ''
                  }`}
                onClick={() => {
                  setSelectedChat(chat);
                  setMobileView('chat');
                  navigate(`/messages/${chat.chat_id}`);
                }}
              >
                <div className="w-12 h-12 bg-blue-500 rounded-full flex items-center justify-center text-white font-semibold mr-3">
                  {chat.second_user.charAt(0).toUpperCase()}
                </div>
                <div className="flex-1 min-w-0">
                  <div className="font-semibold text-gray-900 truncate">{chat.second_user}</div>
                  {chat.last_message && (
                    <div className="text-gray-500 text-sm truncate">{chat.last_message.text}</div>
                  )}
                </div>
              </div>
            ))
          )}
        </div>
      </div>
      {/* --- Сам чат --- */}
      {selectedChat && (
        <div className={`
          flex-1 flex flex-col w-full bg-white
          ${mobileView === 'list' ? 'hidden md:flex' : 'flex'}
        `}>
          <div className="sticky top-0 z-10 flex items-center p-4 border-b border-gray-200 bg-white shadow-sm">
            {/* Кнопка назад для мобильных */}
            <button
              className="md:hidden mr-3 text-gray-600 hover:text-gray-900"
              onClick={handleBack}
            >
              <HiArrowLeft className="w-6 h-6" />
            </button>
            <div className="w-10 h-10 bg-blue-500 rounded-full flex items-center justify-center text-white font-semibold mr-3">
              {selectedChat.second_user.charAt(0).toUpperCase()}
            </div>
            <h2 className="font-semibold text-gray-900">{selectedChat.second_user}</h2>
          </div>

          <div className="flex-1 overflow-y-auto bg-gray-50">
            <div className="max-w-4xl mx-auto space-y-4 p-4">
              {messages.map((message, index) => {
                const isOwn = message.author === user?.username || message.sender === user?.username;
                const showDate = index === 0 || formatDate(message.created_at) !== formatDate(messages[index - 1]?.created_at);
                return (
                  <React.Fragment key={message.id || index}>
                    {showDate && (
                      <div className="flex justify-center my-6">
                        <span className="bg-gray-200 text-gray-600 text-xs px-3 py-1 rounded-full">
                          {formatDate(message.created_at)}
                        </span>
                      </div>
                    )}
                    <div className={`flex ${isOwn ? 'justify-end' : 'justify-start'}`}>
                      {!isOwn && (
                        <div className="w-8 h-8 bg-blue-500 rounded-full flex items-center justify-center text-white text-sm font-semibold mr-2 mt-1">
                          {(message.author || message.sender)?.charAt(0).toUpperCase() || 'U'}
                        </div>
                      )}
                      <div className={`max-w-[70%] px-4 py-3 rounded-2xl ${isOwn ? 'bg-blue-600 text-white rounded-br-md' : 'bg-white text-gray-900 border border-gray-200 rounded-bl-md shadow-sm'
                        }`}>
                        <div className="text-sm break-words">{message.text}</div>
                        <div className={`text-xs mt-1 ${isOwn ? 'text-blue-100' : 'text-gray-400'} text-right`}>
                          {formatTime(message.created_at)}
                        </div>
                      </div>
                    </div>
                  </React.Fragment>
                );
              })}
              <div ref={messagesEndRef} />
            </div>
          </div>

          <div className="p-4 border-t border-gray-200 bg-white fixed md:static bottom-0 left-0 right-0">
            <div className="max-w-4xl mx-auto flex gap-3 items-end">
              <textarea
                ref={inputRef}
                value={newMessage}
                onChange={e => setNewMessage(e.target.value)}
                onKeyPress={handleKeyPress}
                placeholder="Введите сообщение..."
                className="flex-1 px-4 py-3 border border-gray-300 rounded-full resize-none text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent pr-12"
                rows="1"
              />
              <button
                onClick={sendMessage}
                disabled={!newMessage.trim() || !wsConnected}
                className="bg-blue-600 text-white p-2 rounded-full hover:bg-blue-700 disabled:bg-gray-400 disabled:cursor-not-allowed transition-colors"
              >
                <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8" />
                </svg>
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default Messages;
