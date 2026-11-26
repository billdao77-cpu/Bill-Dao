#!/usr/bin/env python3
"""Lập file Word "Hướng dẫn điền tờ khai thuế GTGT" (Mẫu 01/GTGT – Thông tư 89/2026/TT-BTC, kỳ tính thuế từ 01/7/2026)
từ bảng kê hóa đơn (cùng định dạng CSV với tinh_gtgt.py). Gọn, không thừa:
  1. Bảng chỉ tiêu cần điền: chỉ tiêu – nội dung – số điền – lấy từ đâu (chỉ tiêu khác để trống)
  2. Phụ lục giảm thuế GTGT (hàng 8% – Mẫu 01 Phụ lục III NĐ 174/2025) nếu có
  3. Hóa đơn không đưa vào khấu trừ: lý do – việc cần làm
  4. Nộp tờ khai và tiền: hạn (có xét gia hạn NĐ 245/2026)
  5. Kỳ sau nhớ

Cột CSV: chieu (mua-vao|ban-ra), ngay, ban_mst, ban_ten, so, tien_hang, tien_thue, tsuat, thanh_toan (CK|TM|trống), loai_tru, ly_do,
  ten_hang (bán ra 8%: tên hàng hóa, dịch vụ để lập phụ lục giảm thuế)
  loai_tru:  x            → hóa đơn hợp pháp nhưng không được khấu trừ (vẫn ghi [23], [24], không vào [25])
             khong_hop_le → hóa đơn chưa hợp lệ với đơn vị (sai MST người mua, hóa đơn trùng...): không đưa vào tờ khai kỳ này
  Bán ra thuế suất 8% = hàng được giảm từ 10%: khai trong [32], [33] (= [32] × 10% − thuế được giảm) + phụ lục giảm thuế.

  python3 huong_dan_to_khai.py bang_ke.csv --ky 10/2026 --con-khau-tru-ky-truoc 1850000 --ten "Công ty..." --mst 0319876543 --ra huong-dan.docx
"""
import argparse
import csv
import datetime as dt
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from tinh_gtgt import NGUONG, d, so  # noqa: E402
import an_toan  # vn-custom: không ghi đè, chống chèn công thức  # noqa: E402

# Gia hạn nộp TIỀN thuế GTGT năm 2026 (NĐ 245/2026) – chỉ DN nhỏ, siêu nhỏ hoặc ngành Phụ lục I, đã gửi đề nghị trước 02/11/2026
GIA_HAN_2026 = {"05/2026": "20/11/2026", "06/2026": "21/12/2026", "07/2026": "21/12/2026", "08/2026": "21/12/2026",
                "09/2026": "21/12/2026", "Q2/2026": "02/11/2026", "Q3/2026": "30/12/2026"}
TEN_CT = {"21": "Không phát sinh hoạt động mua, bán trong kỳ", "22": "Thuế GTGT còn được khấu trừ kỳ trước chuyển sang",
          "23": "Giá trị hàng hóa, dịch vụ mua vào (chưa thuế)", "24": "Thuế GTGT của hàng hóa, dịch vụ mua vào",
          "25": "Thuế GTGT mua vào được khấu trừ kỳ này", "26": "Hàng hóa, dịch vụ bán ra không chịu thuế GTGT",
          "27": "Hàng hóa, dịch vụ bán ra chịu thuế – giá trị", "28": "Hàng hóa, dịch vụ bán ra chịu thuế – thuế",
          "29": "Bán ra thuế suất 0%", "30": "Bán ra thuế suất 5% – giá trị", "31": "Bán ra thuế suất 5% – thuế",
          "32": "Bán ra thuế suất 10% (gồm hàng giảm còn 8%) – giá trị", "33": "Bán ra thuế suất 10% – thuế (HTKK tự trừ phần được giảm)",
          "34": "Tổng doanh thu bán ra", "35": "Tổng thuế GTGT bán ra", "36": "Thuế GTGT phát sinh trong kỳ ([35] − [25])",
          "37": "Điều chỉnh giảm", "38": "Điều chỉnh tăng",
          "40a": "Thuế GTGT phải nộp của hoạt động SXKD ([36] − [22] + [37] − [38] − [39a])", "40": "Thuế GTGT còn phải nộp trong kỳ",
          "41": "Thuế GTGT chưa khấu trừ hết kỳ này", "43": "Thuế GTGT còn được khấu trừ chuyển kỳ sau"}


def _ky(ky):
    """'10/2026' → ('thang', 10, 2026); 'Q3/2026' → ('quy', 3, 2026)."""
    a, y = ky.upper().split("/")
    return ("quy", int(a[1:]), int(y)) if a.startswith("Q") else ("thang", int(a), int(y))


def _han(ky):
    loai, n, y = _ky(ky)
    if loai == "thang":
        return dt.date(y + (n == 12), n % 12 + 1, 20)
    m = n * 3 % 12 + 1
    y2 = y + (n == 4)
    return dt.date(y2 + (m == 12), m % 12 + 1, 1) - dt.timedelta(days=1)


def _lui_ngay_nghi(day):
    while day.weekday() >= 5:  # ngày lễ: đối chiếu thêm lịch nghỉ lễ
        day += dt.timedelta(days=1)
    return day


def _ngay_vn(s):
    s = (s or "")[:10]
    return f"{s[8:10]}/{s[5:7]}/{s[:4]}" if len(s) == 10 and s[4] == "-" else s


def tinh_chi_tieu(rows, con_kt_truoc=0.0):
    mua = [r for r in rows if r.get("chieu") == "mua-vao"]
    ban = [r for r in rows if r.get("chieu") == "ban-ra"]
    hop_le = [r for r in mua if (r.get("loai_tru") or "").strip().lower() != "khong_hop_le"]
    nhom = {}
    for r in hop_le:
        k = (r.get("ban_mst", ""), r.get("ngay", "")[:10])
        nhom[k] = nhom.get(k, 0) + so(r["tien_hang"]) + so(r["tien_thue"])
    loai, cho_ck = [], []
    duoc_kt = 0.0
    for r in mua:
        lt = (r.get("loai_tru") or "").strip().lower()
        lon = nhom.get((r.get("ban_mst", ""), r.get("ngay", "")[:10]), 0) >= NGUONG
        tt = (r.get("thanh_toan") or "").strip().upper()
        if lt == "khong_hop_le":
            loai.append((r, "Không đưa vào tờ khai kỳ này", r.get("ly_do") or "Hóa đơn chưa hợp lệ với đơn vị"))
        elif lt:
            loai.append((r, "Ghi [23], [24]; không khấu trừ", r.get("ly_do") or "Không đủ điều kiện khấu trừ"))
        elif lon and tt == "TM":
            loai.append((r, "Ghi [23], [24]; không khấu trừ",
                         r.get("ly_do") or "Từ 5 triệu (cùng người bán, cùng ngày) nhưng trả tiền mặt"))
        else:
            duoc_kt += so(r["tien_thue"])
            if lon and tt != "CK":
                cho_ck.append(r)
    ct = {"22": con_kt_truoc, "23": sum(so(r["tien_hang"]) for r in hop_le), "24": sum(so(r["tien_thue"]) for r in hop_le),
          "25": duoc_kt, "26": 0.0, "29": 0.0, "30": 0.0, "31": 0.0, "32": 0.0, "33": 0.0}
    giam, giam_hang = 0.0, {}
    for r in ban:
        ts = (r.get("tsuat") or "").replace("%", "").strip()
        th, thue = so(r["tien_hang"]), so(r["tien_thue"])
        if ts in ("KCT", "kct"):
            ct["26"] += th
        elif ts == "0":
            ct["29"] += th
        elif ts == "5":
            ct["30"] += th
            ct["31"] += thue
        else:  # 10% và 8% (giảm từ 10%)
            ct["32"] += th
            ct["33"] += thue
            if ts == "8":
                giam += th
                ten = (r.get("ten_hang") or "").strip() or "THIẾU – ghi tên hàng hóa, dịch vụ"
                giam_hang[ten] = giam_hang.get(ten, 0) + th
    ct["27"] = ct["29"] + ct["30"] + ct["32"]
    ct["28"] = ct["31"] + ct["33"]
    ct["34"] = ct["26"] + ct["27"]
    ct["35"] = ct["28"]
    ct["36"] = ct["35"] - ct["25"]
    ct["37"] = ct["38"] = 0.0
    con = ct["36"] - ct["22"] + ct["37"] - ct["38"]
    ct["40a"] = ct["40"] = max(con, 0.0)
    ct["41"] = ct["43"] = max(-con, 0.0)
    ct["21"] = "X" if not mua and not ban else ""
    pl = {"gia_tri": giam, "thue_duoc_giam": round(giam * 0.02),
          "hang": [(k, v, round(v * 0.02)) for k, v in giam_hang.items()]} if giam else None
    return ct, loai, cho_ck, pl


def lap_file(ra, ct, loai, cho_ck, pl, ky, ten="", mst="", nhac=()):
    from docx import Document
    from docx.shared import Cm, Pt

    doc = Document()
    sec = doc.sections[0]
    for c in ("left_margin", "right_margin", "top_margin", "bottom_margin"):
        setattr(sec, c, Cm(1.8))
    doc.styles["Normal"].font.name, doc.styles["Normal"].font.size = "Times New Roman", Pt(11)

    def dam(text, co=None):
        r = doc.add_paragraph().add_run(text)
        r.bold = True
        if co:
            r.font.size = Pt(co)

    def bang(tieu_de, hang, rong):
        t = doc.add_table(rows=1, cols=len(tieu_de))
        t.style, t.autofit = "Table Grid", False
        for c, v in zip(t.rows[0].cells, tieu_de):
            c.text = v
            c.paragraphs[0].runs[0].bold = True
        for row in hang:
            for c, v in zip(t.add_row().cells, row):
                c.text = str(v)
        for col, w in zip(t.columns, rong):
            col.width = Cm(w)
        for row in t.rows:
            for c, w in zip(row.cells, rong):
                c.width = Cm(w)

    loai_ky, n, y = _ky(ky)
    ten_ky = f"tháng {n:02d}/{y}" if loai_ky == "thang" else f"quý {n}/{y}"
    dam(f"HƯỚNG DẪN ĐIỀN TỜ KHAI THUẾ GTGT {ten_ky.upper()}", 15)
    doc.add_paragraph(" – ".join(x for x in [ten, f"MST {mst}" if mst else "",
                                              "Mẫu 01/GTGT (Thông tư 89/2026/TT-BTC), phương pháp khấu trừ"] if x))

    dam("1. Chỉ tiêu cần điền (các chỉ tiêu khác để trống)")
    nguon = {"22": "Chỉ tiêu [43] tờ khai kỳ trước", "23": "Bảng kê mua vào – hóa đơn hợp lệ", "24": "Bảng kê mua vào – hóa đơn hợp lệ",
             "25": "Thuế mua vào đủ điều kiện (đã loại mục 3)", "32": "Bảng kê bán ra thuế suất 10% và 8%",
             "33": "HTKK tự tính: [32] × 10% − thuế được giảm (phụ lục mục 2)", "30": "Bảng kê bán ra 5%", "31": "Bảng kê bán ra 5%",
             "29": "Bảng kê bán ra 0%", "26": "Bảng kê bán ra không chịu thuế"}
    hang = []
    for k in ["21", "22", "23", "24", "25", "26", "29", "30", "31", "32", "33", "27", "28", "34", "35", "36", "40a", "40", "41", "43"]:
        v = ct.get(k)
        if v in (0, 0.0, "", None):
            continue
        tu_tinh = k in ("27", "28", "34", "35", "36", "40a", "40", "41", "43")
        hang.append([f"[{k}]", TEN_CT[k], v if isinstance(v, str) else d(v), "HTKK tự tính – kiểm tra khớp" if tu_tinh else nguon.get(k, "")])
    bang(["Chỉ tiêu", "Nội dung", "Số điền", "Lấy từ đâu"], hang, [1.6, 7.2, 3.2, 5.4])

    if pl:
        doc.add_paragraph()
        dam("2. Phụ lục giảm thuế GTGT (Mẫu 01, Phụ lục III NĐ 174/2025) – khi tạo tờ khai chọn kèm phụ lục này")
        bang(["Hàng hóa, dịch vụ được giảm", "Giá trị chưa thuế", "Thuế suất theo quy định", "Thuế suất sau giảm", "Thuế được giảm"],
             [[k, d(v), "10%", "8%", d(g)] for k, v, g in pl["hang"]] +
             ([["Cộng", d(pl["gia_tri"]), "", "", d(pl["thue_duoc_giam"])]] if len(pl["hang"]) > 1 else []),
             [6.0, 3.0, 2.6, 2.4, 3.4])

    doc.add_paragraph()
    so_muc = 3 if pl else 2
    dam(f"{so_muc}. Hóa đơn mua vào cần lưu ý")
    if loai or cho_ck:
        bang(["Hóa đơn", "Người bán", "Thuế", "Cách khai", "Lý do / việc cần làm"],
             [[f"Số {r.get('so')} ngày {_ngay_vn(r.get('ngay'))}", r.get("ban_ten", ""), d(so(r["tien_thue"])), cach, ly]
              for r, cach, ly in loai] +
             [[f"Số {r.get('so')} ngày {_ngay_vn(r.get('ngay'))}", r.get("ban_ten", ""), d(so(r["tien_thue"])),
               "Vẫn khấu trừ (mua trả chậm)", "Khi trả phải chuyển khoản; trả tiền mặt thì khai giảm vào [37] kỳ đến hạn thanh toán"]
              for r in cho_ck], [3.0, 4.2, 2.0, 3.4, 4.8])
    else:
        doc.add_paragraph("Không có.")

    doc.add_paragraph()
    han = _lui_ngay_nghi(_han(ky))
    tien = ct.get("40") or 0
    gh = GIA_HAN_2026.get(ky.upper() if loai_ky == "quy" else f"{n:02d}/{y}")
    dam(f"{so_muc + 1}. Nộp tờ khai và tiền: hạn {han.strftime('%d/%m/%Y')}" + (f" – nộp {d(tien)} đồng." if tien else
                                                                              " – không phát sinh số phải nộp."))
    if gh:
        doc.add_paragraph(f"Nếu đơn vị được gia hạn theo NĐ 245/2026 (đã gửi đề nghị trước 02/11/2026): hạn nộp tiền {gh}; "
                          f"hạn nộp tờ khai không đổi.")
    if nhac:
        dam(f"{so_muc + 2}. Kỳ sau nhớ: " + " · ".join(nhac))
    an_toan.luu_docx(doc, ra)


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("file", nargs="?")
    ap.add_argument("--ky", help="10/2026 hoặc Q3/2026")
    ap.add_argument("--con-khau-tru-ky-truoc", type=so, default=0.0)
    ap.add_argument("--ten", default="")
    ap.add_argument("--mst", default="")
    ap.add_argument("--nhac", action="append", default=[], help="việc kỳ sau (lặp lại được)")
    ap.add_argument("--ra", default="huong-dan-to-khai-gtgt.docx")
    ap.add_argument("--self-test", action="store_true")
    a = ap.parse_args(argv)
    if a.self_test:
        return self_test()
    if not a.file or not a.ky:
        ap.error("cần file bảng kê và --ky")
    with open(a.file, encoding="utf-8-sig") as f:
        rows = list(csv.DictReader(f))
    ct, loai, cho_ck, pl = tinh_chi_tieu(rows, a.con_khau_tru_ky_truoc)
    lap_file(a.ra, ct, loai, cho_ck, pl, a.ky, a.ten, a.mst, a.nhac)
    for k in ["22", "23", "24", "25", "32", "33", "36", "40", "43"]:
        print(f"[{k}] {d(ct[k])}")
    print(f"Đã ghi {a.ra}. Đối chiếu trên HTKK/eTax trước khi nộp.")
    return 0


def self_test():
    import tempfile
    rows = [
        {"chieu": "mua-vao", "ngay": "2026-10-03", "ban_mst": "1", "ban_ten": "A", "so": "1", "tien_hang": "45000000", "tien_thue": "3600000", "thanh_toan": "CK"},
        {"chieu": "mua-vao", "ngay": "2026-10-06", "ban_mst": "2", "ban_ten": "B", "so": "2", "tien_hang": "12000000", "tien_thue": "960000", "thanh_toan": "TM"},
        {"chieu": "mua-vao", "ngay": "2026-10-14", "ban_mst": "3", "ban_ten": "C", "so": "3", "tien_hang": "9800000", "tien_thue": "784000", "thanh_toan": "CK", "loai_tru": "khong_hop_le", "ly_do": "Sai MST người mua"},
        {"chieu": "mua-vao", "ngay": "2026-10-28", "ban_mst": "4", "ban_ten": "D", "so": "4", "tien_hang": "18000000", "tien_thue": "1440000", "thanh_toan": ""},
        {"chieu": "ban-ra", "ngay": "2026-10-05", "so": "9", "tien_hang": "380000000", "tien_thue": "30400000", "tsuat": "8%", "ten_hang": "Giấy"},
        {"chieu": "ban-ra", "ngay": "2026-10-30", "so": "10", "tien_hang": "20000000", "tien_thue": "2000000", "tsuat": "10%"},
    ]
    ct, loai, cho, pl = tinh_chi_tieu(rows, 1850000)
    assert ct["23"] == 75_000_000 and ct["24"] == 6_000_000, ct
    assert ct["25"] == 5_040_000, ct
    assert ct["32"] == 400_000_000 and ct["33"] == 32_400_000 and pl["thue_duoc_giam"] == 7_600_000, (ct, pl)
    assert ct["40"] == 32_400_000 - 5_040_000 - 1_850_000, ct
    assert len(loai) == 2 and len(cho) == 1 and pl["hang"] == [("Giấy", 380_000_000, 7_600_000)]
    assert _han("10/2026") == dt.date(2026, 11, 20) and _han("Q3/2026") == dt.date(2026, 10, 31) and _han("Q4/2026") == dt.date(2027, 1, 31)
    with tempfile.TemporaryDirectory() as t:
        f = Path(t) / "a.docx"
        lap_file(str(f), ct, loai, cho, pl, "10/2026", "Cty", "0300000000", ["nhắc"])
        assert f.exists()
    print("self-test OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
