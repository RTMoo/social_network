import { useContext, useEffect, useState } from 'react';
import { AuthContext } from '../context/AuthContext';
import { postsApi } from '../api';
import PostModal from '../components/PostModal';

export default function Home() {
  const { user } = useContext(AuthContext);
  const [posts, setPosts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [selectedPost, setSelectedPost] = useState(null);
  const [isModalOpen, setIsModalOpen] = useState(false);

  const backendUrl = import.meta.env.VITE_API_URL ? import.meta.env.VITE_API_URL.replace('/api/', '') : 'http://localhost:8000';

  useEffect(() => {
    async function fetchPosts() {
      setLoading(true);
      try {
        const res = await postsApi.getAllPosts();
        setPosts(res.data);
      } catch (e) {
        // Можно добавить обработку ошибок
      } finally {
        setLoading(false);
      }
    }
    fetchPosts();
  }, []);

  const handlePostClick = (post) => {
    setSelectedPost(post);
    setIsModalOpen(true);
  };

  const handleCloseModal = () => {
    setIsModalOpen(false);
    setSelectedPost(null);
  };

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="max-w-4xl mx-auto py-10 px-4">
        <h1 className="text-3xl font-bold mb-8 text-center">Публикации</h1>
        {loading ? (
          <div className="flex justify-center items-center py-8">
            <div className="text-gray-500">Загрузка публикаций...</div>
          </div>
        ) : posts.length > 0 ? (
          <div className="grid grid-cols-3 gap-2 md:gap-4">
            {posts.map((post) => (
              <div
                key={post.id}
                className="aspect-square bg-gray-100 rounded-md overflow-hidden cursor-pointer"
                onClick={() => handlePostClick(post)}
              >
                {post.preview ? (
                  <img
                    src={`${backendUrl}${post.preview}`}
                    alt={post.title || 'Post'}
                    className="w-full h-full object-cover hover:opacity-90 transition-opacity"
                  />
                ) : (
                  <div className="w-full h-full flex items-center justify-center">
                    <span className="text-3xl text-gray-300">📷</span>
                  </div>
                )}
              </div>
            ))}
          </div>
        ) : (
          <div className="text-center py-8 text-gray-500">
            <span className="text-4xl mb-4 block">📷</span>
            <p>Пока нет публикаций</p>
          </div>
        )}
      </div>
      <PostModal
        post={selectedPost}
        isOpen={isModalOpen}
        onClose={handleCloseModal}
        backendUrl={backendUrl}
      />
    </div>
  );
} 