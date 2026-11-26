---
description: Soạn một văn bản văn phòng (báo cáo, đề xuất, kế hoạch, biên bản, email) theo skill phù hợp rồi kiểm định – sự thật, số liệu, thông tin nhạy cảm, văn phong – trước khi giao.
argument-hint: "[loại văn bản, nội dung chính, người nhận, tài liệu nguồn]"
---

Soạn và kiểm tra: $ARGUMENTS

1. Chọn skill: `bao-cao`, `de-xuat`, `ke-hoach`, `bien-ban`, `email-cong-so` (văn bản hành chính NĐ 30, hợp đồng, báo giá, content bán hàng → plugin chuyên sâu nếu đã cài, nếu không → gói `van-phong-mo-rong`).
2. Soạn theo skill; thông tin thiếu → `[CẦN BỔ SUNG]`, không bịa.
3. Agent `bien-tap-kiem-dinh` (hoặc skill `kiem-tra-loi-ai`) đối chiếu với tài liệu nguồn; sửa lỗi CHẶN/CẦN SỬA.
4. `viet-nhu-nguoi` cho văn phong nếu cần – không đổi số liệu, tên, cam kết.

Đầu ra: văn bản hoàn chỉnh + bảng kiểm định (đã sửa / còn lại) + bảng "Thông tin cần bổ sung/kiểm tra". Không gửi, không ký.
