"""Test cho nhánh vn-custom (20skill-van-phong). Chạy: python3 tests/test_vn_custom.py"""
import json
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


def chay(*a, cwd=None):
    return subprocess.run([sys.executable, *map(str, a)], capture_output=True, text=True, timeout=180, cwd=cwd)


def cong_thuc(path):
    from openpyxl import load_workbook
    return [(c.coordinate, c.data_type, c.value) for ws in load_workbook(path).worksheets for r in ws.iter_rows()
            for c in r if isinstance(c.value, str) and c.value.startswith("=")]


def test_an_toan():
    print("test_an_toan")
    r = chay(GOC / "shared/scripts/an_toan.py")
    kiem("doctest an_toan.py", "self-test OK" in r.stdout, r.stdout + r.stderr)


def test_lam_sach():
    print("test_lam_sach")
    sc = S / "bang-excel/scripts/lam_sach.py"
    with tempfile.TemporaryDirectory() as d:
        vao = Path(d) / "khach.csv"
        vao.write_text('ho ten,sdt,ghi chu\nnguyễn văn a,+84912345678,"=HYPERLINK(""http://attacker.example"",""x"")"\n'
                       'nguyễn văn a,+84912345678,"=HYPERLINK(""http://attacker.example"",""x"")"\n', encoding="utf-8")
        ra = Path(d) / "sach.xlsx"
        r = chay(sc, vao, ra)
        ct = cong_thuc(ra) if ra.exists() else []
        kiem("Ô =HYPERLINK trong dữ liệu khách thành chữ", ra.exists() and ct and all(c[1] == "s" for c in ct), (r.stderr, ct))
        kiem("Có cảnh báo", "CẢNH BÁO" in r.stderr, r.stderr)
        r2 = chay(sc, vao, ra)
        kiem("Không ghi đè file kết quả", r2.returncode == 2, r2.stderr)
        x = Path(d) / "x.xlsx"
        x.write_bytes(ra.read_bytes())
        r3 = chay(sc, x, x, "--ghi-de")
        kiem("Không ghi đè chính file nguồn kể cả có --ghi-de", r3.returncode == 2 and "trùng file nguồn" in r3.stderr, r3.stderr)
        from openpyxl import load_workbook
        ws = load_workbook(ra)["Du_lieu_sach"]
        kiem("Chức năng gốc: chuẩn hóa SĐT +84 → 0", ws["B2"].value == "0912345678", ws["B2"].value)


def test_pdf():
    print("test_pdf")
    sc = S / "xu-ly-pdf/scripts/pdf_tool.py"
    with tempfile.TemporaryDirectory() as d:
        try:
            from docx import Document
        except ImportError:
            kiem("python-docx có sẵn", False)
            return
        doc = Document()
        t = doc.add_table(rows=2, cols=2)
        t.style = "Table Grid"  # có đường kẻ để pdfplumber nhận bảng
        t.cell(0, 0).text, t.cell(0, 1).text = "Tên", "Ghi chú"
        t.cell(1, 0).text, t.cell(1, 1).text = "A", '=HYPERLINK("http://attacker.example","x")'
        doc.save(Path(d) / "bang.docx")
        subprocess.run(["soffice", "--headless", "--convert-to", "pdf", "--outdir", d, str(Path(d) / "bang.docx")],
                       capture_output=True, timeout=120)
        pdf = Path(d) / "bang.pdf"
        if not pdf.exists():
            kiem("Tạo PDF mẫu bằng LibreOffice", False, "không có soffice")
            return
        ra = Path(d) / "bang.xlsx"
        r = chay(sc, "bang", pdf, ra)
        ct = cong_thuc(ra) if ra.exists() else []
        kiem("Bảng PDF có =HYPERLINK → ô chữ", ra.exists() and all(c[1] == "s" for c in ct), (r.stdout + r.stderr, ct))
        r = chay(sc, "trich", pdf, pdf, "1")
        kiem("trich không ghi đè chính file nguồn", r.returncode == 2, r.stderr)
        r = chay(sc, "trich", pdf, Path(d) / "t1.pdf", "1")
        kiem("trich ra file mới", r.returncode == 0 and (Path(d) / "t1.pdf").exists(), r.stderr)
        r = chay(sc, "trich", pdf, Path(d) / "t1.pdf", "1")
        kiem("trich không ghi đè kết quả cũ", r.returncode == 2, r.stderr)
        r = chay(sc, "tach", pdf, Path(d) / "tach")
        r2 = chay(sc, "tach", pdf, Path(d) / "tach")
        kiem("tach lần 2 không ghi đè trang đã tách", r.returncode == 0 and r2.returncode == 2, r2.stderr)


def test_tcvn3():
    print("test_tcvn3")
    sc = S / "chuyen-doi-file/scripts/tcvn3_to_unicode.py"
    with tempfile.TemporaryDirectory() as d:
        f = Path(d) / "a.txt"
        f.write_text("Céng hoµ", encoding="latin-1")
        r = chay(sc, f, f)
        kiem("Không ghi đè file nguồn", r.returncode == 2 and f.read_text(encoding="latin-1") == "Céng hoµ", r.stderr)
        r = chay(sc, f, Path(d) / "b.txt")
        kiem("Chuyển ra file mới", r.returncode == 0 and (Path(d) / "b.txt").exists(), r.stderr)


def test_cau_truc():
    print("test_cau_truc")
    mk = json.loads((GOC / ".claude-plugin/marketplace.json").read_text())
    kiem("Marketplace có 2 plugin", [p["name"] for p in mk["plugins"]] == ["van-phong", "van-phong-mo-rong"], mk["plugins"])
    lo = set(p.name for p in S.iterdir() if p.is_dir()) & set(p.name for p in (GOC / "mo-rong/skills").iterdir())
    kiem("Không có skill nằm ở cả 2 plugin", not lo, lo)
    kiem("Không có .mcp.json", not (GOC / ".mcp.json").exists() and not (GOC / "mo-rong/.mcp.json").exists())
    for a in sorted((GOC / "agents").glob("*.md")) if (GOC / "agents").exists() else []:
        tools = next((l for l in a.read_text(encoding="utf-8").splitlines() if l.startswith("tools:")), "")
        kiem(f"agent {a.stem}: không có Write/Edit", tools and "Write" not in tools and "Edit" not in tools, tools)


if __name__ == "__main__":
    for f in [test_an_toan, test_lam_sach, test_pdf, test_tcvn3, test_cau_truc]:
        f()
    print("KẾT QUẢ:", "TẤT CẢ ĐẠT" if not LOI else f"{len(LOI)} LỖI: {LOI}")
    sys.exit(1 if LOI else 0)
