import React, { useState, useMemo } from 'react';
import { useParams } from 'react-router-dom';
import { 
  Users, 
  Search, 
  Filter, 
  Plus, 
  MoreVertical, 
  MapPin, 
  Building2,
  Download,
  Mail,
  UserPlus
} from 'lucide-react';
import { BCH_MEMBERS } from '../data';
import { motion } from 'motion/react';
import { useAuth } from '../App';
import { cn } from '../lib/utils';

export default function Board() {
  const { type } = useParams<{ type: 'BCH' | 'BTV' | 'BKT' }>();
  const { user: currentUser } = useAuth();
  const [search, setSearch] = useState('');
  const [filterLocation, setFilterLocation] = useState('All');

  const boardTitle = useMemo(() => {
    switch (type) {
      case 'BCH': return 'Ban Chấp hành';
      case 'BTV': return 'Ban Thường vụ';
      case 'BKT': return 'Ban Kiểm tra';
      default: return 'Nhân sự Hiệp hội';
    }
  }, [type]);

  const filteredMembers = useMemo(() => {
    return BCH_MEMBERS.filter(m => {
      const matchesType = type === 'BCH' ? true : m.type === type;
      const matchesSearch = m.name.toLowerCase().includes(search.toLowerCase()) || 
                           m.organization.toLowerCase().includes(search.toLowerCase());
      const matchesLocation = filterLocation === 'All' || m.location === filterLocation;
      return matchesType && matchesSearch && matchesLocation;
    });
  }, [type, search, filterLocation]);

  const locations = useMemo(() => {
    const locs = new Set(BCH_MEMBERS.map(m => m.location).filter(l => l));
    return ['All', ...Array.from(locs)];
  }, []);

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <h1 className="text-2xl font-bold text-slate-900">{boardTitle}</h1>
          <p className="text-slate-500">Nhiệm kỳ I (2026 - 2031). Tổng số: {filteredMembers.length} đồng chí.</p>
        </div>
        <div className="flex items-center gap-3">
          <button className="bg-white border border-slate-200 text-slate-600 px-4 py-2 rounded-xl flex items-center gap-2 hover:bg-slate-50 transition-all font-medium text-sm shadow-sm">
            <Download className="w-4 h-4" />
            Xuất Excel
          </button>
          {currentUser?.role !== 'MEMBER' && (
            <button className="bg-blue-600 text-white px-4 py-2 rounded-xl flex items-center gap-2 hover:bg-blue-700 transition-all font-medium text-sm shadow-sm">
              <Plus className="w-4 h-4" />
              Thêm nhân sự
            </button>
          )}
        </div>
      </div>

      {/* Controls */}
      <div className="bg-white p-4 rounded-2xl shadow-sm border border-slate-100 flex flex-col md:flex-row gap-4">
        <div className="relative flex-1">
          <Search className="absolute left-3 top-1/2 -translate-y-1/2 text-slate-400 w-5 h-5" />
          <input 
            type="text" 
            placeholder="Tìm theo tên, đơn vị..." 
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            className="w-full bg-slate-50 border border-slate-100 rounded-xl py-2 pl-10 pr-4 outline-none focus:ring-2 focus:ring-blue-500 transition-all"
          />
        </div>
        <div className="flex items-center gap-3">
          <div className="flex items-center gap-2 bg-slate-50 border border-slate-100 rounded-xl px-3 py-2 text-sm text-slate-600">
            <Filter className="w-4 h-4" />
            <select 
              className="bg-transparent outline-none"
              value={filterLocation}
              onChange={(e) => setFilterLocation(e.target.value)}
            >
              <option value="All">Tất cả khu vực</option>
              {locations.filter(l => l !== 'All').map(l => (
                <option key={l} value={l}>{l}</option>
              ))}
            </select>
          </div>
        </div>
      </div>

      {/* Members Grid/List */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {filteredMembers.map((member, i) => (
          <motion.div
            key={member.id}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: i * 0.02 }}
            className={cn(
              "bg-white rounded-2xl border p-5 shadow-sm hover:shadow-md transition-all group",
              member.isVacant ? "border-dashed border-slate-300 bg-slate-50/50" : "border-slate-100"
            )}
          >
            <div className="flex items-start justify-between mb-4">
              <div className="w-14 h-14 rounded-2xl bg-blue-50 flex items-center justify-center text-blue-600 font-bold text-xl group-hover:bg-blue-600 group-hover:text-white transition-all shadow-sm">
                {member.name.charAt(0)}
              </div>
              <div className="flex items-center gap-2">
                <span className={cn(
                  "text-[10px] uppercase font-bold tracking-wider px-2 py-1 rounded-full",
                  member.type === 'BTV' ? "bg-purple-100 text-purple-600" : 
                  member.type === 'BKT' ? "bg-amber-100 text-amber-600" : 
                  "bg-blue-100 text-blue-600"
                )}>
                  {member.type}
                </span>
                <button className="text-slate-400 hover:text-slate-600">
                  <MoreVertical className="w-5 h-5" />
                </button>
              </div>
            </div>

            <div className="space-y-4">
              <div>
                <h3 className={cn(
                  "font-bold text-lg",
                  member.isVacant ? "text-slate-400 italic" : "text-slate-900"
                )}>
                  {member.name}
                </h3>
                <p className="text-blue-600 font-medium text-sm">{member.position}</p>
              </div>

              <div className="space-y-2 pt-4 border-t border-slate-50">
                <div className="flex items-center gap-2 text-sm text-slate-500">
                  <Building2 className="w-4 h-4 shrink-0 text-slate-400" />
                  <span className="truncate">{member.organization || 'Đang cập nhật'}</span>
                </div>
                <div className="flex items-center gap-2 text-sm text-slate-500">
                  <MapPin className="w-4 h-4 shrink-0 text-slate-400" />
                  <span>{member.location || 'Chưa xác định'}</span>
                </div>
              </div>

              {!member.isVacant && (
                <div className="pt-2 flex gap-2">
                  <button className="flex-1 bg-slate-50 hover:bg-blue-50 hover:text-blue-600 text-slate-600 py-2 rounded-lg text-xs font-bold transition-all border border-slate-100">
                    Liên hệ
                  </button>
                  <button className="flex-1 bg-slate-50 hover:bg-slate-100 text-slate-600 py-2 rounded-lg text-xs font-bold transition-all border border-slate-100">
                    Hồ sơ
                  </button>
                </div>
              )}
            </div>
          </motion.div>
        ))}
      </div>
    </div>
  );
}
