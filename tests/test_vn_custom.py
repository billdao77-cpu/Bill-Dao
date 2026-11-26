"""Test cho các thay đổi của nhánh vn-custom (plugin phapche-hopdong). Chạy: python3 tests/test_vn_custom.py"""
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


def test_tham_so():
    print("test_tham_so")
    r = goi("kiem_tra_phat_vi_pham", {"gia_tri_phan_nghia_vu_vi_pham": 1e9, "ty_le_phat_phan_tram": 10, "x": 1})
    kiem("Tham số lạ bị từ chối", r.get("tham_so_khong_ho_tro") == ["x"], r)
    r = goi("kiem_tra_phat_vi_pham", {"gia_tri_phan_nghia_vu_vi_pham": 1e9, "ty_le_phat_phan_tram": 10, "loai_hop_dong": "abc"})
    kiem("Giá trị ngoài enum bị từ chối", bool(r.get("gia_tri_khong_hop_le")), r)


def test_chong_ghi_de():
    print("test_chong_ghi_de")
    with tempfile.TemporaryDirectory() as d:
        goc = os.path.join(d, "gop-y.docx")
        tham = {"duong_dan_ra": goc, "ten_hop_dong": "HĐ dịch vụ", "ben_toi": "Công ty A", "doi_tac": "Công ty B",
                "thay_doi": [{"dieu": "Điều 1", "quyet_dinh": "chap_nhan", "ban_moi": "x"}]}
        r1 = goi("bang_gop_y_hop_dong", dict(tham))
        kiem("Tạo 2 file góp ý lần đầu", "file_gui_doi_tac" in r1 and os.path.exists(r1["file_gui_doi_tac"]), r1)
        r2 = goi("bang_gop_y_hop_dong", dict(tham))
        kiem("Lần 2 không ghi đè file gửi đối tác/nội bộ", "loi" in r2 and len(r2.get("duong_dan", [])) == 2, r2)
        r3 = goi("bang_gop_y_hop_dong", dict(tham, ghi_de=True))
        kiem("ghi_de=true thì cho ghi", "file_gui_doi_tac" in r3, r3)
        r4 = goi("bang_gop_y_hop_dong", dict(tham, duong_dan_ra=os.path.join(d, "x.txt")))
        kiem("Sai đuôi .docx bị từ chối", "loi" in r4, r4)
        f = os.path.join(d, "lich.ics")
        open(f, "w").write("GOC")
        r5 = goi("tao_file_ics", {"duong_dan_ra": f, "su_kien": [{"ngay": "2026-12-01", "ten": "Hết hạn HĐ"}]})
        kiem("tao_file_ics không ghi đè", "loi" in r5 and open(f).read() == "GOC", r5)


def test_csv():
    print("test_csv")
    with tempfile.TemporaryDirectory() as d:
        goi("them_hop_dong_vao_so", {"so_hop_dong": "01/2026/HĐ", "ten_hop_dong": "+x", "doi_tac": "=HYPERLINK(\"http://x\")",
                                     "ngay_ky": "01/11/2026", "thu_muc": d})
        dong = open(os.path.join(d, "so-theo-doi-hop-dong.csv"), encoding="utf-8-sig").read().splitlines()[1]
        kiem("Sổ hợp đồng vô hiệu hóa ô = và +", ",'+x," in dong and ",\"'=HYPERLINK" in dong, dong)
        r = goi("them_hop_dong_vao_so", {"so_hop_dong": "02/2026/HĐ", "ten_hop_dong": "b", "doi_tac": "C",
                                         "ngay_ky": "02/11/2026", "thu_muc": d})
        kiem("Ghi tiếp sau khi làm sạch", r.get("da_them") == "HD0002", r)


def test_an_phi_va_phat():
    print("test_an_phi_va_phat")
    r = goi("an_phi_so_tham", {"gia_tri_tranh_chap": 50_000_000})
    kiem("Tạm ứng KDTM tối thiểu 3.000.000", r["tam_ung_an_phi_uoc_tinh"] == "3.000.000 đ", r)
    r = goi("an_phi_so_tham", {"gia_tri_tranh_chap": 1_000_000_000})
    kiem("Tạm ứng KDTM 1 tỷ = 50% × 42tr = 21tr", r["tam_ung_an_phi_uoc_tinh"] == "21.000.000 đ", r)
    r = goi("an_phi_so_tham", {"gia_tri_tranh_chap": 3_000_000, "loai": "dan_su"})
    kiem("Tạm ứng dân sự tối thiểu 300.000", r["tam_ung_an_phi_uoc_tinh"] == "300.000 đ", r)
    r = goi("kiem_tra_phat_vi_pham", {"gia_tri_phan_nghia_vu_vi_pham": 1e9, "ty_le_phat_phan_tram": 10})
    kiem("Phạt 10% thương mại vượt trần 8% + cảnh báo luật sửa đổi", r["hop_le"] is False and "01/7/2027" in r["canh_bao_luat_moi"], r)


def test_rui_ro():
    print("test_rui_ro")
    r = goi("danh_gia_rui_ro", {"ben_nguoi_dung": "Bên mua", "danh_sach": [
        {"dieu": "Điều 9", "rui_ro": "Miễn trừ trách nhiệm tuyệt đối cho bên bán", "kha_nang": 4, "anh_huong": 5},
        {"dieu": "Điều 3", "rui_ro": "Thanh toán trước 100%", "kha_nang": 3, "anh_huong": 4},
        {"dieu": "Điều 12", "rui_ro": "Chưa rõ ngôn ngữ ưu tiên", "kha_nang": 2, "anh_huong": 2},
        {"dieu": "Điều 7", "rui_ro": "Điều khoản vô hiệu ít khả năng phát sinh", "kha_nang": 1, "anh_huong": 5}]})
    muc = [x["muc_do"] for x in r["ket_qua"]]
    kiem("Sắp xếp và chấm 4 mức", muc == ["Nghiêm trọng", "Cao", "Cao", "Thấp"], muc)
    kiem("Ảnh hưởng 5 tối thiểu Cao", r["ket_qua"][2]["dieu"] == "Điều 7", r["ket_qua"])
    kiem("Có Nghiêm trọng → không nên ký", r["goi_y_ket_luan"].startswith("Không nên ký"), r)
    r = goi("danh_gia_rui_ro", {"danh_sach": [{"rui_ro": "x", "kha_nang": 7, "anh_huong": 1}]})
    kiem("Điểm ngoài 1–5 bị từ chối", "loi" in r, r)


def test_cli():
    print("test_cli")
    cli = os.path.join(GOC, "tools", "cong_cu.py")
    out = subprocess.run([sys.executable, cli, "--ds"], capture_output=True, text=True, timeout=60)
    kiem("--ds liệt kê công cụ", out.returncode == 0 and "danh_gia_rui_ro" in out.stdout, out.stderr[-300:])
    out = subprocess.run([sys.executable, cli, "lai_cham_tra", "so_tien_cham_tra=1000", "tu_ngay=abc", "den_ngay=01/01/2026"],
                         capture_output=True, text=True, timeout=60)
    kiem("Ngày sai → JSON lỗi, không traceback", '"loi"' in out.stdout and "Traceback" not in out.stderr, out.stdout[-300:])


if __name__ == "__main__":
    for f in [test_tham_so, test_chong_ghi_de, test_csv, test_an_phi_va_phat, test_rui_ro, test_cli]:
        f()
    print("KẾT QUẢ:", "TẤT CẢ ĐẠT" if not LOI else f"{len(LOI)} LỖI: {LOI}")
    sys.exit(1 if LOI else 0)
