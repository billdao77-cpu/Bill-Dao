"""Test cho các thay đổi của nhánh vn-custom (skill-sales-marketing). Chạy: python3 tests/test_vn_custom.py"""
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


def chay(*args):
    return subprocess.run([sys.executable, *map(str, args)], capture_output=True, text=True, timeout=120)


def test_tao_pipeline():
    print("test_tao_pipeline")
    sc = S / "quy-trinh-ban-hang-crm/scripts/tao_pipeline.py"
    with tempfile.TemporaryDirectory() as d:
        f = Path(d) / "pipeline.xlsx"
        r = chay(sc, "--mo-hinh", "b2b", "--ra", f, "--sales", "An,=HYPERLINK(\"http://x\")")
        kiem("Tạo file mới", r.returncode == 0 and f.exists(), r.stderr)
        from openpyxl import load_workbook
        vals = [c.value for ws in load_workbook(f).worksheets for row in ws.iter_rows() for c in row if isinstance(c.value, str)]
        kiem("Tên sales bắt đầu bằng = không thành công thức", any(v.startswith("'=HYPERLINK") for v in vals)
             and not any(v.startswith("=HYPERLINK") for v in vals), [v for v in vals if "HYPERLINK" in v])
        truoc = f.read_bytes()
        r = chay(sc, "--mo-hinh", "b2b", "--ra", f)
        kiem("Không ghi đè file đã có", r.returncode == 2 and f.read_bytes() == truoc, r.stderr)
        r = chay(sc, "--mo-hinh", "b2b", "--ra", f, "--ghi-de")
        kiem("--ghi-de thì cho ghi", r.returncode == 0, r.stderr)
        r = chay(sc, "--mo-hinh", "b2b", "--ra", Path(d) / "x.csv")
        kiem("Sai đuôi bị từ chối", r.returncode == 2, r.stderr)


def test_bang_cai():
    print("test_bang_cai_khuyen_mai")
    sc = S / "gia-san-pham-khuyen-mai/scripts/bang_cai_khuyen_mai.py"
    with tempfile.TemporaryDirectory() as d:
        ct = Path(d) / "ct.json"
        ct.write_text(json.dumps({"ten_chuong_trinh": "T", "loi_nhuan_muc_tieu": "10%", "san_pham": [
            {"sku": "A", "ten": "Serum", "gia_ban": 450000, "gia_von": 135000, "phi": ["phí cố định=10%"], "giam": "10%"}]}),
            encoding="utf-8")
        ra = Path(d) / "bang.docx"
        r = chay(sc, ct, "--ra", ra)
        kiem("Tạo bảng cài mới", r.returncode == 0 and ra.exists(), r.stderr)
        r = chay(sc, ct, "--ra", ra)
        kiem("Không ghi đè bảng cài đã có", r.returncode == 2, r.stderr)
        r = chay(sc, "--self-test")
        kiem("Self-test upstream vẫn đạt", "self-test OK" in r.stdout, r.stdout + r.stderr)


def test_validate_fix():
    print("test_validate_copy_fix")
    sc = S / "kiem-tra-phap-ly-quang-cao/scripts/validate_copy.py"
    with tempfile.TemporaryDirectory() as d:
        f = Path(d) / "bai.md"
        goc = "Sản phẩm tốt.\n"  # chữ tổ hợp (NFD) cố ý
        f.write_text(goc, encoding="utf-8")
        chay(sc, f, "--fix")
        kiem("--fix không sửa file gốc", f.read_text(encoding="utf-8") == goc)
        moi = Path(d) / "bai.nfc.md"
        import unicodedata
        kiem("--fix ghi bản .nfc mới đã chuẩn hóa", moi.exists() and moi.read_text(encoding="utf-8")
             == unicodedata.normalize("NFC", goc))


def test_cau_hinh():
    print("test_cau_hinh")
    kiem(".mcp.json rỗng", json.loads((GOC / ".mcp.json").read_text())["mcpServers"] == {})
    for a in sorted((GOC / "agents").glob("*.md")):
        t = a.read_text(encoding="utf-8")
        tools = next((l for l in t.splitlines() if l.startswith("tools:")), "")
        kiem(f"agent {a.stem}: không có Write/Edit", tools and "Write" not in tools and "Edit" not in tools, tools)
    for s in sorted(S.glob("*/references")):
        kiem(f"{s.parent.name}: có the-skill.md", (s / "the-skill.md").exists())


if __name__ == "__main__":
    for f in [test_tao_pipeline, test_bang_cai, test_validate_fix, test_cau_hinh]:
        f()
    print("KẾT QUẢ:", "TẤT CẢ ĐẠT" if not LOI else f"{len(LOI)} LỖI: {LOI}")
    sys.exit(1 if LOI else 0)
