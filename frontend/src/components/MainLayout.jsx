import Sidebar from './Sidebar';

export default function MainLayout({ children }) {
  return (
    <div className="flex bg-gray-50 min-h-screen">
      <Sidebar />
      <main className="flex-1 p-4 md:p-6 lg:p-8 pb-20 md:pb-6 lg:pb-8">
        {children}
      </main>
    </div>
  );
} 