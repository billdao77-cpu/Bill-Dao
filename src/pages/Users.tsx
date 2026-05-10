import React, { useState } from 'react';
import { 
  Users as UsersIcon, 
  UserPlus, 
  Search, 
  MoreVertical, 
  ShieldCheck, 
  ShieldAlert, 
  Shield, 
  Lock, 
  Mail,
  UserCheck,
  UserX,
  CreditCard
} from 'lucide-react';
import { MockDB } from '../services/db';
import { User, Role } from '../types';
import { motion } from 'motion/react';
import { cn } from '../lib/utils';

export default function Users() {
  const [users, setUsers] = useState<User[]>(MockDB.getUsers());
  const [search, setSearch] = useState('');

  const getRoleBadge = (role: Role) => {
    switch (role) {
      case 'SUPER_ADMIN': return <span className="flex items-center gap-1.5 px-3 py-1 bg-red-100 text-red-600 rounded-full text-[10px] font-bold uppercase tracking-wider"><ShieldCheck className="w-3 h-3" /> Super Admin</span>;
      case 'ADMIN': return <span className="flex items-center gap-1.5 px-3 py-1 bg-blue-100 text-blue-600 rounded-full text-[10px] font-bold uppercase tracking-wider"><Shield className="w-3 h-3" /> Admin</span>;
      case 'MEMBER': return <span className="flex items-center gap-1.5 px-3 py-1 bg-slate-100 text-slate-600 rounded-full text-[10px] font-bold uppercase tracking-wider">Hội viên</span>;
    }
  };

  return (
    <div className="space-y-6">
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <h1 className="text-2xl font-bold text-slate-900 font-mono tracking-tight lowercase">/admin/users</h1>
          <p className="text-slate-500">Quản trị tài khoản và phân quyền truy cập hệ thống.</p>
        </div>
        <button className="bg-slate-900 text-white px-6 py-3 rounded-2xl flex items-center gap-2 hover:bg-black transition-all font-bold text-sm shadow-xl shadow-slate-200">
          <UserPlus className="w-5 h-5" />
          Tạo User mới
        </button>
      </div>

      <div className="bg-white rounded-3xl border border-slate-100 shadow-xl overflow-hidden">
        <div className="p-6 border-b border-slate-50 flex flex-col md:flex-row md:items-center justify-between gap-4 shadow-sm relative z-10">
          <div className="relative flex-1 max-w-md">
            <Search className="absolute left-3 top-1/2 -translate-y-1/2 text-slate-400 w-5 h-5" />
            <input 
              type="text" 
              placeholder="Tìm user theo tên hoặc email..." 
              value={search}
              onChange={(e) => setSearch(e.target.value)}
              className="w-full bg-slate-50 border border-slate-100 rounded-xl py-2 pl-10 pr-4 outline-none focus:ring-2 focus:ring-blue-500 transition-all font-mono text-sm"
            />
          </div>
          <div className="flex items-center gap-2">
             <button className="px-4 py-2 text-sm font-bold text-slate-500 hover:text-slate-900 transition-all">Tất cả</button>
             <button className="px-4 py-2 text-sm font-bold text-slate-500 hover:text-slate-900 transition-all">Đang hoạt động</button>
             <button className="px-4 py-2 text-sm font-bold text-red-500 transition-all">Đã khóa</button>
          </div>
        </div>

        <div className="overflow-x-auto">
          <table className="w-full text-left border-collapse">
            <thead>
              <tr className="bg-slate-50/50">
                <th className="px-6 py-4 text-xs font-bold text-slate-400 uppercase tracking-widest">Người dùng</th>
                <th className="px-6 py-4 text-xs font-bold text-slate-400 uppercase tracking-widest">Vai trò</th>
                <th className="px-6 py-4 text-xs font-bold text-slate-400 uppercase tracking-widest">Trạng thái</th>
                <th className="px-6 py-4 text-xs font-bold text-slate-400 uppercase tracking-widest">Hành động</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-50">
              {users.filter(u => u.name.includes(search) || u.email.includes(search)).map((user, i) => (
                <tr key={user.id} className="hover:bg-slate-50/50 transition-all group">
                  <td className="px-6 py-5">
                    <div className="flex items-center gap-4">
                      <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-slate-100 to-slate-200 flex items-center justify-center text-slate-500 font-bold group-hover:from-blue-100 group-hover:to-blue-200 group-hover:text-blue-600 transition-all">
                        {user.name.charAt(0)}
                      </div>
                      <div>
                        <div className="font-bold text-slate-900">{user.name}</div>
                        <div className="text-xs text-slate-500 flex items-center gap-1"><Mail className="w-3 h-3" /> {user.email}</div>
                      </div>
                    </div>
                  </td>
                  <td className="px-6 py-5">
                    {getRoleBadge(user.role)}
                  </td>
                  <td className="px-6 py-5">
                    {user.mustChangePassword ? (
                      <span className="flex items-center gap-1 text-xs text-amber-500 font-bold"><Lock className="w-3.5 h-3.5" /> Chờ đổi MK</span>
                    ) : (
                      <span className="flex items-center gap-1 text-xs text-emerald-500 font-bold"><UserCheck className="w-3.5 h-3.5" /> Hoạt động</span>
                    )}
                  </td>
                  <td className="px-6 py-5">
                    <div className="flex items-center gap-2 opacity-0 group-hover:opacity-100 transition-all">
                      <button className="p-2 hover:bg-white rounded-lg text-slate-400 hover:text-blue-600 shadow-sm border border-transparent hover:border-slate-100" title="Reset mật khẩu">
                        <Lock className="w-4 h-4" />
                      </button>
                      <button className="p-2 hover:bg-white rounded-lg text-slate-400 hover:text-red-600 shadow-sm border border-transparent hover:border-slate-100" title="Khóa tài khoản">
                        <UserX className="w-4 h-4" />
                      </button>
                      <button className="p-2 hover:bg-white rounded-lg text-slate-400 hover:text-slate-900 shadow-sm border border-transparent hover:border-slate-100">
                        <MoreVertical className="w-4 h-4" />
                      </button>
                    </div>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>

        <div className="p-4 bg-slate-50/50 border-t border-slate-50 text-center">
          <p className="text-xs text-slate-400 font-medium">Hiển thị {users.length} tài khoản trên tổng số {users.length}</p>
        </div>
      </div>
    </div>
  );
}
