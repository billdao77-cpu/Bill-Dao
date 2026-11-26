"""Bộ công cụ tính toán, tra cứu của plugin – dùng chung cho dòng lệnh (cong_cu.py) và test.

Thêm công cụ: viết hàm + mô tả vào TOOLS của một module, rồi thêm module vào MODULES dưới đây.

Bản vn-custom bổ sung lớp bảo vệ tập trung trong goi():
- Kiểm tra tham số theo schema (thiếu tham số bắt buộc, tham số lạ, giá trị ngoài enum) và trả lỗi rõ ràng.
- Công cụ xuất file (BAO_VE_GHI) không ghi đè file đã có trừ khi truyền ghi_de=true, và phải đúng đuôi file.
"""
import importlib
import os

MODULES = ["lich_vn", "doc_so", "so_van_ban", "the_thuc", "lao_dong", "bhxh", "lich_tuan_thu", "cham_cong"]

# tên công cụ -> (tham số đường dẫn ra, đuôi file bắt buộc)
BAO_VE_GHI = {
    "tao_van_ban_docx": ("duong_dan_ra", ".docx"),
    "xuat_d02_lt": ("duong_dan_ra", ".xlsx"),
    "huong_dan_ke_khai_bhxh": ("duong_dan_ra", ".docx"),
    "tao_file_ics": ("duong_dan_ra", ".ics"),
    "lich_tuan_thu_hcns": ("xuat_ics", ".ics"),
}
_GHI_DE = {"type": "boolean", "description": "Cho phép ghi đè file đã có (mặc định false – chỉ dùng khi người dùng đồng ý rõ)"}


def tat_ca():
    ds = []
    for m in MODULES:
        for t in importlib.import_module(f"{__name__}.{m}").TOOLS:
            if t["name"] in BAO_VE_GHI:
                t["schema"].setdefault("properties", {})["ghi_de"] = _GHI_DE
            ds.append(t)
    return ds


def _kiem_tra_tham_so(t, tham_so):
    sc = t.get("schema") or {}
    props = sc.get("properties", {})
    thieu = [k for k in sc.get("required", []) if tham_so.get(k) in (None, "")]
    la = [k for k in tham_so if props and k not in props]
    sai = [f"{k}={tham_so[k]!r} (chỉ nhận: {', '.join(map(str, props[k]['enum']))})"
           for k in tham_so if k in props and "enum" in props[k]
           and str(tham_so[k]) not in {str(x) for x in props[k]["enum"]}]
    if thieu or la or sai:
        return {"loi": "Tham số không hợp lệ", "cong_cu": t["name"], "thieu_bat_buoc": thieu,
                "tham_so_khong_ho_tro": la, "gia_tri_khong_hop_le": sai,
                "tham_so_hop_le": sorted(props)}
    return None


def _kiem_tra_ghi(ten, tham_so):
    khoa, duoi = BAO_VE_GHI[ten]
    ghi_de = bool(tham_so.pop("ghi_de", False))
    p = tham_so.get(khoa)
    if not p:
        return None
    if not str(p).lower().endswith(duoi):
        return {"loi": f"{khoa} phải là file {duoi}", "duong_dan": p}
    if os.path.exists(p) and not ghi_de:
        return {"loi": "File đã tồn tại – không ghi đè để tránh mất dữ liệu", "duong_dan": os.path.abspath(p),
                "goi_y": "Đặt tên file mới (ví dụ thêm _v2 hoặc ngày giờ). Chỉ dùng ghi_de=true khi người dùng xác nhận rõ."}
    return None


def goi(ten, tham_so):
    tham_so = dict(tham_so or {})
    for t in tat_ca():
        if t["name"] == ten:
            loi = _kiem_tra_tham_so(t, tham_so)
            if loi:
                return loi
            if ten in BAO_VE_GHI:
                loi = _kiem_tra_ghi(ten, tham_so)
                if loi:
                    return loi
            return t["fn"](**tham_so)
    raise KeyError(f"Không có công cụ '{ten}'")
