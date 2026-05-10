import React from 'react';
import { 
  Users, 
  UserSquare2, 
  Wallet, 
  Calendar, 
  TrendingUp, 
  Activity, 
  ArrowUpRight, 
  ArrowDownRight,
  MapPin,
  Clock,
  UserCircle,
  Sparkles
} from 'lucide-react';
import { 
  BarChart, 
  Bar, 
  XAxis, 
  YAxis, 
  CartesianGrid, 
  Tooltip, 
  ResponsiveContainer, 
  AreaChart, 
  Area,
  PieChart,
  Pie,
  Cell
} from 'recharts';
import { BCH_MEMBERS, MOCK_MEMBERS } from '../data';
import { formatCurrency, cn } from '../lib/utils';

const STATS_DATA = [
  { name: 'T1', value: 400 },
  { name: 'T2', value: 300 },
  { name: 'T3', value: 600 },
  { name: 'T4', value: 800 },
  { name: 'T5', value: 500 },
  { name: 'T6', value: 900 },
];

const CATEGORY_DATA = [
  { name: 'Lữ hành', value: 16 },
  { name: 'Lưu trú', value: 18 },
  { name: 'Ẩm thực', value: 13 },
  { name: 'Khác', value: 12 },
];

const COLORS = ['#3B82F6', '#10B981', '#F59E0B', '#8B5CF6'];

export default function Dashboard() {
  const totalBCH = 59;
  const vacantBCH = BCH_MEMBERS.filter(m => m.isVacant).length;
  const totalMembers = 242;
  const collectedFees = 120500000; // Mock value

  return (
    <div className="space-y-8">
      {/* Page Header */}
      <div>
        <h1 className="text-2xl font-bold text-slate-900">Tổng quan hệ thống</h1>
        <p className="text-slate-500">Chào mừng bạn quay trở lại. Đây là hoạt động hiệp hội trong 24h qua.</p>
      </div>

      {/* Stats Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        {[
          { label: 'Tổng Hội viên', value: totalMembers, icon: Users, color: 'blue', change: '+12%', up: true, indicator: 'blue' },
          { label: 'UV Ban Chấp hành', value: totalBCH - vacantBCH, icon: UserSquare2, color: 'orange', change: '2026-2031', up: true, indicator: 'orange' },
          { label: 'Quỹ Hội phí (YTD)', value: formatCurrency(collectedFees), icon: Wallet, color: 'emerald', change: '85% hoàn thành', up: true, indicator: 'emerald' },
          { label: 'Sản phẩm Marketplace', value: 1402, icon: Calendar, color: 'purple', change: 'Đang hoạt động', up: true, indicator: 'purple' },
        ].map((stat, i) => (
          <div key={i} className={cn(
            "stat-card p-5 h-32 flex flex-col justify-between",
            i === 0 ? "border-l-blue-600" : i === 1 ? "border-l-orange-500" : i === 2 ? "border-l-emerald-500" : "border-l-purple-500"
          )}>
            <div className="flex justify-between items-start">
              <span className="text-[10px] font-bold text-slate-500 uppercase tracking-wider">{stat.label}</span>
              <span className={cn(
                "text-[10px] font-bold px-2 py-0.5 rounded-full",
                i === 0 ? "text-blue-600 bg-blue-50" : i === 1 ? "text-orange-500 bg-orange-50" : i === 2 ? "text-emerald-600 bg-emerald-50" : "text-purple-600 bg-purple-50"
              )}>
                {stat.change}
              </span>
            </div>
            <div className="text-3xl font-bold text-slate-800">{stat.value}</div>
            <div className="text-[10px] text-slate-400 font-medium">
              {i === 0 ? "Đã xác thực hoạt động" : i === 1 ? "12 Thường vụ / 3 Kiểm tra" : i === 2 ? "Cập nhật 15 phút trước" : "Tour, OCOP, Lưu trú"}
            </div>
          </div>
        ))}
      </div>

      {/* Charts Grid */}
      <div className="grid grid-cols-12 gap-8">
        <div className="col-span-12 lg:col-span-8 glass-panel p-6 rounded-2xl shadow-sm">
          <div className="flex items-center justify-between mb-6">
            <h3 className="font-bold text-slate-800 text-sm uppercase tracking-wide flex items-center gap-2">
              <TrendingUp className="w-4 h-4 text-blue-500" />
              Tăng trưởng Hội viên
            </h3>
            <select className="bg-slate-50 border border-slate-200 rounded-lg px-3 py-1.5 text-[10px] font-bold uppercase tracking-widest outline-none">
              <option>6 tháng qua</option>
              <option>Năm nay</option>
            </select>
          </div>
          <div className="h-[300px] w-full">
            <ResponsiveContainer width="100%" height="100%">
              <AreaChart data={STATS_DATA}>
                <defs>
                  <linearGradient id="colorValue" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%" stopColor="#3B82F6" stopOpacity={0.15}/>
                    <stop offset="95%" stopColor="#3B82F6" stopOpacity={0}/>
                  </linearGradient>
                </defs>
                <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#F1F5F9" />
                <XAxis dataKey="name" axisLine={false} tickLine={false} tick={{fill: '#94A3B8', fontSize: 10, fontWeight: 600}} />
                <YAxis axisLine={false} tickLine={false} tick={{fill: '#94A3B8', fontSize: 10, fontWeight: 600}} />
                <Tooltip 
                  contentStyle={{ borderRadius: '12px', border: 'none', boxShadow: '0 4px 12px rgba(0,0,0,0.05)', fontSize: '12px' }}
                />
                <Area type="monotone" dataKey="value" stroke="#3B82F6" strokeWidth={3} fillOpacity={1} fill="url(#colorValue)" />
              </AreaChart>
            </ResponsiveContainer>
          </div>
        </div>

        <div className="col-span-12 lg:col-span-4 glass-panel p-6 rounded-2xl shadow-sm">
          <h3 className="font-bold text-slate-800 text-sm uppercase tracking-wide mb-6 flex items-center gap-2">
            <Activity className="w-4 h-4 text-purple-500" />
            Cơ cấu UV BCH
          </h3>
          <div className="h-[220px] w-full">
            <ResponsiveContainer width="100%" height="100%">
              <PieChart>
                <Pie
                  data={CATEGORY_DATA}
                  cx="50%"
                  cy="50%"
                  innerRadius={60}
                  outerRadius={80}
                  paddingAngle={8}
                  dataKey="value"
                  stroke="none"
                >
                  {CATEGORY_DATA.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                  ))}
                </Pie>
                <Tooltip />
              </PieChart>
            </ResponsiveContainer>
          </div>
          <div className="space-y-4 mt-6">
            {CATEGORY_DATA.map((item, i) => (
              <div key={i} className="flex items-center justify-between">
                <div className="flex items-center gap-3">
                  <div className="w-3 h-3 rounded-sm shadow-sm" style={{ background: COLORS[i] }} />
                  <span className="text-xs font-semibold text-slate-600">{item.name}</span>
                </div>
                <span className="text-xs font-bold text-slate-900 bg-slate-50 px-2 py-0.5 rounded border border-slate-100">{Math.round((item.value / 59) * 100)}%</span>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Bottom Grid */}
      <div className="grid grid-cols-12 gap-8">
        {/* Recent Activities */}
        <div className="col-span-12 lg:col-span-7 glass-panel rounded-2xl shadow-sm overflow-hidden flex flex-col">
          <div className="p-4 border-b border-slate-100 flex justify-between items-center bg-slate-50/50">
            <h3 className="text-xs font-bold text-slate-800 uppercase tracking-widest flex items-center gap-2">
              <Clock className="w-4 h-4 text-orange-500" />
              Hoạt động & Sự kiện
            </h3>
            <button className="text-[10px] font-bold text-blue-600 uppercase tracking-tighter hover:underline">Tất cả</button>
          </div>
          <div className="flex-1 overflow-y-auto custom-scrollbar p-6 space-y-6">
            {[
              { time: 'HÔM NAY - 14:30', title: 'Họp Ban Thường vụ định kỳ', detail: 'Văn phòng Hiệp hội', color: 'blue' },
              { time: '22/05/2024', title: 'Xúc tiến du lịch tại Hưng Yên', detail: 'Chương trình liên kết các tỉnh lân cận', color: 'emerald' },
              { time: '25/05/2024', title: 'Hạn cuối thu hội phí Quý II', detail: 'Áp dụng cho 145 đơn vị lưu trú', color: 'purple' },
            ].map((activity, i) => (
              <div key={i} className="flex gap-4 relative">
                {i !== 2 && <div className="absolute left-[11px] top-[28px] bottom-[-24px] w-0.5 bg-slate-100" />}
                <div className={cn(
                  "w-6 h-6 rounded-full border-4 border-white shadow-sm shrink-0 z-10",
                  activity.color === 'blue' ? "bg-blue-100" : activity.color === 'emerald' ? "bg-emerald-100" : "bg-purple-100"
                )} />
                <div>
                  <p className="text-[10px] text-slate-400 font-bold mb-0.5">{activity.time}</p>
                  <p className="text-xs font-bold text-slate-800">{activity.title}</p>
                  <p className="text-[10px] text-slate-500 mt-1 font-medium italic">{activity.detail}</p>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* AI Shortcut Card */}
        <div className="col-span-12 lg:col-span-5 bg-blue-600 text-white rounded-2xl p-6 shadow-xl relative overflow-hidden flex flex-col justify-between border-none">
          <Sparkles className="absolute right-[-20px] top-[-20px] w-40 h-40 text-white/10 rotate-12" />
          <div className="relative z-10 space-y-4">
            <div className="flex items-center gap-3">
              <div className="p-3 bg-blue-500/50 rounded-xl backdrop-blur-md border border-white/20">
                <Sparkles className="w-5 h-5 text-white" />
              </div>
              <div>
                <h3 className="text-sm font-bold uppercase tracking-wide">AI Meeting Assistant</h3>
                <p className="text-[10px] opacity-80 font-medium">Phân tích biên bản họp thông minh</p>
              </div>
            </div>
            
            <div className="bg-white/10 rounded-xl p-4 border border-white/10 backdrop-blur-sm">
              <p className="text-[11px] font-bold mb-2 opacity-70 flex items-center gap-1"><Clock className="w-3 h-3" /> Cuộc họp gần nhất:</p>
              <p className="text-xs italic leading-relaxed text-blue-50">"Triển khai kế hoạch xúc tiến du lịch mùa lễ hội Phố Hiến. Phê duyệt 12 hội viên mới thuộc nhóm OCOP..."</p>
            </div>
          </div>

          <button className="w-full py-3 mt-6 bg-white text-blue-700 rounded-xl text-xs font-bold shadow-lg shadow-blue-900/20 hover:scale-[1.02] transition-transform">
            Tải lên & Phân tích ngay
          </button>
        </div>
      </div>
    </div>
  );
}


