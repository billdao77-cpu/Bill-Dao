"""Công cụ kê khai BHXH, BHYT, BHTN: xác định tháng có phải đóng hay không, xuất danh sách đúng mẫu D02-LT.

Căn cứ:
- Mẫu D02-LT "Danh sách tham gia, điều chỉnh đóng BHXH, BHYT, BHTN" ban hành kèm Quyết định 366/QĐ-BHXH ngày 29/4/2026
  của BHXH Việt Nam (Quy trình thu, cấp sổ, thẻ – thay QĐ 595/QĐ-BHXH từ 01/5/2026): phần A thông tin đơn vị (12 mục),
  phần B danh sách gồm cột A, B và cột 1–19.
- Không làm việc và không hưởng lương từ 14 ngày làm việc trở lên trong tháng (tính từ mùng 1 đến cuối tháng) thì không đóng
  tháng đó; nghỉ ốm, thai sản từ 14 ngày làm việc trở lên cũng không đóng; riêng tháng đầu làm việc hoặc tháng đầu trở lại làm
  việc mà nghỉ ốm từ 14 ngày làm việc trở lên thì vẫn đóng (khoản 6 Điều 33 Luật BHXH 2024).
- Mã phương án (cột 18) theo cách ghi đang dùng trên phần mềm kê khai – danh mục có thể khác theo nhà cung cấp I-VAN [Cần kiểm tra].
Công cụ chỉ chuẩn bị số liệu; đơn vị tự kê khai, ký số và nộp.
"""
from datetime import date, timedelta

from . import tham_so
from .lich_vn import _ngay, la_ngay_lam_viec, tap_ngay_nghi

MA_PHUONG_AN = {
    "TM": ("tang", "Tăng mới (lần đầu tham gia tại đơn vị)"),
    "TC": ("tang", "Tăng do chuyển từ tỉnh khác đến"),
    "TD": ("tang", "Tăng do chuyển đơn vị (cùng tỉnh)"),
    "TL": ("tang", "Tăng chỉ tham gia BHTNLĐ-BNN (HĐLĐ thứ hai trở đi)"),
    "ON": ("tang", "Đi làm lại sau nghỉ thai sản (TS), ốm đau (OF), không lương (KL)"),
    "DC": ("dieu_chinh", "Điều chỉnh tiền lương, phụ cấp đóng BHXH, BHYT, BHTN"),
    "DL": ("dieu_chinh", "Điều chỉnh mức đóng chỉ BHTNLĐ-BNN"),
    "CD": ("dieu_chinh", "Điều chỉnh chức danh, nơi làm việc – không thay đổi tiền lương"),
    "GH": ("giam", "Giảm hẳn (nghỉ việc, chấm dứt HĐLĐ, nghỉ hưu...)"),
    "GD": ("giam", "Giảm do chuyển đơn vị (cùng tỉnh)"),
    "GC": ("giam", "Giảm do chuyển sang tỉnh khác"),
    "GN": ("giam", "Giảm tham gia BHTN"),
    "GL": ("giam", "Giảm chỉ tham gia BHTNLĐ-BNN"),
    "TS": ("giam", "Nghỉ thai sản từ 14 ngày làm việc trở lên trong tháng"),
    "OF": ("giam", "Nghỉ ốm đau từ 14 ngày làm việc trở lên trong tháng"),
    "KL": ("giam", "Nghỉ không lương từ 14 ngày làm việc trở lên trong tháng"),
    "TU": ("dieu_chinh", "Thoái thu (hoàn số đã đóng sai)"),
}
CHUC_DANH_CHUNG_CHUNG = {"nhân viên", "công nhân", "lái xe", "kỹ sư", "chuyên viên", "lao động"}


def _thang(s):
    """'11/2026' hoặc '2026-11' → (năm, tháng)."""
    s = str(s).strip()
    if "-" in s:
        y, m = s.split("-")[:2]
    else:
        m, y = s.split("/")[-2:]
    return int(y), int(m)


def _dmy(d):
    return d.strftime("%d/%m/%Y")


def xac_dinh_dong_thang(thang, khoang_nghi=(), ngay_bat_dau_lam=None, nghi_thu_bay=True, ngay_nghi_them=(),
                        thang_dau_tro_lai=False):
    """Đếm ngày làm việc không làm việc trong tháng (từ mùng 1) và kết luận có đóng BHXH tháng đó không.

    khoang_nghi: [{"tu_ngay", "den_ngay", "loai": nghi_viec|om_dau|thai_san|khong_luong|tam_hoan}]
    ngay_bat_dau_lam: người mới vào làm trong tháng (các ngày trước đó tính là không làm việc).
    """
    nam, th = _thang(thang)
    dau = date(nam, th, 1)
    cuoi = (date(nam + (th == 12), th % 12 + 1, 1) - timedelta(days=1))
    nghi_tuan = (5, 6) if nghi_thu_bay else (6,)
    nghi, lam_bu = tap_ngay_nghi(nam, nam, nghi_tuan=nghi_tuan, ngay_nghi_them=ngay_nghi_them)
    ngay_lv = [dau + timedelta(i) for i in range((cuoi - dau).days + 1)]
    ngay_lv = [d for d in ngay_lv if la_ngay_lam_viec(d, nghi, lam_bu, nghi_tuan)]
    theo_loai, khong_lam = {}, set()
    if ngay_bat_dau_lam:
        bd = _ngay(ngay_bat_dau_lam)
        s = {d for d in ngay_lv if d < bd}
        theo_loai["chua_vao_lam"] = len(s)
        khong_lam |= s
    for k in khoang_nghi or []:
        a, b = max(_ngay(k["tu_ngay"]), dau), min(_ngay(k["den_ngay"]) if k.get("den_ngay") else cuoi, cuoi)
        s = {d for d in ngay_lv if a <= d <= b} - khong_lam
        loai = k.get("loai", "khong_luong")
        theo_loai[loai] = theo_loai.get(loai, 0) + len(s)
        khong_lam |= s
    tong = len(khong_lam)
    dong = tong < 14
    ly_do = f"Không làm việc {tong}/{len(ngay_lv)} ngày làm việc trong tháng {th:02d}/{nam} (tính từ 01/{th:02d})"
    if not dong and thang_dau_tro_lai and set(theo_loai) <= {"om_dau", "chua_vao_lam"} and theo_loai.get("om_dau", 0) >= 14:
        dong = True
        ly_do += " – nhưng là tháng đầu làm việc/trở lại làm việc và nghỉ ốm: vẫn đóng (khoản 6 Điều 33 Luật BHXH 2024)"
    else:
        ly_do += " ≥ 14 → KHÔNG đóng tháng này" if not dong else " < 14 → VẪN ĐÓNG tháng này"
    goi_y = None
    if not dong:
        chinh = max((k for k in theo_loai if k != "chua_vao_lam"), key=lambda k: theo_loai[k], default="chua_vao_lam")
        goi_y = {"nghi_viec": f"GH từ {th:02d}/{nam}", "thai_san": f"TS từ {th:02d}/{nam}", "om_dau": f"OF từ {th:02d}/{nam}",
                 "khong_luong": f"KL từ {th:02d}/{nam}", "tam_hoan": f"KL (tạm hoãn HĐLĐ) từ {th:02d}/{nam}",
                 "chua_vao_lam": f"Chưa báo tăng tháng {th:02d}/{nam}; báo tăng từ tháng sau"}.get(chinh)
    elif "chua_vao_lam" in theo_loai:
        goi_y = f"Báo tăng (TM) từ {th:02d}/{nam}"
    elif "nghi_viec" in theo_loai:
        sau = date(nam + (th == 12), th % 12 + 1, 1)
        goi_y = f"Vẫn đóng {th:02d}/{nam}; báo GH từ {sau.month:02d}/{sau.year}"
    return {"thang": f"{th:02d}/{nam}", "so_ngay_lam_viec_trong_thang": len(ngay_lv), "so_ngay_khong_lam_viec": tong,
            "chi_tiet": theo_loai, "phai_dong": dong, "ket_luan": ly_do, "goi_y_phuong_an": goi_y,
            "can_cu": "Quy trình thu BHXH (QĐ 366/QĐ-BHXH); khoản 6 Điều 33 Luật BHXH 2024 – đối chiếu hướng dẫn của BHXH nơi đơn vị đăng ký"}


COT = ["STT", "Họ và tên", "Mã số BHXH", "Ngày/ tháng/ năm sinh", "Chức vụ, chức danh nghề, nghề nghiệp, nơi làm việc",
       "Hệ số lương/ Tiền lương", "Hệ số chênh lệch bảo lưu", "Chức vụ", "Thâm niên VK (%)", "Thâm niên nghề (%)",
       "Các khoản phụ cấp lương và thu nhập bổ sung", "Không xác định thời hạn", "Xác định thời hạn", "HĐ, thỏa thuận khác",
       "Ngày Quyết định, HĐLĐ, HĐLV có hiệu lực", "Từ tháng/ năm", "Đến tháng/ năm", "Nơi đăng ký KCB ban đầu",
       "Hình thức nhận kết quả", "Loại tăng, giảm, điều chỉnh", "Ghi chú"]
TRUONG = ["ho_ten", "ma_so_bhxh", "ngay_sinh", "chuc_danh_noi_lam_viec", "tien_luong", "he_so_chenh_lech_bao_luu",
          "pc_chuc_vu", "pc_tham_nien_vk", "pc_tham_nien_nghe", "phu_cap_bo_sung", "loai_hd", "ngay_hieu_luc",
          "tu_thang", "den_thang", "noi_kcb", "hinh_thuc_nhan_ket_qua", "phuong_an", "ghi_chu"]
DON_VI = [("ma_don_vi", "1. Mã đơn vị"), ("ten_don_vi", "2. Tên đơn vị"), ("dia_chi", "3. Địa chỉ liên hệ"),
          ("email", "4. Địa chỉ thư điện tử"), ("dien_thoai", "5. Số điện thoại liên hệ"), ("nguoi_dai_dien", "6. Người đại diện"),
          ("so_dinh_danh_nguoi_dai_dien", "7. Số định danh cá nhân"), ("loai_hinh", "8. Loại hình đơn vị"),
          ("nganh_nghe", "9. Ngành nghề sản xuất, kinh doanh chính"), ("phuong_thuc_dong", "10. Phương thức đóng"),
          ("doi_tuong", "11. Đối tượng tham gia"), ("co_quan_bhxh", "12. Đăng ký tham gia tại BHXH")]


def kiem_tra_dong_d02(r, vung=1, ngay=None):
    loi, cb = [], []
    pa = str(r.get("phuong_an", "")).split()[0].upper() if r.get("phuong_an") else ""
    ten = r.get("ho_ten", "?")
    if pa not in MA_PHUONG_AN:
        loi.append(f"{ten}: phương án '{r.get('phuong_an')}' không có trong danh mục ({', '.join(MA_PHUONG_AN)})")
        return pa, loi, cb
    nhom = MA_PHUONG_AN[pa][0]
    if not r.get("ngay_sinh"):
        loi.append(f"{ten}: thiếu ngày sinh (cột 2) – ghi như trên căn cước")
    if not r.get("tu_thang"):
        loi.append(f"{ten}: thiếu 'từ tháng/năm' (cột 14)")
    if not r.get("ma_so_bhxh"):
        if pa == "TM":
            cb.append(f"{ten}: chưa có mã số BHXH → lập kèm tờ khai TK1-TS, ghi số định danh cá nhân vào ghi chú")
        else:
            loi.append(f"{ten}: thiếu mã số BHXH (cột 1)")
    cd = str(r.get("chuc_danh_noi_lam_viec", "")).strip()
    if nhom in ("tang", "dieu_chinh"):
        if not cd:
            loi.append(f"{ten}: thiếu chức vụ, chức danh nghề, nơi làm việc (cột 3)")
        elif cd.split(" - ")[0].split(",")[0].strip().lower() in CHUC_DANH_CHUNG_CHUNG:
            cb.append(f"{ten}: chức danh '{cd}' chung chung – ghi cụ thể (vd: Nhân viên kinh doanh, Công nhân may)")
    if pa in ("TM", "TC", "TD", "TL"):
        if r.get("loai_hd") not in ("khong_xac_dinh", "xac_dinh", "khac"):
            loi.append(f"{ten}: chọn 1 loại HĐLĐ (cột 10–12): khong_xac_dinh | xac_dinh | khac")
        if not r.get("ngay_hieu_luc"):
            loi.append(f"{ten}: thiếu ngày HĐLĐ có hiệu lực (cột 13)")
        if not r.get("noi_kcb"):
            cb.append(f"{ten}: chưa ghi nơi đăng ký KCB ban đầu (cột 16)")
        if not r.get("ghi_chu"):
            cb.append(f"{ten}: nên ghi chú số HĐLĐ, ngày ký, thời hạn (cơ quan BHXH kiểm tra khi tăng mới)")
    if pa in ("DC", "DL") and not r.get("ghi_chu"):
        cb.append(f"{ten}: ghi chú căn cứ điều chỉnh (số, ngày quyết định, hiệu lực)")
    if pa in ("GH", "TS", "OF", "KL") and not r.get("ghi_chu"):
        loi.append(f"{ten}: phương án {pa} phải ghi chú (ngày chấm dứt HĐLĐ / thời gian nghỉ từ ngày... đến ngày...)")
    if pa == "GH" and not r.get("hinh_thuc_nhan_ket_qua"):
        cb.append(f"{ten}: giảm do nghỉ việc – ghi hình thức nhận kết quả (cột 17: bản điện tử/bản giấy)")
    luong = r.get("tien_luong")
    if isinstance(luong, (int, float)) and luong > 100 and nhom in ("tang", "dieu_chinh"):
        _, bang, _ = tham_so.theo_ngay(tham_so.LUONG_TOI_THIEU_VUNG, _ngay(ngay) if ngay else date.today())
        ltt = bang[vung][0]
        if ltt and luong < ltt:
            loi.append(f"{ten}: tiền lương {luong:,.0f} thấp hơn lương tối thiểu vùng {vung} ({ltt:,.0f})".replace(",", "."))
    return pa, loi, cb


def xuat_d02_lt(duong_dan_ra, danh_sach, don_vi=None, vung=1, ngay_lap=None, so_hieu=""):
    """Ghi file Excel theo bố cục mẫu D02-LT (QĐ 366/QĐ-BHXH) và kiểm tra từng dòng."""
    try:
        from openpyxl import Workbook
        from openpyxl.styles import Alignment, Border, Font, Side
    except ImportError:
        return {"loi": "Cần thư viện openpyxl: pip install openpyxl"}
    don_vi = don_vi or {}
    loi, canh_bao, tong_hop = [], [], {}
    for r in danh_sach:
        pa, l, c = kiem_tra_dong_d02(r, vung, ngay_lap)
        loi += l
        canh_bao += c
        tong_hop[pa] = tong_hop.get(pa, 0) + 1
    wb = Workbook()
    ws = wb.active
    ws.title = "D02-LT"
    dam, ngang = Font(name="Times New Roman", bold=True, size=11), Alignment(horizontal="center", vertical="center", wrap_text=True)
    thuong = Font(name="Times New Roman", size=11)
    vien = Border(*(Side(style="thin"),) * 4)
    ws["U1"] = "Mẫu D02-LT"
    ws["U1"].font = dam
    ws["Q2"] = "(Ban hành kèm theo QĐ 366/QĐ-BHXH ngày 29/4/2026 của BHXH Việt Nam)"
    ws["Q2"].font = Font(name="Times New Roman", italic=True, size=9)
    ws.merge_cells("A4:U4")
    ws["A4"] = "DANH SÁCH THAM GIA, ĐIỀU CHỈNH ĐÓNG BẢO HIỂM XÃ HỘI, BẢO HIỂM Y TẾ, BẢO HIỂM THẤT NGHIỆP"
    ws["A4"].font, ws["A4"].alignment = Font(name="Times New Roman", bold=True, size=13), ngang
    ws.merge_cells("A5:U5")
    nl = _ngay(ngay_lap) if ngay_lap else None
    ws["A5"] = f"Số: {so_hieu or '....../......'}; ngày {nl.day if nl else '...'} tháng {nl.month if nl else '...'} năm {nl.year if nl else '......'}"
    ws["A5"].alignment = ngang
    ws["A6"] = "A. Đơn vị/Tổ chức quản lý người tham gia"
    ws["A6"].font = dam
    dong = 7
    for i in range(0, len(DON_VI), 3):
        ws.merge_cells(start_row=dong, start_column=1, end_row=dong, end_column=21)
        ws.cell(dong, 1, "; ".join(f"{nhan}: {don_vi.get(k) or '…………'}" for k, nhan in DON_VI[i:i + 3])).font = thuong
        dong += 1
    ws.cell(dong, 1, "B. Danh sách người tham gia").font = dam
    h1, h2, h3, h4 = dong + 1, dong + 2, dong + 3, dong + 4
    for c, t in enumerate(COT, 1):
        ws.cell(h1, c, t)
    for c in [1, 2, 3, 4, 5, 15, 16, 17, 18, 19, 20, 21]:
        ws.merge_cells(start_row=h1, start_column=c, end_row=h3, end_column=c)
    ws.cell(h1, 6, "Tiền lương")
    ws.merge_cells(start_row=h1, start_column=6, end_row=h1, end_column=11)
    ws.cell(h1, 12, "Loại HĐLĐ")
    ws.merge_cells(start_row=h1, start_column=12, end_row=h1, end_column=14)
    for c, t in [(6, COT[5]), (7, COT[6]), (8, "Phụ cấp"), (11, COT[10]), (12, COT[11]), (13, COT[12]), (14, COT[13])]:
        ws.cell(h2, c, t)
    ws.merge_cells(start_row=h2, start_column=8, end_row=h2, end_column=10)
    for c in [6, 7, 11, 12, 13, 14]:
        ws.merge_cells(start_row=h2, start_column=c, end_row=h3, end_column=c)
    for c, t in [(8, COT[7]), (9, COT[8]), (10, COT[9])]:
        ws.cell(h3, c, t)
    for c, t in enumerate(["A", "B"] + [str(i) for i in range(1, 20)], 1):
        ws.cell(h4, c, t)
    for rr in range(h1, h4 + 1):
        for c in range(1, 22):
            x = ws.cell(rr, c)
            x.font, x.alignment, x.border = dam, ngang, vien
    rr = h4
    for i, r in enumerate(danh_sach, 1):
        rr += 1
        pa = str(r.get("phuong_an", "")).split()[0].upper()
        gt = [i, r.get("ho_ten"), r.get("ma_so_bhxh") or "", r.get("ngay_sinh"), r.get("chuc_danh_noi_lam_viec"),
              r.get("tien_luong"), r.get("he_so_chenh_lech_bao_luu"), r.get("pc_chuc_vu"), r.get("pc_tham_nien_vk"),
              r.get("pc_tham_nien_nghe"), r.get("phu_cap_bo_sung"),
              "x" if r.get("loai_hd") == "khong_xac_dinh" else "", "x" if r.get("loai_hd") == "xac_dinh" else "",
              "x" if r.get("loai_hd") == "khac" else "", r.get("ngay_hieu_luc"), r.get("tu_thang"), r.get("den_thang"),
              r.get("noi_kcb"), r.get("hinh_thuc_nhan_ket_qua"),
              f"{pa} - {MA_PHUONG_AN[pa][1]}" if pa in MA_PHUONG_AN else r.get("phuong_an"), r.get("ghi_chu")]
        for c, v in enumerate(gt, 1):
            x = ws.cell(rr, c, v)
            x.font, x.border = thuong, vien
            x.alignment = Alignment(vertical="top", wrap_text=True, horizontal="center" if c in (1, 12, 13, 14) else None)
            if c in (6, 11) and isinstance(v, (int, float)):
                x.number_format = "#,##0"
    rr += 2
    ws.cell(rr, 17, "ĐƠN VỊ LẬP DANH SÁCH").font = dam
    ws.cell(rr + 1, 17, "(Ký, ghi rõ họ tên, đóng dấu)").font = Font(name="Times New Roman", italic=True, size=10)
    for c, w in enumerate([5, 20, 13, 12, 32, 13, 9, 8, 8, 8, 14, 8, 8, 8, 12, 9, 9, 18, 12, 26, 48], 1):
        ws.column_dimensions[ws.cell(1, c).column_letter].width = w
    ws.freeze_panes = ws.cell(h4 + 1, 3)
    kt = wb.create_sheet("Kiem tra")
    kt.append(["Mức", "Nội dung"])
    for x in loi:
        kt.append(["LỖI – phải sửa trước khi nộp", x])
    for x in canh_bao:
        kt.append(["Lưu ý", x])
    if not loi and not canh_bao:
        kt.append(["OK", "Không phát hiện lỗi"])
    kt.column_dimensions["A"].width, kt.column_dimensions["B"].width = 28, 110
    wb.save(duong_dan_ra)
    return {"duong_dan": duong_dan_ra, "so_nguoi": len(danh_sach), "theo_phuong_an": tong_hop, "loi": loi, "luu_y": canh_bao,
            "ghi_chu": "File theo bố cục mẫu D02-LT (QĐ 366/QĐ-BHXH). Phần mềm I-VAN thường có mẫu Excel nhập dữ liệu riêng: "
                       "tải mẫu của phần mềm và chép dữ liệu theo đúng cột, hoặc nhập tay từng dòng. Kiểm tra lại danh mục mã "
                       "phương án trên phần mềm trước khi nộp."}


TOOLS = [
    {"name": "xac_dinh_dong_bhxh_thang", "fn": xac_dinh_dong_thang,
     "description": "Xác định người lao động có phải đóng BHXH, BHYT, BHTN trong một tháng hay không: đếm số ngày làm việc không làm "
                    "việc từ mùng 1 (nghỉ việc, ốm đau, thai sản, không lương, chưa vào làm) so với mốc 14 ngày; áp dụng khoản 6 Điều "
                    "33 Luật BHXH 2024; gợi ý phương án (GH/TS/OF/KL, báo giảm từ tháng sau...).",
     "schema": {"type": "object", "required": ["thang"], "properties": {
         "thang": {"type": "string", "description": "mm/yyyy"},
         "khoang_nghi": {"type": "array", "items": {"type": "object", "properties": {
             "tu_ngay": {"type": "string"}, "den_ngay": {"type": "string"},
             "loai": {"type": "string", "enum": ["nghi_viec", "om_dau", "thai_san", "khong_luong", "tam_hoan"]}}}},
         "ngay_bat_dau_lam": {"type": "string"}, "nghi_thu_bay": {"type": "boolean"},
         "ngay_nghi_them": {"type": "array", "items": {"type": "string"}}, "thang_dau_tro_lai": {"type": "boolean"}}}},
    {"name": "xuat_d02_lt", "fn": xuat_d02_lt,
     "description": "Xuất danh sách tham gia, điều chỉnh đóng BHXH, BHYT, BHTN ra Excel theo bố cục mẫu D02-LT (QĐ 366/QĐ-BHXH: phần A "
                    "thông tin đơn vị, phần B cột A, B, 1–19) kèm sheet kiểm tra lỗi: mã phương án, ngày sinh, mã số BHXH/TK1-TS, "
                    "loại HĐLĐ, ngày hiệu lực, ghi chú bắt buộc khi giảm, chức danh chung chung, lương dưới tối thiểu vùng.",
     "schema": {"type": "object", "required": ["duong_dan_ra", "danh_sach"], "properties": {
         "duong_dan_ra": {"type": "string"},
         "danh_sach": {"type": "array", "items": {"type": "object", "properties": {t: {} for t in TRUONG}},
                       "description": "Mỗi người: " + ", ".join(TRUONG) + ". loai_hd: khong_xac_dinh|xac_dinh|khac; phuong_an: "
                                      + ", ".join(MA_PHUONG_AN)},
         "don_vi": {"type": "object", "description": "Thông tin phần A: " + ", ".join(k for k, _ in DON_VI)},
         "vung": {"type": "integer", "enum": [1, 2, 3, 4]}, "ngay_lap": {"type": "string"}, "so_hieu": {"type": "string"}}}},
]
