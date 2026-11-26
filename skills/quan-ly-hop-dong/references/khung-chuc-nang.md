# Khung 8 chức năng pháp chế – hợp đồng (bản vn-custom)

Áp dụng cùng `nguyen-tac-chung.md`. Mọi chức năng: **không sửa văn bản gốc**, mọi thay đổi thể hiện trong bảng/file mới để người dùng duyệt; mỗi nhận định gắn một trong 4 nhãn **[Quy định đã xác minh] / [Nhận định chuyên môn] / [Giả định] / [Cần luật sư / người có thẩm quyền]**; mức rủi ro dùng 4 mức **Thấp / Trung bình / Cao / Nghiêm trọng** chấm bằng `danh_gia_rui_ro`.

## 1. Rà soát hợp đồng — skill `ra-soat-hop-dong`, lệnh `/ra-soat`
- **Mục tiêu**: tìm rủi ro cho đúng bên của người dùng và đề xuất câu chữ sửa trước khi ký.
- **Bối cảnh**: đối tác gửi dự thảo; hợp đồng mẫu của công ty cần rà định kỳ; trước khi trình ký.
- **Đầu vào**: file hợp đồng (+ phụ lục); người dùng là bên nào; giá trị; điểm lo ngại; hạn ký; giấy tờ chủ thể nếu có.
- **Quy trình**: 10 bước trong `ra-soat-hop-dong/SKILL.md`.
- **Tiêu chí đánh giá**: 10 nhóm `checklist-ra-soat.md`; cân bằng quyền – nghĩa vụ; tuân thủ trần luật định; đủ điều khoản bắt buộc.
- **Đầu ra**: kết luận 1 dòng → bảng `# | Điều khoản | Nội dung hiện tại | Rủi ro | Mức độ | Đề xuất sửa | Căn cứ` → thiếu/mâu thuẫn → câu hỏi đối tác → khối phê duyệt.
- **Giới hạn**: không thay luật sư với hợp đồng yếu tố nước ngoài, M&A, bất động sản, tín dụng, tranh chấp; không xác minh được thông tin ngoài văn bản.
- **Kiểm tra lại**: trích dẫn đúng vị trí; con số tính bằng công cụ; mỗi dòng có nhãn; không có câu "hợp pháp/an toàn tuyệt đối"; tùy chọn agent `tham-dinh-phap-ly`.

## 2. Soạn thảo hợp đồng — skill `soan-hop-dong`, lệnh `/soan`
- **Mục tiêu**: dự thảo hợp đồng/phụ lục/biên bản/thông báo đứng về phía người dùng, đủ điều khoản, câu chữ chặt.
- **Bối cảnh**: giao dịch mới; chuẩn hóa mẫu; phụ lục gia hạn, điều chỉnh giá; biên bản nghiệm thu, thanh lý; thông báo vi phạm, chấm dứt.
- **Đầu vào** (3 thông tin bắt buộc): loại giao dịch, người dùng là bên nào, nội dung thương mại chính (đối tượng, giá, thời hạn); thông tin chủ thể.
- **Quy trình**: hỏi thiếu → chọn khung theo loại → soạn bằng `playbook-dieu-khoan.md` → kiểm tra đầu vào (mục 12 nguyên tắc chung) → tự rà theo checklist rà soát → xuất file mới.
- **Tiêu chí**: đủ nội dung chủ yếu theo loại hợp đồng; định nghĩa nhất quán; số = chữ; tổng đợt thanh toán = 100%; một cơ quan giải quyết tranh chấp.
- **Đầu ra**: dự thảo (.docx mới) + bảng `[CẦN BỔ SUNG]` + danh sách điều khoản đã chọn phương án có lợi kèm lý do.
- **Giới hạn**: không tự đặt giá, tỷ lệ phạt, lãi suất – đưa phương án; dự thảo tham khảo, giá trị lớn cần luật sư.
- **Kiểm tra lại**: chạy `quet_dieu_khoan_hop_dong` trên chính dự thảo; `doc_so_thanh_chu`; `kiem_tra_phat_vi_pham`.

## 3. Kiểm tra điều khoản pháp lý — skill `ra-soat-hop-dong` (chế độ rà theo điều khoản)
- **Mục tiêu**: kiểm tra sâu một hoặc vài điều khoản (thanh toán, phạt vi phạm, bồi thường, chấm dứt, bảo mật, tranh chấp).
- **Bối cảnh**: "Kiểm tra điều khoản thanh toán và phạt vi phạm", đối tác chỉ sửa một điều.
- **Đầu vào**: điều khoản cần kiểm tra + các điều liên quan (định nghĩa, phụ lục); bên người dùng; giá trị.
- **Quy trình**: trích nguyên văn → xác định luật điều chỉnh và thời điểm áp dụng → tính bằng công cụ (`kiem_tra_phat_vi_pham`, `lai_cham_tra`, `thoi_hieu_khoi_kien`) → đối chiếu playbook → chấm rủi ro → câu chữ đề xuất.
- **Tiêu chí**: không vượt trần luật định; đối xứng giữa các bên; điều kiện, thời hạn, hậu quả rõ ràng; không mâu thuẫn với điều khác.
- **Đầu ra**: bảng một dòng mỗi điều khoản (cùng cấu trúc bảng rủi ro) + câu chữ thay thế + phương án lùi.
- **Giới hạn**: chỉ kết luận trong phạm vi điều khoản được giao; nêu rõ điều liên quan chưa đọc.
- **Kiểm tra lại**: đọc lại điều khoản trong toàn văn để phát hiện mâu thuẫn; kiểm tra Luật Thương mại sửa đổi (hiệu lực 01/7/2027).

## 4. Quản trị rủi ro — skill `quan-tri-rui-ro`, lệnh `/rui-ro`
- **Mục tiêu**: lập sổ rủi ro cho một hợp đồng hoặc danh mục hợp đồng, có người phụ trách và biện pháp kiểm soát.
- **Bối cảnh**: sau rà soát; trước khi trình duyệt; định kỳ quý với hợp đồng lớn đang thực hiện.
- **Đầu vào**: danh sách rủi ro (từ báo cáo rà soát hoặc người dùng), bên người dùng, tình trạng thực hiện.
- **Quy trình**: chuẩn hóa mô tả → chấm Khả năng × Ảnh hưởng (`danh_gia_rui_ro`) → chọn biện pháp (sửa điều khoản, bảo lãnh, bảo hiểm, theo dõi mốc, chấp nhận) → giao người phụ trách → mốc xem lại.
- **Tiêu chí**: mỗi rủi ro có mô tả cụ thể, mức, biện pháp, người phụ trách, mốc xem lại.
- **Đầu ra**: ma trận rủi ro + sổ rủi ro (bảng hoặc Excel mới) + rủi ro cần người có thẩm quyền chấp nhận.
- **Giới hạn**: điểm số là nhận định chuyên môn, không phải kết luận pháp lý; quyết định chấp nhận rủi ro thuộc người có thẩm quyền.
- **Kiểm tra lại**: rủi ro Cao/Nghiêm trọng đều có biện pháp; không chấm Nghiêm trọng khi thiếu căn cứ.

## 5. Quản lý thời hạn hợp đồng — skill `quan-ly-hop-dong`
- **Mục tiêu**: không bỏ lỡ mốc hết hạn, hạn báo không gia hạn, mốc thanh toán, bảo hành, bảo lãnh.
- **Bối cảnh**: sau khi ký; rà hằng tháng; trước kỳ gia hạn.
- **Đầu vào**: hợp đồng đã ký hoặc thông tin mốc; người phụ trách.
- **Quy trình**: trích mốc → `them_hop_dong_vao_so` → `moc_hop_dong` (N ngày tới) → xuất .ics mới để người dùng tự nhập lịch.
- **Tiêu chí**: mốc tính đúng ngày (ngày làm việc nếu hợp đồng quy định); có nhắc trước.
- **Đầu ra**: danh sách mốc sắp đến + việc phải làm + file .ics.
- **Giới hạn**: sổ CSV cục bộ, không đồng bộ tự động; không tự gửi thông báo cho đối tác.
- **Kiểm tra lại**: đối chiếu mốc với điều khoản gốc; kiểm tra điều khoản tự động gia hạn.

## 6. Chuẩn hóa văn bản pháp chế — skill `soan-hop-dong` / `kiem_tra_the_thuc`
- **Mục tiêu**: thống nhất cấu trúc, thuật ngữ, định nghĩa, cách ghi số – ngày – tiền; công văn, nghị quyết đúng thể thức NĐ 30/2020.
- **Bối cảnh**: xây bộ mẫu hợp đồng công ty; văn bản gửi đối tác, cơ quan nhà nước.
- **Đầu vào**: văn bản/mẫu hiện có; quy ước của công ty (nếu có).
- **Quy trình**: lập bảng thuật ngữ – định nghĩa → phát hiện chỗ dùng không nhất quán → đề xuất chuẩn hóa dạng bảng "hiện tại → đề xuất" → file mới sau khi người dùng duyệt.
- **Tiêu chí**: một khái niệm – một thuật ngữ; đánh số điều khoản liên tục; viện dẫn chéo đúng số điều.
- **Đầu ra**: bảng thay đổi đề xuất + bản chuẩn hóa (file mới).
- **Giới hạn**: chuẩn hóa không làm thay đổi nội dung thương mại; thay đổi có thể ảnh hưởng nghĩa phải liệt kê riêng.
- **Kiểm tra lại**: so sánh bản gốc và bản chuẩn hóa bằng `so_sanh_van_ban` để bảo đảm chỉ có thay đổi đã duyệt.

## 7. Checklist ký kết — skill `checklist-ky-ket`, lệnh `/checklist-ky`
- **Mục tiêu**: bảo đảm hợp đồng đủ điều kiện để ký và lưu trữ: chủ thể, thẩm quyền, nội dung đã chốt, hình thức ký, hồ sơ kèm theo.
- **Bối cảnh**: ngay trước khi trình ký/ký số; trước buổi ký kết.
- **Đầu vào**: bản cuối cùng, báo cáo rà soát, giấy tờ chủ thể, ủy quyền, nghị quyết phê duyệt.
- **Quy trình**: theo checklist 6 phần trong `checklist-ky-ket/SKILL.md`.
- **Tiêu chí**: mọi mục CHẶN đã xử lý; bản ký trùng bản đã duyệt.
- **Đầu ra**: checklist ☐/☑ + mục CHẶN còn mở + việc sau ký.
- **Giới hạn**: không ký, không đóng dấu, không gửi đi ký điện tử thay người dùng.
- **Kiểm tra lại**: `so_sanh_van_ban` giữa bản đã duyệt và bản đem ký.

## 8. So sánh phiên bản — skill `so-sanh-phien-ban`, lệnh `/so-sanh`
- **Mục tiêu**: thấy mọi thay đổi giữa hai bản, nhất là chỗ đối tác **sửa không báo**.
- **Bối cảnh**: đối tác trả lại dự thảo; bản ký khác bản duyệt; phụ lục mới.
- **Đầu vào**: hai file (bản cũ, bản mới) hoặc hai nội dung.
- **Quy trình**: `so_sanh_van_ban` → phân loại thay đổi (nội dung/câu chữ) → đánh giá rủi ro từng thay đổi → quyết định chấp nhận/sửa/từ chối → `bang_gop_y_hop_dong` (2 file tách: gửi đối tác / nội bộ).
- **Tiêu chí**: không bỏ sót thay đổi; mỗi thay đổi có ý kiến.
- **Đầu ra**: bảng thay đổi + bảng ý kiến gửi đối tác + bản trình duyệt nội bộ.
- **Giới hạn**: công cụ so theo đoạn – định dạng, bảng phức tạp, ảnh có thể bị bỏ sót; PDF scan phải OCR trước.
- **Kiểm tra lại**: file gửi đối tác không chứa phần đánh giá nội bộ; người có thẩm quyền duyệt trước khi gửi.
