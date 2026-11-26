#!/usr/bin/env python3
"""Đồng bộ bản vn-custom: chép shared/*.md và tools/ vào từng skill rồi kiểm tra – KHÔNG sinh lại .mcp.json, dist/, chatgpt/, openai/.

Chạy từ gốc repo:  python3 custom/dong_bo.py
(Dùng lại hàm dong_bo() và kiem_tra() của scripts/build.py upstream; không gọi ket_noi.py để không khai báo lại connector.)
"""
import sys
from pathlib import Path

GOC = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(GOC / "scripts"))
import build  # noqa: E402

build.dong_bo()
loi = build.kiem_tra()
mcp = (GOC / ".mcp.json").read_text(encoding="utf-8")
if '"mcpServers": {}' not in mcp.replace("\n", "").replace("  ", ""):
    loi.append(".mcp.json không còn rỗng – bản vn-custom không khai báo MCP server")
print(f"Đã đồng bộ {len(build.ds_skill())} skill.")
if loi:
    print("LỖI:\n" + "\n".join("  - " + x for x in loi))
    raise SystemExit(1)
