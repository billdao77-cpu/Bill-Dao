import React, { useState } from 'react';
import { 
  FileText, 
  Sparkles, 
  History, 
  ChevronRight, 
  Download, 
  Share2, 
  CheckSquare,
  Clock,
  User,
  AlertCircle
} from 'lucide-react';
import { GoogleGenAI } from '@google/genai';
import { motion, AnimatePresence } from 'motion/react';
import { MOCK_MEETINGS } from '../data';
import { cn } from '../lib/utils';

export default function MeetingsAI() {
  const [inputText, setInputText] = useState('');
  const [analyzing, setAnalyzing] = useState(false);
  const [result, setResult] = useState<any>(null);
  const [meetings, setMeetings] = useState(MOCK_MEETINGS);

  const handleAnalyze = async () => {
    if (!inputText.trim()) return;
    setAnalyzing(true);
    
    try {
      const genAI = new GoogleGenAI({ apiKey: process.env.GEMINI_API_KEY || '' });
      const model = genAI.getGenerativeModel({ model: "gemini-3-flash-preview" });
      
      const prompt = `
        Hãy đóng vai là một thư ký chuyên nghiệp của Hiệp hội Du lịch. 
        Phân tích nội dung biên bản họp sau đây và xuất kết quả dưới dạng JSON:
        - summary: Tóm tắt nội dung chính (1-2 câu).
        - conclusions: Các kết luận quan trọng (mảng chuỗi).
        - tasks: Danh sách nhiệm vụ, người chịu trách nhiệm và deadline (mảng object {task, PIC, deadline}).
        - suggestions: Gợi ý kế hoạch hành động tiếp theo.

        Nội dung cuộc họp:
        ${inputText}
      `;

      const response = await model.generateContent(prompt);
      const text = response.response.text();
      
      // Attempt to parse JSON from response
      const jsonMatch = text.match(/\{[\s\S]*\}/);
      if (jsonMatch) {
        const parsed = JSON.parse(jsonMatch[0]);
        setResult(parsed);
      } else {
        // Fallback if not JSON
        setResult({
          summary: text.substring(0, 200),
          conclusions: ["Xem chi tiết trong nội dung phân tích"],
          tasks: [],
          suggestions: "Dữ liệu không định dạng được JSON, vui lòng kiểm tra lại."
        });
      }
    } catch (error) {
      console.error(error);
      alert('Đã xảy ra lỗi khi gọi AI. Vui lòng thử lại.');
    } finally {
      setAnalyzing(true); 
      // Simulated delay for UI feel
      setTimeout(() => setAnalyzing(false), 1500);
    }
  };

  return (
    <div className="max-w-6xl mx-auto space-y-8">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-3">
          <div className="w-12 h-12 bg-purple-600 rounded-2xl flex items-center justify-center text-white shadow-lg shrink-0">
            <Sparkles className="w-6 h-6" />
          </div>
          <div>
            <h1 className="text-2xl font-bold text-slate-900">AI Biên bản họp</h1>
            <p className="text-slate-500">Tự động tóm tắt, trích xuất nhiệm vụ và gợi ý kế hoạch.</p>
          </div>
        </div>
        <button className="bg-white border border-slate-200 text-slate-600 px-4 py-2 rounded-xl flex items-center gap-2 hover:bg-slate-50 transition-all font-medium text-sm shadow-sm">
          <History className="w-4 h-4" />
          Lịch sử họp
        </button>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        {/* Input Side */}
        <div className="space-y-6">
          <div className="bg-white p-6 rounded-2xl border border-slate-200 shadow-sm space-y-4">
            <div className="flex items-center justify-between mb-2">
              <h3 className="font-bold text-slate-900">Nội dung cuộc họp</h3>
              <span className="text-[10px] uppercase font-bold text-slate-400">Dán văn bản hoặc tải file</span>
            </div>
            <textarea 
              value={inputText}
              onChange={(e) => setInputText(e.target.value)}
              placeholder="Nhập nội dung biên bản họp hoặc ghi chú thô tại đây..."
              className="w-full h-80 bg-slate-50 border border-slate-100 rounded-xl p-4 text-slate-700 outline-none focus:ring-2 focus:ring-purple-500 transition-all resize-none text-sm placeholder:italic"
            />
            <div className="flex items-center gap-3">
              <button 
                onClick={handleAnalyze}
                disabled={analyzing || !inputText.trim()}
                className="flex-1 bg-purple-600 hover:bg-purple-700 text-white font-bold py-3 px-6 rounded-xl transition-all shadow-lg shadow-purple-200 flex items-center justify-center gap-2 disabled:opacity-50"
              >
                {analyzing ? (
                  <div className="w-5 h-5 border-2 border-white border-t-transparent rounded-full animate-spin" />
                ) : (
                  <>
                    <Sparkles className="w-4 h-4" />
                    Phân tích bằng AI
                  </>
                )}
              </button>
              <button className="bg-slate-100 hover:bg-slate-200 text-slate-600 p-3 rounded-xl transition-all">
                <FileText className="w-5 h-5" />
              </button>
            </div>
          </div>

          <div className="bg-amber-50 border border-amber-100 p-4 rounded-xl flex gap-3 text-sm text-amber-800">
            <AlertCircle className="w-5 h-5 shrink-0" />
            <p>Mẹo: Sử dụng ghi âm sau đó chuyển thành văn bản (Speech-to-Text) sẽ cho kết quả tốt nhất khi đưa vào AI.</p>
          </div>
        </div>

        {/* Result Side */}
        <div className="relative">
          <AnimatePresence mode="wait">
            {!result && !analyzing ? (
              <motion.div 
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                className="h-full min-h-[400px] border-2 border-dashed border-slate-200 rounded-3xl flex flex-col items-center justify-center p-8 text-center"
              >
                <div className="w-20 h-20 bg-slate-100 rounded-full flex items-center justify-center text-slate-400 mb-4">
                  <FileText className="w-10 h-10" />
                </div>
                <h4 className="font-bold text-slate-400">Chưa có kết quả phân tích</h4>
                <p className="text-slate-400 text-sm mt-2 max-w-xs">Nhấn "Phân tích bằng AI" để trích xuất thông tin thông minh từ biên bản họp.</p>
              </motion.div>
            ) : analyzing ? (
              <motion.div 
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                className="h-full min-h-[400px] bg-white border border-slate-200 rounded-3xl p-8 flex flex-col items-center justify-center space-y-6"
              >
                <div className="relative">
                  <div className="w-24 h-24 border-4 border-purple-100 border-t-purple-600 rounded-full animate-spin" />
                  <Sparkles className="absolute left-1/2 top-1/2 -translate-x-1/2 -translate-y-1/2 w-8 h-8 text-purple-600 animate-pulse" />
                </div>
                <div className="text-center">
                  <h4 className="font-bold text-slate-900 text-lg">AI đang xử lý...</h4>
                  <p className="text-slate-500 text-sm mt-1 italic">Đang tóm tắt, trích xuất nhiệm vụ và phân vai trách nhiệm</p>
                </div>
              </motion.div>
            ) : (
              <motion.div 
                initial={{ opacity: 0, x: 20 }}
                animate={{ opacity: 1, x: 0 }}
                className="bg-white border border-slate-200 rounded-3xl p-8 shadow-xl space-y-8"
              >
                <div className="flex items-center justify-between">
                  <h3 className="font-black text-xl text-slate-900 bg-purple-50 text-purple-600 px-4 py-1 rounded-lg">AI REPORT</h3>
                  <div className="flex gap-2">
                    <button className="p-2 hover:bg-slate-100 rounded-lg text-slate-400"><Download className="w-5 h-5" /></button>
                    <button className="p-2 hover:bg-slate-100 rounded-lg text-slate-400"><Share2 className="w-5 h-5" /></button>
                  </div>
                </div>

                <div className="space-y-2">
                  <div className="flex items-center gap-2 text-xs font-bold text-slate-400 uppercase tracking-widest">
                    <FileText className="w-3 h-3" /> Tóm tắt
                  </div>
                  <p className="text-slate-700 leading-relaxed font-medium">{result.summary}</p>
                </div>

                <div className="space-y-4">
                  <div className="flex items-center gap-2 text-xs font-bold text-slate-400 uppercase tracking-widest">
                    <CheckSquare className="w-3 h-3" /> Nhiệm vụ cần thực hiện
                  </div>
                  <div className="space-y-3">
                    {result.tasks?.map((task: any, i: number) => (
                      <div key={i} className="p-4 rounded-2xl bg-slate-50 border border-slate-100 flex items-start gap-4">
                        <div className="mt-1"><div className="w-5 h-5 border-2 border-purple-400 rounded-full flex items-center justify-center text-xs text-white font-bold">{i+1}</div></div>
                        <div className="flex-1">
                          <p className="text-sm font-bold text-slate-900">{task.task}</p>
                          <div className="flex items-center gap-4 mt-2">
                            <div className="flex items-center gap-1 text-[11px] text-slate-500">
                              <User className="w-3 h-3" /> {task.PIC}
                            </div>
                            <div className="flex items-center gap-1 text-[11px] text-slate-500">
                              <Clock className="w-3 h-3" /> {task.deadline}
                            </div>
                          </div>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>

                <div className="p-5 bg-gradient-to-br from-purple-600 to-indigo-700 rounded-2xl text-white">
                  <div className="flex items-center gap-2 text-xs font-bold text-white/70 uppercase tracking-widest mb-2">
                    <Sparkles className="w-3 h-3" /> Gợi ý từ AI
                  </div>
                  <p className="text-sm leading-relaxed italic">{result.suggestions}</p>
                </div>
              </motion.div>
            )}
          </AnimatePresence>
        </div>
      </div>
    </div>
  );
}
