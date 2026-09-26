---
date: 2026-09-27
tags: [tech]
type: tech-tool-study
status: draft
---

# Claudian — References

> [[README|목차로 돌아가기]] · [[02-ecosystem|이전: Ecosystem]] · [[04-learning/01-getting-started|다음: Getting Started]]

## 권장 읽기 순서

1. **Plugin 범위와 안전성**: README와 Obsidian Community Plugin 보안 안내를 읽어 plugin·provider·vault의 신뢰 경계를 설정한다.
2. **설치 호환성**: manifest와 requirements에서 Obsidian version, Desktop 제한, 지원 CLI를 확인한다.
3. **구현/변경 확인**: `package.json`, Releases에서 adapter와 build 환경, 최근 변경을 확인한다.
4. **확장과 운영**: provider의 공식 문서, OpenCode migration, Collab 문서를 필요할 때 읽는다.

## Primary sources

| 출처 | 확인할 내용 |
|---|---|
| [Claudian GitHub repository / README](https://github.com/YishenTu/claudian) | 기능, 사용법, requirements, architecture, privacy, troubleshooting |
| [Claudian Community Plugin listing](https://community.obsidian.md/plugins/realclaudian) | Community Plugin 배포 정보와 다운로드 지표 |
| [manifest.json](https://raw.githubusercontent.com/YishenTu/claudian/main/manifest.json) | 현재 plugin version, 최소 Obsidian version |
| [package.json](https://raw.githubusercontent.com/YishenTu/claudian/main/package.json) | Node 범위, 의존성, build/test script |
| [Claudian Releases](https://github.com/YishenTu/claudian/releases) | 2.3.x를 포함한 release 변화 |
| [Claudian Collab overview](https://claudian.md/docs/collab-mode/) | Collab의 범위와 진입점 |
| [Claudian Collab — How it works](https://claudian.md/docs/collab-mode/how-it-works/) | Git-backed architecture와 safety model |
| [Obsidian Community Plugins](https://help.obsidian.md/community-plugins) | third-party code 설치의 보안 주의 |
| [Claude Code documentation](https://code.claude.com/docs/en/overview) | CLI-first 대안과 native workflow |
| [OpenCode v2 migration guide](https://opencode.ai/v2/docs/migrate-v1) | v1에서 v2로의 migration |

## 사실 확인 메모

- version, download count, 지원 provider, compatibility는 시간이 지나는 값이다. 노트를 갱신할 때는 README보다 manifest, release, Community listing의 최신 값을 우선 확인한다.
- provider별 도구 권한과 privacy 정책은 Claudian 문서만으로 완결되지 않는다. 실제 사용하는 Claude Code, Codex, OpenCode 등의 공식 문서와 local config를 함께 점검한다.
- README에서 “지원”이라고 해도 모든 provider가 동일한 UX/capability를 제공한다는 뜻은 아니다.

## Sources

- [Claudian GitHub repository](https://github.com/YishenTu/claudian)
- [Claudian Releases](https://github.com/YishenTu/claudian/releases)
- [Obsidian Community Plugins](https://help.obsidian.md/community-plugins)
