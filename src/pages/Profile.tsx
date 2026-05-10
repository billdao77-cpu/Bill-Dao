import React, { useState } from 'react';
import { useAuth } from '../App';
import { 
  User, 
  Mail, 
  Lock, 
  Shield, 
  Camera, 
  Save, 
  AlertTriangle,
  CheckCircle2
} from 'lucide-react';
import { motion } from 'motion/react';

export default function Profile() {
  const { user, updateUser } = useAuth();
  const [name, setName] = useState(user?.name || '');
  const [currentPassword, setCurrentPassword] = useState('');
  const [newPassword, setNewPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [status, setStatus] = useState<{ type: 'success' | 'error', msg: string } | null>(null);

  const handleUpdateProfile = (e: React.FormEvent) => {
    e.preventDefault();
    updateUser({ name });
    setStatus({ type: 'success', msg: 'Hồ sơ đã được cập nhật thành công!' });
    setTimeout(() => setStatus(null), 3000);
  };

  const handleChangePassword = (e: React.FormEvent) => {
    e.preventDefault();
    if (newPassword !== confirmPassword) {
      setStatus({ type: 'error', msg: 'Mật khẩu xác nhận không khớp!' });
      return;
    }
    updateUser({ mustChangePassword: false });
    setStatus({ type: 'success', msg: 'Mật khẩu đã được thay đổi!' });
    setNewPassword('');
    setConfirmPassword('');
    setCurrentPassword('');
    setTimeout(() => setStatus(null), 3000);
  };

  return (
    <div className="max-w-4xl mx-auto space-y-8">
      <div>
        <h1 className="text-2xl font-bold text-slate-900">Hồ sơ cá nhân</h1>
        <p className="text-slate-500">Quản lý thông tin tài khoản và bảo mật cá nhân.</p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        {/* Left Column: Avatar & Summary */}
        <div className="lg:col-span-1 space-y-6">
          <div className="bg-white p-8 rounded-3xl border border-slate-100 shadow-sm text-center space-y-4">
            <div className="relative inline-block">
              <div className="w-32 h-32 rounded-full bg-blue-100 border-4 border-white flex items-center justify-center text-blue-600 text-4xl font-black shadow-xl mx-auto overflow-hidden">
                 {user?.avatar ? <img src={user.avatar} className="w-full h-full object-cover" /> : user?.name.charAt(0)}
              </div>
              <button className="absolute bottom-0 right-0 p-2 bg-blue-600 text-white rounded-full border-4 border-white shadow-lg hover:scale-110 transition-all">
                <Camera className="w-4 h-4" />
              </button>
            </div>
            <div>
              <h3 className="font-bold text-xl text-slate-900">{user?.name}</h3>
              <p className="text-sm text-slate-500">{user?.email}</p>
            </div>
            <div className="flex items-center justify-center gap-2">
               <span className="px-3 py-1 bg-blue-50 text-blue-600 rounded-full text-[10px] font-bold uppercase tracking-widest border border-blue-100">
                {user?.role.replace('_', ' ')}
               </span>
            </div>
          </div>

          <div className="bg-slate-900 rounded-2xl p-6 text-white space-y-4">
            <div className="flex items-center gap-3">
              <Shield className="w-5 h-5 text-blue-400" />
              <h4 className="font-bold">Bảo mật tài khoản</h4>
            </div>
            <p className="text-white/60 text-xs leading-relaxed">Đảm bảo mật khẩu của bạn có ít nhất 8 ký tự, bao gồm cả chữ số và ký hiệu đặc biệt.</p>
          </div>
        </div>

        {/* Right Column: Forms */}
        <div className="lg:col-span-2 space-y-8">
          {/* Status Message */}
          {status && (
            <motion.div 
              initial={{ opacity: 0, y: -10 }}
              animate={{ opacity: 1, y: 0 }}
              className={cn(
                "p-4 rounded-xl flex items-center gap-3 text-sm font-bold border",
                status.type === 'success' ? "bg-emerald-50 text-emerald-700 border-emerald-100" : "bg-red-50 text-red-700 border-red-100"
              )}
            >
              {status.type === 'success' ? <CheckCircle2 className="w-5 h-5" /> : <AlertTriangle className="w-5 h-5" />}
              {status.msg}
            </motion.div>
          )}

          {/* First Login Alert */}
          {user?.mustChangePassword && (
            <div className="bg-amber-50 border border-amber-200 p-6 rounded-2xl flex gap-4">
              <AlertTriangle className="text-amber-600 w-8 h-8 shrink-0" />
              <div>
                <h4 className="font-bold text-amber-900 text-lg">Yêu cầu đổi mật khẩu</h4>
                <p className="text-amber-800 text-sm mt-1 leading-relaxed">Đây là lần đầu bạn đăng nhập. Để an toàn, vui lòng thay đổi mật khẩu mặc định bằng mật khẩu mới của riêng bạn.</p>
              </div>
            </div>
          )}

          {/* Profile Form */}
          <section className="bg-white p-8 rounded-3xl border border-slate-100 shadow-sm space-y-6">
            <h3 className="font-bold text-slate-900 flex items-center gap-2">
              <User className="w-5 h-5 text-blue-500" /> Thông tin cơ bản
            </h3>
            <form onSubmit={handleUpdateProfile} className="space-y-4">
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div className="space-y-2">
                  <label className="text-xs font-bold text-slate-400 uppercase tracking-widest pl-1">Họ và tên</label>
                  <input 
                    type="text" 
                    value={name}
                    onChange={(e) => setName(e.target.value)}
                    className="w-full bg-slate-50 border border-slate-100 rounded-xl py-3 px-4 outline-none focus:ring-2 focus:ring-blue-500 transition-all font-medium"
                  />
                </div>
                <div className="space-y-2">
                  <label className="text-xs font-bold text-slate-400 uppercase tracking-widest pl-1">Email (Không thể đổi)</label>
                  <input 
                    type="email" 
                    value={user?.email}
                    disabled
                    className="w-full bg-slate-100 border border-slate-100 rounded-xl py-3 px-4 outline-none cursor-not-allowed opacity-60 font-medium"
                  />
                </div>
              </div>
              <button 
                type="submit"
                className="bg-blue-600 hover:bg-blue-700 text-white font-bold py-3 px-8 rounded-xl transition-all shadow-lg shadow-blue-200 flex items-center gap-2"
              >
                <Save className="w-4 h-4" /> Cập nhật hồ sơ
              </button>
            </form>
          </section>

          {/* Password Form */}
          <section className="bg-white p-8 rounded-3xl border border-slate-100 shadow-sm space-y-6">
             <h3 className="font-bold text-slate-900 flex items-center gap-2">
              <Lock className="w-5 h-5 text-red-500" /> Đổi mật khẩu
            </h3>
            <form onSubmit={handleChangePassword} className="space-y-4">
              <div className="space-y-2">
                <label className="text-xs font-bold text-slate-400 uppercase tracking-widest pl-1">Mật khẩu hiện tại</label>
                <input 
                  type="password" 
                  value={currentPassword}
                  onChange={(e) => setCurrentPassword(e.target.value)}
                  className="w-full bg-slate-50 border border-slate-100 rounded-xl py-3 px-4 outline-none focus:ring-2 focus:ring-red-500 transition-all"
                  placeholder="••••••••"
                />
              </div>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div className="space-y-2">
                  <label className="text-xs font-bold text-slate-400 uppercase tracking-widest pl-1">Mật khẩu mới</label>
                  <input 
                    type="password" 
                    value={newPassword}
                    onChange={(e) => setNewPassword(e.target.value)}
                    className="w-full bg-slate-50 border border-slate-100 rounded-xl py-3 px-4 outline-none focus:ring-2 focus:ring-blue-500 transition-all"
                    placeholder="••••••••"
                  />
                </div>
                <div className="space-y-2">
                  <label className="text-xs font-bold text-slate-400 uppercase tracking-widest pl-1">Xác nhận mật khẩu mới</label>
                  <input 
                    type="password" 
                    value={confirmPassword}
                    onChange={(e) => setConfirmPassword(e.target.value)}
                    className="w-full bg-slate-50 border border-slate-100 rounded-xl py-3 px-4 outline-none focus:ring-2 focus:ring-blue-500 transition-all"
                    placeholder="••••••••"
                  />
                </div>
              </div>
              <button 
                type="submit"
                className={cn(
                  "font-bold py-3 px-8 rounded-xl transition-all shadow-lg flex items-center gap-2",
                  user?.mustChangePassword ? "bg-red-600 hover:bg-red-700 text-white shadow-red-200" : "bg-slate-900 hover:bg-black text-white"
                )}
              >
                Xác nhận đổi mật khẩu
              </button>
            </form>
          </section>
        </div>
      </div>
    </div>
  );
}
