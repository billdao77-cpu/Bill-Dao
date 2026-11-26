#!/usr/bin/env python3
"""Gọi công cụ từ dòng lệnh (dùng khi không có MCP, ví dụ skill chạy trên claude.ai).

    python3 scripts/cong_cu.py                      # liệt kê công cụ (hoặc --ds)
    python3 scripts/cong_cu.py --schema <ten_cong_cu> # xem tham số của một công cụ
    python3 scripts/cong_cu.py <ten_cong_cu> '{"tham_so": "gia_tri"}'
    python3 scripts/cong_cu.py <ten_cong_cu> tham_so=gia_tri tham_so2=gia_tri2
"""
import json
import os
import sys

_D = os.path.dirname(os.path.abspath(__file__))
sys.path[:0] = [_D, os.path.dirname(_D)]  # chạy được cả trong skill (scripts/tools) lẫn gốc repo (tools/)

import tools  # noqa: E402


def _gia_tri(v):
    try:
        return json.loads(v)
    except ValueError:
        return v


if __name__ == "__main__":
    if len(sys.argv) < 2 or sys.argv[1] == "--ds":
        for t in tools.tat_ca():
            print(f"{t['name']}: {t['description'][:110]}...")
        sys.exit(0)
    ten = sys.argv[1]
    if ten in ("-h", "--help"):
        print(__doc__)
        sys.exit(0)
    if ten == "--schema":
        t = next((x for x in tools.tat_ca() if len(sys.argv) > 2 and x["name"] == sys.argv[2]), None)
        print(json.dumps({"loi": "Không có công cụ này"} if t is None else
                         {"name": t["name"], "description": t["description"], "schema": t["schema"]},
                         ensure_ascii=False, indent=1))
        sys.exit(0 if t else 2)
    args = {}
    try:
        for a in sys.argv[2:]:
            if a.strip().startswith("{"):
                args.update(json.loads(a))
            elif "=" in a:
                k, v = a.split("=", 1)
                args[k] = _gia_tri(v)
        kq = tools.goi(ten, args)
    except KeyError as e:
        kq = {"loi": str(e).strip('"'), "goi_y": "Chạy với --ds để xem danh sách công cụ"}
    except (TypeError, ValueError) as e:  # dữ liệu đầu vào sai kiểu/định dạng (ngày, số...)
        kq = {"loi": f"Dữ liệu đầu vào không hợp lệ: {e}", "goi_y": f"Xem tham số: --schema {ten}"}
    print(json.dumps(kq, ensure_ascii=False, indent=1, default=str))
