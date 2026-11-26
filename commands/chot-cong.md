---
description: Chốt công tháng – rà bảng chấm công (lỗi dữ liệu, giới hạn làm thêm giờ) và tính tiền làm thêm, làm đêm cho từng người; xuất bảng cần xác minh.
argument-hint: "[tháng/năm, file bảng chấm công, file/mức lương làm căn cứ]"
---

Chốt công cho: $ARGUMENTS

1. Dùng skill `cham-cong-tinh-luong`: hỏi những gì còn thiếu (chế độ giờ làm, ngày nghỉ hằng tuần, ngày công chuẩn, lương làm căn cứ, giờ làm thêm lũy kế từ đầu năm).
2. Đọc đúng file người dùng chỉ; chạy `kiem_tra_gio_lam_them` cho từng người; lập bảng **Cần xác minh** – không tự sửa số công.
3. Chạy `tinh_luong_lam_them` cho người có làm thêm/làm đêm; ghi tham số đã dùng.
4. Đầu ra: bảng kiểm tra công, bảng tiền làm thêm, danh sách vi phạm giới hạn kèm căn cứ (Điều 107 BLLĐ 2019). Nếu xuất Excel: tạo file mới, không ghi đè.
5. Nhắc: đây là bảng tính tham khảo – kế toán chốt bảng lương, người có thẩm quyền duyệt chi.
