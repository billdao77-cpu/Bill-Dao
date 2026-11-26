#!/usr/bin/env python3
"""Đồng bộ bản vn-custom cho 2 plugin (skills/ và mo-rong/skills/): chép shared/*.md, doc_so.py theo quy tắc của
scripts/build.py upstream, và shared/scripts/an_toan.py vào mọi thư mục scripts/ – KHÔNG sinh lại marketplace, dist/, chatgpt/.
Chạy từ gốc repo: python3 custom/dong_bo.py
"""
import re
import shutil
import sys
from pathlib import Path

GOC = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(GOC / "scripts"))
import build  # noqa: E402

loi = []
for thu_muc in (GOC / "skills", GOC / "mo-rong" / "skills"):
    build.SKILLS = thu_muc
    build.dong_bo()
    for sk in sorted(p for p in thu_muc.iterdir() if p.is_dir()):
        if (GOC / "shared" / "the-skill.md").exists():
            shutil.copy(GOC / "shared" / "the-skill.md", sk / "references")
        if (sk / "scripts").exists():
            shutil.copy(GOC / "shared" / "scripts" / "an_toan.py", sk / "scripts")
        text = (sk / "SKILL.md").read_text(encoding="utf-8")
        m = re.match(r"^---\n(.*?)\n---\n", text, re.S)
        meta = dict(re.findall(r"^(\w+):\s*(.*)$", m.group(1), re.M)) if m else {}
        if meta.get("name") != sk.name:
            loi.append(f"{sk.name}: name trong frontmatter không khớp thư mục")
        if not 50 < len(meta.get("description", "")) <= 1024:
            loi.append(f"{sk.name}: description dài {len(meta.get('description', ''))} ký tự")
        for ref in re.findall(r"`((?:references|scripts)/[\w./-]+)`", text):
            if not (sk / ref).exists():
                loi.append(f"{sk.name}: thiếu {ref}")
print("Đã đồng bộ:", ", ".join(f"{d.parent.name if d.parent != GOC else ''}/{d.name}" for d in
                               (GOC / "skills", GOC / "mo-rong" / "skills")))
if loi:
    print("LỖI:\n" + "\n".join("  - " + x for x in loi))
    raise SystemExit(1)
