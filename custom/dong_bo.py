#!/usr/bin/env python3
"""Đồng bộ bản vn-custom: chép shared/*.md (gồm the-skill.md) và vn_money.py vào từng skill rồi kiểm tra –
KHÔNG sinh lại .mcp.json, marketplace, dist/, bản ChatGPT. Chạy từ gốc repo: python3 custom/dong_bo.py
"""
import sys
from pathlib import Path

GOC = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(GOC / "scripts"))
import build  # noqa: E402

if "the-skill.md" not in build.SHARED_MD:
    build.SHARED_MD.append("the-skill.md")
build.dong_bo()
loi = list(build.kiem_tra()) if hasattr(build, "kiem_tra") else []
mcp = (GOC / ".mcp.json").read_text(encoding="utf-8")
if '"mcpServers": {}' not in mcp.replace("\n", "").replace("  ", ""):
    loi.append(".mcp.json không còn rỗng – bản vn-custom không khai báo MCP server")
print(f"Đã đồng bộ {len(build.ds_skill())} skill.")
if loi:
    print("LỖI:\n" + "\n".join("  - " + str(x) for x in loi))
    raise SystemExit(1)
