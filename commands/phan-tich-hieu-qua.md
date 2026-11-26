---
description: Workflow 5 – Phân tích hiệu quả kinh doanh: thu thập dữ liệu → kiểm tra chất lượng → phân tích KPI → xác định vấn đề → đề xuất giải pháp → kế hoạch đo lường kết quả.
argument-hint: "[kỳ phân tích, các file số liệu (ads, sàn, CRM, sao kê, đơn hàng), mục tiêu]"
---

Phân tích hiệu quả kinh doanh cho: $ARGUMENTS

Giao cho agent `growth-analyst`.

1. **Thu thập dữ liệu** – danh sách nguồn, kỳ, cột chính; nguồn thiếu → ảnh hưởng tới kết luận.
2. **Kiểm tra chất lượng dữ liệu** – trùng, hủy/hoàn, lệch cột, kỳ, đơn vị; bảng chất lượng (nguồn – vấn đề – cách xử lý – ảnh hưởng).
3. **Phân tích KPI** – `doi_soat.py` (doanh thu thật đa kênh), `doc_so_ads.py`, `rfm.py`, `hoa_hong_du_bao.py` tùy dữ liệu; so ngưỡng hòa vốn; phễu theo tầng.
4. **Xác định vấn đề** – xếp hạng điểm nghẽn theo tác động tới lợi nhuận; tách nguyên nhân dữ liệu với nguyên nhân kinh doanh.
5. **Đề xuất giải pháp** – tối đa 3 việc ưu tiên: giả thuyết, việc làm, người, chi phí ước tính [Giả định], kỳ vọng có nhãn.
6. **Đo lường kết quả** – chỉ số, giá trị nền, ngưỡng thành công, thời gian đo, cách so (trước/sau, nhóm đối chứng).

Đầu ra: báo cáo 1 trang (kết luận → bảng KPI → điểm nghẽn → 3 việc ưu tiên → kế hoạch đo) + bảng "Cần anh/chị kiểm tra". Không kết luận khi dữ liệu chưa đủ kỳ hoặc chi tiêu chưa đủ.
