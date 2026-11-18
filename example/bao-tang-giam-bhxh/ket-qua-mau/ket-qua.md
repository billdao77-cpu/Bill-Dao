# Kết quả mẫu – Báo tăng, giảm, điều chỉnh BHXH tháng 11/2026

Công ty TNHH Công nghệ Bình Minh (giả lập), vùng I, làm việc thứ Hai – thứ Sáu. Số ngày làm việc đếm bằng công cụ `ngay_lam_viec`, tiền đóng tính bằng công cụ `luong_net_gross` (có trần) của plugin. Câu chữ AI trả lời có thể khác, **phương án và con số phải giống**.

File kết quả:
- **`D02-LT_thang-11-2026.xlsx`** – danh sách đúng bố cục **mẫu D02-LT theo QĐ 366/QĐ-BHXH** (phần A thông tin đơn vị, phần B cột A, B, 1–19, mã phương án ở cột 18), kèm sheet "Kiem tra" (không còn lỗi; 2 lưu ý TK1-TS). Tạo bằng công cụ `xuat_d02_lt`.
- `danh-sach-bao-tang-giam-thang-11.xlsx` – bảng làm việc nội bộ: lý do từng người + tiền đóng tháng 11.
- `huong-dan-nop.md` – các bước nộp trên phần mềm I-VAN cho đúng hồ sơ tháng này.

## 1. Danh sách kê khai tháng 11/2026

| # | Họ tên | Mã (cột 18) | Từ tháng | Mức lương đóng | Lý do |
|---|---|---|---|---:|---|
| 1 | Nguyễn Văn An | **TM** | 11/2026 | 13.000.000 | HĐLĐ 12 tháng; lương 12tr + phụ cấp trách nhiệm 1tr. **Không** cộng tiền ăn trưa (trả theo ngày công) [Cần kiểm tra] |
| 2 | Ngô Văn Khoa | **TM** | 11/2026 | 8.000.000 | Gọi là "cộng tác viên" nhưng làm giờ hành chính, chấm công → bản chất HĐLĐ (Điều 13 BLLĐ) → phải đóng |
| 3 | Phạm Thị Dung | **TS** | 11/2026 | 11.000.000 | Nghỉ từ 10/11: không làm việc 15 ngày làm việc trong tháng (≥ 14) → không đóng; thời gian nghỉ thai sản vẫn tính là thời gian đóng BHXH |
| 4 | Hoàng Văn Em | **KL** | 11/2026 | 9.000.000 | Nghỉ 09/11–30/11 = 16 ngày làm việc (≥ 14) → không đóng tháng 11; báo tăng lại khi đi làm |
| 5 | Vũ Thị Hoa | **DC** | 11/2026 | 17.000.000 | 15tr → 17tr theo QĐ 45/QĐ-BM |
| 6 | Bùi Quốc Long | **DC** | 11/2026 | 60.000.000 | BHXH, BHYT tính trên **trần 50.600.000**; BHTN tính trên 60.000.000 (trần BHTN vùng I 106.200.000) |
| 7 | Lê Văn Cường | **GH** | **12/2026** | 14.000.000 | Ngày làm cuối 13/11 → chỉ không làm việc 11 ngày làm việc trong tháng 11 (< 14) → **vẫn đóng tháng 11**, báo giảm từ tháng 12 |

**Không kê khai tháng này:**
- **Trần Thị Bình** – ký hợp đồng thử việc riêng, không phải HĐLĐ → chưa đóng; báo tăng khi ký HĐLĐ [Cần kiểm tra hướng dẫn hiện hành; nếu thử việc ghi ngay trong HĐLĐ thì phải đóng].
- **Đỗ Thị Giang** – nghỉ ốm 10 ngày làm việc (< 14) → vẫn đóng tháng 11; lập hồ sơ hưởng chế độ ốm đau.

Tháng 11/2026 có 21 ngày làm việc (đếm bằng công cụ `xac_dinh_dong_bhxh_thang`). Quy tắc dùng xuyên suốt: người lao động **không làm việc và không hưởng lương từ 14 ngày làm việc trở lên trong tháng** thì không đóng BHXH tháng đó.

## 2. Tiền đóng tháng 11 so với tháng 10

| | Tháng 10 (10 người) | Tháng 11 (10 người) |
|---|---:|---:|
| Người lao động đóng (10,5%) | 17.167.500 | **18.164.500** |
| Doanh nghiệp đóng (21,5%) | 35.152.500 | **37.095.500** |
| **Tổng nộp cơ quan BHXH** | 52.320.000 | **55.260.000** |

Chưa gồm kinh phí công đoàn 2%. Riêng ông Long: người lao động đóng 5.407.000 (không phải 6.300.000 nếu quên trần).

## 3. Lỗi hay gặp nếu làm tay (và ví dụ này đã tránh)

| Lỗi | Hậu quả |
|---|---|
| Báo giảm anh Cường ngay tháng 11 | Đóng thiếu 1 tháng → truy đóng, tiền chậm đóng; anh Cường hụt 1 tháng BHXH, BHTN |
| Không báo giảm chị Dung, anh Em | Đóng thừa 2 người; thủ tục thai sản của chị Dung bị vướng |
| Không báo tăng anh Khoa vì "chỉ là cộng tác viên" | Trốn đóng BHXH → truy đóng, phạt; rủi ro tranh chấp khi anh Khoa nghỉ |
| Cộng tiền ăn trưa vào mức đóng của anh An | Đóng thừa cho cả công ty và người lao động |
| Tính ông Long trên đủ 60 triệu | Trừ lương ông Long thừa 893.000đ mỗi tháng |
| Báo tăng chị Bình ngay khi thử việc | Đóng sai đối tượng, phải làm thủ tục thoái thu |

## 4. Giấy tờ và việc kèm theo

| Người | Việc phải làm |
|---|---|
| An, Khoa | Kê khai TK1-TS (chưa có mã số BHXH), ghi số định danh cá nhân; đính kèm HĐLĐ / hợp đồng "cộng tác viên" |
| Dung | Hướng dẫn nộp bản sao giấy khai sinh hoặc giấy chứng sinh để làm chế độ thai sản |
| Giang | Giấy ra viện → hồ sơ hưởng chế độ ốm đau |
| Cường | Chốt sổ, xác nhận thời gian đóng, trả giấy tờ trong 14 ngày làm việc kể từ ngày nghỉ việc (Điều 48 BLLĐ); hướng dẫn hưởng trợ cấp thất nghiệp (nộp hồ sơ trong 3 tháng) |
| Em | Tháng 12/2026 báo **ON** (đi làm lại sau KL từ 01/12/2026) |

## 5. Nộp hồ sơ

Xem `huong-dan-nop.md`. Tóm tắt: đăng nhập phần mềm I-VAN → thủ tục báo tăng, giảm, điều chỉnh (thường mã 600) → nhập 7 dòng theo file D02-LT (nhập tay, hoặc chép sang **mẫu Excel nhập liệu của chính phần mềm** rồi import) → TK1-TS cho An, Khoa → đính kèm giấy tờ → ký số, nộp → theo dõi kết quả.

## 6. HCNS vẫn phải tự làm

- Tải mẫu nhập liệu mới nhất trên phần mềm I-VAN đang dùng; file D02-LT theo QĐ 366 không chắc khớp cột với mẫu import của từng phần mềm.
- Đối chiếu quy chế lương: phụ cấp nào trả cố định thì phải tính vào mức đóng.
- Kê khai, ký số và nộp trên phần mềm I-VAN / Cổng dịch vụ công BHXH – plugin **không nộp thay**.
