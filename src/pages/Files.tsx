import React, { useState } from 'react';
import { 
  FileBox, 
  Upload, 
  Search, 
  FileText, 
  Image as ImageIcon, 
  Archive, 
  Video, 
  MoreVertical, 
  Download, 
  Trash2, 
  Clock,
  HardDrive
} from 'lucide-react';
import { useDropzone } from 'react-dropzone';
import { motion, AnimatePresence } from 'motion/react';
import { cn } from '../lib/utils';

export default function Files() {
  const [files, setFiles] = useState([
    { id: '1', name: 'De_an_nhan_su_2026.pdf', type: 'pdf', size: '2.4 MB', category: 'Ban Chấp hành', date: '2026-04-10' },
    { id: '2', name: 'Quy_che_HHDL_Hung_Yen.docx', type: 'doc', size: '1.1 MB', category: 'Chính sách', date: '2026-03-15' },
    { id: '3', name: 'Logo_HHYTA_HighRes.png', type: 'image', size: '4.5 MB', category: 'Media', date: '2026-04-20' },
    { id: '4', name: 'Bien_ban_hop_T4.pdf', type: 'pdf', size: '890 KB', category: 'Biên bản', date: '2026-05-01' },
  ]);

  const onDrop = (acceptedFiles: File[]) => {
    const newFiles = acceptedFiles.map(file => ({
      id: Math.random().toString(36).substr(2, 9),
      name: file.name,
      type: file.type.split('/')[1] || 'unknown',
      size: `${(file.size / (1024 * 1024)).toFixed(1)} MB`,
      category: 'Tải lên mới',
      date: new Date().toISOString().split('T')[0]
    }));
    setFiles([...newFiles, ...files]);
  };

  const { getRootProps, getInputProps, isDragActive } = useDropzone({ onDrop });

  const getFileIcon = (type: string) => {
    switch (type) {
      case 'pdf': return <FileText className="text-red-500" />;
      case 'doc':
      case 'docx': return <FileText className="text-blue-500" />;
      case 'image':
      case 'png':
      case 'jpg': return <ImageIcon className="text-emerald-500" />;
      case 'zip':
      case 'rar': return <Archive className="text-amber-500" />;
      default: return <FileBox className="text-slate-400" />;
    }
  };

  return (
    <div className="space-y-8">
      {/* Header with Usage */}
      <div className="flex flex-col md:flex-row md:items-end justify-between gap-6">
        <div>
          <h1 className="text-2xl font-bold text-slate-900">Quản lý File & Tài liệu</h1>
          <p className="text-slate-500">Quản trị kho lưu trữ tài chính, nhân sự và sự kiện.</p>
        </div>
        <div className="bg-white p-4 rounded-2xl border border-slate-100 shadow-sm flex items-center gap-4 min-w-[300px]">
          <div className="w-12 h-12 bg-blue-50 rounded-xl flex items-center justify-center text-blue-600 shrink-0">
            <HardDrive className="w-6 h-6" />
          </div>
          <div className="flex-1">
            <div className="flex justify-between text-xs font-bold mb-1">
              <span className="text-slate-500 uppercase tracking-wider">Dung lượng sử dụng</span>
              <span className="text-slate-900">12.5 GB / 50 GB</span>
            </div>
            <div className="h-2 bg-slate-100 rounded-full overflow-hidden">
              <div className="h-full bg-blue-600 w-1/4 rounded-full" />
            </div>
          </div>
        </div>
      </div>

      {/* Upload Zone */}
      <div 
        {...getRootProps()} 
        className={cn(
          "border-2 border-dashed rounded-3xl p-12 transition-all cursor-pointer flex flex-col items-center justify-center text-center space-y-4",
          isDragActive ? "border-blue-500 bg-blue-50" : "border-slate-200 bg-white hover:bg-slate-50"
        )}
      >
        <input {...getInputProps()} />
        <div className="w-16 h-16 bg-blue-100 rounded-full flex items-center justify-center text-blue-600">
          <Upload className="w-8 h-8" />
        </div>
        <div>
          <p className="text-lg font-bold text-slate-900">Kéo thả file vào đây hoặc click để chọn</p>
          <p className="text-slate-500 mt-1 uppercase text-[10px] font-bold tracking-widest">Hỗ trợ: PDF, DOCX, XLXS, PNG, JPG, ZIP</p>
        </div>
      </div>

      {/* File List Header */}
      <div className="flex items-center justify-between">
        <h3 className="font-bold text-slate-900 flex items-center gap-2">
          Tất cả tài liệu
          <span className="bg-slate-100 text-slate-500 text-[10px] px-2 py-0.5 rounded-full">{files.length}</span>
        </h3>
        <div className="relative">
          <Search className="absolute left-3 top-1/2 -translate-y-1/2 text-slate-400 w-4 h-4" />
          <input 
            type="text" 
            placeholder="Tìm file..." 
            className="bg-white border border-slate-200 rounded-lg py-1.5 pl-9 pr-4 text-sm outline-none focus:ring-2 focus:ring-blue-500 w-64"
          />
        </div>
      </div>

      {/* Grid of Files */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        {files.map((file) => (
          <motion.div 
            key={file.id}
            layout
            initial={{ opacity: 0, scale: 0.9 }}
            animate={{ opacity: 1, scale: 1 }}
            className="bg-white p-5 rounded-2xl border border-slate-100 shadow-sm hover:shadow-md transition-all group relative"
          >
            <div className="flex items-start justify-between mb-4">
              <div className="p-3 bg-slate-50 rounded-xl">
                {getFileIcon(file.type)}
              </div>
              <button className="text-slate-400 hover:text-slate-600 opacity-0 group-hover:opacity-100 transition-all">
                <MoreVertical className="w-5 h-5" />
              </button>
            </div>
            
            <div className="space-y-1">
              <h4 className="font-bold text-slate-900 truncate text-sm" title={file.name}>{file.name}</h4>
              <p className="text-xs text-slate-400 font-medium">{file.size} • {file.category}</p>
            </div>

            <div className="mt-4 pt-4 border-t border-slate-50 flex items-center justify-between">
              <div className="flex items-center gap-1.5 text-[10px] text-slate-400 font-bold uppercase">
                <Clock className="w-3 h-3" /> {file.date}
              </div>
              <div className="flex gap-1">
                <button className="p-2 hover:bg-slate-100 rounded-lg text-slate-500 transition-all">
                  <Download className="w-4 h-4" />
                </button>
                <button className="p-2 hover:bg-red-50 rounded-lg text-red-400 transition-all">
                  <Trash2 className="w-4 h-4" />
                </button>
              </div>
            </div>
          </motion.div>
        ))}
      </div>
    </div>
  );
}
