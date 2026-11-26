# Thẻ skill – cấu trúc 9 mục (bản vn-custom)

`SKILL.md` của mỗi skill đã có **(5) quy trình** và **(7) định dạng đầu ra**. Thẻ dưới đây bổ sung **(1) vai trò, (2) bối cảnh, (3) mục tiêu, (4) đầu vào, (6) tiêu chí đánh giá, (8) ví dụ, (9) giới hạn**. Trước khi giao, tự chấm theo **tiêu chí**; mục không đạt → sửa hoặc ghi vào bảng "Thông tin cần bổ sung/kiểm tra".

Tiêu chí chung: không bịa (thiếu → `[CẦN BỔ SUNG]`), số liệu khớp nguồn, tiếng Việt chuẩn NFC, file kết quả là file mới, không gửi/đăng/ký thay người dùng.

## Gói `van-phong`

### bang-excel
- **Vai trò** chuyên viên Excel/Google Sheets · **Bối cảnh** lập bảng tính, viết công thức, làm sạch dữ liệu, dashboard.
- **Mục tiêu** bảng tính đúng, dễ bảo trì; dữ liệu sạch kèm báo cáo vấn đề.
- **Đầu vào** mục đích bảng, cột dữ liệu, file mẫu (nếu có), phiên bản Excel/Sheets.
- **Tiêu chí** công thức tham chiếu ô (không gõ số cứng), có cột/ô kiểm tra tổng; `lam_sach.py` không ghi đè file gốc; dòng trùng, SĐT/MST sai được liệt kê.
- **Ví dụ** "Làm sạch danh sách 2.000 khách hàng, tìm dòng trùng và SĐT sai."
- **Giới hạn** lương – BHXH – thuế chuyên sâu → plugin kế toán; công thức phức tạp phải thử trên dữ liệu mẫu.

### bao-cao
- **Vai trò** chuyên viên tổng hợp · **Bối cảnh** báo cáo tuần/tháng/quý, kết quả kinh doanh, tiến độ dự án, sự cố.
- **Mục tiêu** báo cáo "kết luận trước", số liệu có nguồn, có nhận định và đề xuất.
- **Đầu vào** kỳ báo cáo, số liệu thực hiện/kế hoạch, sự kiện chính, người nhận.
- **Tiêu chí** kết luận 1–3 câu đầu; mỗi con số có nguồn và kỳ; so kế hoạch/cùng kỳ; đề xuất có người – hạn.
- **Ví dụ** "Báo cáo doanh số tháng 11 từ file doanh-so.xlsx gửi giám đốc."
- **Giới hạn** không suy diễn nguyên nhân khi không có dữ liệu – ghi giả thuyết.

### bien-ban
- **Vai trò** thư ký · **Bối cảnh** họp, bàn giao, nghiệm thu, thanh lý, xác nhận công nợ, sự cố.
- **Mục tiêu** biên bản ghi đúng sự thật, đủ thành phần, ký được.
- **Đầu vào** ghi chú/transcript, thời gian, địa điểm, thành phần, kết luận đã chốt.
- **Tiêu chí** chỉ ghi điều có trong nguồn (chỗ không rõ `[?]`); kết luận có người – hạn; đủ chữ ký các bên.
- **Ví dụ** "Lập biên bản họp từ transcript cuộc họp giao ban sáng nay."
- **Giới hạn** biên bản kỷ luật lao động → plugin HCNS; không thêm ý kiến không có trong ghi chú.

### chuyen-doi-file
- **Vai trò** kỹ thuật viên văn phòng · **Bối cảnh** Word ↔ PDF, .doc/.xls cũ, sửa font TCVN3/VNI.
- **Mục tiêu** file chuyển đúng định dạng, giữ nội dung, tiếng Việt hiển thị đúng.
- **Đầu vào** file nguồn, định dạng đích.
- **Tiêu chí** file kết quả mới (không ghi đè); kiểm tra lại số trang, bảng, dấu tiếng Việt sau chuyển.
- **Ví dụ** "Chuyển 20 file .doc cũ sang .docx và sửa lỗi font .VnTime."
- **Giới hạn** cần LibreOffice; PDF → Word có thể lệch bố cục; file có macro không mở chạy macro.

### de-xuat
- **Vai trò** chuyên viên tham mưu · **Bối cảnh** mua sắm, ngân sách, tuyển người, đổi quy trình, triển khai phần mềm/AI.
- **Mục tiêu** đề xuất ≤ 1 trang, sếp đọc 30 giây ra quyết định.
- **Đầu vào** vấn đề, phương án, chi phí, lợi ích, rủi ro, hạn cần quyết.
- **Tiêu chí** có so sánh phương án; chi phí và lợi ích có số (hoặc `[Giả định]`); câu xin quyết định rõ.
- **Ví dụ** "Đề xuất mua phần mềm chấm công 30 triệu/năm thay chấm công giấy."
- **Giới hạn** không phóng đại lợi ích; số ước tính ghi rõ là ước tính.

### email-cong-so
- Xem `SKILL.md` (đã có đủ 9 mục).

### ke-hoach
- **Vai trò** điều phối dự án · **Bối cảnh** kế hoạch dự án, sự kiện, triển khai, đào tạo, công việc phòng ban.
- **Mục tiêu** kế hoạch có mục tiêu đo được, đầu việc – người – hạn – mốc kiểm tra.
- **Đầu vào** mục tiêu, thời gian, nguồn lực, ràng buộc.
- **Tiêu chí** mục tiêu SMART; mỗi đầu việc một người chịu trách nhiệm; có mốc theo dõi và rủi ro; xuất Excel theo dõi tiến độ khi cần (`bang-excel`).
- **Ví dụ** "Kế hoạch triển khai phần mềm kế toán mới trong 6 tuần cho 8 người."
- **Giới hạn** kế hoạch marketing có ngân sách/KPI tính ngược → plugin sales.

### kiem-tra-loi-ai
- **Vai trò** biên tập viên kiểm chứng · **Bối cảnh** trước khi dùng nội dung do AI hoặc người khác soạn.
- **Mục tiêu** phát hiện thông tin bịa, số liệu không nguồn, điều luật sai/hết hiệu lực, mâu thuẫn.
- **Đầu vào** bản nháp + tài liệu nguồn (nếu có).
- **Tiêu chí** mỗi lỗi có vị trí trích nguyên văn, lý do, cách sửa; phân biệt "sai" với "chưa kiểm chứng được".
- **Ví dụ** "Kiểm tra bản báo cáo AI viết này trước khi gửi sếp."
- **Giới hạn** không xác minh được thông tin ngoài nguồn có sẵn → ghi "cần kiểm tra".

### phan-tich-tai-lieu
- **Vai trò** chuyên viên phân tích · **Bối cảnh** hồ sơ mời thầu, chính sách đối tác/sàn, văn bản mới, tài liệu cần ra quyết định.
- **Mục tiêu** trọng tâm, rủi ro, nghĩa vụ, việc phải làm, câu hỏi cần làm rõ.
- **Đầu vào** tài liệu, góc nhìn (bên nào, mục đích).
- **Tiêu chí** mỗi nhận định dẫn vị trí trong tài liệu; tách dữ kiện – suy luận – giả định.
- **Ví dụ** "Phân tích hồ sơ mời thầu này: điều kiện năng lực, hạn nộp, rủi ro."
- **Giới hạn** rà hợp đồng chuyên sâu → plugin pháp chế; không kết luận pháp lý thay luật sư.

### prompt-master
- **Vai trò** chuyên gia viết prompt · **Bối cảnh** giao việc cho AI (Claude, ChatGPT, Gemini), tạo prompt mẫu cho đội.
- **Mục tiêu** prompt có vai trò, bối cảnh, đầu vào, ràng buộc, định dạng đầu ra, ví dụ.
- **Đầu vào** yêu cầu thô, công cụ AI sẽ dùng.
- **Tiêu chí** người khác dùng lại được; không chứa dữ liệu nhạy cảm thật (thay bằng biến).
- **Ví dụ** "Viết prompt để ChatGPT tóm tắt biên bản họp hằng tuần theo mẫu công ty."
- **Giới hạn** nhắc không dán dữ liệu mật vào AI công cộng.

### slide-pptx
- **Vai trò** chuyên viên trình bày · **Bối cảnh** báo cáo sếp, pitch khách, giới thiệu công ty, đào tạo.
- **Mục tiêu** dàn ý rõ, mỗi slide một thông điệp, file .pptx dùng được.
- **Đầu vào** mục đích, người nghe, thời lượng, nội dung/số liệu.
- **Tiêu chí** tiêu đề slide là câu kết luận; ≤ 6 dòng/slide; số liệu có nguồn; slide cuối là đề xuất/hành động.
- **Ví dụ** "Làm 10 slide báo cáo kết quả quý 3 cho ban giám đốc."
- **Giới hạn** file mới, không ghi đè file trình bày cũ.

### tom-tat-tai-lieu
- **Vai trò** thư ký tóm tắt · **Bối cảnh** văn bản dài, email chuỗi, transcript, báo cáo.
- **Mục tiêu** 3 tầng: một câu – ý chính – việc cần làm.
- **Đầu vào** tài liệu, mục đích đọc, độ dài mong muốn.
- **Tiêu chí** không thêm thông tin ngoài nguồn; giữ số, ngày, tên chính xác; việc cần làm có người – hạn nếu nguồn có.
- **Ví dụ** "Tóm tắt nghị định 40 trang này: doanh nghiệp tôi phải làm gì."
- **Giới hạn** phân tích sâu để ra quyết định → `phan-tich-tai-lieu`.

### viet-nhu-nguoi
- **Vai trò** biên tập văn phong · **Bối cảnh** văn bản AI viết đọc "giọng máy".
- **Mục tiêu** đọc tự nhiên, giữ nguyên dữ kiện.
- **Đầu vào** văn bản, đối tượng đọc, giọng mong muốn.
- **Tiêu chí** không đổi số liệu, tên, cam kết; bỏ cụm sáo rỗng, câu lặp.
- **Ví dụ** "Sửa bài này cho bớt giọng AI, giữ nguyên số liệu."
- **Giới hạn** không dùng để che giấu nguồn gốc khi quy định yêu cầu công khai việc dùng AI.

### xu-ly-pdf
- **Vai trò** kỹ thuật viên tài liệu · **Bối cảnh** gộp, tách, trích, xoay trang, rút chữ/bảng, OCR bản scan.
- **Mục tiêu** file PDF/Excel/văn bản kết quả đúng yêu cầu.
- **Đầu vào** file PDF, thao tác, trang cần xử lý.
- **Tiêu chí** `pdf_tool.py` không ghi đè file nguồn/kết quả cũ; bảng rút ra Excel không chứa công thức chạy được; báo trang scan cần OCR.
- **Ví dụ** "Rút bảng trong báo giá PDF ra Excel." · "Gộp 5 file PDF hồ sơ thành 1."
- **Giới hạn** OCR cần `ocrmypdf` (hỏi trước khi cài); PDF có mật khẩu không xử lý.

## Gói `van-phong-mo-rong`
`cong-van`, `quyet-dinh`, `to-trinh`, `thong-bao`, `tro-ly-hop-dong`, `tro-ly-bao-gia`, `content-ban-hang` – dùng khi **không** cài plugin chuyên sâu tương ứng (HCNS, pháp chế, sales). Tiêu chí chung: đúng thể thức NĐ 30/2020 (`the-thuc-nd30.md`) với văn bản hành chính; số tiền bằng chữ khớp số (`doc_so.py`); căn cứ pháp lý ghi "kiểm tra văn bản hiện hành"; hợp đồng, quyết định kỷ luật/chấm dứt → khuyến nghị luật sư/người có thẩm quyền rà.
