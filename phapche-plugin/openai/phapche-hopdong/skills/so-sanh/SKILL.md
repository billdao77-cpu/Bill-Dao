---
name: so-sanh
description: "Quy trình trọn gói: So sánh hai phiên bản hợp đồng (bản mình gửi và bản đối tác trả lại) – liệt kê mọi chỗ sửa theo Điều, đánh dấu thay đổi nhạy cảm và sửa không báo, đánh giá có lợi/bất lợi."
---

Thông tin cần có từ người dùng: [file bản cũ] [file bản mới] [bạn là bên nào]. Thiếu thông tin quan trọng thì hỏi gọn một lần.


So sánh phiên bản: yêu cầu của người dùng

Dùng skill `so-sanh-phien-ban`: chạy `so_sanh_van_ban`, đọc ngữ cảnh từng thay đổi, đánh giá tác động với bên người dùng, đối chiếu danh sách sửa đổi đối tác gửi kèm (nếu có) để tìm sửa không báo. Chốt quyết định từng điểm rồi xuất `bang_gop_y_hop_dong`: 1 file bảng ý kiến gửi đối tác và 1 file trình duyệt nội bộ.
