#!/usr/bin/env python3
"""Lập file Word "Bảng cài chương trình khuyến mại" – mở ra là cài được trên kênh bán (sàn, website, cửa hàng), không gắn sàn nào.

Đầu vào: file JSON
{
  "ten_chuong_trinh": "Sale 11.11", "kenh": "Shopee", "tu_ngay": "10/11/2026", "den_ngay": "12/11/2026",
  "loi_nhuan_muc_tieu": "10%",            # lãi tối thiểu sau quảng cáo để chạy (mặc định 0 = hòa vốn)
  "san_pham": [ {"sku": "LG30", "ten": "Serum ...", "gia_ban": 450000, "gia_von": 135000,
                 "phi": ["phí cố định=10%", "thanh toán=5%", "hạ tầng=3000"], "ty_le_hoan": "8%",
                 "chi_phi_moi_don_hoan": 45000, "ads_moi_don": 70000, "giam": "40%", "gioi_han_mua": 2} ],
  "noi_dung": [ {"cho": "Tiêu đề", "cu": "...", "moi": "...", "ly_do": "..."} ],
  "phap_ly": ["Giảm ≤ 50%: hợp lệ, không phải thông báo Sở Công Thương", ...],
  "ngay_kiem_phi": "02/11/2026"
}
Ô chưa có số (giá vốn, phí, tỷ lệ hoàn, quảng cáo) → để trống: file ghi THIẾU, không giả định.
Mỗi SKU 1 dòng: hành động CHẠY / SỬA MỨC GIẢM (mức đề xuất còn đạt lãi mục tiêu) / KHÔNG CHẠY.

  python3 bang_cai_khuyen_mai.py chuong_trinh.json --ra bang-cai-khuyen-mai.docx
"""
from __future__ import annotations

import argparse
import json
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from tinh_gia import TRAN_GIAM_GIA, doc_phi, gia_cho_bien, tinh  # noqa: E402
from vn_money import doc_phan_tram, doc_tien, in_pt, in_tien  # noqa: E402

CAN = ["gia_ban", "gia_von", "phi", "ty_le_hoan", "ads_moi_don"]
TEN_TRUONG = {"gia_ban": "giá đang bán", "gia_von": "giá vốn", "phi": "phí kênh bán", "ty_le_hoan": "tỷ lệ hoàn đơn",
              "ads_moi_don": "chi phí quảng cáo mỗi đơn", "giam": "mức giảm muốn chạy"}


def _pt_gon(x):
    return (f"{x * 100:.1f}".rstrip("0").rstrip(".").replace(".", ",") + "%") if x is not None else ""


def _so(x):
    return doc_tien(str(x)) if x not in (None, "") else None


def _pt(x):
    return doc_phan_tram(str(x)) if x not in (None, "") else None


def tinh_sku(sp, muc_tieu=0.0):
    thieu = [k for k in CAN if sp.get(k) in (None, "", [])]
    if "gia_ban" in thieu or "giam" not in sp:
        return {"thieu": thieu + ([] if "giam" in sp else ["giam"]), "hanh_dong": "THIẾU SỐ LIỆU"}
    gia_ban, giam = _so(sp["gia_ban"]), _pt(sp["giam"])
    gia_km = round(gia_ban * (1 - giam))
    kq = {"gia_ban": gia_ban, "giam": giam, "gia_km": gia_km, "thieu": thieu}
    if thieu:
        kq["hanh_dong"] = "THIẾU SỐ LIỆU"
        return kq
    pt, cd = doc_phi(sp["phi"] if isinstance(sp["phi"], list) else [sp["phi"]])
    hoan, cp_hoan, ads, von = _pt(sp["ty_le_hoan"]), _so(sp.get("chi_phi_moi_don_hoan") or 0), _so(sp["ads_moi_don"]), _so(sp["gia_von"])
    r = tinh(gia_km, von, pt, cd, hoan, cp_hoan, ads)
    kq.update(lai=r["loi_nhuan_sau_ads"], lai_pt=r["loi_nhuan_sau_ads_pt"], roas=r["roas_hoa_von"])
    g_muc_tieu = gia_cho_bien(von, pt, cd, hoan * cp_hoan, ads, muc_tieu)
    if giam > TRAN_GIAM_GIA:
        kq["hanh_dong"] = "SỬA MỨC GIẢM"
        kq["ly_do"] = f"Giảm {_pt_gon(giam)} vượt trần 50% (khoản 1 Điều 4 TT 39/2025/TT-BCT)"
    elif r["loi_nhuan_sau_ads_pt"] >= muc_tieu - 1e-9:
        kq["hanh_dong"] = "CHẠY"
    else:
        kq["hanh_dong"] = "SỬA MỨC GIẢM"
        kq["ly_do"] = f"Giảm {_pt_gon(giam)}: {'lỗ' if r['loi_nhuan_sau_ads'] < 0 else 'lãi'} {in_tien(r['loi_nhuan_sau_ads'])}/đơn"
    if kq["hanh_dong"] == "SỬA MỨC GIẢM":
        if g_muc_tieu and g_muc_tieu < gia_ban:
            giam_dx = min(math.floor((1 - g_muc_tieu / gia_ban) * 100) / 100, TRAN_GIAM_GIA)
            gia_dx = round(gia_ban * (1 - giam_dx))
            r2 = tinh(gia_dx, von, pt, cd, hoan, cp_hoan, ads)
            kq.update(giam_dx=giam_dx, gia_dx=gia_dx, lai_dx=r2["loi_nhuan_sau_ads"], roas_dx=r2["roas_hoa_von"])
        else:
            kq["hanh_dong"] = "KHÔNG CHẠY"
            kq["ly_do"] = (kq.get("ly_do", "") + "; giá bán hiện tại chưa đạt lãi mục tiêu – không nên giảm").strip("; ")
    return kq


def lap_file(ra, ct):
    from docx import Document
    from docx.enum.section import WD_ORIENT
    from docx.shared import Cm, Pt

    doc = Document()
    sec = doc.sections[0]
    sec.orientation = WD_ORIENT.LANDSCAPE
    sec.page_width, sec.page_height = sec.page_height, sec.page_width
    for c in ("left_margin", "right_margin", "top_margin", "bottom_margin"):
        setattr(sec, c, Cm(1.5))
    doc.styles["Normal"].font.name, doc.styles["Normal"].font.size = "Times New Roman", Pt(10.5)

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
                c.text = str(v if v not in (None, "") else "–")
        for col, w in zip(t.columns, rong):
            col.width = Cm(w)
        for row in t.rows:
            for c, w in zip(row.cells, rong):
                c.width = Cm(w)

    muc_tieu = _pt(ct.get("loi_nhuan_muc_tieu")) or 0.0
    thoi_gian = f"{ct.get('tu_ngay', '')} – {ct.get('den_ngay', '')}".strip(" –")
    dam(f"BẢNG CÀI CHƯƠNG TRÌNH KHUYẾN MẠI: {ct.get('ten_chuong_trinh', '').upper()}", 14)
    doc.add_paragraph(" · ".join(x for x in [f"Kênh: {ct['kenh']}" if ct.get("kenh") else "", f"Thời gian: {thoi_gian}" if thoi_gian else "",
                                             f"Chỉ chạy SKU lãi từ {in_pt(muc_tieu)} sau quảng cáo" if muc_tieu else "Chỉ chạy SKU không lỗ",
                                             f"Phí kênh kiểm ngày {ct['ngay_kiem_phi']}" if ct.get("ngay_kiem_phi") else ""] if x))

    dam("1. Cài giá khuyến mại (mỗi dòng 1 SKU)")
    hang, thieu_all, kq_all = [], [], []
    for sp in ct.get("san_pham", []):
        k = tinh_sku(sp, muc_tieu)
        kq_all.append((sp, k))
        if k["thieu"]:
            thieu_all.append(f"{sp.get('sku')} {sp.get('ten', '')}: thiếu " + ", ".join(TEN_TRUONG.get(x, x) for x in k["thieu"]))
        hd = k["hanh_dong"]
        if hd == "SỬA MỨC GIẢM" and "giam_dx" in k:
            cai_giam, cai_gia = _pt_gon(k["giam_dx"]), in_tien(k["gia_dx"])
            lai, roas = in_tien(k["lai_dx"]), (f"{k['roas_dx']:.2f}".replace(".", ",") if k.get("roas_dx") else "")
            ghi = f"{k.get('ly_do')} → cài giảm {cai_giam}"
        elif hd == "CHẠY":
            cai_giam, cai_gia, lai = _pt_gon(k["giam"]), in_tien(k["gia_km"]), in_tien(k["lai"])
            roas, ghi = (f"{k['roas']:.2f}".replace(".", ",") if k.get("roas") else ""), ""
        else:
            cai_giam = cai_gia = lai = roas = ""
            ghi = k.get("ly_do") or ("THIẾU: " + ", ".join(TEN_TRUONG.get(x, x) for x in k["thieu"]) + " – chưa cài")
        hang.append([sp.get("sku"), sp.get("ten"), in_tien(k["gia_ban"]) if k.get("gia_ban") else "THIẾU", hd, cai_giam, cai_gia,
                     lai, roas, sp.get("gioi_han_mua") or "", ghi])
    bang(["SKU", "Sản phẩm", "Giá đang bán", "Hành động", "% giảm cài", "Giá khuyến mại cài", "Lãi/đơn sau QC",
          "ROAS tối thiểu", "Giới hạn mua/khách", "Ghi chú"], hang, [1.6, 4.0, 2.0, 2.3, 1.7, 2.2, 2.0, 1.8, 1.8, 6.4])
    doc.add_paragraph("ROAS tối thiểu = doanh thu quảng cáo / chi phí quảng cáo để không lỗ ở giá khuyến mại – đặt làm ROAS mục tiêu "
                      "hoặc tắt quảng cáo khi thấp hơn. Giá đang bán phải là giá thật đã bán ngay trước khuyến mại.")

    if thieu_all:
        dam("Còn thiếu số liệu – xin trước khi cài (không giả định):")
        for x in thieu_all:
            doc.add_paragraph(x, style="List Bullet")
    if ct.get("noi_dung"):
        dam("2. Sửa nội dung sản phẩm, banner")
        bang(["Chỗ", "Chữ cũ", "Chữ mới", "Lý do"], [[x.get("cho"), x.get("cu"), x.get("moi"), x.get("ly_do")] for x in ct["noi_dung"]],
             [2.4, 7.4, 8.6, 7.4])
    so = 3 if ct.get("noi_dung") else 2
    if ct.get("phap_ly"):
        dam(f"{so}. Pháp lý")
        for x in ct["phap_ly"]:
            doc.add_paragraph(x, style="List Bullet")
        so += 1
    doc.save(ra)
    return kq_all


def _khong_ghi_de(duong_dan, ghi_de=False):
    """vn-custom: không ghi đè file đã có (trừ khi người dùng đồng ý rõ và truyền --ghi-de)."""
    import os
    if os.path.exists(duong_dan) and not ghi_de:
        print(f"LỖI: {duong_dan} đã tồn tại – không ghi đè để tránh mất dữ liệu. Đặt tên file mới, "
              "hoặc thêm --ghi-de khi người dùng đồng ý rõ.", file=sys.stderr)
        return False
    return True


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("file", nargs="?")
    ap.add_argument("--ra", default="bang-cai-khuyen-mai.docx")
    ap.add_argument("--self-test", action="store_true")
    ap.add_argument("--ghi-de", action="store_true", help="cho phép ghi đè file đã có (chỉ khi người dùng đồng ý)")
    a = ap.parse_args(argv)
    if a.self_test:
        return self_test()
    if not a.file:
        ap.error("cần file JSON chương trình")
    if not a.ra.lower().endswith(".docx"):
        ap.error("--ra phải là file .docx")
    if not _khong_ghi_de(a.ra, a.ghi_de):
        return 2
    ct = json.loads(Path(a.file).read_text(encoding="utf-8"))
    for sp, k in lap_file(a.ra, ct):
        print(f"{sp.get('sku')}: {k['hanh_dong']}" + (f" – cài giảm {_pt_gon(k['giam_dx'])}" if "giam_dx" in k else ""))
    print(f"Đã ghi {a.ra}. Tự cài trên kênh bán; đối chiếu biểu phí hiện hành.")
    return 0


def self_test():
    import tempfile
    sp = {"sku": "A", "ten": "Serum", "gia_ban": 450000, "gia_von": 135000,
          "phi": ["phí cố định=10%", "thanh toán=5%", "Freeship=6%", "Voucher=3%", "hạ tầng=3000", "đóng gói=8000"],
          "ty_le_hoan": "8%", "chi_phi_moi_don_hoan": 45000, "ads_moi_don": 70000, "giam": "40%"}
    k = tinh_sku(sp, 0.10)
    assert k["hanh_dong"] == "SỬA MỨC GIẢM" and round(k["lai"]) == -14400, k
    assert k["giam_dx"] == 0.26 and k["lai_dx"] / k["gia_dx"] >= 0.10, k
    assert tinh_sku(dict(sp, giam="10%"), 0.10)["hanh_dong"] == "CHẠY"
    assert tinh_sku(dict(sp, giam="60%"), 0.0)["hanh_dong"] == "SỬA MỨC GIẢM"
    assert tinh_sku(dict(sp, gia_von=None), 0.1)["thieu"] == ["gia_von"]
    with tempfile.TemporaryDirectory() as t:
        f = Path(t) / "a.docx"
        lap_file(str(f), {"ten_chuong_trinh": "T", "san_pham": [sp, dict(sp, sku="B", gia_von=None)], "loi_nhuan_muc_tieu": "10%"})
        assert f.exists()
    print("self-test OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
