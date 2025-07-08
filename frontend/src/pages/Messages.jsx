import React, { useState, useEffect, useRef } from 'react';
import { useAuth } from '../context/AuthContext';
import { getChats, createChat, getChatMessages } from '../api/endpoints/chats';
import { searchProfiles } from '../api/endpoints/search';
import { useParams, useNavigate } from 'react-router-dom';

const Messages = () => {
  const { user } = useAuth();
  const [chats, setChats] = useState([]);
  const [selectedChat, setSelectedChat] = useState(null);
  const [messages, setMessages] = useState([]);
  const [newMessage, setNewMessage] = useState('');
  const [searchQuery, setSearchQuery] = useState('');
  const [searchResults, setSearchResults] = useState([]);
  const [showSearch, setShowSearch] = useState(false);
  const [loading, setLoading] = useState(false);
  const [ws, setWs] = useState(null);
  const [wsConnected, setWsConnected] = useState(false);
  const messagesEndRef = useRef(null);
  const inputRef = useRef(null);
  const { chat_id } = useParams();
  const navigate = useNavigate();

  // Прокрутка к последнему сообщению
  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  // Загрузка чатов
  useEffect(() => {
    const loadChats = async () => {
      try {
        setLoading(true);
        const response = await getChats();
        setChats(response.data);
        if (chat_id) {
          const found = response.data.find(chat => String(chat.chat_id) === String(chat_id));
          if (found) setSelectedChat(found);
        }
      } catch (error) {
        console.error('Ошибка загрузки чатов:', error);
      } finally {
        setLoading(false);
      }
    };

    loadChats();
  }, [chat_id]);

  // WebSocket подключение
  useEffect(() => {
    if (selectedChat) {
      // Закрываем предыдущее подключение
      if (ws) {
        ws.close();
      }

      const wsUrl = `ws://localhost:8000/ws/chat/${selectedChat.chat_id}/`;
      const websocket = new WebSocket(wsUrl);

      websocket.onopen = () => {
        console.log('WebSocket подключен');
        setWsConnected(true);
      };

      websocket.onmessage = (event) => {
        const message = JSON.parse(event.data);
        setMessages(prev => [...prev, message]);
      };

      websocket.onerror = (error) => {
        console.error('WebSocket ошибка:', error);
        setWsConnected(false);
      };

      websocket.onclose = () => {
        console.log('WebSocket отключен');
        setWsConnected(false);
      };

      setWs(websocket);

      return () => {
        websocket.close();
      };
    }
  }, [selectedChat]);

  // Загрузка сообщений при выборе чата
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

  // Поиск пользователей
  const handleSearch = async () => {
    if (searchQuery.trim()) {
      try {
        const response = await searchProfiles(searchQuery);
        setSearchResults(response.data);
        setShowSearch(true);
      } catch (error) {
        console.error('Ошибка поиска:', error);
      }
    }
  };

  // Создание нового чата
  const handleCreateChat = async (username) => {
    try {
      const response = await createChat(username);
      const newChat = response.data;
      
      // Добавляем новый чат в список, если его там нет
      if (!chats.find(chat => chat.chat_id === newChat.chat_id)) {
        setChats(prev => [newChat, ...prev]);
      }
      
      setSelectedChat(newChat);
      navigate(`/messages/${newChat.chat_id}`);
      setShowSearch(false);
      setSearchQuery('');
      setSearchResults([]);
    } catch (error) {
      console.error('Ошибка создания чата:', error);
    }
  };

  // Отправка сообщения
  const sendMessage = () => {
    if (newMessage.trim() && ws && ws.readyState === WebSocket.OPEN) {
      ws.send(JSON.stringify({ text: newMessage }));
      setNewMessage('');
    }
  };

  // Обработка нажатия Enter
  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  };

  const formatTime = (timestamp) => {
    const date = new Date(timestamp);
    return date.toLocaleTimeString('ru-RU', { 
      hour: '2-digit', 
      minute: '2-digit' 
    });
  };

  const formatDate = (timestamp) => {
    const date = new Date(timestamp);
    const today = new Date();
    const yesterday = new Date(today);
    yesterday.setDate(yesterday.getDate() - 1);

    if (date.toDateString() === today.toDateString()) {
      return 'Сегодня';
    } else if (date.toDateString() === yesterday.toDateString()) {
      return 'Вчера';
    } else {
      return date.toLocaleDateString('ru-RU');
    }
  };

  return (
    <div className="flex h-screen bg-gray-100">
      {/* Левая панель - сообщения */}
      <div className="flex-1 flex flex-col bg-white">
        {selectedChat ? (
          <>
            {/* Заголовок чата */}
            <div className="sticky top-0 z-10 flex items-center p-4 border-b border-gray-200 bg-white shadow-sm">
              <div className="w-10 h-10 bg-blue-500 rounded-full flex items-center justify-center text-white font-semibold mr-3">
                {selectedChat.second_user.charAt(0).toUpperCase()}
              </div>
              <div className="flex-1">
                <h2 className="font-semibold text-gray-900">{selectedChat.second_user}</h2>
                
              </div>
            </div>

            {/* Область сообщений */}
            <div className="flex-1 overflow-y-auto bg-gray-50">
              <div className="max-w-4xl mx-auto space-y-4">
                {messages.map((message, index) => {
                  // Проверяем, является ли текущий пользователь автором сообщения
                  // Учитываем как author (из API), так и sender (из WebSocket)
                  const isOwnMessage = message.author === user?.username || message.sender === user?.username;
                  const showDate = index === 0 || 
                    formatDate(message.created_at) !== formatDate(messages[index - 1]?.created_at);
                  
                  return (
                    <React.Fragment key={message.id || index}>
                      {showDate && (
                        <div className="flex justify-center my-6">
                          <span className="bg-gray-200 text-gray-600 text-xs px-3 py-1 rounded-full">
                            {formatDate(message.created_at)}
                          </span>
                        </div>
                      )}
                      
                      {/* Сообщение */}
                      <div className={`flex ${isOwnMessage ? 'justify-end' : 'justify-start'}`}>
                        {!isOwnMessage && (
                          <div className="w-8 h-8 bg-blue-500 rounded-full flex items-center justify-center text-white text-sm font-semibold mr-2 mt-1">
                            {(message.author || message.sender)?.charAt(0).toUpperCase() || 'U'}
                          </div>
                        )}
                        
                        <div className={`max-w-[70%] px-4 py-3 rounded-2xl ${
                          isOwnMessage 
                            ? 'bg-blue-600 text-white rounded-br-md' 
                            : 'bg-white text-gray-900 border border-gray-200 rounded-bl-md shadow-sm'
                        }`}>
                          <div className="text-sm leading-relaxed break-words">{message.text}</div>
                          <div className={`text-xs mt-1 ${isOwnMessage ? 'text-blue-100' : 'text-gray-400'} text-right`}>
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

            {/* Поле ввода сообщения */}
            <div className="p-4 border-t border-gray-200 bg-white z-40 md:z-auto fixed md:static bottom-14 left-0 right-0">
              <div className="max-w-4xl mx-auto flex gap-3 items-end">
                <div className="flex-1 relative">
                  <textarea
                    ref={inputRef}
                    value={newMessage}
                    onChange={(e) => setNewMessage(e.target.value)}
                    onKeyPress={handleKeyPress}
                    placeholder="Введите сообщение..."
                    className="w-full px-4 py-3 border border-gray-300 rounded-full resize-none text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent pr-12"
                    rows="1"
                  />
                  <button 
                    onClick={sendMessage}
                    disabled={!newMessage.trim() || !wsConnected}
                    className="absolute right-2 bottom-2 bg-blue-600 text-white p-2 rounded-full hover:bg-blue-700 disabled:bg-gray-400 disabled:cursor-not-allowed transition-colors"
                  >
                    <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8" />
                    </svg>
                  </button>
                </div>
              </div>
            </div>
          </>
        ) : (
          <div className="flex-1 flex items-center justify-center bg-gray-50">
            <div className="text-center text-gray-500">
              <div className="w-20 h-20 bg-gray-200 rounded-full flex items-center justify-center mx-auto mb-4">
                <svg className="w-10 h-10 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z" />
                </svg>
              </div>
              <h3 className="text-xl font-semibold mb-2">Выберите чат</h3>
              <p className="text-sm">Выберите чат из списка справа, чтобы начать общение</p>
            </div>
          </div>
        )}
      </div>

      {/* Правая панель - чаты */}
      <div className="w-80 border-l border-gray-200 bg-white flex flex-col">
        {/* Заголовок */}
        <div className="sticky top-0 z-10 p-4 border-b border-gray-200 flex justify-between items-center bg-white">
          <h2 className="text-lg font-semibold text-gray-900">Сообщения</h2>
          <button 
            className="bg-blue-600 text-white p-2 rounded-full hover:bg-blue-700 transition-colors"
            onClick={() => setShowSearch(!showSearch)}
            title="Новый чат"
          >
            <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 4v16m8-8H4" />
            </svg>
          </button>
        </div>

        {/* Поиск пользователей */}
        {showSearch && (
          <div className="p-4 border-b border-gray-200 bg-gray-50">
            <div className="flex gap-2 mb-3">
              <input
                type="text"
                placeholder="Поиск пользователей..."
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                onKeyPress={(e) => e.key === 'Enter' && handleSearch()}
                className="flex-1 px-3 py-2 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              />
              <button 
                onClick={handleSearch}
                className="bg-green-600 text-white px-3 py-2 rounded-lg text-sm font-medium hover:bg-green-700 transition-colors"
              >
                Поиск
              </button>
            </div>
            
            {searchResults.length > 0 && (
              <div className="max-h-48 overflow-y-auto space-y-2">
                {searchResults.map(user => (
                  <div 
                    key={user.id}
                    className="flex items-center p-2 cursor-pointer rounded-lg hover:bg-gray-100 transition-colors"
                    onClick={() => handleCreateChat(user.username)}
                  >
                    <div className="w-8 h-8 bg-blue-500 rounded-full flex items-center justify-center text-white text-sm font-semibold mr-3">
                      {user.username.charAt(0).toUpperCase()}
                    </div>
                    <div className="flex-1">
                      <div className="font-medium text-sm">
                        {user.username}
                        {user.username === user?.username && (
                          <span className="text-gray-500 ml-1">(Вы)</span>
                        )}
                      </div>
                      <div className="text-xs text-gray-500">{user.first_name} {user.last_name}</div>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>
        )}

        {/* Список чатов */}
        <div className="flex-1 overflow-y-auto">
          {loading ? (
            <div className="p-4 text-center text-gray-500 text-sm">Загрузка чатов...</div>
          ) : chats.length === 0 ? (
            <div className="p-4 text-center text-gray-500 text-sm">Нет активных чатов</div>
          ) : (
            <div className="space-y-1">
              {chats.map(chat => (
                <div
                  key={chat.chat_id}
                  className={`flex items-center p-4 cursor-pointer hover:bg-gray-50 transition-colors ${
                    selectedChat?.chat_id === chat.chat_id ? 'bg-blue-50 border-r-2 border-blue-600' : ''
                  }`}
                  onClick={() => { setSelectedChat(chat); navigate(`/messages/${chat.chat_id}`); }}
                >
                  <div className="w-12 h-12 bg-blue-500 rounded-full flex items-center justify-center text-white font-semibold mr-3">
                    {chat.second_user.charAt(0).toUpperCase()}
                  </div>
                  <div className="flex-1 min-w-0">
                    <div className="flex justify-between items-center mb-1">
                      <span className="font-semibold text-gray-900 text-sm truncate">
                        {chat.second_user}
                        {chat.second_user === user?.username && (
                          <span className="text-gray-500 ml-1">(Вы)</span>
                        )}
                      </span>
                      {chat.last_message && (
                        <span className="text-gray-400 text-xs">
                          {formatTime(chat.last_message.created_at || chat.created_at)}
                        </span>
                      )}
                    </div>
                    {chat.last_message && (
                      <div className="text-gray-500 text-sm truncate">
                        <span className={chat.last_message.author === user?.username ? 'text-blue-600 font-medium' : ''}>
                          {chat.last_message.text}
                        </span>
                      </div>
                    )}
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default Messages; 