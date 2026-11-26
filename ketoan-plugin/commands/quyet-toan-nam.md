---
description: Quyết toán năm – khóa sổ năm, lập nháp BCTC TT133, kiểm tra số liệu, quyết toán TNDN (thuế suất, miễn giảm, chuyển lỗ), phân tích tài chính và lịch nộp; không tự nộp.
argument-hint: "[năm, bảng cân đối số phát sinh trước kết chuyển, doanh thu năm trước, các khoản điều chỉnh thuế]"
---

Quyết toán năm cho: $ARGUMENTS

1. `khoa-so-cuoi-ky` (cuối năm) – checklist, bút toán kết chuyển đề xuất.
2. `bao-cao-tai-chinh` – nháp B01a/B02/F01 (`lap_bctc.py --xlsx <tên mới>.xlsx`); kiểm tra số liệu và tỷ số (`phan_tich_tai_chinh.py`).
3. `thue-tndn` – quyết toán (`tinh_tndn.py`): thuế suất theo doanh thu năm trước, khoản không được trừ, miễn/giảm, chuyển lỗ.
4. Agent `ke-toan-truong-soat-xet` soát xét BCTC và quyết toán.
5. `lich-thue-dn` – hạn nộp BCTC và quyết toán.

Đầu ra: bộ BCTC nháp + bảng kiểm tra số liệu; bảng tính TNDN theo chỉ tiêu; danh sách điều chỉnh tăng/giảm có căn cứ; rủi ro khi quyết toán; việc người dùng tự làm (ký, nộp).
