---
description: Chuẩn bị kê khai thuế một kỳ – đọc hóa đơn XML, kiểm tra chứng từ, tính GTGT, TNCN khấu trừ, thuế nhà thầu nếu có, hướng dẫn điền tờ khai, hạn nộp; không tự nộp.
argument-hint: "[kỳ tháng/quý, thư mục hóa đơn XML, MST công ty, bảng lương, hợp đồng với bên nước ngoài nếu có]"
---

Chuẩn bị kê khai thuế cho: $ARGUMENTS

Giao cho agent `chuyen-vien-thue`.

1. `doc-hoa-don-xml`: bảng kê mua vào/bán ra (`doc_hoa_don.py --mst-cua-toi ...`), cảnh báo thiếu MCCQT, thuế suất.
2. `kiem-tra-chung-tu`: hóa đơn đầu vào đủ điều kiện về chứng từ, thanh toán không dùng tiền mặt.
3. `thue-gtgt-dn`: số thuế phải nộp/còn được khấu trừ (`tinh_gtgt.py`); file hướng dẫn điền tờ khai (`huong_dan_to_khai.py --ra <tên mới>.docx`).
4. `luong-bao-hiem`: TNCN khấu trừ từ bảng lương (`tinh_luong.py`).
5. `thue-nha-thau` nếu có thanh toán cho bên nước ngoài.
6. `lich-thue-dn`: hạn nộp hồ sơ và tiền (`tao_lich_thue.py`).

Đầu ra: bảng số liệu theo chỉ tiêu tờ khai, danh sách hóa đơn loại khỏi khấu trừ kèm lý do, hạn nộp, bảng "Cần anh/chị kiểm tra", việc tự làm trên eTax. Kết thúc: "Đối chiếu văn bản hiện hành và hỏi cơ quan thuế quản lý trước khi kê khai."
