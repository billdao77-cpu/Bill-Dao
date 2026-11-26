#!/usr/bin/env python3
"""Phân tích báo cáo tài chính DNNVV theo mã chỉ tiêu B01a-DNN / B02-DNN (TT133/2016) – bản vn-custom.

Kiểm tra số liệu TRƯỚC khi tính: 200 = 500; 200 = 110+…+180; 500 = 300+400; 10 = 01−02; 20 = 10−11; 30 = 20+21−22−24;
40 = 31−32; 50 = 30+40; 60 = 50−51. Sai lệch → báo lỗi, tỷ số vẫn tính nhưng đánh dấu "số liệu chưa khớp".

CSV đầu vào: chi_tieu,nam_nay,nam_truoc   (mã B01a cuối năm và B02 cả năm; nam_truoc có thể để trống)
  python3 phan_tich_tai_chinh.py bctc.csv --ten-dn "Công ty ABC" --nam 2026 [--xlsx phan_tich_2026.xlsx]

Tỷ số (TT133 không tách ngắn hạn/dài hạn → các chỉ số thanh toán là XẤP XỈ):
  biên LN gộp 20/10 · biên LN ròng 60/10 · thanh toán hiện hành ≈ (110+120+130+140)/300 · thanh toán nhanh ≈ (110+120+130)/300
  nợ/vốn chủ 300/400 · ROA 60/bq(200) · ROE 60/bq(400) · vòng quay phải thu 10/bq(131) · vòng quay hàng tồn kho 11/bq(141|140)
  khả năng trả lãi (50+23)/23.  bq = bình quân (năm trước + năm nay)/2; thiếu năm trước → dùng số cuối kỳ, ghi rõ.

>>> chuan_so("1.250.000"), chuan_so("(2.000.000)"), chuan_so(""), chuan_so("12,5")
(1250000.0, -2000000.0, None, 12.5)
"""
import argparse
import csv
import io
import sys

import an_toan  # vn-custom: không ghi đè, chống chèn công thức  # noqa: E402

KIEM_TRA = [
    ("200", ["110", "120", "130", "140", "150", "160", "170", "180"], "+", "Tổng tài sản = 110+…+180"),
    ("500", ["300", "400"], "+", "Tổng nguồn vốn = 300+400"),
    ("10", ["01", "-02"], "", "10 = 01 − 02"),
    ("20", ["10", "-11"], "", "20 = 10 − 11"),
    ("30", ["20", "21", "-22", "-24"], "", "30 = 20 + 21 − 22 − 24"),
    ("40", ["31", "-32"], "", "40 = 31 − 32"),
    ("50", ["30", "40"], "", "50 = 30 + 40"),
    ("60", ["50", "-51"], "", "60 = 50 − 51"),
]


def chuan_so(s):
    if s is None:
        return None
    s = str(s).strip().replace(" ", "").replace("đ", "")
    if not s:
        return None
    am = s.startswith("(") and s.endswith(")")
    s = s.strip("()")
    if s.count(".") >= 1 and "," not in s and all(len(p) == 3 for p in s.split(".")[1:]):
        s = s.replace(".", "")
    s = s.replace(",", ".")
    v = float(s)
    return -v if am else v


def doc(path_or_text):
    f = path_or_text if isinstance(path_or_text, io.StringIO) else open(path_or_text, encoding="utf-8-sig")
    with f:
        r = csv.DictReader(f)
        thieu = {"chi_tieu", "nam_nay"} - set(r.fieldnames or [])
        if thieu:
            raise ValueError(f"CSV thiếu cột: {', '.join(sorted(thieu))}")
        nay, truoc, loi = {}, {}, []
        for i, d in enumerate(r, 2):
            ma = (d.get("chi_tieu") or "").strip().zfill(2)
            try:
                v1, v0 = chuan_so(d.get("nam_nay")), chuan_so(d.get("nam_truoc"))
            except ValueError:
                loi.append(f"Dòng {i} (chỉ tiêu {ma}): số không đọc được → [?]")
                continue
            if ma in nay:
                loi.append(f"Dòng {i}: chỉ tiêu {ma} bị lặp")
            if v1 is not None:
                nay[ma] = v1
            if v0 is not None:
                truoc[ma] = v0
    return nay, truoc, loi


def kiem_tra_khop(c, nhan):
    loi = []
    for tong, thanh_phan, _, mo_ta in KIEM_TRA:
        if tong not in c:
            continue
        co = [x.lstrip("-") for x in thanh_phan if x.lstrip("-") in c]
        if not co:
            continue
        tinh = sum((-1 if x.startswith("-") else 1) * c.get(x.lstrip("-"), 0.0) for x in thanh_phan)
        if abs(tinh - c[tong]) > 1:
            loi.append(f"{nhan}: {mo_ta} không khớp – báo cáo {c[tong]:,.0f}, tính lại {tinh:,.0f}".replace(",", "."))
    if "200" in c and "500" in c and abs(c["200"] - c["500"]) > 1:
        loi.append(f"{nhan}: Tổng tài sản (200) ≠ Tổng nguồn vốn (500)")
    if c.get("400", 0) < 0:
        loi.append(f"{nhan}: Vốn chủ sở hữu (400) âm – ROE, nợ/vốn chủ không có ý nghĩa thông thường")
    return loi


def _chia(a, b):
    return None if a is None or not b else a / b


def _bq(nay, truoc, ma):
    if ma not in nay:
        return None, ""
    if ma in truoc:
        return (nay[ma] + truoc[ma]) / 2, "bình quân"
    return nay[ma], "cuối kỳ (thiếu năm trước)"


def ty_so(nay, truoc):
    g = nay.get
    kq = []

    def them(ten, v, dang, cong_thuc, ghi_chu=""):
        kq.append({"ty_so": ten, "gia_tri": v, "dang": dang, "cong_thuc": cong_thuc, "ghi_chu": ghi_chu})

    them("Biên lợi nhuận gộp", _chia(g("20"), g("10")), "%", "20/10")
    them("Biên lợi nhuận ròng", _chia(g("60"), g("10")), "%", "60/10")
    ts_nh = sum(g(x, 0.0) for x in ("110", "120", "130", "140")) if "300" in nay else None
    them("Khả năng thanh toán hiện hành (xấp xỉ)", _chia(ts_nh, g("300")), "lần", "(110+120+130+140)/300",
         "TT133 không tách ngắn/dài hạn")
    them("Khả năng thanh toán nhanh (xấp xỉ)", _chia(sum(g(x, 0.0) for x in ("110", "120", "130")) if "300" in nay else None,
                                                     g("300")), "lần", "(110+120+130)/300", "TT133 không tách ngắn/dài hạn")
    them("Nợ phải trả / Vốn chủ sở hữu", _chia(g("300"), g("400")) if g("400", 0) > 0 else None, "lần", "300/400")
    for ten, tu, ma, dang in (("ROA", "60", "200", "%"), ("ROE", "60", "400", "%")):
        bq, kieu = _bq(nay, truoc, ma)
        them(ten, _chia(g(tu), bq) if (bq or 0) > 0 else None, dang, f"{tu}/{ma} {kieu}".strip())
    bq, kieu = _bq(nay, truoc, "131")
    vq = _chia(g("10"), bq)
    them("Vòng quay phải thu khách hàng", vq, "vòng", f"10/131 {kieu}".strip())
    them("Kỳ thu tiền bình quân", _chia(365, vq), "ngày", "365/vòng quay phải thu")
    ma_htk = "141" if "141" in nay else "140"
    bq, kieu = _bq(nay, truoc, ma_htk)
    vq = _chia(g("11"), bq)
    them("Vòng quay hàng tồn kho", vq, "vòng", f"11/{ma_htk} {kieu}".strip())
    them("Số ngày tồn kho bình quân", _chia(365, vq), "ngày", "365/vòng quay hàng tồn kho")
    them("Khả năng trả lãi vay", _chia((g("50") or 0) + (g("23") or 0), g("23")) if g("23") else None, "lần", "(50+23)/23")
    return kq


def bien_dong(nay, truoc):
    ds = []
    for ma, ten in (("10", "Doanh thu thuần"), ("20", "Lợi nhuận gộp"), ("60", "Lợi nhuận sau thuế"),
                    ("200", "Tổng tài sản"), ("300", "Nợ phải trả"), ("400", "Vốn chủ sở hữu"), ("131", "Phải thu khách hàng"),
                    ("141", "Hàng tồn kho")):
        if ma in nay and ma in truoc:
            tang = nay[ma] - truoc[ma]
            ds.append({"chi_tieu": f"{ma} {ten}", "nam_nay": nay[ma], "nam_truoc": truoc[ma], "chenh_lech": tang,
                       "ty_le": _chia(tang, abs(truoc[ma]))})
    return ds


def _in(v, dang):
    if v is None:
        return "không tính được"
    if dang == "%":
        return f"{v * 100:.1f}%".replace(".", ",")
    if dang == "ngày":
        return f"{v:.0f} ngày"
    return f"{v:.2f} {dang}".replace(".", ",")


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("file", nargs="?")
    ap.add_argument("--ten-dn", default="[CẦN BỔ SUNG: tên doanh nghiệp]")
    ap.add_argument("--nam", default="[CẦN BỔ SUNG: năm]")
    ap.add_argument("--xlsx")
    ap.add_argument("--self-test", action="store_true")
    a = ap.parse_args(argv)
    if a.self_test:
        return self_test()
    if not a.file:
        ap.error("cần file CSV chi_tieu,nam_nay,nam_truoc")
    nay, truoc, loi = doc(a.file)
    loi += kiem_tra_khop(nay, "Năm nay") + (kiem_tra_khop(truoc, "Năm trước") if truoc else [])
    kq, bd = ty_so(nay, truoc), bien_dong(nay, truoc)
    print(f"PHÂN TÍCH BÁO CÁO TÀI CHÍNH – {a.ten_dn} – năm {a.nam}")
    print("\nKIỂM TRA SỐ LIỆU: " + ("khớp." if not loi else f"{len(loi)} vấn đề – tỷ số dưới đây CHƯA đáng tin cho đến khi sửa:"))
    for x in loi:
        print("  ✗ " + x)
    print("\nTỶ SỐ:")
    for x in kq:
        print(f"  {x['ty_so']:42} {_in(x['gia_tri'], x['dang']):>16}   ({x['cong_thuc']}{'; ' + x['ghi_chu'] if x['ghi_chu'] else ''})")
    if bd:
        print("\nBIẾN ĐỘNG SO NĂM TRƯỚC:")
        for x in bd:
            tl = "" if x["ty_le"] is None else f" ({x['ty_le'] * 100:+.1f}%)".replace(".", ",")
            print(f"  {x['chi_tieu']:32} {x['chenh_lech']:>+20,.0f}{tl}".replace(",", "."))
    print("\nĐã kiểm tra phép tính. Tỷ số là chỉ báo – cần đọc cùng thuyết minh và bối cảnh ngành; không có 'mức chuẩn' "
          "nếu chưa có nguồn so sánh cùng ngành, cùng quy mô.")
    if a.xlsx:
        from openpyxl import Workbook
        wb = Workbook()
        ws = wb.active
        ws.title = "Ty so"
        ws.append(["Tỷ số", "Giá trị", "Đơn vị", "Công thức", "Ghi chú"])
        for x in kq:
            ws.append([x["ty_so"], x["gia_tri"], x["dang"], x["cong_thuc"], x["ghi_chu"]])
        ws2 = wb.create_sheet("Kiem tra so lieu")
        ws2.append(["Vấn đề"])
        for x in loi or ["Số liệu khớp"]:
            ws2.append([x])
        an_toan.luu_xlsx(wb, a.xlsx)
        print(f"Đã ghi {a.xlsx}")
    return 1 if loi else 0


def self_test():
    import doctest
    assert doctest.testmod().failed == 0
    du = io.StringIO("chi_tieu,nam_nay,nam_truoc\n110,200000000,150000000\n130,300000000,250000000\n131,280000000,220000000\n"
                     "140,250000000,200000000\n141,250000000,200000000\n150,250000000,300000000\n200,1000000000,900000000\n"
                     "300,400000000,380000000\n400,600000000,520000000\n500,1000000000,900000000\n01,3100000000,2600000000\n"
                     "02,100000000,100000000\n10,3000000000,2500000000\n11,2200000000,1900000000\n20,800000000,600000000\n"
                     "21,0,0\n22,40000000,30000000\n23,40000000,30000000\n24,560000000,450000000\n30,200000000,120000000\n"
                     "31,0,0\n32,0,0\n40,0,0\n50,200000000,120000000\n51,40000000,24000000\n60,160000000,96000000\n")
    nay, truoc, loi = doc(du)
    assert not loi and not kiem_tra_khop(nay, "x") and not kiem_tra_khop(truoc, "y"), kiem_tra_khop(nay, "x")
    k = {x["ty_so"]: x["gia_tri"] for x in ty_so(nay, truoc)}
    assert abs(k["Biên lợi nhuận gộp"] - 800 / 3000) < 1e-9
    assert abs(k["Khả năng thanh toán hiện hành (xấp xỉ)"] - 750 / 400) < 1e-9
    assert abs(k["ROE"] - 160 / 560) < 1e-9 and abs(k["Vòng quay phải thu khách hàng"] - 3000 / 250) < 1e-9
    assert abs(k["Khả năng trả lãi vay"] - 6.0) < 1e-9
    nay["200"] = 999_000_000
    assert any("200" in x for x in kiem_tra_khop(nay, "x"))
    nay2, _, _ = doc(io.StringIO("chi_tieu,nam_nay,nam_truoc\n10,0,\n20,5,\n"))
    assert ty_so(nay2, {})[0]["gia_tri"] is None  # chia cho 0 → không tính được
    print("self-test OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
