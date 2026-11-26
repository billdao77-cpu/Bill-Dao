---
description: Khóa sổ tháng – đối soát ngân hàng, công nợ, khấu hao – phân bổ – trích trước, kiểm tra bút toán và bảng cân đối số phát sinh, checklist khóa sổ; mọi bút toán điều chỉnh là đề xuất.
argument-hint: "[tháng/năm, file sổ 112, sao kê, sổ chi tiết công nợ, danh sách TSCĐ/CCDC, file bút toán]"
---

Khóa sổ cho: $ARGUMENTS

1. Skill `khoa-so-cuoi-ky`: checklist theo thứ tự; khấu hao và phân bổ 242 (`khau_hao.py`), trích trước 335.
2. Skill `doi-soat`: sổ 112 ↔ sao kê (`doi_soat_ngan_hang.py`), tuổi nợ phải thu/phải trả (`tuoi_no.py`).
3. Skill `kiem-tra-chung-tu` cho chứng từ phát sinh chưa ghi sổ.
4. Skill `dinh-khoan`: kiểm tra toàn bộ bút toán (`kiem_tra_but_toan.py`) – cân Nợ/Có, tài khoản tồn tại trong TT133.
5. Agent `ke-toan-truong-soat-xet` soát xét kết quả.

Đầu ra: (1) checklist ☑/☐ với bằng chứng; (2) bảng bút toán điều chỉnh **đề xuất** (Nợ – Có – số tiền – lý do – chứng từ); (3) chênh lệch chưa giải thích; (4) file Excel mới nếu cần. Không sửa sổ gốc.
