---
name: cham-cong-tinh-luong
description: Rà soát bảng chấm công và tính tiền làm thêm giờ, làm việc ban đêm cho phòng HCNS doanh nghiệp Việt Nam theo Điều 98, 105–107 BLLĐ 2019 và NĐ 145/2020 — kiểm tra dữ liệu chấm công (ngày trùng, ngày sai, giờ âm hoặc quá 24 giờ, giờ bình thường vào ngày nghỉ, thiếu ngày), phân loại ngày thường/nghỉ hằng tuần/lễ Tết, giới hạn làm thêm (50% giờ bình thường/ngày hoặc 12 giờ/ngày, 40 giờ/tháng, 200 hoặc 300 giờ/năm), tiền lương giờ, hệ số 150%/200%/300%, ban đêm +30%, làm thêm ban đêm 200%/210%/270%/390%, đối chiếu ngày công với bảng lương. Dùng khi người dùng nói "kiểm tra bảng chấm công", "tính tiền tăng ca", "làm thêm giờ có vượt không", "lương làm đêm", "đi làm ngày lễ được bao nhiêu", "chốt công tháng".
---

# Chấm công – Làm thêm giờ

Đọc trước: `references/nguyen-tac-chung.md`, `references/quy-dinh-lao-dong-2026.md`.

> Skill này lo **dữ liệu công** và **tiền làm thêm/ban đêm**. Bảng lương chính thức (BHXH, thuế TNCN, quyết toán) do kế toán chốt; ước tính gross ↔ net dùng `luong_net_gross`. Mọi kết quả là **bảng tính tham khảo** – người làm lương và người có thẩm quyền duyệt trước khi chi trả.

## A. Nhận và kiểm tra dữ liệu chấm công

1. Hỏi đủ trước khi tính: kỳ công (tháng/năm), chế độ giờ làm (theo ngày hay theo tuần), số giờ bình thường/ngày, ngày nghỉ hằng tuần (có nghỉ thứ Bảy không), số ngày công chuẩn trong quy chế lương, tiền lương thực trả làm căn cứ tính lương giờ, ngành nghề có thuộc trường hợp được làm đến 300 giờ/năm không, số giờ làm thêm lũy kế từ đầu năm.
2. Dữ liệu Excel/CSV: đọc file người dùng chỉ; chỉ lấy cột cần (mã/họ tên, ngày, giờ vào – ra hoặc số giờ, ghi chú nghỉ). **Không chép bảng công, lương sang file khác** ngoài file kết quả người dùng yêu cầu.
3. Chạy `python3 scripts/cong_cu.py kiem_tra_gio_lam_them '{"bang_cham_cong": [...], "so_gio_binh_thuong_ngay": 8}'` cho **từng người**. Công cụ báo: dòng lỗi dữ liệu, ngày trùng, ngày ở tương lai, giờ bình thường vào ngày nghỉ, vi phạm giới hạn, tổng giờ theo loại ngày.
4. Tự rà thêm các mâu thuẫn công cụ không thấy: ngày công > số ngày trong tháng; có công trong thời gian nghỉ thai sản/ốm/không lương; ngày vào làm sau ngày có công; người đã nghỉ việc vẫn có công; giờ vào – ra không khớp số giờ khai; làm thêm không có phiếu đề nghị/đồng ý của NLĐ.
5. Lỗi dữ liệu → ghi vào bảng **Cần xác minh** (người, ngày, vấn đề, cần ai xác nhận). **Không tự sửa số công**, không đoán giờ.

## B. Giới hạn làm thêm giờ (Điều 107 BLLĐ 2019) [Chắc chắn]

| Giới hạn | Mức |
|---|---|
| Đồng ý của NLĐ | Bắt buộc (trừ trường hợp Điều 108) |
| Theo ngày | ≤ 50% số giờ làm việc bình thường/ngày; chế độ theo tuần: giờ bình thường + làm thêm ≤ 12 giờ/ngày |
| Theo tháng | ≤ 40 giờ |
| Theo năm | ≤ 200 giờ; ≤ 300 giờ với ngành nghề, công việc tại khoản 3 Điều 107 – phải thông báo Sở Nội vụ |

Nghị quyết nới giới hạn tạm thời trước đây (NQ 17/2022/UBTVQH15) đã hết hiệu lực; nếu người dùng nhắc một văn bản mới → xác minh hiệu lực trước khi áp dụng. [Cần kiểm tra khi có văn bản mới]

## C. Tính tiền làm thêm, ban đêm

`python3 scripts/cong_cu.py tinh_luong_lam_them luong_thang=... so_ngay_lam_viec_thang=26 so_gio_ngay=8 gio_ngay_thuong=... gio_nghi_hang_tuan=... gio_le_tet=... gio_dem_ngay_thuong=...`

| Trường hợp | Mức tối thiểu so với lương giờ ngày thường |
|---|---|
| Làm thêm ngày thường / nghỉ hằng tuần / lễ, Tết, nghỉ có hưởng lương | 150% / 200% / 300% |
| Làm việc ban đêm (22h–6h) trong giờ bình thường | +30% |
| Làm thêm ban đêm ngày thường (chưa / đã làm thêm ban ngày) | 200% / 210% |
| Làm thêm ban đêm ngày nghỉ hằng tuần / lễ, Tết | 270% / 390% |

- Tiền lương giờ = tiền lương thực trả của tháng ÷ số ngày làm việc bình thường theo quy chế ÷ số giờ/ngày. Hỏi quy chế lương nếu chưa rõ khoản nào được tính (mức lương, phụ cấp lương, bổ sung xác định được mức tiền).
- NLĐ hưởng lương ngày làm thêm vào ngày lễ còn được hưởng lương ngày lễ.
- Mức trong HĐLĐ, thỏa ước, quy chế cao hơn → áp dụng mức cao hơn.
- Ngày lễ, nghỉ bù: công cụ tính theo Điều 112 BLLĐ 2019; năm có quyết định hoán đổi ngày làm việc → hỏi người dùng và điều chỉnh.

## D. Đầu ra

1. **Bảng kiểm tra công** theo người: tổng giờ bình thường, giờ làm thêm theo loại ngày, kết luận (Trong giới hạn / Có vi phạm / Cần sửa dữ liệu).
2. **Bảng tính tiền làm thêm, ban đêm** theo người: số giờ × hệ số × lương giờ, tổng; ghi tham số đã dùng.
3. **Bảng Cần xác minh** (lỗi dữ liệu, mâu thuẫn) và **Vi phạm giới hạn** kèm căn cứ.
4. Xuất Excel khi người dùng yêu cầu: file **mới**, tên `YYYY-MM-DD_Bang-cong_Thang-MM-YYYY.xlsx`, không ghi đè file gốc.
5. Nhắc: vi phạm giới hạn làm thêm có thể bị xử phạt hành chính – báo người có thẩm quyền điều chỉnh kế hoạch làm thêm; skill **không quyết định** trả hay không trả, chỉ tính theo quy định.

## Bảo mật
Bảng công, lương là dữ liệu cá nhân. Trong câu trả lời chỉ nêu người có vấn đề; khi trình bày ví dụ hoặc chia sẻ ra ngoài, dùng mã nhân viên thay họ tên. Không đưa họ tên, mức lương vào truy vấn tìm kiếm web.
