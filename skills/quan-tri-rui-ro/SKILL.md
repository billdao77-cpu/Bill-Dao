---
name: quan-tri-rui-ro
description: Quản trị rủi ro pháp lý hợp đồng cho doanh nghiệp Việt Nam — lập sổ rủi ro cho một hợp đồng hoặc danh mục hợp đồng, chấm mức rủi ro thống nhất 4 mức Thấp/Trung bình/Cao/Nghiêm trọng theo ma trận Khả năng × Ảnh hưởng, biện pháp kiểm soát (sửa điều khoản, bảo lãnh, bảo hiểm, giữ lại tiền, theo dõi mốc, chấp nhận rủi ro), người phụ trách, mốc xem lại, rủi ro cần người có thẩm quyền chấp nhận, báo cáo rủi ro định kỳ. Dùng khi người dùng nói "lập bảng rủi ro", "sổ rủi ro hợp đồng", "đánh giá mức độ rủi ro", "ma trận rủi ro", "rủi ro nào cần báo giám đốc", "kiểm soát rủi ro hợp đồng đang thực hiện".
---

# Quản trị rủi ro hợp đồng

Đọc trước: `references/nguyen-tac-chung.md`, `references/khung-chuc-nang.md` (mục 4).

## Quy trình
1. **Thu thập rủi ro** – từ báo cáo rà soát (`ra-soat-hop-dong`), so sánh phiên bản, tình hình thực hiện (chậm thanh toán, chậm giao hàng, thay đổi pháp luật) hoặc danh sách người dùng đưa. Xác định bên người dùng.
2. **Chuẩn hóa mô tả** – mỗi rủi ro: *sự kiện* → *hậu quả cho bên người dùng* → *điều khoản/nguồn*. Ví dụ: "Bên bán giao chậm (Điều 5) → dây chuyền dừng, không có phạt vì Điều 9 miễn trừ".
3. **Chấm mức** – `python3 scripts/cong_cu.py danh_gia_rui_ro '{"ben_nguoi_dung": "...", "danh_sach": [{"dieu": "...", "rui_ro": "...", "kha_nang": 1-5, "anh_huong": 1-5}]}'`. Giải thích ngắn vì sao chọn điểm; thiếu thông tin → chấm thận trọng và ghi **[Giả định]**.
4. **Biện pháp** – với mỗi rủi ro Trung bình trở lên: sửa điều khoản (câu chữ từ playbook), biện pháp bảo đảm (bảo lãnh, đặt cọc, giữ lại tiền bảo hành), bảo hiểm, quy trình nội bộ (theo dõi mốc, nghiệm thu chặt), hoặc **chấp nhận rủi ro** – chỉ người có thẩm quyền quyết định chấp nhận.
5. **Giao trách nhiệm** – người phụ trách, mốc xem lại (Nghiêm trọng/Cao: trước khi ký hoặc hằng tháng; Trung bình: hằng quý).
6. **Báo cáo** – rủi ro Cao/Nghiêm trọng đưa lên đầu, kèm đề xuất quyết định.

## Đầu ra
1. Tóm tắt: số rủi ro theo mức, gợi ý kết luận của công cụ, rủi ro cần quyết định.
2. Sổ rủi ro: `# | Hợp đồng/Điều | Rủi ro (sự kiện → hậu quả) | Khả năng | Ảnh hưởng | Mức | Biện pháp | Người phụ trách | Mốc xem lại | Căn cứ + nhãn | Trạng thái`.
3. Ma trận 5×5 (chữ hoặc bảng) đặt mã rủi ro vào ô.
4. Xuất Excel/Word khi người dùng yêu cầu: **file mới**, không ghi đè sổ cũ.

## Giới hạn và kiểm tra lại
- Điểm số là **[Nhận định chuyên môn]**, không phải kết luận pháp lý; không đổi điểm để "đẹp" báo cáo.
- Không tự đánh dấu rủi ro là "đã xử lý" khi chưa có bằng chứng (bản sửa đã ký, bảo lãnh đã nhận).
- Rủi ro có dấu hiệu tranh chấp, hình sự, yếu tố nước ngoài → **[Cần luật sư / người có thẩm quyền]**.
- Kiểm tra lại: mọi rủi ro Cao/Nghiêm trọng đều có biện pháp và người phụ trách; mô tả đủ sự kiện → hậu quả → nguồn.
