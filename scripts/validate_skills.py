#!/usr/bin/env python3
"""Kiểm cấu trúc bộ skill trước khi merge. Chỉ dùng thư viện chuẩn, Python 3.9+.

    python3 scripts/validate_skills.py

Kiểm:
- mỗi skills/<tên>/SKILL.md có frontmatter name (trùng tên thư mục) và description (1–1024 ký tự), thân dưới 500 dòng;
- mọi đường dẫn tương đối nhắc trong SKILL.md và references (../wealbee-data/..., references/..., link Markdown) tồn tại;
- plugin.json, marketplace.json đọc được, cùng phiên bản với wealbee.py;
- eval: case.yaml có schema_version "1.1", name trùng thư mục, có prompt.md và ít nhất một grader đúng khuôn;
- không có khoá Wealbee lộ trong file nào.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

GOC = Path(__file__).resolve().parent.parent
SKILLS = GOC / "skills"
loi: list[str] = []


def bao(p: Path, msg: str) -> None:
    loi.append(f"{p.relative_to(GOC)}: {msg}")


def frontmatter(text: str) -> tuple[dict, str] | None:
    m = re.match(r"^---\n(.*?)\n---\n(.*)$", text, re.S)
    if not m:
        return None
    meta = {}
    for dong in m.group(1).splitlines():
        if ":" in dong and not dong.startswith(" "):
            k, v = dong.split(":", 1)
            meta[k.strip()] = v.strip()
    return meta, m.group(2)


def kiem_duong_dan(p: Path, text: str) -> None:
    """Đường dẫn trong `...` hoặc link Markdown ](...) phải tồn tại, tính từ thư mục của file."""
    ngoai_khoi_ma = re.sub(r"```.*?```", "", text, flags=re.S)   # link trong khuôn mẫu (```) là chỗ trống, không kiểm
    ung_vien = set(re.findall(r"\]\(([^)\s]+)\)", ngoai_khoi_ma))
    ung_vien |= set(re.findall(r"`((?:\.\./|references/|scripts/)[^`\s]+)`", text))
    for u in ung_vien:
        if re.match(r"^(https?:|mailto:|#)", u) or "<" in u:
            continue
        duong = u.split("#", 1)[0]
        if duong and not (p.parent / duong).exists():
            bao(p, f"đường dẫn không tồn tại: {u}")


def kiem_skill(d: Path) -> None:
    f = d / "SKILL.md"
    if not f.exists():
        return bao(d, "thiếu SKILL.md")
    text = f.read_text(encoding="utf-8")
    fm = frontmatter(text)
    if fm is None:
        return bao(f, "thiếu frontmatter --- name/description ---")
    meta, than = fm
    if meta.get("name") != d.name:
        bao(f, f"name '{meta.get('name')}' khác tên thư mục '{d.name}'")
    if not re.fullmatch(r"[a-z0-9]+(-[a-z0-9]+)*", d.name or ""):
        bao(f, "tên skill chỉ gồm chữ thường, số, gạch nối")
    mo_ta = meta.get("description", "")
    if not (1 <= len(mo_ta) <= 1024):
        bao(f, f"description dài {len(mo_ta)} ký tự (cần 1–1024)")
    if len(than.splitlines()) > 500:
        bao(f, f"thân SKILL.md {len(than.splitlines())} dòng (nên dưới 500)")
    kiem_duong_dan(f, than)
    for r in (d / "references").glob("*.md"):
        kiem_duong_dan(r, r.read_text(encoding="utf-8"))
    for case in sorted((d / "evals").glob("*/")) if (d / "evals").exists() else []:
        kiem_eval(case)


def kiem_eval(case: Path) -> None:
    if case.name in {"results", "mocks", "node_modules", "files", "true", "false", "null"}:
        return
    y = case / "case.yaml"
    if not y.exists():
        return bao(case, "thiếu case.yaml")
    t = y.read_text(encoding="utf-8")
    if not re.search(r'^schema_version:\s*"1\.1"\s*$', t, re.M):
        bao(y, 'cần schema_version: "1.1" (có ngoặc kép)')
    m = re.search(r"^name:\s*(\S+)\s*$", t, re.M)
    if not m or m.group(1) != case.name:
        bao(y, "name phải trùng tên thư mục case")
    pm = case / "prompt.md"
    if not pm.exists():
        bao(case, "thiếu prompt.md")
    else:
        fm = frontmatter(pm.read_text(encoding="utf-8"))
        if fm is None or not fm[1].strip():
            bao(pm, "cần khối thiết lập --- ... --- rồi tới câu hỏi")
        else:
            la = set(fm[0]) - {"tags", "max_turns", "timeout_seconds", "allowed_tools"}
            if la:
                bao(pm, f"khoá lạ trong khối thiết lập: {sorted(la)}")
    graders = sorted((case / "graders").glob("*.md"))
    if not graders:
        bao(case, "cần ít nhất một grader trong graders/")
    for g in graders:
        if not re.fullmatch(r"\d{2}-[a-z0-9-]+\.md", g.name):
            bao(g, "tên grader dạng NN-vai-tu.md")
        fm = frontmatter(g.read_text(encoding="utf-8"))
        if fm is None or "type" not in fm[0] or not fm[1].strip():
            bao(g, "grader cần khối type/focus/weight và một câu kiểm")


def kiem_plugin() -> None:
    try:
        plugin = json.loads((GOC / ".claude-plugin" / "plugin.json").read_text(encoding="utf-8"))
        cho = json.loads((GOC / ".claude-plugin" / "marketplace.json").read_text(encoding="utf-8"))
    except (OSError, ValueError) as e:
        return loi.append(f".claude-plugin: {e}")
    m = re.search(r'^PHIEN_BAN = "([^"]+)"', (SKILLS / "wealbee-data" / "scripts" / "wealbee.py").read_text(encoding="utf-8"), re.M)
    ban = {plugin.get("version"), m and m.group(1)} | {p.get("version") for p in cho.get("plugins", []) if p.get("name") == plugin.get("name")}
    if len(ban) != 1:
        loi.append(f"phiên bản lệch nhau giữa plugin.json, marketplace.json, wealbee.py: {sorted(map(str, ban))}")
    if not any(p.get("name") == plugin.get("name") for p in cho.get("plugins", [])):
        loi.append("marketplace.json chưa liệt kê plugin trong plugin.json")


def quet_khoa() -> None:
    mau = re.compile(r"wb_(?:live|test)_[A-Za-z0-9]{12,}")
    for f in GOC.rglob("*"):
        if f.is_file() and ".git" not in f.parts and f.suffix in {".md", ".py", ".json", ".yaml", ".yml", ".txt", ".csv", ".env", ""}:
            try:
                if mau.search(f.read_text(encoding="utf-8", errors="ignore")):
                    bao(f, "có chuỗi giống khoá Wealbee: xoá và đổi khoá ngay")
            except OSError:
                pass


def main() -> int:
    ds = sorted(d for d in SKILLS.iterdir() if d.is_dir())
    for d in ds:
        kiem_skill(d)
    kiem_plugin()
    kiem_duong_dan(GOC / "README.md", (GOC / "README.md").read_text(encoding="utf-8"))
    quet_khoa()
    if loi:
        print(f"{len(loi)} lỗi:")
        print("\n".join(f"  - {x}" for x in loi))
        return 1
    so_eval = sum(1 for _ in SKILLS.glob("*/evals/*/case.yaml"))
    print(f"OK: {len(ds)} skill, {so_eval} eval, plugin hợp lệ, không thấy khoá lộ.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
