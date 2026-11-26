"""An toàn khi ghi file kết quả (bản vn-custom) – chép vào scripts/ của mọi skill bởi custom/dong_bo.py.

1. Không ghi đè file đã có, không ghi đè chính file nguồn. Muốn ghi đè file kết quả cũ (chỉ khi người dùng đồng ý rõ):
   thêm cờ --ghi-de (vẫn không bao giờ ghi đè file nguồn).
2. Kiểm tra đuôi file kết quả.
3. Chống chèn công thức: dữ liệu từ Excel/CSV khách hàng, bảng trong PDF bên ngoài có thể chứa chuỗi như
   =HYPERLINK("http://...") hoặc =WEBSERVICE(...). Script văn phòng không tự tạo công thức nào, nên MỌI ô công thức
   trong file xuất ra được chuyển thành chữ (giữ nguyên nội dung, không chạy).

>>> o_csv("=1+2"), o_csv("@SUM(A1)"), o_csv("Nguyễn Văn A"), o_csv(5)
("'=1+2", "'@SUM(A1)", 'Nguyễn Văn A', 5)
>>> import tempfile, os
>>> d = tempfile.mkdtemp(); f = os.path.join(d, "a.xlsx"); open(f, "w").close()
>>> try:
...     kiem_tra_dich(f, ".xlsx")
... except SystemExit as e:
...     print("chặn", e.code)
chặn 2
>>> try:
...     kiem_tra_dich(os.path.join(d, "b.txt"), ".xlsx")
... except SystemExit as e:
...     print("chặn", e.code)
chặn 2
"""
import os
import sys

GHI_DE = "--ghi-de" in sys.argv
if GHI_DE:  # bỏ cờ trước khi script đọc sys.argv
    sys.argv = [x for x in sys.argv if x != "--ghi-de"]


def _loi(msg):
    print("LỖI: " + msg, file=sys.stderr)
    raise SystemExit(2)


def kiem_tra_dich(path, duoi=None, nguon=()):
    p = os.path.realpath(str(path))
    if duoi and not p.lower().endswith(duoi):
        _loi(f"{path} phải có đuôi {duoi}")
    if any(os.path.realpath(str(x)) == p for x in nguon if x):
        _loi(f"{path} trùng file nguồn – không ghi đè file gốc, hãy đặt tên file kết quả khác")
    if os.path.exists(p) and not GHI_DE:
        _loi(f"{path} đã tồn tại – không ghi đè để tránh mất dữ liệu. Đặt tên file mới, hoặc thêm --ghi-de khi "
             "người dùng đồng ý rõ.")


def o_csv(v):
    if isinstance(v, str) and v[:1] in ("=", "+", "-", "@", "\t", "\r"):
        return "'" + v
    return v


def vo_hieu_cong_thuc(wb):
    """Chuyển mọi ô công thức thành chữ; trả số ô đã chuyển và in cảnh báo nếu có."""
    n = 0
    for ws in wb.worksheets:
        for row in ws.iter_rows():
            for c in row:
                if c.data_type == "f":
                    c.data_type = "s"
                    n += 1
    if n:
        print(f"CẢNH BÁO: {n} ô dữ liệu có dạng công thức (ví dụ =HYPERLINK...) đã được giữ ở dạng chữ, không chạy – "
              "kiểm tra nguồn dữ liệu.", file=sys.stderr)
    return n


if __name__ == "__main__":
    import doctest
    print("self-test OK" if doctest.testmod().failed == 0 else "self-test LỖI")
