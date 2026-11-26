---
name: checklist-ky-ket
description: Lập và kiểm tra checklist trước khi ký hợp đồng cho doanh nghiệp Việt Nam — chủ thể và tình trạng pháp lý của đối tác, thẩm quyền người ký (đại diện theo pháp luật, giấy ủy quyền còn hạn, nghị quyết ĐHĐCĐ/HĐTV/HĐQT cho giao dịch cần chấp thuận), bản đem ký trùng bản đã duyệt, các rủi ro Cao/Nghiêm trọng đã xử lý, hình thức hợp đồng (công chứng, chứng thực, đăng ký khi luật yêu cầu), ký số theo Luật Giao dịch điện tử 2023, ký nháy, đóng dấu, số bản, phụ lục, hồ sơ kèm theo (bảo lãnh, giấy phép), thuế – hóa đơn – ngoại hối, việc sau ký (vào sổ hợp đồng, mốc hạn, lưu bản gốc). Dùng khi người dùng nói "checklist trước khi ký", "chuẩn bị ký hợp đồng", "hợp đồng đã đủ điều kiện ký chưa", "kiểm tra trước buổi ký kết", "ký số hợp đồng cần gì".
---

# Checklist ký kết hợp đồng

Đọc trước: `references/nguyen-tac-chung.md`, `references/quy-dinh-phap-ly-2026.md`, `references/khung-chuc-nang.md` (mục 7).

## Đầu vào cần có
Bản cuối cùng dự kiến ký; bản đã được duyệt nội bộ (hoặc báo cáo rà soát); thông tin/giấy tờ các bên; giấy ủy quyền, nghị quyết (nếu có); hình thức ký (giấy/ký số); ngày ký dự kiến. Thiếu → đánh dấu mục tương ứng **CHƯA KIỂM TRA ĐƯỢC**, không đánh ☑.

## Quy trình
1. Xác định người dùng là bên nào, loại hợp đồng, giá trị, hình thức ký.
2. Chạy `so_sanh_van_ban` giữa **bản đã duyệt** và **bản đem ký** – mọi khác biệt chưa duyệt là mục **CHẶN**.
3. Đi qua 6 phần dưới đây; mỗi mục: ☑ Đạt · ☐ Chưa đạt · ⚠ Chưa kiểm tra được · — Không áp dụng. Mục **CHẶN** chưa đạt → kết luận "Chưa đủ điều kiện ký".
4. Rủi ro còn mở từ báo cáo rà soát: liệt kê, chấm lại bằng `danh_gia_rui_ro` nếu tình hình thay đổi; rủi ro Nghiêm trọng chưa xử lý là **CHẶN**.

## 6 phần kiểm tra

**A. Chủ thể** – tên, mã số doanh nghiệp, địa chỉ khớp giấy đăng ký đang hiệu lực (địa giới mới từ 01/7/2025); đối tác đang hoạt động (người dùng tự tra cổng đăng ký doanh nghiệp/cơ quan thuế, hoặc đồng ý cho tra); ngành nghề có điều kiện → có giấy phép. **CHẶN** nếu sai tên/mã số.

**B. Thẩm quyền** – người ký là đại diện theo pháp luật hoặc có ủy quyền còn hạn, đúng phạm vi, đúng giá trị; giao dịch cần chấp thuận của ĐHĐCĐ/HĐTV/HĐQT (giao dịch với người có liên quan, giá trị lớn so với tổng tài sản theo Luật Doanh nghiệp) đã có nghị quyết [Cần kiểm tra ngưỡng theo điều lệ và Luật DN hiện hành]; bên ta: hạn mức ký theo quy chế nội bộ. **CHẶN** nếu thiếu thẩm quyền.

**C. Nội dung đã chốt** – bản ký trùng bản duyệt (bước 2); số = chữ (`doc_so_thanh_chu`); tổng đợt thanh toán = 100%; phạt trong trần (`kiem_tra_phat_vi_pham`; lưu ý Luật Thương mại sửa đổi hiệu lực 01/7/2027); một cơ quan giải quyết tranh chấp; phụ lục được nhắc đều có, đánh số, có chữ ký; điền đủ chỗ trống (không còn `[...]`, `....`).

**D. Hình thức và ký** – hợp đồng thuộc diện phải công chứng/chứng thực/đăng ký theo luật chuyên ngành (bất động sản, quyền sử dụng đất, biện pháp bảo đảm…) → đã sắp xếp [Cần kiểm tra theo loại hợp đồng]; ký số: chứng thư số còn hiệu lực, đúng người ký, định dạng lưu trữ (Luật Giao dịch điện tử số 20/2023/QH15) [Quy định đã xác minh khi đã đối chiếu]; bản giấy: ký nháy từng trang/giáp lai (thông lệ, [Nhận định chuyên môn]), đóng dấu nếu điều lệ/đối tác/hợp đồng yêu cầu; số bản và ngôn ngữ ưu tiên.

**E. Hồ sơ kèm theo và tuân thủ** – bảo lãnh (tạm ứng, thực hiện) đúng mẫu và hiệu lực; giấy phép, chứng nhận theo đối tượng hợp đồng; thuế – hóa đơn (thời điểm xuất hóa đơn, thuế nhà thầu nếu đối tác nước ngoài); giá/thanh toán bằng ngoại tệ trong giao dịch trong nước → rủi ro vi phạm quy định ngoại hối [Cần kiểm tra]; dữ liệu cá nhân: điều khoản xử lý dữ liệu khi có chuyển giao (Luật 91/2025/QH15).

**F. Sau khi ký** – vào sổ (`them_hop_dong_vao_so`), lấy mốc (`moc_hop_dong`) và xuất .ics mới; nơi lưu bản gốc; người phụ trách theo dõi; gửi bản ký cho bộ phận liên quan (kế toán, mua hàng) – **người dùng tự gửi**.

## Đầu ra
1. **Kết luận 1 dòng**: Đủ điều kiện ký / Chưa đủ điều kiện ký – N mục CHẶN / Cần bổ sung thông tin.
2. Bảng checklist: `Phần | Mục | Kết quả (☑/☐/⚠/—) | Ghi chú – bằng chứng | Mức (CHẶN/CẦN XỬ LÝ/GỢI Ý)`.
3. Danh sách mục CHẶN và người cần xử lý.
4. Việc sau ký.
5. Khối phê duyệt: `Người lập · Ngày · Người có thẩm quyền xác nhận đủ điều kiện ký · Ý kiến`.

## Giới hạn và kiểm tra lại
- Trợ lý **không** ký, đóng dấu, gửi đi ký điện tử, nộp công chứng. Không tự tra cứu thông tin đối tác trên Internet khi người dùng chưa đồng ý.
- Mục không có bằng chứng → ⚠, không đánh ☑ theo suy đoán.
- Trước khi trả kết quả: rà lại mọi ☑ đều có ghi chú bằng chứng; bước so sánh bản duyệt – bản ký đã chạy.
