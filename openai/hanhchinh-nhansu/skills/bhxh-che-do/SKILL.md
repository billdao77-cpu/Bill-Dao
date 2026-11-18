---
name: bhxh-che-do
description: Hướng dẫn nghiệp vụ bảo hiểm xã hội, bảo hiểm y tế, bảo hiểm thất nghiệp cho phòng HCNS theo Luật BHXH 2024 (hiệu lực 01/7/2025) và Luật Việc làm 2025 (hiệu lực 01/01/2026) — đối tượng tham gia bắt buộc (HĐLĐ từ đủ 1 tháng), tiền lương đóng và mức trần (50,6 triệu từ 01/7/2026), báo tăng/giảm/điều chỉnh, chế độ ốm đau, thai sản (lao động nữ sinh con, chồng nghỉ khi vợ sinh, khám thai, trợ cấp một lần), dưỡng sức phục hồi, tai nạn lao động – bệnh nghề nghiệp, trợ cấp thất nghiệp (điều kiện 12/24 tháng, nộp hồ sơ trong 3 tháng), chốt sổ, hồ sơ và thời hạn; soạn danh sách đề nghị, hướng dẫn NLĐ. Dùng khi người dùng nói "báo tăng BHXH", "nhân viên nghỉ thai sản", "chồng nghỉ mấy ngày khi vợ sinh", "nghỉ ốm được hưởng bao nhiêu", "chốt sổ bảo hiểm", "nhân viên nghỉ việc hưởng thất nghiệp thế nào", "mức đóng BHXH tối đa", "cộng tác viên có phải đóng BHXH".
---

# BHXH – BHYT – BHTN

Đọc trước: `references/nguyen-tac-chung.md`, `references/quy-dinh-lao-dong-2026.md`, `references/che-do-bhxh.md`, và khi kê khai tăng/giảm/điều chỉnh: `references/huong-dan-d02-lt.md`.

> Hồ sơ nộp qua phần mềm kê khai BHXH điện tử (I-VAN) hoặc Cổng dịch vụ công BHXH; mẫu biểu do BHXH Việt Nam ban hành, **thay đổi thường xuyên** → luôn nhắc người dùng tải mẫu mới nhất trên phần mềm/cổng. Plugin chuẩn bị số liệu, danh sách, hướng dẫn – **không nộp thay**.

## Việc thường gặp

### 1. Ai phải tham gia BHXH bắt buộc?
HĐLĐ (kể cả tên gọi khác nhưng có nội dung HĐLĐ) **từ đủ 1 tháng trở lên** [Chắc chắn – Luật BHXH 2024]; người quản lý doanh nghiệp, kiểm soát viên, thành viên HĐQT/HĐTV có hưởng tiền lương [Chắc chắn]; NLĐ làm việc không trọn thời gian có tiền lương tháng ≥ mức theo luật [Cần kiểm tra mức]; lao động nước ngoài có giấy phép lao động (trừ ngoại lệ) [Cần kiểm tra]. "Cộng tác viên" có chấm công, chịu quản lý → bản chất HĐLĐ → phải đóng.

### 2. Mức đóng
`luong_net_gross` cho từng người (trần BHXH/BHYT 20 × lương cơ sở – 46,8 triệu đến 30/6/2026, 50,6 triệu từ 01/7/2026; trần BHTN 20 × lương tối thiểu vùng). Tỷ lệ: NLĐ 10,5%, DN 21,5% (+ KPCĐ 2%). Bảng lương chính thức → bộ kế toán.

### 3. Báo tăng / giảm / điều chỉnh (Mẫu D02-LT theo QĐ 366/QĐ-BHXH)
Phát sinh trong tháng → kê khai trong tháng. Người trong danh sách đang đóng mà không có biến động thì giữ nguyên, không kê khai. Trình tự:
1. **Từng người có biến động → có đóng tháng đó không:** chạy `python3 scripts/cong_cu.py xac_dinh_dong_bhxh_thang thang=11/2026 khoang_nghi='[{"tu_ngay":"16/11/2026","loai":"nghi_viec"}]'` (người mới: `ngay_bat_dau_lam=`). Mốc: không làm việc từ 14 ngày làm việc trở lên trong tháng (tính từ mùng 1) thì không đóng; nghỉ việc giữa tháng chưa đủ 14 ngày → vẫn đóng, báo GH từ tháng sau.
2. **Chọn mã phương án** (TM, ON, DC, CD, GH, TS, OF, KL...) và ghi chú bắt buộc theo bảng ở `references/huong-dan-d02-lt.md` mục 3. Chặn các lỗi hay gặp: "cộng tác viên" chấm công là HĐLĐ → TM; hợp đồng thử việc riêng chưa báo tăng [Cần kiểm tra]; khoản trả theo ngày công thực tế (ăn trưa) không đưa vào mức đóng [Cần kiểm tra]; giám đốc vượt trần chỉ đóng BHXH, BHYT trên trần.
3. **Tính tiền đóng** bằng `luong_net_gross` (có trần) – tổng trước và sau biến động.
4. **Xuất file hướng dẫn kê khai (ĐẦU RA CHÍNH)** bằng `python3 scripts/cong_cu.py huong_dan_ke_khai_bhxh duong_dan_ra=huong-dan-ke-khai-thang-11.docx thang=11/2026 danh_sach='[...]' don_vi='{...}' khong_ke_khai='[...]' tien_dong='{...}' phan_mem=ibh` (`ibh` | `cong_bhxh` | `chung` – hỏi người dùng đang dùng phần mềm nào). File Word để người chưa có nghiệp vụ làm theo từ trên xuống: tóm tắt + tổng tiền + hạn đóng; thông tin còn thiếu kèm tin nhắn xin người lao động; hồ sơ nộp gì (tăng, giảm, điều chỉnh **nộp chung 1 hồ sơ 600**, TK1-TS cho người chưa có mã số BHXH, hồ sơ nào làm riêng); khối "gõ vào phần mềm" cho từng người (tab, phương án, từ tháng, lương, ghi chú chép nguyên văn); giấy tờ đính kèm; ai không kê khai và vì sao; thao tác trên phần mềm; sau khi nộp; việc tháng sau. Mỗi người cần thêm `ly_do` (giải thích ngắn); người mới cần đủ trường TK1-TS (giới tính, số định danh, ngày cấp, dân tộc, quốc tịch, số điện thoại, nơi khai sinh, địa chỉ, nơi KCB) – thiếu thì để trống, công cụ tự liệt kê, **không tự điền**.
5. **File D02-LT** (`xuat_d02_lt`) chỉ xuất khi người dùng cần lưu hồ sơ, trình duyệt hoặc nộp giấy – phần mềm kê khai tự tạo D02-LT khi gõ tay, nên không xuất mặc định. Nếu phần mềm có chức năng nhập Excel và người dùng đưa file mẫu của phần mềm, chép dữ liệu đúng cột của file đó; không đoán cột.

### 4. Chế độ ốm đau, thai sản, dưỡng sức
Tra `references/che-do-bhxh.md` → nêu: điều kiện, số ngày, mức hưởng, giấy tờ NLĐ nộp, việc DN làm, hạn. Tính ngày nghỉ (ngày làm việc hay ngày lịch – mỗi chế độ khác nhau) bằng `ngay_lam_viec`/`cong_ngay_lich`. Số tiền: nêu công thức + tham số (lương bình quân đóng BHXH 6 tháng, lương cơ sở) – số chính xác do cơ quan BHXH duyệt.

### 5. Nghỉ việc – chốt sổ – thất nghiệp
- Báo giảm; hoàn thành thủ tục xác nhận thời gian đóng BHXH, trả lại giấy tờ cho NLĐ (Điều 48 BLLĐ). Nợ BHXH thì phải đóng đủ mới xác nhận được.
- Hướng dẫn NLĐ trợ cấp thất nghiệp: điều kiện chính – đóng BHTN đủ **12 tháng trong 24 tháng** trước khi chấm dứt HĐ; nộp hồ sơ tại trung tâm dịch vụ việc làm **trong 03 tháng** kể từ ngày chấm dứt; không thuộc trường hợp đơn phương chấm dứt trái luật, hưởng lương hưu (Luật Việc làm 2025) [Chắc chắn về các mốc chính; chi tiết mức hưởng – cần kiểm tra nghị định].

### 6. Tai nạn lao động
Sơ cứu, cấp cứu → khai báo, điều tra theo Luật ATVSLĐ → DN trả chi phí y tế đến khi ổn định, trả đủ lương trong thời gian điều trị; BHXH chi trả theo mức suy giảm khả năng lao động. Hướng dẫn biên bản, khai báo [Cần kiểm tra mẫu hiện hành].

## Đầu ra
Kết luận có phải đóng/được hưởng không (kèm căn cứ + nhãn) · file Word hướng dẫn kê khai (tăng/giảm/điều chỉnh từng người, thông tin còn thiếu, hồ sơ nộp gì, thao tác, hạn đóng tiền) · file D02-LT khi được yêu cầu · hướng dẫn từng bước cho NLĐ (gửi Zalo/email dạng nháp) · lịch hạn · cảnh báo mẫu biểu cần tải mới.

<!-- KET-NOI:BAT-DAU (sinh tự động từ scripts/ket_noi.json – sửa ở đó rồi chạy build) -->
## Kết nối ứng dụng

Connector dùng cho skill này: **Google Drive** · **Gmail** · **Google Calendar** · **Microsoft 365 (Outlook, OneDrive/SharePoint, Teams)**. Đọc quy tắc trong `references/ket-noi.md` trước khi dùng.

1. Đọc danh sách lao động, bảng lương trên Drive để lập danh sách báo tăng/giảm, tính mức đóng.
2. Tìm email thông báo của cơ quan BHXH, giấy tờ người lao động gửi (giấy khai sinh, giấy ra viện) để lập hồ sơ chế độ.
3. Tạo nhắc hạn nộp hồ sơ, hạn đóng BHXH hằng tháng trên lịch người phụ trách.

**Khi chưa kết nối:** làm đủ phần soạn thảo, tính toán; đưa nội dung sẵn để người dùng tự dán vào email, lịch, thư mục; nhắc **một lần** cách bật connector, không dừng việc chỉ vì chưa kết nối.
<!-- KET-NOI:KET-THUC -->
