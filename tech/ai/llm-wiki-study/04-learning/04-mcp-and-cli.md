# 4-4. Obsidian CLI + 커뮤니티 MCP

## 🔑 핵심: Obsidian의 입장은 "CLI + Skills로 충분"

Obsidian은 **공식 MCP server를 만들지 않는다**고 결정했습니다. 이유:
- Skills 스펙(Anthropic Agent Skills)이 더 일반적
- CLI는 모든 환경에서 작동 (Claude Code, Cursor, Codex, 셸 스크립트)
- MCP는 한 가지 통합 패턴일 뿐 — vendor 종속 위험

**다만 커뮤니티 MCP는 활발**: PulseMCP 등록 66개 (의미 있는 것 ~8개).

## 🥇 옵션 1: Obsidian CLI만 사용 (Karpathy + kepano 권장 경로)

```bash
# 설치
brew install obsidian-cli

# vault 등록
obsidian vault add /Users/sm/code/leetangle/Note --alias leetangle

# 확인
obsidian vault list
```

### Claude Code에서 자연스럽게 사용

Claude Code는 Bash 도구로 obsidian CLI 호출 가능. Skill을 추가하지 않아도 작동.

```
사용자: "본 vault에서 'compounding' 들어간 노트 3개 찾아줘"
   ↓
Claude: obsidian search-content "compounding" --vault leetangle --max 3 --json
   ↓
결과 표시
```

### 자주 쓰는 패턴

```bash
# 1. 패턴 검색
obsidian search "LLM Wiki" --json | jq -r '.results[].path'

# 2. 백링크 분석
obsidian backlinks "study/tech/ai/llm-wiki-study/README.md"

# 3. 새 wiki 페이지 자동 생성
cat <<EOF | obsidian note create "study/wiki/concepts/compounding-knowledge.md" --stdin
---
tags: [llm-wiki, karpathy]
date: 2026-05-23
---
# Compounding Knowledge
...
EOF

# 4. 그래프 export → 시각화
obsidian graph export --vault leetangle --format json > /tmp/graph.json

# 5. 데일리 노트에 ingest log 추가
echo "[$(date)] ingest karpathy-gist 완료" | \
  obsidian note append "$(obsidian daily --path-only)" --stdin
```

## 🥈 옵션 2: 커뮤니티 MCP server 추가

Claude Code/Cursor에서 **도구로 노출**하고 싶을 때 (자연어 호출이 더 자연스러움).

### 추천: marcelmarais/obsidian-mcp-server

```bash
# 설치
npx -y marcelmarais/obsidian-mcp-server@latest --help
```

```json
// ~/.claude/mcp.json 또는 settings.json
{
  "mcpServers": {
    "obsidian": {
      "command": "npx",
      "args": ["-y", "marcelmarais/obsidian-mcp-server"],
      "env": {
        "OBSIDIAN_VAULT_PATH": "/Users/sm/code/leetangle/Note"
      }
    }
  }
}
```

Claude Code 재시작 후 도구 호출 가능:
```
"vault에서 LangGraph 언급된 노트 찾고 본 README와 연결"
→ LLM이 자동으로 vault.search → vault.read → vault.write
```

### 다른 선택지

| MCP server | 특징 | 적합 |
|------------|------|------|
| `marcelmarais/obsidian-mcp-server` | 검색·읽기·쓰기 기본 | 일반 사용 |
| `MarkusPfundstein/mcp-obsidian` | Local REST API 플러그인 통합 | Obsidian 실행 중일 때 |
| `cyanheads/obsidian-mcp-server` | frontmatter surgical edit | 정밀 편집 |
| `@bitbonsai/mcpvault` | 구 mcp-obsidian, trademark rename | 호환성 |

## 🥉 옵션 3: Obsidian REST API 플러그인 (Obsidian 실행 중 한정)

Obsidian 앱이 켜져 있을 때만 동작. 단점은 macOS 로그아웃 시 끊김.

```
1. Obsidian → Settings → Community plugins → "Local REST API" 설치
2. API key 발급
3. http://localhost:27123/vault/ 엔드포인트 사용
```

LLM에서:
```bash
curl http://localhost:27123/vault/study/tech/ai/llm-wiki-study/README.md \
  -H "Authorization: Bearer ${OBSIDIAN_API_KEY}"
```

## 🆚 셋 중 어떤 걸 쓸까

| 시나리오 | 선택 |
|---------|------|
| Claude Code에서 자연어로 vault 조작 | ⭐ MCP server (옵션 2) |
| 셸 스크립트·cron 자동화 | ⭐ CLI (옵션 1) |
| GUI 작업 중 LLM 보조 | ⭐ REST API (옵션 3) |
| Obsidian이 안 켜져 있어도 작동 필요 | CLI 또는 MCP |
| 한 가지만 고르라면 | **CLI** — 가장 보편적 |

## 🛡️ 보안 고려

- **MCP server는 vault 전체 권한**: 시크릿 파일 격리. `.env`, `secrets/` 같은 폴더 제외 패턴 명시.
- **REST API key 노출 위험**: `OBSIDIAN_API_KEY` env에만, 코드 commit ✗.
- **Git pre-commit hook**: LLM이 raw/ 수정 시 차단.

```bash
# .git/hooks/pre-commit
#!/bin/bash
if git diff --cached --name-only | grep -E '^raw/' > /dev/null; then
  if ! git config user.name | grep -q "Simon"; then
    echo "ERROR: raw/는 사람만 수정. LLM 작성 시도 차단."
    exit 1
  fi
fi
```

## ✅ 체크포인트

- [ ] obsidian-cli 설치 + `obsidian search` 실행 성공
- [ ] (선택) marcelmarais/obsidian-mcp-server를 Claude Code에 등록
- [ ] Claude Code에서 자연어로 vault 검색 동작
- [ ] vault 통째 commit·push (LLM 변경 추적)
- [ ] (선택) Git pre-commit hook으로 raw/ 보호

## 🔗 다음

→ 실전 시나리오 → [../05-projects.md](../05-projects.md)
