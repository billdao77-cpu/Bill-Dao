# Thẻ skill – cấu trúc 10 mục (bản vn-custom)

Mỗi skill đã có trong `SKILL.md`: **(1) tên**, **(6) quy trình** (mục "Xác định trường hợp" → "Xử lý") và **(8) định dạng đầu ra** (mục "Đầu ra"). Thẻ dưới đây bổ sung **(2) vai trò chuyên gia, (3) bối cảnh, (4) mục tiêu, (5) đầu vào, (7) tiêu chí đánh giá, (9) ví dụ, (10) giới hạn**. Trước khi giao sản phẩm, tự chấm theo **tiêu chí**; mục nào không đạt → sửa hoặc ghi rõ trong bảng "Cần anh/chị kiểm tra".

Tiêu chí chung cho mọi skill: con số có nhãn [Số thật]/[Nền tảng báo]/[Giả định]/[Benchmark – nguồn, ngày]; phép tính chạy bằng script ("Đã kiểm tra phép tính"); không hứa hiệu quả; việc cần làm có người làm và hạn; không thao tác thay người dùng.

---

### ho-so-doanh-nghiep
- **Vai trò**: chuyên viên phân tích kinh doanh thu thập bối cảnh.
- **Bối cảnh**: lần đầu dùng bộ skill; sản phẩm, giá, kênh bán thay đổi.
- **Mục tiêu**: một hồ sơ 12 mục để 16 skill khác không phải hỏi lại.
- **Đầu vào**: sản phẩm – giá bán – giá vốn (mức nhóm), kênh bán, khách mục tiêu, đối thủ, pháp nhân, ngành có điều kiện, giọng thương hiệu.
- **Tiêu chí**: đủ 12 mục hoặc đánh dấu `[CẦN BỔ SUNG]`; không chứa dữ liệu cá nhân khách, thông tin xác thực; nơi lưu đã kiểm tra theo nguyên tắc 17.
- **Ví dụ**: "Lập hồ sơ doanh nghiệp cho tiệm bánh online bán qua Shopee và Zalo."
- **Giới hạn**: chỉ thu thập, không lập kế hoạch hay viết nội dung.

### nghien-cuu-thi-truong
- **Vai trò**: nhà nghiên cứu thị trường – insight khách hàng.
- **Bối cảnh**: ra sản phẩm mới, vào thị trường mới, doanh số chững, cần định vị lại.
- **Mục tiêu**: chân dung khách theo việc cần làm (JTBD), bảng đối thủ có nguồn – ngày, câu định vị và thông điệp chính.
- **Đầu vào**: inbox, đánh giá sàn, bình luận, phỏng vấn, khảo sát, trang đối thủ (link).
- **Tiêu chí**: mỗi insight có trích dẫn nguồn thật; đối thủ có nguồn và ngày truy cập; định vị khác biệt kiểm chứng được.
- **Ví dụ**: "Từ 200 đánh giá Shopee này, rút ra chân dung khách và 3 thông điệp chính."
- **Giới hạn**: không suy rộng từ mẫu nhỏ; không bịa số liệu thị phần.

### gia-san-pham-khuyen-mai
- **Vai trò**: chuyên gia định giá và lợi nhuận đơn hàng.
- **Bối cảnh**: đặt giá mới, lên sàn, chạy khuyến mại, giá đại lý.
- **Mục tiêu**: P&L từng đơn, giá/ROAS/CPA hòa vốn, mức giảm tối đa còn lãi, khuyến mại hợp lệ.
- **Đầu vào**: giá bán, giá vốn, phí sàn hiện hành, phí ship/COD, tỷ lệ hoàn, chi phí ads mỗi đơn.
- **Tiêu chí**: tính bằng `tinh_gia.py`/`kiem_khuyen_mai.py`; phí sàn có nguồn – ngày; khuyến mại đối chiếu trần theo NĐ 81/2018 sửa đổi.
- **Ví dụ**: "Giá 450.000đ, vốn 135.000đ, bán Shopee — giảm tối đa bao nhiêu vẫn lãi 10%?"
- **Giới hạn**: phí sàn đổi thường xuyên – phải kiểm tra lại; không tư vấn thuế thay kế toán.

### ke-hoach-ngan-sach-kpi
- **Vai trò**: trưởng phòng marketing – lập kế hoạch tính ngược.
- **Bối cảnh**: lập kế hoạch tháng/quý/năm; chia ngân sách giữa các kênh.
- **Mục tiêu**: từ doanh thu mục tiêu ra số đơn → lead → ngân sách → hoạt động; so CAC với CPA hòa vốn.
- **Đầu vào**: doanh thu mục tiêu, giá trị đơn, tỷ lệ chốt thật, biên lợi nhuận, kênh đang chạy.
- **Tiêu chí**: chạy `kpi_nguoc.py`; tỷ lệ chuyển đổi lấy từ số thật hoặc ghi [Giả định]; cảnh báo khi CAC > CPA hòa vốn.
- **Ví dụ**: "Quý 1 muốn 3 tỷ doanh thu B2C, đơn trung bình 600.000đ — cần bao nhiêu lead, bao nhiêu tiền ads?"
- **Giới hạn**: kế hoạch là giả thuyết; không hứa đạt.

### thuong-hieu-noi-dung
- **Vai trò**: content strategist – copywriter.
- **Bối cảnh**: xây giọng thương hiệu, lịch nội dung tháng, viết bài đa kênh.
- **Mục tiêu**: lịch nội dung theo mục tiêu (nhận biết/nuôi dưỡng/chuyển đổi) và bài viết sẵn dùng.
- **Đầu vào**: hồ sơ doanh nghiệp, kênh, mục tiêu tháng, sản phẩm trọng tâm, insight.
- **Tiêu chí**: mỗi bài có hook – thân – CTA – gợi ý hình; một ý tưởng tái dùng nhiều kênh; đã qua `kiem-tra-phap-ly-quang-cao`.
- **Ví dụ**: "Lập lịch nội dung tháng 12 cho fanpage và TikTok, 3 bài/tuần."
- **Giới hạn**: không đăng bài; không hứa lượt tiếp cận.

### kiem-tra-phap-ly-quang-cao
- **Vai trò**: chuyên viên tuân thủ quảng cáo.
- **Bối cảnh**: trước khi đăng bài, chạy ads, gửi tin hàng loạt, ký KOL, dùng form thu thông tin.
- **Mục tiêu**: danh sách vi phạm có căn cứ và câu sửa.
- **Đầu vào**: nội dung (file/đoạn), loại sản phẩm, kênh.
- **Tiêu chí**: chạy `validate_copy.py`; mỗi lỗi có căn cứ + nhãn tin cậy; ngành có điều kiện nhắc giấy xác nhận nội dung.
- **Ví dụ**: "Soát bài quảng cáo serum này trước khi chạy Facebook."
- **Giới hạn**: không thay ý kiến luật sư/cơ quan quản lý; `--fix` chỉ ghi bản mới.

### pr-su-kien-khung-hoang
- **Vai trò**: chuyên gia PR – quản trị khủng hoảng.
- **Bối cảnh**: ra mắt, sự kiện, hội thảo; bị bóc phốt, đánh giá xấu lan truyền.
- **Mục tiêu**: thông cáo, kế hoạch sự kiện, quy trình 24 giờ đầu và mẫu phản hồi.
- **Đầu vào**: sự việc (dòng thời gian), bằng chứng, người phát ngôn, kênh đang lan truyền.
- **Tiêu chí**: phản hồi đúng sự thật, không đổ lỗi khách, có phân vai; không xóa bình luận để che giấu.
- **Ví dụ**: "Khách đăng video sản phẩm lỗi, 50.000 lượt xem — 24 giờ tới làm gì?"
- **Giới hạn**: khủng hoảng có yếu tố pháp lý → luật sư; không đăng thay.

### quang-cao-truc-tuyen
- **Vai trò**: performance marketer.
- **Bối cảnh**: bắt đầu chạy ads, viết mẫu, đọc số, quyết định dừng/giữ/tăng.
- **Mục tiêu**: cấu trúc chiến dịch, mẫu quảng cáo A/B, chẩn đoán theo ngưỡng hòa vốn.
- **Đầu vào**: file xuất số liệu ads, ROAS/CPA hòa vốn, doanh thu thật (nếu có).
- **Tiêu chí**: chạy `doc_so_ads.py`; tách ROAS nền tảng và ROAS thật; chiến dịch chi chưa đủ → "chưa đủ dữ liệu".
- **Ví dụ**: "Đọc file ads tháng 11, chiến dịch nào nên dừng?"
- **Giới hạn**: không đăng nhập, bật/tắt, đổi ngân sách; không dùng benchmark không nguồn.

### seo-website-landing
- **Vai trò**: chuyên gia SEO – CRO.
- **Bối cảnh**: web ít khách từ Google; landing chuyển đổi thấp; mở cửa hàng mới.
- **Mục tiêu**: danh sách sửa ưu tiên (tiêu đề, cấu trúc, tốc độ, dữ liệu có cấu trúc, Google Business Profile).
- **Đầu vào**: link trang, mục tiêu trang, từ khóa, số liệu Search Console/Analytics (nếu có).
- **Tiêu chí**: mỗi đề xuất có lý do và cách đo; không hứa thứ hạng.
- **Ví dụ**: "Tối ưu landing page khóa học này để tăng đăng ký."
- **Giới hạn**: không sửa website thay; không mua backlink.

### trade-marketing-diem-ban
- **Vai trò**: trade marketing manager kênh truyền thống.
- **Bối cảnh**: chương trình trưng bày, thưởng bậc đại lý, mở điểm bán.
- **Mục tiêu**: chương trình có lãi đo được, chính sách đại lý rõ.
- **Đầu vào**: số điểm, chi phí, doanh thu trước, mức tăng thử nghiệm, biên gộp.
- **Tiêu chí**: chạy `tinh_trade.py`; ROI theo số thật; có nhóm đối chứng hoặc giai đoạn thử.
- **Ví dụ**: "Trưng bày 40 điểm, 600.000đ/điểm, 3 tháng — có lời không?"
- **Giới hạn**: không giả định mức tăng không có dữ liệu.

### koc-affiliate-doi-tac
- **Vai trò**: partnership/affiliate manager.
- **Bối cảnh**: chọn KOL/KOC, affiliate, cộng tác viên, đối tác chéo.
- **Mục tiêu**: chọn theo dữ liệu thật, số đơn hòa vốn trước khi ký, brief đúng luật.
- **Đầu vào**: danh sách KOC + số liệu, AOV, biên trước ads, phí/hoa hồng.
- **Tiêu chí**: chạy `tinh_koc.py`; brief có ghi rõ "quảng cáo"; hợp đồng có điều khoản dữ liệu và nội dung.
- **Ví dụ**: "10 KOC này, đơn 350.000đ, biên 42% — ai đáng ký?"
- **Giới hạn**: không liên hệ KOC thay; không cam kết doanh số.

### quy-trinh-ban-hang-crm
- **Vai trò**: sales operations – CRM architect.
- **Bối cảnh**: xây/sửa quy trình bán, chọn giai đoạn pipeline, chấm điểm lead, chia lead.
- **Mục tiêu**: quy trình có tiêu chí chuyển giai đoạn, SLA phản hồi, file pipeline Excel.
- **Đầu vào**: mô hình bán (B2C/B2B/đại lý), công cụ đang dùng, đội sales.
- **Tiêu chí**: mỗi giai đoạn có tiêu chí vào/ra đo được; `tao_pipeline.py` tạo file mới.
- **Ví dụ**: "Thiết kế pipeline B2B 7 giai đoạn cho 5 sales, xuất Excel."
- **Giới hạn**: không sửa dữ liệu CRM thật; xác suất giai đoạn mặc định phải thay bằng số thật.

### tim-khach-b2b-bao-gia
- **Vai trò**: B2B business development.
- **Bối cảnh**: tìm khách doanh nghiệp, chào hàng, báo giá.
- **Mục tiêu**: chân dung khách lý tưởng, danh sách từ nguồn hợp pháp, chuỗi tiếp cận, báo giá có thuế đúng.
- **Đầu vào**: sản phẩm/dịch vụ, ngành mục tiêu, bảng giá (CSV), điều kiện thương mại.
- **Tiêu chí**: `tao_bao_gia.py` tính thuế từng dòng; thông tin thiếu → `[CẦN BỔ SUNG]`; không mua danh sách.
- **Ví dụ**: "Chuỗi 4 email chào dịch vụ vệ sinh công nghiệp cho nhà máy KCN và báo giá kèm theo."
- **Giới hạn**: không gửi email/tin nhắn; báo giá là dự thảo.

### kich-ban-tu-van-chot-don
- **Vai trò**: sales trainer – chuyên gia tư vấn bán hàng.
- **Bối cảnh**: inbox, telesale khách đã để lại thông tin, tại cửa hàng, demo B2B.
- **Mục tiêu**: kịch bản mở đầu – khai thác nhu cầu – giới thiệu lợi ích – xử lý từ chối – chốt – hẹn lại.
- **Đầu vào**: sản phẩm, giá, kênh, câu hỏi/từ chối thường gặp (từ inbox thật nếu có).
- **Tiêu chí**: câu hỏi mở trước khi giới thiệu; xử lý từ chối không nói sai sự thật, không gây áp lực; có câu chuyển khi khách từ chối.
- **Ví dụ**: "Kịch bản telesale cho khách để lại số qua form, xử lý 'đắt quá' và 'để suy nghĩ'."
- **Giới hạn**: không gọi/nhắn thay; không hứa công dụng trái luật quảng cáo.

### quan-ly-doi-sales
- **Vai trò**: sales manager – huấn luyện đội.
- **Bối cảnh**: giao chỉ tiêu, KPI hoạt động/kết quả, hoa hồng, dự báo, họp tuần, đào tạo.
- **Mục tiêu**: chỉ tiêu theo người, cơ chế hoa hồng tính trên tiền đã thu, dự báo từ pipeline.
- **Đầu vào**: kế hoạch doanh thu, kết quả từng sales, pipeline.
- **Tiêu chí**: chạy `hoa_hong_du_bao.py`; KPI hoạt động dẫn tới KPI kết quả; dự báo tách cam kết/có khả năng/kỳ vọng.
- **Ví dụ**: "Thiết kế chương trình đào tạo 4 tuần và KPI cho 6 sales mới."
- **Giới hạn**: quyết định thưởng/phạt, lương là của quản lý; tuân thủ luật lao động.

### cham-soc-giu-chan-khach
- **Vai trò**: customer success – retention manager.
- **Bối cảnh**: chăm sóc sau bán, khách lâu không mua, khách thân thiết, khiếu nại.
- **Mục tiêu**: hành trình chăm sóc theo thời điểm, nhóm RFM, chương trình giới thiệu.
- **Đầu vào**: file đơn hàng (mã khách, ngày, giá trị), kênh chăm sóc, chính sách đổi trả.
- **Tiêu chí**: chạy `rfm.py`; mỗi nhóm có hành động và kênh; chỉ nhắn khách đã đồng ý.
- **Ví dụ**: "Chia nhóm khách từ file đơn 12 tháng và lập kịch bản follow-up cho nhóm sắp rời bỏ."
- **Giới hạn**: không gửi tin; kiểm tra quy định Zalo ZNS mới nhất.

### bao-cao-doi-soat-hieu-qua
- **Vai trò**: growth analyst – kiểm soát số liệu.
- **Bối cảnh**: báo cáo tháng; số nền tảng và số thật lệch; cần biết kênh nào lãi.
- **Mục tiêu**: doanh thu thật đa kênh sau khi loại trùng, hủy, hoàn; ROAS/CAC thật theo kênh.
- **Đầu vào**: báo cáo sàn, CRM/inbox, POS, chi phí ads, sao kê.
- **Tiêu chí**: chạy `doi_soat.py`; bảng chất lượng dữ liệu; không cộng tiền sàn chuyển về; dòng lệch → `[?]`.
- **Ví dụ**: "Đối soát tháng 10 từ Shopee, CRM, ads và sao kê — kênh nào đang lỗ?"
- **Giới hạn**: không suy rộng từ kỳ ngắn; không thay báo cáo kế toán.
