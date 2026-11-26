#!/usr/bin/env python3
"""Đồng bộ bản vn-custom: chép shared/* vào references/ (theo SHARED_MAP của upstream) và shared/scripts/an_toan.py vào
scripts/ của mọi skill có script, rồi kiểm tra – KHÔNG sinh lại .mcp.json, marketplace, dist/, bản ChatGPT.
Chạy từ gốc repo: python3 custom/dong_bo.py
"""
import shutil
import sys
from pathlib import Path

GOC = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(GOC / "scripts"))
import build  # noqa: E402

THEM = {}  # skill mới của bản vn-custom: {"ten-skill": [file shared]}
for k, v in THEM.items():
    build.SHARED_MAP.setdefault(k, v)
for f in ["the-skill.md"]:
    if (GOC / "shared" / f).exists() and f not in build.CHUNG:
        build.CHUNG.append(f)
build.dong_bo()
for sc in sorted((GOC / "skills").glob("*/scripts")):
    shutil.copy(GOC / "shared" / "scripts" / "an_toan.py", sc / "an_toan.py")
loi = list(build.kiem_tra())
mcp = (GOC / ".mcp.json").read_text(encoding="utf-8")
if '"mcpServers": {}' not in mcp.replace("\n", "").replace("  ", ""):
    loi.append(".mcp.json không còn rỗng – bản vn-custom không khai báo MCP server")
print(f"Đã đồng bộ {len(build.ds_skill())} skill.")
if loi:
    print("LỖI:\n" + "\n".join("  - " + str(x) for x in loi))
    raise SystemExit(1)
