# Paperclip Cheat Sheet

## 🚀 셋업
```bash
npx paperclipai onboard --yes
# 또는
git clone https://github.com/paperclipai/paperclip && cd paperclip
pnpm install && pnpm db:migrate && pnpm dev
```

## 🧑‍💼 직원 (Agents)
```bash
paperclip agent create -f agents/code-reviewer.yaml
paperclip agent list
paperclip agent show code-reviewer
paperclip agent pause code-reviewer
paperclip agent resume code-reviewer
paperclip agent update code-reviewer --budget.monthly 50
paperclip agent delete code-reviewer
```

## 🎫 티켓
```bash
paperclip ticket create --agent <id> --title "..." --description "..."
paperclip ticket list --status pending|in_progress|completed|failed
paperclip ticket show <id>
paperclip ticket cancel <id>
paperclip ticket retry <id>
```

## ⏰ 루틴
```bash
paperclip routine create -f routines/morning-briefing.yaml
paperclip routine list
paperclip routine test <id>          # dry-run
paperclip routine pause <id>
paperclip routine show <id>          # next_run 확인
```

## 💰 예산
```bash
paperclip budget status              # 현재 사용량
paperclip budget reset --dry-run     # 리셋 미리보기
paperclip budget reset --confirm     # 강제 리셋 (월초)
```

## 🛡️ 승인
```bash
paperclip approval list --pending
paperclip approval approve <id> --note "확인"
paperclip approval reject <id> --reason "..."
```

## 📜 감사로그
```bash
paperclip activity tail --since 1h
paperclip activity --agent code-reviewer --since 24h
paperclip activity export --since 7d --out events.jsonl
paperclip activity prune --before 90d
```

## 🔐 시크릿
```bash
paperclip secrets list
paperclip secrets set GITHUB_TOKEN <value>
paperclip secrets get GITHUB_TOKEN   # 보기 (admin only)
paperclip secrets delete <key>
paperclip secrets rotate GITHUB_TOKEN
```

## 🏢 회사
```bash
paperclip company list
paperclip company create --name "Home OS" --budget 100
paperclip company switch home-os
paperclip company export home-os --out home-os-backup.tar.gz
paperclip company import home-os-backup.tar.gz
```

## 🛠️ 운영
```bash
# 헬스체크
curl http://localhost:3000/api/health

# DB
pnpm db:status
pnpm db:migrate
pnpm db:backup --out backups/

# 업데이트
git pull && pnpm install && pnpm db:migrate

# launchd 자동시작
launchctl load ~/Library/LaunchAgents/com.user.paperclip.plist
```

## 📂 주요 경로
| 경로 | 용도 |
|------|------|
| `~/paperclip/.env` | 시크릿 (chmod 600) |
| `~/paperclip/agents/*.yaml` | 직원 정의 |
| `~/paperclip/routines/*.yaml` | 정기 루틴 |
| `~/paperclip/governance/policies.yaml` | 승인 정책 |
| `~/paperclip/skills/registry.yaml` | Skill 카탈로그 |
| `~/paperclip/workspaces/<agent>/` | 직원별 워크스페이스 |

## 🔗 빠른 링크
- 공식: https://github.com/paperclipai/paperclip
- Docs: https://github.com/paperclipai/paperclip/tree/main/docs
- 본 study: `study/tech/ai/multi-agent-platforms/paperclip/`
