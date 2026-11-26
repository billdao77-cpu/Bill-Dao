---
description: Workflow 2 – Xây dựng chiến dịch quảng cáo: mục tiêu → khách hàng → thông điệp → nội dung → creative brief → landing page → KPI → kế hoạch đánh giá. Không bật quảng cáo, không chi tiền.
argument-hint: "[sản phẩm, kênh (Facebook/TikTok/Google...), ngân sách dự kiến, thời gian]"
---

Xây dựng chiến dịch quảng cáo cho: $ARGUMENTS

Dùng agent `content-creator` cho nội dung và `growth-analyst` cho ngưỡng – KPI (hoặc trực tiếp các skill dưới đây).

1. **Mục tiêu** – mục tiêu kinh doanh → mục tiêu tối ưu trên nền tảng khớp cách bán (`quang-cao-truc-tuyen`); ROAS/CPA hòa vốn (`gia-san-pham-khuyen-mai`, `tinh_gia.py`).
2. **Khách hàng** – 2–3 tệp đối tượng, insight, lý do (`nghien-cuu-thi-truong` nếu có).
3. **Thông điệp** – mỗi tệp 1 thông điệp chính + bằng chứng.
4. **Nội dung** – 3–5 mẫu quảng cáo/tệp: hook – lợi ích – bằng chứng – CTA; biến thể A/B.
5. **Creative brief** – bảng: mã mẫu, định dạng, thời lượng, cảnh/hình, lời thoại/chữ trên màn hình, CTA, yêu cầu thương hiệu.
6. **Landing page** – cấu trúc khối, tiêu đề, form (không tick sẵn đồng ý) theo `seo-website-landing`.
7. **Soát pháp lý** – `kiem-tra-phap-ly-quang-cao` (`validate_copy.py`) cho toàn bộ nội dung và landing.
8. **KPI** – bảng chỉ số (CPM, CTR, CPC, chi phí/kết quả, ROAS thật), ngưỡng dừng/giữ/tăng theo hòa vốn, ngân sách thử nghiệm và thời gian đủ dữ liệu.
9. **Đánh giá** – lịch đọc số (ngày 3, 7, 14), dùng `doc_so_ads.py` trên file xuất; quy tắc ra quyết định.

Đầu ra: bản kế hoạch chiến dịch + creative brief + đề cương landing + bảng KPI. "Anh/chị tự làm": tạo chiến dịch, duyệt mẫu, thanh toán trong Trình quản lý quảng cáo.
