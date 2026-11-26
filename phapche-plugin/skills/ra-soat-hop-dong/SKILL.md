---
name: ra-soat-hop-dong
description: Rà soát hợp đồng do đối tác gửi hoặc hợp đồng sắp ký để tìm rủi ro cho đúng bên của người dùng — chạy công cụ quét điều khoản (thiếu điều khoản, vừa Tòa án vừa Trọng tài, phạt vượt 8%, giá ngoại tệ, tự động gia hạn, miễn trừ trách nhiệm tuyệt đối, viện dẫn luật cũ, địa chỉ quận/huyện, số tiền bằng chữ sai), đọc kỹ theo checklist 10 nhóm, xếp rủi ro 3 mức, đề xuất câu chữ sửa thay thế (redline), câu hỏi cần làm rõ với đối tác, kết luận nên ký / ký sau khi sửa / không ký. Dùng khi người dùng nói "rà hợp đồng này", "hợp đồng đối tác gửi có rủi ro gì", "có nên ký không", "kiểm tra hợp đồng trước khi ký", "điều khoản nào bất lợi cho tôi", "sửa giúp các điều khoản bất lợi".
---

# Rà soát hợp đồng

Đọc trước: `references/nguyen-tac-chung.md`, `references/quy-dinh-phap-ly-2026.md`, `references/playbook-dieu-khoan.md`, `references/checklist-ra-soat.md`, `references/khung-chuc-nang.md` (mục 1).

## Quy trình 10 bước (bản vn-custom)

**1. Tiếp nhận** – đọc đúng file người dùng chỉ định (.docx/.pdf/.txt hoặc nội dung dán). File gốc **chỉ đọc**, không sửa, không ghi đè. PDF scan không trích được chữ → báo người dùng, không đoán nội dung.

**2. Xác định loại hợp đồng và mục đích giao dịch** – loại (mua bán, dịch vụ, gia công, đại lý, thuê, xây dựng, NDA…), luật điều chỉnh (BLDS 2015 / LTM 2005 / luật chuyên ngành), **người dùng là bên nào**, giá trị, quan hệ với đối tác, điểm người dùng lo nhất, hạn ký. Thiếu "bên nào" → hỏi; không hỏi được → ghi **[Giả định]** ở đầu báo cáo.

**3. Kiểm tra thông tin các bên** – theo nhóm 1 của checklist và mục 12 `nguyen-tac-chung.md`: tên, mã số doanh nghiệp, địa chỉ (địa giới mới), người đại diện, chức danh, căn cứ thẩm quyền ký (điều lệ, ủy quyền còn hạn, nghị quyết cho giao dịch cần chấp thuận), ngành nghề có điều kiện. Thông tin cần tra cứu bên ngoài (cổng đăng ký doanh nghiệp, cơ quan thuế) → liệt kê để người dùng tự tra hoặc đồng ý cho tra.

**4. Phân tích quyền và nghĩa vụ** – bảng ngắn: nghĩa vụ chính của mỗi bên, mốc thời hạn, điều kiện thanh toán, hậu quả khi vi phạm. Chỉ ra chỗ **không cân bằng** (một bên chịu phạt, bên kia không; quyền chấm dứt một chiều).

**5. Phát hiện điều khoản bất lợi, thiếu, mâu thuẫn** – chạy `quet_dieu_khoan_hop_dong` (`python3 scripts/cong_cu.py quet_dieu_khoan_hop_dong duong_dan=...`) để sàng lọc, rồi **đọc toàn văn** theo 10 nhóm `checklist-ra-soat.md`. Tập trung: thanh toán, phạt vi phạm, bồi thường – giới hạn trách nhiệm, chấm dứt, bảo mật – dữ liệu cá nhân, SHTT, bất khả kháng, giải quyết tranh chấp. Tính lại con số bằng công cụ: `kiem_tra_phat_vi_pham`, `lai_cham_tra`, `doc_so_thanh_chu`, `thoi_hieu_khoi_kien`.

**6. Đánh giá mức rủi ro** – mỗi rủi ro chấm Khả năng (1–5) × Ảnh hưởng (1–5) bằng `danh_gia_rui_ro` → **Thấp / Trung bình / Cao / Nghiêm trọng**. Không phóng đại: chỉ Nghiêm trọng khi có thể mất tiền lớn, điều khoản/hợp đồng vô hiệu, trách nhiệm không giới hạn, hoặc rủi ro hình sự.

**7. Đề xuất phương án sửa** – câu chữ thay thế cụ thể (lấy từ `playbook-dieu-khoan.md` khi phù hợp) + **phương án lùi** nếu đối tác không đồng ý. Đề xuất là bản đề nghị trong bảng, **không** sửa vào văn bản gốc.

**8. Đối chiếu căn cứ pháp luật** – mỗi dòng ghi căn cứ (văn bản, số hiệu, điều – khoản) và nhãn: **[Quy định đã xác minh]** / **[Nhận định chuyên môn]** / **[Giả định]** / **[Cần luật sư / người có thẩm quyền]** (mục 9–10 `nguyen-tac-chung.md`). Kiểm tra thời điểm áp dụng – đặc biệt Luật Thương mại sửa đổi hiệu lực 01/7/2027.

**9. Xuất báo cáo rà soát** – đúng thứ tự:
1. **Kết luận 1 dòng**: Có thể ký / Ký sau khi xử lý N rủi ro Cao–Nghiêm trọng / Không nên ký – lý do chính. Kèm [Giả định] đã dùng.
2. **Bảng rủi ro** (sắp theo mức, Nghiêm trọng trước):

| # | Điều khoản | Nội dung hiện tại (trích nguyên văn) | Rủi ro cho bên [người dùng] | Mức độ | Đề xuất sửa (+ phương án lùi) | Căn cứ + nhãn |
|---|---|---|---|---|---|---|

3. **Điều khoản còn thiếu** (kèm câu chữ mẫu).
4. **Thông tin còn thiếu / mâu thuẫn** (bảng Đã có – Còn thiếu – Mâu thuẫn).
5. **Câu hỏi cần đối tác làm rõ**.
6. **Không kết luận được / cần luật sư**.
Người dùng muốn file: xuất Word **mới** (`YYYY-MM-DD_Ra-soat_<ten-hop-dong>.docx`); khi cần tách bản gửi đối tác và bản nội bộ → `bang_gop_y_hop_dong`.

**10. Chuyển người có thẩm quyền phê duyệt** – cuối báo cáo thêm khối:
`Người rà soát: … · Ngày: … · Đề xuất: ☐ Ký ☐ Ký sau khi sửa ☐ Không ký · Người có thẩm quyền duyệt: … · Ý kiến: …`
Trợ lý **không** quyết định ký, không gửi đối tác, không gửi đi ký điện tử.

**Kiểm tra lại trước khi trả kết quả**: mọi dòng trong bảng có trích nguyên văn đúng vị trí; số liệu đã tính bằng công cụ; không có câu "hợp đồng hợp pháp/an toàn"; mỗi căn cứ có nhãn; không sửa gì ngoài bảng đề xuất. Văn bản quan trọng → đề nghị chạy agent `tham-dinh-phap-ly` và/hoặc `luat-su-doi-phuong` (góc nhìn đối tác).

**Bản sửa (nếu người dùng yêu cầu)** – file **mới** có đánh dấu `[SỬA]`/`[THÊM]`/`[XÓA]` hoặc bảng redline; chuẩn bị đàm phán → skill `dam-phan-hop-dong`.

## Nguyên tắc
- Không phóng đại rủi ro để tỏ ra kỹ lưỡng: chỉ 🔴 khi hậu quả thật sự nghiêm trọng.
- Không khẳng định "hợp đồng hợp pháp/an toàn"; nói "chưa phát hiện thêm rủi ro trong phạm vi đã rà".
- Hợp đồng có yếu tố nước ngoài, giá trị lớn, M&A, bất động sản, vay vốn → khuyến nghị luật sư rà soát.

<!-- KET-NOI:BAT-DAU (sinh tự động từ scripts/ket_noi.json – sửa ở đó rồi chạy build) -->
## Kết nối ứng dụng

Connector dùng cho skill này: **Google Drive** · **Gmail** · **Microsoft 365 (Outlook, OneDrive/SharePoint, Teams)**. Đọc quy tắc trong `references/ket-noi.md` trước khi dùng.

1. Mở hợp đồng cần rà trực tiếp từ Drive hoặc tệp đính kèm trong thư đối tác gửi (`from:doitac has:attachment filename:docx`).
2. Đọc chuỗi email trao đổi trước đó để biết điều khoản nào đã thỏa thuận miệng mà hợp đồng chưa ghi.
3. Lưu báo cáo rà soát và bản sửa đề xuất thành file mới cạnh file gốc; không ghi đè bản của đối tác.

**Khi chưa kết nối:** làm đủ phần soạn thảo, tính toán; đưa nội dung sẵn để người dùng tự dán vào email, lịch, thư mục; nhắc **một lần** cách bật connector, không dừng việc chỉ vì chưa kết nối.
<!-- KET-NOI:KET-THUC -->
