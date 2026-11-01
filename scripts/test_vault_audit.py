#!/usr/bin/env python3
"""Tests for scripts/vault-audit.py against a throwaway vault. Run: python3 scripts/test_vault_audit.py"""
import importlib.util
import os
import shutil
import tempfile
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location("vault_audit", os.path.join(HERE, "vault-audit.py"))
va = importlib.util.module_from_spec(spec)
spec.loader.exec_module(va)

FM = "---\ndate: 2026-11-01\ntags: [tech]\ntype: tech-tool-study\nstatus: draft\n---\n\n"


class VaultCase(unittest.TestCase):
    def setUp(self):
        self.root = tempfile.mkdtemp(prefix="vault-audit-")
        self.write("README.md", "# repo\n")
        self.write("Home.md", FM + "# Home\n\n- [[MOCs/Index]]\n")
        self.write("MOCs/Index.md", FM + "# Index\n\n- [[MOCs/AI]]\n- [[Home]]\n")
        self.write("MOCs/AI.md", FM + "# AI\n\n## Tool Studies\n\n- [[tech/ai/foo/README|Foo]]\n")
        self.write("tech/ai/foo/README.md", FM + "# Foo\n\n- [[01-overview|Overview]]\n- [[MOCs/AI]]\n")
        self.write("tech/ai/foo/01-overview.md", FM + "# Overview\n\n- [[README]]\n")
        self.write("Templates/Tool Study.md", FM + "# {{title}}\n")

    def tearDown(self):
        shutil.rmtree(self.root)

    def write(self, rel, text):
        path = os.path.join(self.root, rel)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(text)

    def append(self, rel, text):
        with open(os.path.join(self.root, rel), "a", encoding="utf-8") as fh:
            fh.write(text)

    def test_clean_vault_is_ok(self):
        r = va.audit(self.root)
        self.assertTrue(r["ok"], r)
        self.assertEqual(r["studies"], {"ai": 1})

    def test_broken_wiki_link(self):
        self.append("tech/ai/foo/README.md", "- [[tech/ai/nope/README|Nope]]\n")
        r = va.audit(self.root)
        self.assertEqual(r["broken_links"], [("tech/ai/foo/README.md", "tech/ai/nope/README")])
        self.assertFalse(r["ok"])

    def test_broken_relative_markdown_link(self):
        self.append("tech/ai/foo/README.md", "[next](./02-missing.md)\n")
        self.assertEqual(va.audit(self.root)["broken_links"], [("tech/ai/foo/README.md", "./02-missing.md")])

    def test_markdown_link_counts_as_inbound(self):
        self.write("tech/ai/foo/README.md", FM + "# Foo\n\n[overview](./01-overview.md)\n- [[MOCs/AI]]\n")
        r = va.audit(self.root)
        self.assertEqual(r["orphan_notes"], [])
        self.assertTrue(r["ok"], r)

    def test_links_inside_code_and_table_escapes_are_ignored(self):
        self.append("tech/ai/foo/README.md",
                    "```toml\n[[r2_buckets]]\n```\n`[[not-a-note]]`\n| [[01-overview\\|Overview]] |\n")
        r = va.audit(self.root)
        self.assertEqual(r["broken_links"], [])
        self.assertTrue(r["ok"], r)

    def test_link_resolution_order(self):
        self.write("tech/ai/foo/notes/01-overview.md", FM + "# nested\n\n- [[README]]\n")
        self.append("tech/ai/foo/README.md", "- [[notes/01-overview|nested]]\n")
        v = va.Vault(self.root)
        self.assertEqual(v.resolve("tech/ai/foo/01-overview", "Home.md"), "tech/ai/foo/01-overview")
        self.assertEqual(v.resolve("01-overview", "tech/ai/foo/notes/x.md"), "tech/ai/foo/notes/01-overview")
        self.assertEqual(v.resolve("foo/README", "Home.md"), "tech/ai/foo/README")
        self.assertEqual(v.resolve("README.md", "Home.md"), "README")
        self.assertIsNone(v.resolve("ai/README", "Home.md"))

    def test_orphan_note(self):
        self.write("tech/ai/foo/cheatsheet.md", FM + "# Cheatsheet\n")
        r = va.audit(self.root)
        self.assertEqual(r["orphan_notes"], ["tech/ai/foo/cheatsheet.md"])
        self.assertFalse(r["ok"])

    def test_embeds(self):
        self.write("tech/ai/foo/attachments/diagram.png", "png")
        self.append("tech/ai/foo/README.md", "![[diagram.png]]\n![[attachments/diagram.png]]\n![[01-overview]]\n![[gone.jpeg]]\n")
        r = va.audit(self.root)
        self.assertEqual(r["missing_embeds"], [("tech/ai/foo/README.md", "gone.jpeg")])

    def test_study_unlinked_from_moc_and_folder_without_readme(self):
        self.write("tech/ai/bar/01-overview.md", FM + "# Bar\n\n- [[tech/ai/foo/README]]\n")
        self.append("tech/ai/foo/README.md", "- [[tech/ai/bar/01-overview]]\n")
        r = va.audit(self.root)
        self.assertEqual(r["unlinked_from_moc"], ["tech/ai/bar"])
        self.assertEqual(r["folders_without_readme"], ["tech/ai/bar"])

    def test_frontmatter_and_status(self):
        self.write("tech/ai/foo/02-ecosystem.md", "# no frontmatter\n")
        self.write("tech/ai/foo/03-references.md", "---\ndate: 2026-11-01\ntags: [tech]\n---\n# no status\n")
        self.append("tech/ai/foo/README.md", "- [[02-ecosystem]]\n- [[03-references]]\n")
        r = va.audit(self.root)
        self.assertEqual(r["notes_without_frontmatter"], ["tech/ai/foo/02-ecosystem.md"])
        self.assertEqual(r["notes_without_status"], ["tech/ai/foo/03-references.md"])
        self.assertEqual(r["status"]["draft"], 6)  # Home, Index, AI, foo README, 01-overview, Template
        self.assertEqual(r["status"]["<none>"], 3)  # repo README, no-frontmatter, no-status

    def test_odd_folder_names(self):
        for name in ("https-example-com-post", "이거-정리해줘"):
            self.write(f"tech/ai/{name}/README.md", FM + "# x\n\n- [[MOCs/AI]]\n")
            self.append("MOCs/AI.md", f"- [[tech/ai/{name}/README]]\n")
        r = va.audit(self.root)
        self.assertEqual(r["odd_folder_names"], ["tech/ai/https-example-com-post", "tech/ai/이거-정리해줘"])

    def test_duplicate_slug_and_alias(self):
        self.write("tech/data/foo/README.md", FM + "# Foo again\n\n- [[MOCs/AI]]\n")
        self.write("tech/ai/baz/README.md",
                   "---\ndate: 2026-11-01\naliases:\n  - foo\n  - old-baz\nstatus: draft\n---\n# Baz\n\n- [[MOCs/AI]]\n")
        self.append("MOCs/AI.md", "- [[tech/data/foo/README]]\n- [[tech/ai/baz/README]]\n")
        r = va.audit(self.root)
        self.assertEqual(r["duplicate_slugs"], {"foo": ["tech/ai/baz", "tech/ai/foo", "tech/data/foo"]})
        self.assertFalse(r["ok"])

    def test_frontmatter_list_forms(self):
        self.assertEqual(va.frontmatter_list("aliases: [a, 'b c']\nx: 1", "aliases"), ["a", "b c"])
        self.assertEqual(va.frontmatter_list("aliases:\n  - a\n  - b\ntags: [t]", "aliases"), ["a", "b"])
        self.assertEqual(va.frontmatter_list("aliases: solo\n", "aliases"), ["solo"])
        self.assertEqual(va.frontmatter_list("tags: [t]\n", "aliases"), [])


if __name__ == "__main__":
    unittest.main()
