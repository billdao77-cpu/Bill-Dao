---
description: Phân tích tài chính cho chủ doanh nghiệp – kiểm tra số liệu BCTC, tỷ số, biến động so năm trước, tuổi nợ, dự báo dòng tiền 13 tuần, điểm nghẽn và 3 việc ưu tiên có cách đo.
argument-hint: "[file BCTC (chi_tieu,nam_nay,nam_truoc) hoặc bảng cân đối số phát sinh, số dư tiền, thu chi dự kiến]"
---

Phân tích tài chính cho: $ARGUMENTS

Giao cho agent `chuyen-vien-phan-tich-tai-chinh`.

1. Kiểm tra số liệu – `phan_tich_tai_chinh.py` (200 = 500, dòng tổng B02); lỗi → dừng, liệt kê cần sửa.
2. Tỷ số và biến động – bảng tỷ số năm nay/năm trước, giải thích biến động lớn bằng số liệu.
3. Công nợ – tuổi nợ phải thu (`tuoi_no.py`) nếu có sổ chi tiết.
4. Dòng tiền – dự báo 13 tuần (`dong_tien.py`), tuần âm quỹ, kịch bản khách trả trễ.
5. Điểm nghẽn và đề xuất – tối đa 3 việc: chỉ số, giá trị hiện tại, ngưỡng mục tiêu, thời gian đo, người làm.

Đầu ra: báo cáo 1 trang cho chủ doanh nghiệp (kết luận → bảng tỷ số → dòng tiền → 3 việc) + bảng "Cần anh/chị kiểm tra". Không so "chuẩn ngành" khi không có nguồn.
