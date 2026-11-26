---
description: Chuẩn hóa một file dữ liệu Excel/CSV (danh sách khách hàng, nhân sự, nhà cung cấp, đơn hàng) – Unicode, khoảng trắng, họ tên, SĐT, email, MST, dòng trùng, giá trị nghi sai; xuất file mới kèm báo cáo vấn đề.
argument-hint: "[file Excel/CSV, sheet nếu có, cột cần ưu tiên]"
---

Chuẩn hóa dữ liệu: $ARGUMENTS

1. Đọc cấu trúc file (tên cột, số dòng) – chỉ file người dùng chỉ định; trình bày dữ liệu với SĐT, email, CCCD đã che.
2. Chạy `bang-excel/scripts/lam_sach.py <vào> <tên mới>.xlsx [--sheet ...]` – không ghi đè file gốc.
3. Rà báo cáo vấn đề: dòng trùng, SĐT/MST sai định dạng; nhóm theo loại, đếm số dòng.
4. Đề xuất bước tiếp theo (gộp trùng thủ công, hỏi lại khách, khóa định dạng cột bằng Data Validation) – không tự xóa dòng.

Đầu ra: file sạch (mới) + bảng tóm tắt vấn đề + cảnh báo nếu có ô dạng công thức trong dữ liệu (đã vô hiệu hóa). Không gửi dữ liệu ra ngoài.
