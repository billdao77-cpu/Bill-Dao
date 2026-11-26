"""Chấm công và tiền lương làm thêm giờ, làm việc ban đêm (bản vn-custom).

Căn cứ: Điều 98, 105–107 Bộ luật Lao động 2019; Nghị định 145/2020/NĐ-CP (Điều 55–57 về tiền lương làm thêm giờ, ban đêm;
điều, khoản cụ thể về giới hạn làm thêm cần đối chiếu văn bản gốc).
Mọi kết quả là bảng tính tham khảo cho người làm lương; mức trả cao hơn theo HĐLĐ, thỏa ước, quy chế lương thì
áp dụng mức cao hơn. Giới hạn giờ làm thêm có thể được Quốc hội/Chính phủ điều chỉnh tạm thời (như NQ 17/2022, đã hết
hiệu lực 31/12/2022) – luôn kiểm tra văn bản mới nhất trước khi chốt.
"""
from datetime import date

from . import lich_vn
from .lich_vn import _ngay

CAN_CU_LUONG = "Điều 98 BLLĐ 2019; Điều 55–57 NĐ 145/2020/NĐ-CP"
CAN_CU_GIO = "Điều 107 BLLĐ 2019; NĐ 145/2020/NĐ-CP (mục làm thêm giờ)"

# Hệ số tối thiểu so với tiền lương giờ thực trả của ngày làm việc bình thường
HE_SO = {
    "ngay_thuong": 1.5,
    "nghi_hang_tuan": 2.0,
    "le_tet": 3.0,  # ngày nghỉ lễ, Tết, ngày nghỉ có hưởng lương (chưa gồm lương ngày lễ của NLĐ hưởng lương ngày)
}
# Hệ số giờ ban ngày dùng cho khoản 20% khi làm thêm ban đêm (Điều 57 NĐ 145/2020)
HE_SO_BAN_NGAY_CHO_20 = {"ngay_thuong": 1.0, "ngay_thuong_co_lam_them_ban_ngay": 1.5, "nghi_hang_tuan": 2.0, "le_tet": 3.0}


def _tien(x):
    return f"{round(x):,}".replace(",", ".") + " đ"


def _luong_gio(luong_thang, luong_gio, so_ngay_lam_viec_thang, so_gio_ngay):
    if luong_gio:
        return float(luong_gio), "Tiền lương giờ người dùng cung cấp"
    if not luong_thang:
        raise ValueError("Cần luong_thang hoặc luong_gio")
    n, g = float(so_ngay_lam_viec_thang), float(so_gio_ngay)
    if not (0 < n <= 31 and 0 < g <= 12):
        raise ValueError("so_ngay_lam_viec_thang phải trong (0, 31], so_gio_ngay trong (0, 12]")
    return float(luong_thang) / n / g, (f"{_tien(float(luong_thang))} / {n:g} ngày / {g:g} giờ "
                                         "(số ngày làm việc bình thường trong tháng theo quy chế lương; cách tính tiền lương giờ: NĐ 145/2020 [Cần kiểm tra điều, khoản cụ thể])")


def tinh_luong_lam_them(luong_thang=None, luong_gio=None, so_ngay_lam_viec_thang=26, so_gio_ngay=8,
                        gio_ngay_thuong=0, gio_nghi_hang_tuan=0, gio_le_tet=0,
                        gio_dem_ngay_thuong=0, gio_dem_nghi_hang_tuan=0, gio_dem_le_tet=0,
                        dem_sau_khi_da_lam_them_ban_ngay=False, gio_lam_dem_binh_thuong=0):
    lg, cach_tinh = _luong_gio(luong_thang, luong_gio, so_ngay_lam_viec_thang, so_gio_ngay)
    gio = {k: float(v or 0) for k, v in dict(
        gio_ngay_thuong=gio_ngay_thuong, gio_nghi_hang_tuan=gio_nghi_hang_tuan, gio_le_tet=gio_le_tet,
        gio_dem_ngay_thuong=gio_dem_ngay_thuong, gio_dem_nghi_hang_tuan=gio_dem_nghi_hang_tuan,
        gio_dem_le_tet=gio_dem_le_tet, gio_lam_dem_binh_thuong=gio_lam_dem_binh_thuong).items()}
    am = [k for k, v in gio.items() if v < 0]
    if am:
        return {"loi": f"Số giờ không được âm: {', '.join(am)}"}
    k20_thuong = HE_SO_BAN_NGAY_CHO_20["ngay_thuong_co_lam_them_ban_ngay" if dem_sau_khi_da_lam_them_ban_ngay else "ngay_thuong"]
    dong = [
        ("Làm thêm ban ngày – ngày thường", gio["gio_ngay_thuong"], HE_SO["ngay_thuong"]),
        ("Làm thêm ban ngày – ngày nghỉ hằng tuần", gio["gio_nghi_hang_tuan"], HE_SO["nghi_hang_tuan"]),
        ("Làm thêm ban ngày – ngày lễ, Tết, nghỉ có hưởng lương", gio["gio_le_tet"], HE_SO["le_tet"]),
        ("Làm thêm ban đêm – ngày thường", gio["gio_dem_ngay_thuong"], HE_SO["ngay_thuong"] + 0.3 + 0.2 * k20_thuong),
        ("Làm thêm ban đêm – ngày nghỉ hằng tuần", gio["gio_dem_nghi_hang_tuan"],
         HE_SO["nghi_hang_tuan"] + 0.3 + 0.2 * HE_SO_BAN_NGAY_CHO_20["nghi_hang_tuan"]),
        ("Làm thêm ban đêm – ngày lễ, Tết", gio["gio_dem_le_tet"], HE_SO["le_tet"] + 0.3 + 0.2 * HE_SO_BAN_NGAY_CHO_20["le_tet"]),
        ("Làm việc ban đêm trong giờ bình thường (chỉ phần trả thêm 30%)", gio["gio_lam_dem_binh_thuong"], 0.3),
    ]
    bang, tong = [], 0.0
    for ten, h, k in dong:
        if h:
            tien = h * lg * k
            tong += tien
            bang.append({"khoan": ten, "so_gio": h, "he_so_toi_thieu": f"{k * 100:g}%", "thanh_tien": _tien(tien)})
    canh_bao = []
    tong_gio_them = sum(v for k, v in gio.items() if k != "gio_lam_dem_binh_thuong")
    if tong_gio_them > 40:
        canh_bao.append(f"Tổng {tong_gio_them:g} giờ làm thêm – nếu đây là số giờ trong 1 tháng thì vượt giới hạn 40 giờ/tháng "
                        "(điểm b khoản 2 Điều 107 BLLĐ 2019). Kiểm tra bằng kiem_tra_gio_lam_them.")
    return {
        "tien_luong_gio": _tien(lg), "cach_tinh_luong_gio": cach_tinh,
        "bang_tinh": bang, "tong_tien_lam_them_va_ban_dem": _tien(tong),
        "ban_dem": "Từ 22 giờ đến 6 giờ sáng hôm sau (Điều 106 BLLĐ 2019).",
        "can_cu": CAN_CU_LUONG + " [Chắc chắn – mức tối thiểu; doanh nghiệp được trả cao hơn]",
        "luu_y": ["Tiền lương giờ tính theo tiền lương thực trả theo công việc đang làm (mức lương theo HĐLĐ, phụ cấp lương, "
                  "khoản bổ sung xác định được mức tiền) – đối chiếu Điều 55 NĐ 145/2020 và quy chế lương của doanh nghiệp.",
                  "NLĐ hưởng lương ngày làm thêm vào ngày lễ, Tết còn được hưởng tiền lương ngày lễ (Điều 98 BLLĐ 2019).",
                  "Nếu doanh nghiệp bố trí nghỉ bù cho giờ làm thêm thì đối chiếu quy định về nghỉ bù tại NĐ 145/2020 [Cần kiểm tra] và thỏa thuận với NLĐ.",
                  "Kết quả là bảng tính tham khảo; người làm lương và người có thẩm quyền duyệt trước khi chi trả."] + canh_bao,
    }


def _loai_ngay(d, nghi_tuan, cache):
    if d.year not in cache:
        le, bu = lich_vn.ngay_le(d.year, nghi_tuan=nghi_tuan)
        cache[d.year] = ({x for x, _ in le} | {x for x, _ in bu})
    if d in cache[d.year]:
        return "le_tet"
    if d.weekday() in nghi_tuan:
        return "nghi_hang_tuan"
    return "ngay_thuong"


def kiem_tra_gio_lam_them(bang_cham_cong, so_gio_binh_thuong_ngay=8, che_do="theo_ngay", gioi_han_nam=200,
                          gio_lam_them_tu_dau_nam_truoc_ky=0, nghi_thu_bay=True, ho_ten=""):
    """bang_cham_cong: [{"ngay": "dd/mm/yyyy", "gio_binh_thuong": 8, "gio_lam_them": 2, "gio_lam_them_dem": 0}]"""
    nghi_tuan = (5, 6) if nghi_thu_bay else (6,)
    loi_du_lieu, vi_pham, theo_thang, theo_loai = [], [], {}, {"ngay_thuong": 0.0, "nghi_hang_tuan": 0.0, "le_tet": 0.0}
    da_thay, cache = set(), {}
    if not isinstance(bang_cham_cong, list) or not bang_cham_cong:
        return {"loi": "bang_cham_cong phải là danh sách ngày công, ví dụ [{\"ngay\": \"02/11/2026\", \"gio_lam_them\": 2}]"}
    if int(gioi_han_nam) not in (200, 300):
        return {"loi": "gioi_han_nam chỉ nhận 200 (mặc định) hoặc 300 (ngành nghề, công việc tại khoản 3 Điều 107 BLLĐ 2019)"}
    tran_ngay = 12 if che_do == "theo_tuan" else float(so_gio_binh_thuong_ngay) * 1.5
    for i, r in enumerate(bang_cham_cong, 1):
        try:
            d = _ngay(r.get("ngay"))
        except (TypeError, ValueError):
            loi_du_lieu.append(f"Dòng {i}: ngày không hợp lệ {r.get('ngay')!r}")
            continue
        try:
            bt = float(r.get("gio_binh_thuong", so_gio_binh_thuong_ngay) or 0)
            lt = float(r.get("gio_lam_them", 0) or 0) + float(r.get("gio_lam_them_dem", 0) or 0)
        except (TypeError, ValueError):
            loi_du_lieu.append(f"Dòng {i} ({d:%d/%m/%Y}): số giờ không phải là số")
            continue
        if d in da_thay:
            loi_du_lieu.append(f"Dòng {i}: ngày {d:%d/%m/%Y} bị chấm trùng")
        da_thay.add(d)
        if bt < 0 or lt < 0 or bt + lt > 24:
            loi_du_lieu.append(f"Dòng {i} ({d:%d/%m/%Y}): số giờ bất thường (bình thường {bt:g}, làm thêm {lt:g})")
            continue
        if d > date.today():
            loi_du_lieu.append(f"Dòng {i}: ngày {d:%d/%m/%Y} ở tương lai – kiểm tra lại kỳ chấm công")
        loai = _loai_ngay(d, nghi_tuan, cache)
        if loai != "ngay_thuong" and bt:
            loi_du_lieu.append(f"Dòng {i} ({d:%d/%m/%Y}): ngày {'lễ/Tết' if loai == 'le_tet' else 'nghỉ hằng tuần'} nhưng có "
                               f"{bt:g} giờ bình thường – nếu làm việc thì đây là giờ làm thêm")
        theo_loai[loai] += lt
        k = f"{d.month:02d}/{d.year}"
        theo_thang[k] = theo_thang.get(k, 0.0) + lt
        tong_ngay = bt + lt
        if loai == "ngay_thuong" and che_do == "theo_ngay" and lt > 0.5 * float(so_gio_binh_thuong_ngay):
            vi_pham.append(f"{d:%d/%m/%Y}: làm thêm {lt:g} giờ > 50% số giờ bình thường/ngày")
        elif lt and tong_ngay > (12 if loai != "ngay_thuong" else tran_ngay):
            vi_pham.append(f"{d:%d/%m/%Y}: tổng {tong_ngay:g} giờ/ngày vượt "
                           f"{12 if loai != 'ngay_thuong' else tran_ngay:g} giờ")
    for k, v in theo_thang.items():
        if v > 40:
            vi_pham.append(f"Tháng {k}: {v:g} giờ làm thêm > 40 giờ/tháng")
    tong_ky = sum(theo_thang.values())
    luy_ke = float(gio_lam_them_tu_dau_nam_truoc_ky or 0) + tong_ky
    if luy_ke > int(gioi_han_nam):
        vi_pham.append(f"Lũy kế năm {luy_ke:g} giờ > {int(gioi_han_nam)} giờ/năm")
    canh_bao_nam = []
    if 200 < luy_ke <= 300 and int(gioi_han_nam) == 300:
        canh_bao_nam.append("Làm thêm trên 200 giờ/năm: phải thuộc trường hợp khoản 3 Điều 107 và thông báo cho Sở Nội vụ "
                            "(khoản 4 Điều 107 BLLĐ 2019; thủ tục chi tiết tại NĐ 145/2020 [Cần kiểm tra điều cụ thể]).")
    return {
        "nguoi_lao_dong": ho_ten or "(không ghi tên)",
        "so_dong": len(bang_cham_cong), "loi_du_lieu": loi_du_lieu,
        "ket_luan": "CÓ VI PHẠM GIỚI HẠN" if vi_pham else ("CẦN SỬA DỮ LIỆU" if loi_du_lieu else "Trong giới hạn"),
        "vi_pham": vi_pham,
        "gio_lam_them_theo_thang": theo_thang,
        "gio_lam_them_theo_loai_ngay": theo_loai,
        "gio_lam_them_luy_ke_nam": luy_ke,
        "goi_y_tinh_tien": "Dùng tinh_luong_lam_them với gio_ngay_thuong / gio_nghi_hang_tuan / gio_le_tet theo bảng trên "
                           "(tách riêng giờ làm thêm ban đêm 22h–6h).",
        "can_cu": CAN_CU_GIO + " [Chắc chắn với các mức của Điều 107 BLLĐ 2019: 50%/ngày, 12 giờ/ngày, 40 giờ/tháng, 200/300 giờ/năm; "
                               "Cần kiểm tra: điều cụ thể của NĐ 145/2020 và nghị quyết điều chỉnh tạm thời mới nếu có]",
        "luu_y": ["Làm thêm giờ phải có sự đồng ý của người lao động (điểm a khoản 2 Điều 107).",
                  "Ngày lễ, nghỉ bù được xác định theo Điều 112 BLLĐ 2019 – năm có quyết định hoán đổi ngày làm việc "
                  "của Thủ tướng thì cần điều chỉnh tay."] + canh_bao_nam,
    }


TOOLS = [
    {"name": "tinh_luong_lam_them", "fn": tinh_luong_lam_them,
     "description": "Tính tiền lương làm thêm giờ và làm việc ban đêm theo Điều 98 BLLĐ 2019, Điều 57 NĐ 145/2020: "
                    "150%/200%/300%, ban đêm +30%, làm thêm ban đêm 200%/210%/270%/390%; từ lương tháng hoặc lương giờ.",
     "schema": {"type": "object", "properties": {
         "luong_thang": {"type": "number", "description": "Tiền lương tháng thực trả theo công việc"},
         "luong_gio": {"type": "number", "description": "Nếu đã có tiền lương giờ thì nhập thay luong_thang"},
         "so_ngay_lam_viec_thang": {"type": "number", "description": "Số ngày làm việc bình thường trong tháng theo quy chế (mặc định 26)"},
         "so_gio_ngay": {"type": "number", "description": "Số giờ làm việc bình thường/ngày (mặc định 8)"},
         "gio_ngay_thuong": {"type": "number"}, "gio_nghi_hang_tuan": {"type": "number"}, "gio_le_tet": {"type": "number"},
         "gio_dem_ngay_thuong": {"type": "number"}, "gio_dem_nghi_hang_tuan": {"type": "number"},
         "gio_dem_le_tet": {"type": "number"},
         "dem_sau_khi_da_lam_them_ban_ngay": {"type": "boolean", "description": "Ngày thường: đã làm thêm ban ngày trước khi làm thêm ban đêm"},
         "gio_lam_dem_binh_thuong": {"type": "number", "description": "Giờ làm ca đêm trong giờ bình thường (không phải làm thêm)"}}}},
    {"name": "kiem_tra_gio_lam_them", "fn": kiem_tra_gio_lam_them,
     "description": "Rà bảng chấm công của một người: lỗi dữ liệu (ngày sai, trùng, giờ âm/>24, ngày tương lai, giờ bình thường "
                    "vào ngày nghỉ), phân loại ngày thường/nghỉ tuần/lễ Tết, kiểm tra giới hạn làm thêm 50%/ngày hoặc 12 giờ/ngày, "
                    "40 giờ/tháng, 200/300 giờ/năm (Điều 107 BLLĐ 2019).",
     "schema": {"type": "object", "required": ["bang_cham_cong"], "properties": {
         "bang_cham_cong": {"type": "array", "items": {"type": "object", "required": ["ngay"], "properties": {
             "ngay": {"type": "string"}, "gio_binh_thuong": {"type": "number"}, "gio_lam_them": {"type": "number"},
             "gio_lam_them_dem": {"type": "number"}}}},
         "so_gio_binh_thuong_ngay": {"type": "number"},
         "che_do": {"type": "string", "enum": ["theo_ngay", "theo_tuan"]},
         "gioi_han_nam": {"type": "integer", "enum": [200, 300]},
         "gio_lam_them_tu_dau_nam_truoc_ky": {"type": "number"},
         "nghi_thu_bay": {"type": "boolean"}, "ho_ten": {"type": "string"}}}},
]
