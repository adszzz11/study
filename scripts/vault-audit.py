#!/usr/bin/env python3
"""Audit the study vault and print a JSON summary (read-only).

Usage: python3 scripts/vault-audit.py [vault-root]   (defaults to the repo root)
Exit status 1 when a check fails:
  - a wiki-link or relative markdown link that resolves to no note
    (fenced and inline code are ignored)
  - an embed (![[...]]) whose file is not in the vault
  - a tech/<domain>/<slug> study not linked from its MOC (MOCs/Index.md: Maintenance)
  - a folder under tech/<domain>/ without a README.md
  - a note without frontmatter, or without `status:` (the repository README is exempt)
  - a note no other note links to (Home.md, the repository README and Templates are exempt)
  - a study folder named after a URL or a request sentence
  - a study slug or alias used by two folders (morae's comment loopback finds a study by slug)
Tests: python3 scripts/test_vault_audit.py
"""
import json
import os
import re
import sys
from collections import Counter, defaultdict

SKIP_DIRS = {".git", ".obsidian", "scripts"}
WIKI = re.compile(r"(?<!!)\[\[([^\]|#]+?)\\?(?:#[^\]|]*)?(?:\\?\|[^\]]*)?\]\]")
EMBED = re.compile(r"!\[\[([^\]|#]+?)(?:#[^\]|]*)?(?:\|[^\]]*)?\]\]")
MDLINK = re.compile(r"(?<!!)\[[^\]]*\]\(([^)\s#]+)(?:#[^)]*)?\)")
FENCE = re.compile(r"```.*?```", re.S)
INLINE = re.compile(r"`[^`\n]*`")
FRONTMATTER = re.compile(r"\A---\n(.*?)\n---(?:\n|\Z)", re.S)
ODD_NAME = re.compile(r"^(https?-|www-)|(해줘|알려줘|확인해|싶어|이거|어떤)")
ORPHAN_EXEMPT = {"README.md", "Home.md"}


def prose(text):
    return INLINE.sub("", FENCE.sub("", text))


def frontmatter(text):
    m = FRONTMATTER.match(text)
    return m.group(1) if m else None


def frontmatter_field(fm, name):
    m = re.search(rf"^{name}:\s*(.*?)\s*$", fm or "", re.M)
    return m.group(1) if m else None


def frontmatter_list(fm, name):
    """Values of a YAML list field, inline (`[a, b]`) or block (`- a`)."""
    m = re.search(rf"^{name}:[ \t]*(.*)$", fm or "", re.M)
    if not m:
        return []
    inline = m.group(1).strip()
    if inline.startswith("["):
        return [v.strip().strip("'\"") for v in inline.strip("[]").split(",") if v.strip()]
    if inline:
        return [inline.strip("'\"")]
    values = []
    for line in (fm or "")[m.end():].lstrip("\n").splitlines():
        lm = re.match(r"^\s+-\s+(.+?)\s*$", line)
        if not lm:
            break
        values.append(lm.group(1).strip("'\""))
    return values


class Vault:
    def __init__(self, root):
        self.root = os.path.abspath(root)
        self.notes = {}
        self.files = set()
        for dp, dn, fn in os.walk(self.root):
            dn[:] = [d for d in dn if d not in SKIP_DIRS]
            for f in fn:
                rel = os.path.relpath(os.path.join(dp, f), self.root)
                if f.endswith(".md"):
                    with open(os.path.join(dp, f), encoding="utf-8", errors="replace") as fh:
                        self.notes[rel] = fh.read()
                else:
                    self.files.add(rel)
        self.by_path = {p[:-3] for p in self.notes}
        self.by_base = defaultdict(list)
        for p in self.notes:
            self.by_base[os.path.basename(p)[:-3]].append(p[:-3])
        self.file_base = defaultdict(list)
        for p in self.files:
            self.file_base[os.path.basename(p)].append(p)

    def resolve(self, target, src):
        """Note path (without .md) a link resolves to, in Obsidian's order: vault root,
        relative to the source note, unique path suffix, basename. None when unresolved."""
        t = target.strip()
        t = t[:-3] if t.endswith(".md") else t
        if t in self.by_path:
            return t
        rel = os.path.normpath(os.path.join(os.path.dirname(src), t))
        if rel in self.by_path:
            return rel
        if "/" not in t:
            hits = self.by_base.get(t, [])
            return hits[0] if hits else None
        hits = [q for q in self.by_path if q.endswith("/" + t)]
        return hits[0] if len(hits) == 1 else None

    def has_file(self, target, src):
        t = target.strip()
        if t.endswith(".md") or self.resolve(t, src):
            return True
        if t in self.files or os.path.normpath(os.path.join(os.path.dirname(src), t)) in self.files:
            return True
        return bool(self.file_base.get(os.path.basename(t)))


def audit(root):
    v = Vault(root)
    broken, missing_embeds = [], []
    inbound = defaultdict(set)
    for p, text in v.notes.items():
        body = prose(text)
        for m in WIKI.finditer(body):
            target = v.resolve(m.group(1), p)
            if target is None:
                broken.append((p, m.group(1)))
            else:
                inbound[target].add(p)
        for m in MDLINK.finditer(body):
            t = m.group(1)
            if "://" in t or t.startswith("mailto:") or not t.endswith(".md"):
                continue
            target = v.resolve(t, p)
            if target is None:
                broken.append((p, t))
            else:
                inbound[target].add(p)
        for m in EMBED.finditer(body):
            if not v.has_file(m.group(1), p):
                missing_embeds.append((p, m.group(1)))

    studies = defaultdict(set)
    no_readme, odd = [], []
    slug_owners = defaultdict(list)
    tech = os.path.join(v.root, "tech")
    for domain in sorted(os.listdir(tech)) if os.path.isdir(tech) else []:
        for name in sorted(os.listdir(os.path.join(tech, domain))):
            full = os.path.join(tech, domain, name)
            slug = name[:-3] if name.endswith(".md") else name
            studies[domain].add(slug)
            study = f"tech/{domain}/{slug}"
            slug_owners[slug].append(study)
            if ODD_NAME.search(name):
                odd.append(f"tech/{domain}/{name}")
            if os.path.isdir(full):
                readme = f"{study}/README.md"
                if readme not in v.notes:
                    no_readme.append(study)
                    continue
                for alias in frontmatter_list(frontmatter(v.notes[readme]), "aliases"):
                    if alias != slug:
                        slug_owners[alias].append(study)
    duplicate_slugs = {s: sorted(o) for s, o in slug_owners.items() if len(set(o)) > 1}

    mocs = "\n".join(text for p, text in v.notes.items() if p.startswith("MOCs/"))
    unlinked = sorted(f"tech/{d}/{s}" for d, names in studies.items() for s in names if f"tech/{d}/{s}" not in mocs)
    no_frontmatter, no_status = [], []
    status = Counter()
    for p, text in sorted(v.notes.items()):
        fm = frontmatter(text)
        if fm is None:
            if p != "README.md":
                no_frontmatter.append(p)
            status["<none>"] += 1
            continue
        s = frontmatter_field(fm, "status")
        if not s and p != "README.md":
            no_status.append(p)
        status[s or "<none>"] += 1
    orphans = sorted(p for p in v.notes
                     if p[:-3] not in inbound and p not in ORPHAN_EXEMPT and not p.startswith("Templates/"))

    report = {
        "notes": len(v.notes),
        "studies": {d: len(s) for d, s in sorted(studies.items())},
        "broken_links": sorted(broken),
        "missing_embeds": sorted(missing_embeds),
        "unlinked_from_moc": unlinked,
        "folders_without_readme": sorted(no_readme),
        "notes_without_frontmatter": no_frontmatter,
        "notes_without_status": no_status,
        "orphan_notes": orphans,
        "odd_folder_names": sorted(odd),
        "duplicate_slugs": duplicate_slugs,
        "status": dict(status),
    }
    report["ok"] = not any(report[k] for k in (
        "broken_links", "missing_embeds", "unlinked_from_moc", "folders_without_readme",
        "notes_without_frontmatter", "notes_without_status", "orphan_notes", "odd_folder_names",
        "duplicate_slugs"))
    return report


def main(argv):
    root = argv[1] if len(argv) > 1 else os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
    report = audit(root)
    print(json.dumps(report, ensure_ascii=False, indent=1))
    return 0 if report["ok"] else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
