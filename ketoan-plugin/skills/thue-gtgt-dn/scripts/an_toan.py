"""An toàn khi ghi file kết quả (bản vn-custom) – chép vào scripts/ của mọi skill bởi custom/dong_bo.py.

1. Không ghi đè file đã có. Muốn ghi đè (chỉ khi người dùng đồng ý rõ): thêm cờ --ghi-de vào lệnh.
2. Kiểm tra đuôi file (.xlsx/.csv/.ics/.docx).
3. Chống chèn công thức (formula/CSV injection): dữ liệu lấy từ hóa đơn XML của nhà cung cấp, diễn giải sao kê do
   người chuyển tiền tự gõ, tên khách hàng... có thể chứa chuỗi bắt đầu bằng '=' như =HYPERLINK("http://...")
   hoặc =WEBSERVICE(...). openpyxl hiểu chuỗi đó là công thức → Excel chạy được. Module này chỉ giữ lại công thức
   do chính script tạo (SUM và phép + - * / giữa các ô); mọi công thức khác chuyển thành chữ thường.

>>> la_cong_thuc_noi_bo("=SUM(C2:C10)"), la_cong_thuc_noi_bo("=D3+E3-F3"), la_cong_thuc_noi_bo("=G2")
(True, True, True)
>>> la_cong_thuc_noi_bo('=HYPERLINK("http://x","y")'), la_cong_thuc_noi_bo("=WEBSERVICE(A1)"), la_cong_thuc_noi_bo("=cmd|' /c calc'!A0")
(False, False, False)
>>> o_csv("=1+2"), o_csv("+84 912"), o_csv("Công ty A"), o_csv(12000)
("'=1+2", "'+84 912", 'Công ty A', 12000)
"""
import os
import re
import sys

GHI_DE = "--ghi-de" in sys.argv
if GHI_DE:  # bỏ cờ trước khi argparse của script đọc sys.argv
    sys.argv = [x for x in sys.argv if x != "--ghi-de"]

_O = re.compile(r"\$?[A-Z]{1,3}\$?\d+")


def la_cong_thuc_noi_bo(s):
    if not isinstance(s, str) or not s.startswith("="):
        return False
    than = s[1:]
    if not re.fullmatch(r"[A-Z0-9:+\-*/() $.]*", than):
        return False
    for t in re.findall(r"\$?[A-Z]+\$?\d*", than):
        if t != "SUM" and not _O.fullmatch(t):
            return False
    return True


def o_csv(v):
    if isinstance(v, str) and v[:1] in ("=", "+", "-", "@", "\t", "\r"):
        return "'" + v
    return v


def dong_csv(dong):
    return [o_csv(v) for v in dong]


def _kiem_tra_dich(path, duoi):
    p = str(path)
    if not p.lower().endswith(duoi):
        print(f"LỖI: {p} phải có đuôi {duoi}", file=sys.stderr)
        raise SystemExit(2)
    if os.path.exists(p) and not GHI_DE:
        print(f"LỖI: {p} đã tồn tại – không ghi đè để tránh mất dữ liệu. Đặt tên file mới, hoặc thêm --ghi-de khi "
              "người dùng đồng ý rõ.", file=sys.stderr)
        raise SystemExit(2)


def lam_sach_wb(wb):
    """Chuyển mọi ô công thức không do script tạo thành chữ; trả số ô đã chuyển."""
    n = 0
    for ws in wb.worksheets:
        for row in ws.iter_rows():
            for c in row:
                if c.data_type == "f" and not la_cong_thuc_noi_bo(c.value):
                    c.data_type = "s"
                    n += 1
    return n


def luu_xlsx(wb, path):
    _kiem_tra_dich(path, ".xlsx")
    n = lam_sach_wb(wb)
    if n:
        print(f"CẢNH BÁO: {n} ô dữ liệu có dạng công thức (có thể từ hóa đơn/sao kê bên ngoài) đã được giữ ở dạng chữ, "
              "không chạy – kiểm tra nguồn dữ liệu.", file=sys.stderr)
    wb.save(path)


def luu_docx(doc, path):
    _kiem_tra_dich(path, ".docx")
    doc.save(path)


def mo_ghi(path, duoi, **kw):
    _kiem_tra_dich(path, duoi)
    return open(path, "w", **kw)


if __name__ == "__main__":
    import doctest
    print("self-test OK" if doctest.testmod().failed == 0 else "self-test LỖI")
