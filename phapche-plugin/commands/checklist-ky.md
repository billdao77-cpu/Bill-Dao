---
description: Lập checklist trước khi ký một hợp đồng – chủ thể, thẩm quyền, bản ký trùng bản duyệt, hình thức ký, hồ sơ kèm theo, việc sau ký; chỉ ra mục CHẶN.
argument-hint: "[file bản đem ký, file bản đã duyệt hoặc báo cáo rà soát, bên của công ty]"
---

Lập checklist ký kết cho: $ARGUMENTS

1. Dùng skill `checklist-ky-ket`: hỏi những gì còn thiếu (bên của công ty, bản đã duyệt, giấy ủy quyền/nghị quyết, hình thức ký).
2. Chạy `so_sanh_van_ban` giữa bản đã duyệt và bản đem ký; khác biệt chưa duyệt là CHẶN.
3. Đi qua 6 phần A–F; mục không có bằng chứng ghi ⚠, không đánh ☑.
4. Đầu ra: kết luận 1 dòng → bảng checklist → mục CHẶN → việc sau ký → khối phê duyệt. Không ký, không gửi đi ký thay người dùng.
