import React, { useState } from 'react';
import { 
  Store, 
  Search, 
  Plus, 
  ShoppingBag, 
  Tag, 
  Filter, 
  ArrowRight,
  MessageCircle,
  Eye
} from 'lucide-react';
import { MOCK_MARKETPLACE } from '../data';
import { motion } from 'motion/react';
import { useAuth } from '../App';
import { formatCurrency } from '../lib/utils';

export default function Marketplace() {
  const { user } = useAuth();
  const [search, setSearch] = useState('');
  const [category, setCategory] = useState('All');

  const categories = ['All', 'Tour du lịch', 'Phòng khách sạn', 'Đặc sản/OCOP', 'Quà tặng', 'Làng nghề', 'Dịch vụ vận chuyển'];

  return (
    <div className="space-y-8">
      {/* Hero Section */}
      <div className="relative rounded-3xl overflow-hidden bg-gradient-to-r from-blue-600 to-indigo-700 h-64 flex items-center p-12 text-white">
        <div className="relative z-10 max-w-2xl">
          <h1 className="text-4xl font-black mb-4">Marketplace Hội viên</h1>
          <p className="text-blue-100 text-lg">Khám phá sản phẩm, dịch vụ và ưu đãi đặc quyền từ cộng đồng Hiệp hội Du lịch Hưng Yên.</p>
        </div>
        <Store className="absolute right-[-20px] bottom-[-20px] w-80 h-80 text-white/10 rotate-12" />
      </div>

      {/* Main Content */}
      <div className="flex flex-col lg:flex-row gap-8">
        {/* Filters Sidebar */}
        <aside className="lg:w-64 space-y-8 shrink-0">
          <div>
            <h4 className="text-xs font-bold text-slate-400 uppercase tracking-widest mb-4">Phân loại</h4>
            <div className="space-y-1">
              {categories.map(cat => (
                <button
                  key={cat}
                  onClick={() => setCategory(cat)}
                  className={`w-full text-left px-3 py-2 rounded-lg text-sm font-medium transition-all ${
                    category === cat ? "bg-blue-50 text-blue-600" : "text-slate-600 hover:bg-slate-100"
                  }`}
                >
                  {cat === 'All' ? 'Tất cả sản phẩm' : cat}
                </button>
              ))}
            </div>
          </div>

          <div className="bg-slate-900 rounded-2xl p-6 text-white text-center space-y-4">
            <ShoppingBag className="w-10 h-10 mx-auto text-blue-400" />
            <h4 className="font-bold">Đăng bán sản phẩm</h4>
            <p className="text-white/60 text-xs leading-relaxed">Dành riêng cho hội viên chính thức của Hiệp hội.</p>
            <button className="w-full bg-blue-600 hover:bg-blue-500 py-2.5 rounded-xl font-bold transition-all text-sm">
              Tạo gian hàng
            </button>
          </div>
        </aside>

        {/* Product Grid */}
        <div className="flex-1 space-y-6">
          <div className="flex flex-col md:flex-row gap-4">
            <div className="relative flex-1">
              <Search className="absolute left-4 top-1/2 -translate-y-1/2 text-slate-400 w-5 h-5" />
              <input 
                type="text" 
                placeholder="Bạn đang tìm kiếm dịch vụ gì?..." 
                value={search}
                onChange={(e) => setSearch(e.target.value)}
                className="w-full bg-white border border-slate-200 rounded-2xl py-3 pl-12 pr-4 outline-none focus:ring-2 focus:ring-blue-500 shadow-sm"
              />
            </div>
            <button className="bg-white border border-slate-200 p-3 rounded-2xl text-slate-600 hover:bg-slate-50 transition-all font-medium">
              <Filter className="w-5 h-5" />
            </button>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-6">
            {MOCK_MARKETPLACE.map((item, i) => (
              <motion.div 
                key={item.id}
                initial={{ opacity: 0, scale: 0.95 }}
                animate={{ opacity: 1, scale: 1 }}
                transition={{ delay: i * 0.1 }}
                className="bg-white rounded-3xl border border-slate-100 overflow-hidden shadow-sm hover:shadow-xl transition-all group"
              >
                <div className="relative h-48 overflow-hidden">
                  <img src={item.images[0]} alt={item.title} className="w-full h-full object-cover group-hover:scale-110 transition-all duration-500" />
                  <div className="absolute top-4 left-4">
                    <span className="bg-black/50 backdrop-blur-md text-white text-[10px] font-bold uppercase tracking-widest px-3 py-1 rounded-full border border-white/20">
                      {item.category}
                    </span>
                  </div>
                </div>
                
                <div className="p-6 space-y-4">
                  <div className="space-y-1">
                    <h3 className="font-bold text-slate-900 line-clamp-2 min-h-[48px]">{item.title}</h3>
                    <p className="text-xl font-black text-blue-600">{item.price ? formatCurrency(item.price) : 'Liên hệ'}</p>
                  </div>
                  
                  <div className="flex items-center gap-2 text-xs text-slate-500">
                    <Tag className="w-3.5 h-3.5" />
                    <span>Chiết khấu hội viên: <span className="text-emerald-600 font-bold">10%</span></span>
                  </div>

                  <div className="flex gap-2 pt-2 border-t border-slate-50">
                    <button className="flex-1 bg-slate-50 hover:bg-slate-100 text-slate-900 py-2.5 rounded-xl text-xs font-bold transition-all flex items-center justify-center gap-2">
                      <Eye className="w-4 h-4" /> Chi tiết
                    </button>
                    <button className="flex-1 bg-blue-600 hover:bg-blue-700 text-white py-2.5 rounded-xl text-xs font-bold transition-all flex items-center justify-center gap-2">
                       Liên hệ
                    </button>
                  </div>
                </div>
              </motion.div>
            ))}

            {/* Empty State / Add Suggestion */}
            <div className="border-2 border-dashed border-slate-200 rounded-3xl p-8 flex flex-col items-center justify-center text-center space-y-4 bg-slate-50/50">
              <div className="w-16 h-16 bg-white rounded-2xl flex items-center justify-center text-slate-300 shadow-sm">
                <Plus className="w-8 h-8" />
              </div>
              <div>
                <h4 className="font-bold text-slate-400">Đăng tin của bạn</h4>
                <p className="text-slate-400 text-xs mt-1">Kết nối với mạng lưới hội viên ngay hôm nay.</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
