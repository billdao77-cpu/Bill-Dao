import React, { useState } from 'react';
import { 
  Users, 
  Search, 
  Filter, 
  Plus, 
  MoreVertical, 
  MapPin, 
  Phone,
  Mail,
  ExternalLink,
  Tag,
  CreditCard,
  Building,
  CheckCircle2,
  XCircle,
  FileBadge
} from 'lucide-react';
import { MOCK_MEMBERS } from '../data';
import { motion } from 'motion/react';
import { cn } from '../lib/utils';
import { useAuth } from '../App';

export default function Members() {
  const { user } = useAuth();
  const [search, setSearch] = useState('');
  const [filterCategory, setFilterCategory] = useState('All');
  const [activeFeeStatus, setActiveFeeStatus] = useState('All');

  const categories = ['All', 'Lữ hành', 'Lưu trú', 'Nhà hàng', 'Điểm đến', 'OCOP', 'Làng nghề', 'Vận tải'];

  const filteredMembers = MOCK_MEMBERS.filter(m => {
    const matchesSearch = m.businessName.toLowerCase().includes(search.toLowerCase()) || 
                         m.representative.toLowerCase().includes(search.toLowerCase());
    const matchesCategory = filterCategory === 'All' || m.category === filterCategory;
    const matchesFee = activeFeeStatus === 'All' || m.feeStatus === activeFeeStatus;
    return matchesSearch && matchesCategory && matchesFee;
  });

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <h1 className="text-2xl font-bold text-slate-900">Quản lý Hội viên</h1>
          <p className="text-slate-500">Tổng cộng {MOCK_MEMBERS.length} hội viên chính thức.</p>
        </div>
        <div className="flex items-center gap-3">
          <button className="bg-slate-100 text-slate-600 px-4 py-2 rounded-xl flex items-center gap-2 hover:bg-slate-200 transition-all font-medium text-sm">
            <FileBadge className="w-4 h-4" />
            Báo cáo hội viên
          </button>
          {user?.role !== 'MEMBER' && (
            <button className="bg-blue-600 text-white px-4 py-2 rounded-xl flex items-center gap-2 hover:bg-blue-700 transition-all font-medium text-sm shadow-lg shadow-blue-200">
              <Plus className="w-4 h-4" />
              Thêm hội viên
            </button>
          )}
        </div>
      </div>

      {/* Tabs / Filters Sidebar style internal */}
      <div className="flex flex-col lg:flex-row gap-8">
        <aside className="lg:w-64 space-y-6 shrink-0">
          <div>
            <h4 className="text-xs font-bold text-slate-400 uppercase tracking-widest mb-4">Danh mục</h4>
            <div className="space-y-1">
              {categories.map(cat => (
                <button
                  key={cat}
                  onClick={() => setFilterCategory(cat)}
                  className={cn(
                    "w-full text-left px-3 py-2 rounded-lg text-sm font-medium transition-all",
                    filterCategory === cat ? "bg-blue-50 text-blue-600" : "text-slate-600 hover:bg-slate-100"
                  )}
                >
                  {cat === 'All' ? 'Tất cả lĩnh vực' : cat}
                </button>
              ))}
            </div>
          </div>

          <div>
            <h4 className="text-xs font-bold text-slate-400 uppercase tracking-widest mb-4">Trạng thái Hội phí</h4>
            <div className="space-y-1">
              {['All', 'Đã đóng', 'Chưa đóng', 'Quá hạn'].map(status => (
                <button
                  key={status}
                  onClick={() => setActiveFeeStatus(status)}
                  className={cn(
                    "w-full text-left px-3 py-2 rounded-lg text-sm font-medium transition-all flex items-center justify-between",
                    activeFeeStatus === status ? "bg-slate-100 text-slate-900" : "text-slate-600 hover:bg-slate-100"
                  )}
                >
                  <span>{status === 'All' ? 'Tất cả' : status}</span>
                  {status !== 'All' && (
                    <div className={cn(
                      "w-2 h-2 rounded-full",
                      status === 'Đã đóng' ? "bg-emerald-500" : 
                      status === 'Chưa đóng' ? "bg-amber-500" : "bg-red-500"
                    )} />
                  )}
                </button>
              ))}
            </div>
          </div>
        </aside>

        <div className="flex-1 space-y-6">
          {/* Search bar */}
          <div className="bg-white p-2 rounded-2xl shadow-sm border border-slate-100 flex items-center gap-2">
            <div className="relative flex-1">
              <Search className="absolute left-4 top-1/2 -translate-y-1/2 text-slate-400 w-5 h-5" />
              <input 
                type="text" 
                placeholder="Tìm kiếm doanh nghiệp, mã số thuế, đại diện..." 
                value={search}
                onChange={(e) => setSearch(e.target.value)}
                className="w-full bg-white border-none rounded-xl py-3 pl-12 pr-4 outline-none text-slate-700"
              />
            </div>
            <button className="bg-slate-800 text-white px-6 py-3 rounded-xl font-bold transition-all hover:bg-slate-900 shrink-0">
              Tìm kiếm
            </button>
          </div>

          {/* Members List */}
          <div className="grid grid-cols-1 gap-4">
            {filteredMembers.map((member, i) => (
              <motion.div
                key={member.id}
                initial={{ opacity: 0, x: -10 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ delay: i * 0.05 }}
                className="bg-white p-6 rounded-2xl border border-slate-100 shadow-sm hover:shadow-md transition-all group relative overflow-hidden"
              >
                <div className="flex flex-col md:flex-row gap-6">
                  {/* Logo Placeholder */}
                  <div className="w-24 h-24 bg-slate-50 border border-slate-100 rounded-2xl flex items-center justify-center shrink-0 group-hover:bg-blue-50 transition-all">
                    <Building className="w-10 h-10 text-slate-300 group-hover:text-blue-200" />
                  </div>

                  <div className="flex-1 space-y-4">
                    <div className="flex items-start justify-between">
                      <div>
                        <div className="flex items-center gap-3">
                          <h3 className="text-xl font-bold text-slate-900">{member.businessName}</h3>
                          <span className={cn(
                            "px-3 py-1 rounded-full text-[10px] font-bold uppercase tracking-wider",
                            member.feeStatus === 'Đã đóng' ? "bg-emerald-100 text-emerald-600" : "bg-amber-100 text-amber-600"
                          )}>
                            {member.feeStatus}
                          </span>
                        </div>
                        <p className="text-slate-500 font-medium mt-1 flex items-center gap-2 italic">
                          Đại diện: {member.representative} • 
                          <span className="flex items-center gap-1"><Tag className="w-3 h-3" /> {member.category}</span>
                        </p>
                      </div>
                      <button className="p-2 text-slate-400 hover:text-slate-600 hover:bg-slate-100 rounded-lg">
                        <MoreVertical className="w-5 h-5" />
                      </button>
                    </div>

                    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4 text-sm text-slate-600 pt-4 border-t border-slate-50">
                      <div className="flex items-center gap-2">
                        <CreditCard className="w-4 h-4 text-slate-400" />
                        MST: <span className="font-medium text-slate-900">{member.taxCode}</span>
                      </div>
                      <div className="flex items-center gap-2">
                        <Phone className="w-4 h-4 text-slate-400" />
                        SĐT: <span className="font-medium text-slate-900">{member.phone}</span>
                      </div>
                      <div className="flex items-center gap-2">
                        <Mail className="w-4 h-4 text-slate-400" />
                        Email: <span className="font-medium text-slate-900">{member.email}</span>
                      </div>
                      <div className="flex items-center gap-2 lg:col-span-2">
                        <MapPin className="w-4 h-4 text-slate-400" />
                        Đ/c: <span className="font-medium text-slate-900 truncate">{member.address}</span>
                      </div>
                      {member.website && (
                        <div className="flex items-center gap-2">
                          <ExternalLink className="w-4 h-4 text-slate-400" />
                          Web: <a href={`https://${member.website}`} className="text-blue-600 hover:underline">{member.website}</a>
                        </div>
                      )}
                    </div>
                  </div>
                </div>
              </motion.div>
            ))}
          </div>

          {filteredMembers.length === 0 && (
            <div className="text-center py-20 bg-slate-50 rounded-3xl border border-dashed border-slate-200">
              <Users className="w-16 h-16 text-slate-300 mx-auto mb-4" />
              <h3 className="text-lg font-bold text-slate-500">Không tìm thấy hội viên nào</h3>
              <p className="text-slate-400">Hãy thử thay đổi bộ lọc hoặc từ khóa tìm kiếm.</p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
