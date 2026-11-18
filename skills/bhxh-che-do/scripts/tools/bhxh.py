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



# ---------------------------------------------------------------- File hướng dẫn kê khai cho người mới
LOAI_HD = {"khong_xac_dinh": "Không xác định thời hạn", "xac_dinh": "Xác định thời hạn", "khac": "HĐ, thỏa thuận khác"}
GIAY_TO_MAC_DINH = {
    "TM": ["HĐLĐ (bản scan)", "Tờ khai TK1-TS có chữ ký người lao động (nếu chưa có mã số BHXH)"],
    "TC": ["HĐLĐ (bản scan)"], "TD": ["HĐLĐ (bản scan)"], "TL": ["HĐLĐ (bản scan)"],
    "ON": ["Xác nhận ngày đi làm lại (bảng chấm công)"],
    "DC": ["Quyết định điều chỉnh lương / phụ lục HĐLĐ (bản scan)"], "DL": ["Quyết định điều chỉnh (bản scan)"],
    "CD": ["Quyết định / phụ lục HĐLĐ thay đổi chức danh, nơi làm việc"],
    "GH": ["Quyết định chấm dứt HĐLĐ hoặc thỏa thuận chấm dứt (bản scan)"],
    "TS": ["Đơn xin nghỉ thai sản (bản scan); giấy chứng sinh / giấy khai sinh khi có"],
    "OF": ["Giấy ra viện / giấy chứng nhận nghỉ việc hưởng BHXH"], "KL": ["Đơn xin nghỉ không lương đã được duyệt (bản scan)"],
}
TK1_TRUONG = [("ho_ten", "[01] Họ và tên"), ("gioi_tinh", "[02] Giới tính"), ("ngay_sinh", "[03] Ngày, tháng, năm sinh"),
              ("so_dinh_danh", "[04] Số CCCD/định danh cá nhân/hộ chiếu"), ("dan_toc", "[05] Dân tộc"), ("quoc_tich", "[06] Quốc tịch"),
              ("dien_thoai", "[07] Số điện thoại di động"), ("email", "[08] Email nhận sổ, thẻ điện tử"),
              ("noi_kcb", "[09] Nơi đăng ký KCB ban đầu"), ("hinh_thuc_nhan_ket_qua", "[10] Nhận kết quả (điện tử/giấy)"),
              ("ngay_cap", "Ngày cấp căn cước (phần mềm hỏi)"), ("noi_khai_sinh", "Nơi đăng ký giấy khai sinh (phần mềm hỏi)"),
              ("dia_chi", "Địa chỉ nhận hồ sơ / nơi sinh sống (phần mềm hỏi)")]
TK1_BAT_BUOC = {"ho_ten", "gioi_tinh", "ngay_sinh", "so_dinh_danh", "dan_toc", "quoc_tich", "dien_thoai", "noi_kcb",
                "ngay_cap", "noi_khai_sinh", "dia_chi"}
NHAN_IBH = {"TM": "Tăng mới chưa có sổ",
            "TC": "Tăng chuyển đã có sổ, di chuyển từ tỉnh khác đến", "TD": "Tăng đến đã có sổ, di chuyển trong địa bàn tỉnh",
            "ON": "Nghỉ không lương / Nghỉ ốm / Nghỉ thai sản đi làm lại (chọn đúng trường hợp)"}
THAO_TAC = {
    "ibh": ("Phần mềm iBH (ivan.vn)", [
        "Người MỚI (chưa có trong phần mềm): menu \"Doanh nghiệp\" → \"Người lao động\" → \"Tạo mới\", khai tab Thông tin chung và "
        "Thông tin tham gia BHXH, BHYT theo khối thông tin của từng người ở mục IV (TĂNG) (ô có dấu * đỏ là bắt buộc).",
        "Nghiệp vụ \"Thu\" → chọn hồ sơ 600 → \"Tạo mới\"; chọn kỳ kê khai.",
        "Tab D02 → nút \"Thêm\" → chọn tab TĂNG LAO ĐỘNG / GIẢM LAO ĐỘNG / TĂNG TIỀN LƯƠNG... → tích người cần kê khai → \"Thêm\".",
        "Bấm nút sửa ở cuối dòng từng người, gõ đúng các ô trong khối của người đó (mục IV, V, VI).",
        "Tab TK1-TS: kiểm tra thông tin người tăng mới; tab \"Tệp đính kèm\": tải giấy tờ ở mục VII.",
        "\"Lưu\" → ký số → nộp. Theo dõi trạng thái hồ sơ trên phần mềm."]),
    "cong_bhxh": ("Cổng giao dịch điện tử BHXH Việt Nam", [
        "Đăng nhập mục \"Tổ chức\" bằng mã số thuế đơn vị; cắm chữ ký số, dùng Chrome và đã cài phần mềm hỗ trợ ký số của BHXH.",
        "\"Kê khai hồ sơ\" → \"Quản lý lao động\": bấm \"Nạp vào từ BHXH\" để lấy người đang đóng; thêm người MỚI theo khối thông tin ở mục IV (TĂNG).",
        "\"Danh sách thủ tục\" → thủ tục 600 → chọn kỳ kê khai.",
        "Tích chọn từng người, chọn phân loại (tăng lao động, giảm lao động, tăng/giảm tiền lương, khác) → \"Áp dụng\".",
        "Gõ các ô của từng người theo mục IV, V, VI; đính kèm giấy tờ ở mục VII.",
        "Ký số → gửi hồ sơ. Theo dõi kết quả trên cổng."]),
    "chung": ("Phần mềm kê khai BHXH (I-VAN) hoặc cổng BHXH", [
        "Người MỚI: thêm vào danh sách lao động của phần mềm theo khối thông tin ở mục IV (TĂNG).",
        "Chọn thủ tục báo tăng, giảm, điều chỉnh (thường mã 600), chọn kỳ kê khai.",
        "Thêm từng người vào danh sách D02-LT, chọn đúng phương án, gõ các ô theo mục IV, V, VI.",
        "Khai TK1-TS cho người chưa có mã số BHXH; đính kèm giấy tờ ở mục VII.",
        "Kiểm tra lỗi phần mềm báo → ký số → nộp. Theo dõi kết quả."]),
}


def _thang_sau(thang):
    y, m = _thang(thang)
    return f"{m % 12 + 1:02d}/{y + (m == 12)}"


def _cuoi_thang_sau(thang):
    y, m = _thang(thang)
    y2, m2 = y + (m == 12), m % 12 + 1
    d = date(y2 + (m2 == 12), m2 % 12 + 1, 1) - timedelta(days=1)
    return _dmy(d)


def _tien(x):
    return f"{x:,.0f}".replace(",", ".") if isinstance(x, (int, float)) else (x or "")


def huong_dan_ke_khai(duong_dan_ra, thang, danh_sach, don_vi=None, khong_ke_khai=(), tien_dong=None, viec_thang_sau=(),
                      phan_mem="chung", vung=1, ngay_lap=None):
    """Ghi file Word "Hướng dẫn kê khai BHXH tháng ..." cho người mới: nộp gì, gõ gì cho từng người, còn thiếu gì, sau khi nộp."""
    try:
        from docx import Document
        from docx.enum.text import WD_ALIGN_PARAGRAPH
        from docx.shared import Pt, RGBColor
    except ImportError:
        return {"loi": "Cần thư viện python-docx: pip install python-docx"}
    don_vi = don_vi or {}
    nhom = {"tang": [], "giam": [], "dieu_chinh": []}
    loi_dl, thieu = [], []
    for r in danh_sach:
        pa, l, _ = kiem_tra_dong_d02(r, vung, ngay_lap)
        loi_dl += l
        if pa in MA_PHUONG_AN:
            nhom[MA_PHUONG_AN[pa][0]].append((pa, r))
        if pa == "TM" and not r.get("ma_so_bhxh"):
            con = [nhan for k, nhan in TK1_TRUONG if k in TK1_BAT_BUOC and not r.get(k)]
            if con:
                thieu.append((r.get("ho_ten", "?"), con))
    can_tk1 = [r.get("ho_ten") for pa, r in nhom["tang"] if pa == "TM" and not r.get("ma_so_bhxh")]

    doc = Document()
    st = doc.styles["Normal"]
    st.font.name, st.font.size = "Times New Roman", Pt(12)
    do = RGBColor(0xB4, 0x23, 0x18)

    def h(text, lv=1):
        doc.add_heading(text, level=lv)

    def p(text, dam=False, mau=None):
        para = doc.add_paragraph()
        run = para.add_run(text)
        run.bold = dam
        if mau:
            run.font.color.rgb = mau
        return para

    def bang(hang, rong=None, tieu_de=None):
        t = doc.add_table(rows=0, cols=len(hang[0]) if hang else 2)
        t.style = "Table Grid"
        for i, row in enumerate(([tieu_de] if tieu_de else []) + hang):
            cells = t.add_row().cells
            for c, v in zip(cells, row):
                c.text = str(v if v is not None else "")
                if tieu_de and i == 0:
                    for run in c.paragraphs[0].runs:
                        run.bold = True
        doc.add_paragraph()
        return t

    tieu = doc.add_heading(f"HƯỚNG DẪN KÊ KHAI BHXH THÁNG {_thang(thang)[1]:02d}/{_thang(thang)[0]}", 0)
    tieu.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p(f"Đơn vị: {don_vi.get('ten_don_vi', '…')} – Mã đơn vị BHXH: {don_vi.get('ma_don_vi', '…')}"
      + (f" – Lập ngày {ngay_lap}" if ngay_lap else ""))
    p("Đọc từ trên xuống, làm lần lượt. Mỗi người có một khối \"gõ vào phần mềm\": chép đúng từng ô. "
      "Ai không có trong file này thì giữ nguyên như tháng trước, không kê khai.")

    h("I. Tóm tắt tháng này")
    tong = tien_dong or {}
    bang([["Tăng", f"{len(nhom['tang'])} người: " + ", ".join(f"{r.get('ho_ten')} ({pa})" for pa, r in nhom["tang"])],
          ["Giảm", f"{len(nhom['giam'])} người: " + ", ".join(f"{r.get('ho_ten')} ({pa})" for pa, r in nhom["giam"])],
          ["Điều chỉnh", f"{len(nhom['dieu_chinh'])} người: " + ", ".join(f"{r.get('ho_ten')} ({pa})" for pa, r in nhom["dieu_chinh"])],
          ["Không kê khai", f"{len(khong_ke_khai)} người: " + ", ".join(x.get("ho_ten", "") for x in khong_ke_khai)],
          ["Tổng tiền phải nộp tháng này", f"{_tien(tong.get('tong'))} đồng (người lao động {_tien(tong.get('nld'))}; công ty "
                                           f"{_tien(tong.get('dn'))})" + (f" – tháng trước {_tien(tong.get('tong_thang_truoc'))}"
                                                                          if tong.get("tong_thang_truoc") else "") if tong else "—"],
          ["Hạn đóng tiền", f"Chậm nhất {_cuoi_thang_sau(thang)} (ngày cuối cùng của tháng tiếp theo – Luật BHXH 2024)"]],
         tieu_de=["Nội dung", "Chi tiết"])
    if loi_dl or thieu:
        p("CHÚ Ý: còn thiếu thông tin – làm mục II trước khi kê khai.", dam=True, mau=do)

    h("II. Việc làm TRƯỚC: thông tin còn thiếu")
    if not thieu and not loi_dl:
        p("Đủ thông tin – làm tiếp mục III.")
    for ten, con in thieu:
        p(f"{ten}: thiếu " + ", ".join(con), dam=True)
        p(f"Tin nhắn gửi {ten}: \"Chào anh/chị, phòng nhân sự cần thông tin để báo tăng BHXH, BHYT tháng {thang}: "
          + "; ".join(x.split('] ')[-1].replace(" (phần mềm hỏi)", "").lower() for x in con) + ". Anh/chị gửi giúp em trong hôm nay, kèm ảnh 2 mặt căn cước. Cảm ơn anh/chị.\"")
    for x in loi_dl:
        doc.add_paragraph(x, style="List Bullet")

    h("III. Hồ sơ tháng này nộp gì")
    hs = [["1", f"1 hồ sơ thủ tục 600 (báo tăng, giảm, điều chỉnh) kỳ {thang}: tăng, giảm, điều chỉnh NỘP CHUNG trong hồ sơ này"],
          ["2", f"Danh sách D02-LT gồm {sum(len(v) for v in nhom.values())} dòng – phần mềm tự tạo khi bạn gõ từng người ở mục IV, V, VI"]]
    if can_tk1:
        hs.append(["3", "Tờ khai TK1-TS cho người chưa có mã số BHXH: " + ", ".join(can_tk1)])
    hs.append([str(len(hs) + 1), "Giấy tờ đính kèm theo mục VII"])
    bang(hs, tieu_de=["#", "Thành phần"])
    rieng = []
    if any(pa == "TS" for pa, _ in nhom["giam"]):
        rieng.append("Chế độ thai sản: hồ sơ hưởng chế độ nộp riêng (ngoài thủ tục 600) khi có giấy chứng sinh/giấy khai sinh.")
    if any(pa == "GH" for pa, _ in nhom["giam"]):
        rieng.append("Trợ cấp thất nghiệp: người lao động tự nộp tại trung tâm dịch vụ việc làm trong 3 tháng kể từ ngày nghỉ việc.")
    if rieng:
        p("Không nằm trong hồ sơ 600 (làm riêng):", dam=True)
        for x in rieng:
            doc.add_paragraph(x, style="List Bullet")

    def khoi(i, pa, r):
        doc.add_heading(f"{i}. {r.get('ho_ten')} – {pa}: {MA_PHUONG_AN[pa][1]}", level=2)
        if r.get("ly_do"):
            p("Vì sao: " + r["ly_do"])
        dong = [["Họ và tên", r.get("ho_ten")],
                ["Mã số BHXH", r.get("ma_so_bhxh") or "Chưa có → để trống, khai TK1-TS"],
                ["Ngày sinh", r.get("ngay_sinh")]]
        if MA_PHUONG_AN[pa][0] != "giam":
            dong += [["Chức vụ, chức danh nghề, nơi làm việc", r.get("chuc_danh_noi_lam_viec")],
                     ["Tiền lương" + (" (mới)" if r.get("luong_cu") else ""), _tien(r.get("tien_luong"))]]
            if r.get("luong_cu"):
                dong.append(["Tiền lương cũ (để đối chiếu, không gõ)", _tien(r.get("luong_cu"))])
            if r.get("phu_cap_bo_sung"):
                dong.append(["Phụ cấp lương (iBH: ô \"Phụ cấp lương\"; khoản thu nhập bổ sung: ô \"Các khoản bổ sung\")",
                             _tien(r.get("phu_cap_bo_sung"))])
            if r.get("loai_hd"):
                dong.append(["Loại HĐLĐ", LOAI_HD.get(r["loai_hd"], r["loai_hd"])])
            if r.get("ngay_hieu_luc"):
                dong.append(["Ngày HĐLĐ / quyết định có hiệu lực", r.get("ngay_hieu_luc")])
        if phan_mem == "ibh":
            tab = {"tang": "TĂNG LAO ĐỘNG", "giam": "GIẢM LAO ĐỘNG"}.get(MA_PHUONG_AN[pa][0])
            if MA_PHUONG_AN[pa][0] == "dieu_chinh":
                tab = "GIẢM TIỀN LƯƠNG" if (r.get("luong_cu") or 0) > (r.get("tien_luong") or 0) else "TĂNG TIỀN LƯƠNG"
            dong.insert(0, ["Tab chọn khi bấm \"Thêm\" (iBH)", tab])
            if MA_PHUONG_AN[pa][0] != "giam":
                dong += [["Vùng lương", f"Vùng {['I', 'II', 'III', 'IV'][vung - 1]}"],
                         ["Tỷ lệ đóng", "32% (đóng đủ BHXH, BHYT, BHTN, BHTNLĐ-BNN)"]]
        nhan_pa = NHAN_IBH.get(pa) if phan_mem == "ibh" and NHAN_IBH.get(pa) else ""
        if nhan_pa and pa == "TM" and r.get("ma_so_bhxh") and r.get("da_co_so"):
            nhan_pa = "Tăng mới"
        dong += [["Phương án", f"{pa} – {MA_PHUONG_AN[pa][1]}" + (f" → trên iBH chọn: \"{nhan_pa}\"" if nhan_pa else
                                                                  " (chọn dòng có nội dung tương ứng)")],
                 ["Từ tháng/năm", r.get("tu_thang")]]
        if r.get("den_thang"):
            dong.append(["Đến tháng/năm", r.get("den_thang")])
        if r.get("noi_kcb") and MA_PHUONG_AN[pa][0] == "tang":
            dong.append(["Nơi đăng ký KCB ban đầu", r.get("noi_kcb")])
        if r.get("hinh_thuc_nhan_ket_qua"):
            dong.append(["Hình thức nhận kết quả", r.get("hinh_thuc_nhan_ket_qua")])
        dong.append(["Ghi chú (chép nguyên văn)", r.get("ghi_chu")])
        bang(dong, tieu_de=["Ô trên phần mềm", "Gõ vào"])
        if pa == "TM" and not r.get("ma_so_bhxh"):
            p("Thông tin tờ khai TK1-TS / thêm người mới vào danh sách lao động:", dam=True)
            bang([[nhan, r.get(k) or ("CÒN THIẾU – hỏi người lao động" if k in TK1_BAT_BUOC else "(không bắt buộc)")]
                  for k, nhan in TK1_TRUONG] + [["[17] Hồ sơ kèm theo", "; ".join(r.get("giay_to") or GIAY_TO_MAC_DINH["TM"][:1])]],
                 tieu_de=["Trường TK1-TS", "Giá trị"])
            p("Người lao động ký TK1-TS với câu \"Tôi chịu trách nhiệm trước pháp luật về nội dung đã kê khai\". "
              "Phần mềm có thể hỏi thêm (nơi đăng ký khai sinh, địa chỉ, ngày cấp căn cước) – hỏi người lao động, không đoán.")

    so = 0
    for ma, ten in (("tang", "IV. TĂNG"), ("giam", "V. GIẢM"), ("dieu_chinh", "VI. ĐIỀU CHỈNH")):
        h(f"{ten} ({len(nhom[ma])} người)")
        if not nhom[ma]:
            p("Không có.")
        for pa, r in nhom[ma]:
            so += 1
            khoi(so, pa, r)

    h("VII. Giấy tờ đính kèm (scan PDF, đặt tên rõ)")
    gt = []
    for ma in ("tang", "giam", "dieu_chinh"):
        for pa, r in nhom[ma]:
            for x in r.get("giay_to") or GIAY_TO_MAC_DINH.get(pa, []):
                if "TK1-TS" in x and r.get("ma_so_bhxh"):
                    continue
                gt.append([r.get("ho_ten"), x])
    bang(gt or [["—", "—"]], tieu_de=["Người", "Giấy tờ"])

    h("VIII. Không kê khai tháng này")
    bang([[x.get("ho_ten"), x.get("ly_do")] for x in khong_ke_khai] or [["—", "—"]], tieu_de=["Người", "Lý do"])

    ten_pm, buoc = THAO_TAC.get(phan_mem, THAO_TAC["chung"])
    h(f"IX. Thao tác trên {ten_pm}")
    p("Chuẩn bị 1 lần (nếu chưa làm):", dam=True)
    for x in (["Tạo danh sách Phòng ban và Chức vụ trong phần mềm trước khi thêm người lao động (iBH bắt buộc)."] if phan_mem == "ibh" else []) + [
            f"Đầu hồ sơ: Kỳ kê khai = {thang}; Người nộp = {don_vi.get('nguoi_nop') or 'họ tên người làm hồ sơ'}; "
            f"Số điện thoại = {don_vi.get('dien_thoai_nguoi_nop') or don_vi.get('dien_thoai') or 'số của người làm hồ sơ'}.",
            "Chữ ký số của doanh nghiệp còn hạn, đã cắm vào máy, đã cài phần mềm ký số."]:
        doc.add_paragraph(x, style="List Bullet")
    for b in buoc:
        doc.add_paragraph(b, style="List Number")
    p("Các bước theo hướng dẫn của nhà cung cấp/BHXH; tên nút có thể khác theo phiên bản – làm theo đúng các ô ở mục IV, V, VI.")

    h("X. Sau khi nộp")
    for x in ["Lưu mã hồ sơ, biên nhận. Cơ quan BHXH thông báo trả lại/bổ sung trong không quá 03 ngày làm việc nếu hồ sơ thiếu, sai "
              "(QĐ 366/QĐ-BHXH) – sửa theo lý do rồi nộp lại.",
              f"Chuyển khoản tiền đóng tháng {thang} chậm nhất {_cuoi_thang_sau(thang)}: số tài khoản thu của cơ quan BHXH ghi trên "
              "Thông báo kết quả đóng (C12-TS) hoặc hỏi BHXH cơ sở; nội dung chuyển khoản ghi mã đơn vị "
              f"{don_vi.get('ma_don_vi', '…')} + \"nộp BHXH tháng {thang}\". Chậm đóng bị tính tiền chậm đóng.",
              "Đối chiếu số tiền với Thông báo kết quả đóng (Mẫu C12-TS) cơ quan BHXH gửi hằng tháng.",
              "Lưu toàn bộ hồ sơ vào thư mục BHXH theo tháng."]:
        doc.add_paragraph(x, style="List Bullet")

    h("XI. Việc phải nhớ tháng sau")
    nho = list(viec_thang_sau)
    for pa, r in nhom["giam"]:
        if pa in ("KL", "OF") and r.get("den_thang") == thang:
            nho.append(f"{r.get('ho_ten')}: báo ON (đi làm lại) kỳ {_thang_sau(thang)} nếu đã đi làm lại.")
        if pa == "TS":
            nho.append(f"{r.get('ho_ten')}: báo ON khi đi làm lại sau thai sản; làm hồ sơ hưởng chế độ thai sản.")
        if pa == "GH":
            nho.append(f"{r.get('ho_ten')}: chốt sổ, trả giấy tờ trong 14 ngày làm việc kể từ ngày nghỉ việc (Điều 48 BLLĐ).")
    for x in nho or ["—"]:
        doc.add_paragraph(x, style="List Bullet")
    doc.save(duong_dan_ra)
    return {"duong_dan": duong_dan_ra, "tang": len(nhom["tang"]), "giam": len(nhom["giam"]), "dieu_chinh": len(nhom["dieu_chinh"]),
            "can_tk1_ts": can_tk1, "thong_tin_con_thieu": thieu, "loi": loi_dl, "han_dong_tien": _cuoi_thang_sau(thang)}

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
    {"name": "huong_dan_ke_khai_bhxh", "fn": huong_dan_ke_khai,
     "description": "Xuất file Word 'Hướng dẫn kê khai BHXH tháng ...' cho người mới làm: tóm tắt tăng/giảm/điều chỉnh, tổng tiền, hạn đóng; "
                    "hồ sơ nộp gì (chung 1 hồ sơ 600, TK1-TS cho ai); khối 'gõ vào phần mềm' cho từng người; thông tin TK1-TS còn thiếu "
                    "kèm tin nhắn xin người lao động; giấy tờ đính kèm; ai không kê khai và vì sao; thao tác trên iBH (ivan) / cổng BHXH; "
                    "sau khi nộp; việc tháng sau. Đây là đầu ra chính khi báo tăng, giảm, điều chỉnh.",
     "schema": {"type": "object", "required": ["duong_dan_ra", "thang", "danh_sach"], "properties": {
         "duong_dan_ra": {"type": "string"}, "thang": {"type": "string", "description": "mm/yyyy"},
         "danh_sach": {"type": "array", "items": {"type": "object"},
                       "description": "Mỗi người như xuat_d02_lt + ly_do, luong_cu, giay_to (list), và cho TM chưa có mã: so_dinh_danh, "
                                      "gioi_tinh, dan_toc, quoc_tich, dien_thoai, email"},
         "don_vi": {"type": "object"},
         "khong_ke_khai": {"type": "array", "items": {"type": "object", "properties": {"ho_ten": {}, "ly_do": {}}}},
         "tien_dong": {"type": "object", "description": "nld, dn, tong, tong_thang_truoc (tính bằng luong_net_gross)"},
         "viec_thang_sau": {"type": "array", "items": {"type": "string"}},
         "phan_mem": {"type": "string", "enum": ["chung", "ibh", "cong_bhxh"]},
         "vung": {"type": "integer"}, "ngay_lap": {"type": "string"}}}},
]
