"""Test cho các thay đổi của nhánh vn-custom. Chạy: python3 tests/test_vn_custom.py"""
import json
import os
import subprocess
import sys
import tempfile

GOC = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, GOC)

from tools import goi  # noqa: E402

LOI = []


def kiem(ten, dk, kq=None):
    print(("  ok  " if dk else "  SAI ") + ten)
    if not dk:
        LOI.append(ten)
        print("       ", json.dumps(kq, ensure_ascii=False, default=str)[:400])


def test_kiem_tra_tham_so():
    print("test_kiem_tra_tham_so")
    r = goi("tro_cap_thoi_viec", {"ngay_bat_dau": "01/01/2020", "ngay_nghi": "01/01/2026",
                                  "luong_binh_quan_6_thang": 10e6, "abc": 1})
    kiem("Tham số lạ bị từ chối", r.get("tham_so_khong_ho_tro") == ["abc"], r)
    r = goi("tro_cap_thoi_viec", {"ngay_bat_dau": "01/01/2020"})
    kiem("Thiếu tham số bắt buộc", set(r.get("thieu_bat_buoc", [])) == {"ngay_nghi", "luong_binh_quan_6_thang"}, r)
    r = goi("tra_cuu_so_van_ban", {"loai": "../../etc/x"})
    kiem("loai ngoài enum bị từ chối (chặn ghép đường dẫn)", bool(r.get("gia_tri_khong_hop_le")), r)
    r = goi("kiem_tra_luong_toi_thieu", {"muc_luong": 6e6, "vung": "1"})
    kiem("vung='1' (chuỗi) vẫn hợp lệ", "loi" not in r or r.get("loi") != "Tham số không hợp lệ", r)


def test_chong_ghi_de():
    print("test_chong_ghi_de")
    with tempfile.TemporaryDirectory() as d:
        f = os.path.join(d, "lich.ics")
        sk = [{"ngay": "2026-12-01", "ten": "Hạn HĐLĐ"}]
        r1 = goi("tao_file_ics", {"duong_dan_ra": f, "su_kien": sk})
        kiem("Tạo file mới", os.path.exists(f) and "da_tao" in r1, r1)
        with open(f, "w", encoding="utf-8") as h:
            h.write("DU LIEU GOC")
        r2 = goi("tao_file_ics", {"duong_dan_ra": f, "su_kien": sk})
        with open(f, encoding="utf-8") as h:
            giu = h.read() == "DU LIEU GOC"
        kiem("Không ghi đè file đã có", "loi" in r2 and giu, r2)
        r3 = goi("tao_file_ics", {"duong_dan_ra": f, "su_kien": sk, "ghi_de": True})
        kiem("Ghi đè khi ghi_de=true", "da_tao" in r3, r3)
        r4 = goi("tao_file_ics", {"duong_dan_ra": os.path.join(d, "x.docx"), "su_kien": sk})
        kiem("Sai đuôi file bị từ chối", "loi" in r4, r4)
        r5 = goi("lich_tuan_thu_hcns", {"nam": 2026, "xuat_ics": f})
        kiem("lich_tuan_thu_hcns cũng không ghi đè", "loi" in r5, r5)


def test_csv_an_toan():
    print("test_csv_an_toan")
    with tempfile.TemporaryDirectory() as d:
        goi("dang_ky_van_ban_den", {"co_quan_ban_hanh": '=HYPERLINK("http://x","y")', "so_ky_hieu": "1/TB",
                                    "trich_yeu": "+cmd", "thu_muc": d, "ngay_den": "02/11/2026"})
        with open(os.path.join(d, "so-van-ban-den-2026.csv"), encoding="utf-8-sig") as h:
            dong = h.read().splitlines()[1]
        kiem("Ô bắt đầu bằng = / + được vô hiệu hóa", ",\"'=HYPERLINK" in dong and ",'+cmd," in dong, dong)
        r = goi("dang_ky_van_ban_den", {"co_quan_ban_hanh": '=HYPERLINK("http://x","y")', "so_ky_hieu": "2/TB",
                                        "trich_yeu": "b", "thu_muc": d, "ngay_den": "02/11/2026"})
        kiem("Đọc lại sổ đã làm sạch vẫn cấp số tiếp", r.get("so_den") == 2, r)


def test_luong_lam_them():
    print("test_luong_lam_them")
    r = goi("tinh_luong_lam_them", {"luong_thang": 10_400_000, "gio_ngay_thuong": 1, "gio_nghi_hang_tuan": 1, "gio_le_tet": 1,
                                    "gio_dem_ngay_thuong": 1, "gio_dem_nghi_hang_tuan": 1, "gio_dem_le_tet": 1,
                                    "gio_lam_dem_binh_thuong": 1})
    he_so = [x["he_so_toi_thieu"] for x in r["bang_tinh"]]
    kiem("Lương giờ 10,4tr/26/8 = 50.000", r["tien_luong_gio"] == "50.000 đ", r)
    kiem("Hệ số 150/200/300/200/270/390/30", he_so == ["150%", "200%", "300%", "200%", "270%", "390%", "30%"], he_so)
    r = goi("tinh_luong_lam_them", {"luong_gio": 50_000, "gio_dem_ngay_thuong": 1, "dem_sau_khi_da_lam_them_ban_ngay": True})
    kiem("Làm thêm đêm sau khi đã làm thêm ngày = 210%", r["bang_tinh"][0]["he_so_toi_thieu"] == "210%", r)
    r = goi("tinh_luong_lam_them", {"luong_gio": 50_000, "gio_ngay_thuong": -2})
    kiem("Giờ âm bị từ chối", "loi" in r, r)


def test_kiem_tra_gio():
    print("test_kiem_tra_gio")
    bang = [{"ngay": "02/11/2026", "gio_lam_them": 5},          # thứ Hai: 5 > 4 giờ (50%)
            {"ngay": "02/11/2026", "gio_lam_them": 1},          # trùng
            {"ngay": "08/11/2026", "gio_binh_thuong": 0, "gio_lam_them": 8},  # Chủ nhật
            {"ngay": "02/09/2026", "gio_binh_thuong": 0, "gio_lam_them": 4},  # Quốc khánh
            {"ngay": "31/02/2026", "gio_lam_them": 1}]          # ngày sai
    bang += [{"ngay": f"{d:02d}/10/2026", "gio_lam_them": 3} for d in (1, 2, 5, 6, 7, 8, 9, 12, 13, 14, 15, 16, 19, 20)]
    r = goi("kiem_tra_gio_lam_them", {"bang_cham_cong": bang})
    vp = " | ".join(r["vi_pham"])
    kiem("Bắt vượt 50%/ngày", "02/11/2026: làm thêm" in vp, r)
    kiem("Bắt vượt 40 giờ/tháng", "Tháng 10/2026" in vp, r)
    kiem("Bắt chấm trùng và ngày sai", any("trùng" in x for x in r["loi_du_lieu"])
         and any("không hợp lệ" in x for x in r["loi_du_lieu"]), r["loi_du_lieu"])
    kiem("Phân loại Chủ nhật và lễ", r["gio_lam_them_theo_loai_ngay"]["nghi_hang_tuan"] == 8
         and r["gio_lam_them_theo_loai_ngay"]["le_tet"] == 4, r["gio_lam_them_theo_loai_ngay"])
    r = goi("kiem_tra_gio_lam_them", {"bang_cham_cong": [{"ngay": "03/11/2026", "gio_lam_them": 2}],
                                      "gio_lam_them_tu_dau_nam_truoc_ky": 199})
    kiem("Bắt vượt 200 giờ/năm (lũy kế)", any("Lũy kế năm" in x for x in r["vi_pham"]), r)


def test_cli():
    print("test_cli")
    cli = os.path.join(GOC, "tools", "cong_cu.py")
    out = subprocess.run([sys.executable, cli, "--ds"], capture_output=True, text=True, timeout=60)
    kiem("--ds liệt kê công cụ", out.returncode == 0 and "tinh_luong_lam_them" in out.stdout, out.stderr[-300:])
    out = subprocess.run([sys.executable, cli, "khong_co"], capture_output=True, text=True, timeout=60)
    kiem("Công cụ không có → JSON lỗi, không traceback", '"loi"' in out.stdout and "Traceback" not in out.stderr, out.stderr[-300:])
    out = subprocess.run([sys.executable, cli, "phep_nam", "ngay_bat_dau=abc", "nam=2026"], capture_output=True, text=True, timeout=60)
    kiem("Ngày sai định dạng → JSON lỗi", '"loi"' in out.stdout and "Traceback" not in out.stderr, out.stdout[-300:])


if __name__ == "__main__":
    for f in [test_kiem_tra_tham_so, test_chong_ghi_de, test_csv_an_toan, test_luong_lam_them, test_kiem_tra_gio, test_cli]:
        f()
    print("KẾT QUẢ:", "TẤT CẢ ĐẠT" if not LOI else f"{len(LOI)} LỖI: {LOI}")
    sys.exit(1 if LOI else 0)
