#!/usr/bin/env python3
"""Audit the study vault and print a JSON summary (read-only).

Usage: python3 scripts/vault-audit.py [vault-root]   (defaults to the repo root)
Exit status 1 when a check fails:
  - a wiki-link that resolves to no note (fenced and inline code are ignored)
  - a tech/<domain>/<slug> study not linked from its MOC (MOCs/Index.md: Maintenance)
  - a folder under tech/<domain>/ without a README.md
  - a note without frontmatter (the repository README is exempt)
  - a study folder named after a URL or a request sentence
"""
import json
import os
import re
import sys
from collections import Counter, defaultdict

ROOT = os.path.abspath(sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(__file__), ".."))
LINK = re.compile(r"(?<!!)\[\[([^\]|#]+?)\\?(?:#[^\]|]*)?(?:\\?\|[^\]]*)?\]\]")
FENCE = re.compile(r"```.*?```", re.S)
INLINE = re.compile(r"`[^`\n]*`")
ODD_NAME = re.compile(r"^(https?-|www-)|(해줘|알려줘|확인해|싶어|이거|어떤)")


def prose(text):
    return INLINE.sub("", FENCE.sub("", text))


notes = {}
for dp, dn, fn in os.walk(ROOT):
    dn[:] = [d for d in dn if d not in {".git", ".obsidian", "scripts"}]
    for f in fn:
        if f.endswith(".md"):
            rel = os.path.relpath(os.path.join(dp, f), ROOT)
            with open(os.path.join(dp, f), encoding="utf-8", errors="replace") as fh:
                notes[rel] = fh.read()

by_path = {p[:-3] for p in notes}
by_base = defaultdict(list)
for p in notes:
    by_base[os.path.basename(p)[:-3]].append(p)


def resolves(target, src):
    t = target.strip()
    t = t[:-3] if t.endswith(".md") else t
    if t in by_path:
        return True
    if os.path.normpath(os.path.join(os.path.dirname(src), t)) in by_path:
        return True
    if "/" not in t:
        return bool(by_base.get(t))
    return len([q for q in by_path if q.endswith("/" + t)]) == 1


broken = [(p, m.group(1)) for p, text in notes.items() for m in LINK.finditer(prose(text)) if not resolves(m.group(1), p)]

studies = defaultdict(set)
no_readme, odd = [], []
for domain in sorted(os.listdir(os.path.join(ROOT, "tech"))):
    for name in sorted(os.listdir(os.path.join(ROOT, "tech", domain))):
        full = os.path.join(ROOT, "tech", domain, name)
        slug = name[:-3] if name.endswith(".md") else name
        studies[domain].add(slug)
        if os.path.isdir(full) and not os.path.exists(os.path.join(full, "README.md")):
            no_readme.append(f"tech/{domain}/{name}")
        if ODD_NAME.search(name):
            odd.append(f"tech/{domain}/{name}")

mocs = "\n".join(text for p, text in notes.items() if p.startswith("MOCs/"))
unlinked = sorted(f"tech/{d}/{s}" for d, names in studies.items() for s in names if f"tech/{d}/{s}" not in mocs)
no_frontmatter = sorted(p for p, text in notes.items() if not text.startswith("---") and p != "README.md")
status = Counter()
for text in notes.values():
    m = re.search(r"^status:\s*(.+)$", text.split("\n---", 1)[0], re.M) if text.startswith("---") else None
    status[m.group(1).strip() if m else "<none>"] += 1

report = {
    "notes": len(notes),
    "studies": {d: len(s) for d, s in sorted(studies.items())},
    "broken_links": broken,
    "unlinked_from_moc": unlinked,
    "folders_without_readme": no_readme,
    "notes_without_frontmatter": no_frontmatter,
    "odd_folder_names": odd,
    "status": dict(status),
}
report["ok"] = not (broken or unlinked or no_readme or no_frontmatter or odd)
print(json.dumps(report, ensure_ascii=False, indent=1))
sys.exit(0 if report["ok"] else 1)
