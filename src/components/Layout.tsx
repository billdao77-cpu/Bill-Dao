import React, { useState } from 'react';
import { Outlet, Link, useLocation, useNavigate } from 'react-router-dom';
import { 
  LayoutDashboard, 
  Users, 
  UserSquare2, 
  ShieldCheck, 
  FileText, 
  History, 
  Settings, 
  LogOut, 
  Menu, 
  X, 
  Bell, 
  Search,
  Store,
  UploadCloud,
  FileBox,
  UserCircle
} from 'lucide-react';
import { useAuth } from '../App';
import { motion, AnimatePresence } from 'motion/react';
import { cn } from '../lib/utils';

export default function Layout() {
  const { user, logout } = useAuth();
  const location = useLocation();
  const navigate = useNavigate();
  const [isSidebarOpen, setIsSidebarOpen] = useState(true);

  const menuItems = [
    { name: 'Dashboard', path: '/', icon: LayoutDashboard },
    { name: 'Quản lý Hội viên', path: '/members', icon: Users },
    { name: 'Ban Chấp hành', path: '/board/BCH', icon: UserSquare2 },
    { name: 'Ban Thường vụ', path: '/board/BTV', icon: ShieldCheck },
    { name: 'Ban Kiểm tra', path: '/board/BKT', icon: UserCircle },
    { name: 'Biên bản họp AI', path: '/meetings-ai', icon: History },
    { name: 'Marketplace', path: '/marketplace', icon: Store },
    { name: 'Quản lý File', path: '/files', icon: FileBox },
  ];

  if (user?.role === 'SUPER_ADMIN') {
    menuItems.push({ name: 'Quản trị User', path: '/users', icon: Settings });
  }

  return (
    <div className="flex h-screen bg-slate-50 overflow-hidden font-sans">
      {/* Sidebar */}
      <motion.aside 
        initial={false}
        animate={{ width: isSidebarOpen ? 260 : 80 }}
        className="bg-slate-900 text-slate-300 flex flex-col flex-shrink-0 shadow-2xl relative z-20"
      >
        <div className="p-6 flex items-center gap-3 border-b border-slate-800">
          <div className="w-10 h-10 blue-gradient rounded-lg flex items-center justify-center text-white font-bold shrink-0 shadow-lg">
            HY
          </div>
          {isSidebarOpen && (
            <motion.div 
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              className="flex flex-col"
            >
              <h1 className="text-sm font-bold text-white leading-tight uppercase">HHDL Hưng Yên</h1>
              <p className="text-[10px] opacity-60 uppercase tracking-widest font-bold">Admin Portal</p>
            </motion.div>
          )}
        </div>

        <nav className="flex-1 overflow-y-auto py-6 px-3 space-y-1 custom-scrollbar">
          {menuItems.map((item, idx) => (
            <Link
              key={item.path}
              to={item.path}
              className={cn(
                "flex items-center gap-3 px-3 py-2.5 rounded-lg transition-all text-sm font-medium",
                location.pathname === item.path 
                  ? "sidebar-active" 
                  : "hover:bg-slate-800 hover:text-white"
              )}
            >
              <item.icon className={cn("w-5 h-5 shrink-0", location.pathname === item.path ? "text-white" : "text-slate-500")} />
              {isSidebarOpen && <span className="truncate">{item.name}</span>}
            </Link>
          ))}
        </nav>

        <div className="p-4 bg-slate-950 border-t border-slate-800">
          {isSidebarOpen && (
            <div className="flex items-center gap-3 mb-4 px-2">
              <div className="w-8 h-8 rounded-full bg-blue-500 flex items-center justify-center text-xs font-bold text-white shadow-inner">
                {user?.name.charAt(0)}
              </div>
              <div className="text-xs truncate">
                <p className="text-white font-semibold truncate">{user?.name}</p>
                <p className="text-slate-500 text-[10px] uppercase font-bold tracking-tighter">{user?.role.replace('_', ' ')}</p>
              </div>
            </div>
          )}
          <button 
            onClick={logout}
            className="w-full py-2 bg-slate-800 hover:bg-red-900 hover:text-white transition-all rounded-md text-xs font-medium flex items-center justify-center gap-2"
          >
            <LogOut className="w-3.5 h-3.5" />
            {isSidebarOpen && <span>Đăng xuất</span>}
          </button>
        </div>

        <button 
          onClick={() => setIsSidebarOpen(!isSidebarOpen)}
          className="absolute -right-3 top-20 w-6 h-6 bg-slate-900 border border-slate-700 text-slate-400 rounded-full flex items-center justify-center shadow-lg hover:text-white z-30"
        >
          {isSidebarOpen ? <X className="w-3 h-3" /> : <Menu className="w-3 h-3" />}
        </button>
      </motion.aside>

      {/* Main Content */}
      <div className="flex-1 flex flex-col min-w-0">
        {/* Header */}
        <header className="h-16 bg-white border-b border-slate-200 flex items-center justify-between px-8 sticky top-0 z-10 shadow-sm">
          <div className="flex items-center gap-4 text-sm text-slate-500 font-medium">
             <span>Hệ thống Quản trị</span>
             <span className="text-slate-300">/</span>
             <span className="text-blue-700 font-bold">{menuItems.find(i => i.path === location.pathname)?.name || 'Trang chủ'}</span>
          </div>

          <div className="flex items-center gap-6">
            <div className="hidden md:flex items-center gap-2 px-4 py-1.5 bg-emerald-50 text-emerald-700 border border-emerald-200 rounded-full text-[11px] font-bold uppercase tracking-wide">
              <div className="w-2 h-2 bg-emerald-500 rounded-full animate-pulse" />
              Hệ thống Trực tuyến
            </div>
            
            <div className="flex items-center gap-6">
              <button className="relative text-slate-400 hover:text-blue-600 transition-colors">
                <Bell className="w-5 h-5" />
                <span className="absolute -top-0.5 -right-0.5 w-2 h-2 bg-red-500 rounded-full border-2 border-white"></span>
              </button>
              
              <div className="h-6 w-px bg-slate-200" />

              <div className="flex items-center gap-3 cursor-pointer group" onClick={() => navigate('/profile')}>
                <div className="text-right hidden sm:block">
                  <div className="text-xs font-bold text-slate-800 group-hover:text-blue-600 transition-colors">{user?.name}</div>
                  <div className="text-[10px] text-slate-500 font-medium">{user?.role === 'SUPER_ADMIN' ? 'Tổng quản trị' : user?.role === 'ADMIN' ? 'Quản lý viên' : 'Hội viên'}</div>
                </div>
                <div className="w-8 h-8 rounded-lg bg-blue-50 border border-slate-200 flex items-center justify-center text-blue-700 font-bold overflow-hidden shadow-sm group-hover:border-blue-300 transition-all">
                  {user?.avatar ? <img src={user.avatar} className="w-full h-full object-cover" /> : user?.name.charAt(0)}
                </div>
              </div>
            </div>
          </div>
        </header>

        {/* Content Area */}
        <main className="flex-1 overflow-y-auto p-8 custom-scrollbar">
          <AnimatePresence mode="wait">
            <motion.div
              key={location.pathname}
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -10 }}
              transition={{ duration: 0.2 }}
            >
              <Outlet />
            </motion.div>
          </AnimatePresence>
        </main>
      </div>
    </div>
  );
}
