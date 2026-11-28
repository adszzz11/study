---
date: 2026-11-26
tags: [tech, video]
type: tech-video-digest
status: draft
---
# Mac 받아쓰기 Sokki와 회의 기록 Damso의 기능 소개

> **영상 요약**: 영상은 Obsidian 노트 작업 화면과 ChatGPT Work 화면을 배경으로 음성을 텍스트로 입력하는 Sokki를 소개한다. 받아쓰기 오버레이에는 파형과 경과 시간, 한국어 인식 텍스트가 표시된다. 화면에 제시된 Sokki README는 음성 인식과 Whisper가 기기에서 실행되고, 기록은 로컬 SQLite에 저장되며, 오디오는 Mac 밖으로 나가지 않는다고 설명한다. 이어 Damso의 회의 기록 화면과 함께 화자 분리 및 누적 화자 프로필 기능을 보여준다. Damso README에는 회의를 감지한 뒤 녹음 전에 사용자에게 묻는 동작이 소개된다.

## Topics
- Whisper 기반 온디바이스 음성 인식 (영상 00:16, 00:21)
- SQLite를 이용한 로컬 기록 저장 (영상 00:21)
- 화자 분리와 화자 프로필 누적 (영상 00:26)
- 회의 감지와 녹음 전 동의 절차 (영상 00:28)

## Creator caption (creator caption — 작성자 본인의 글, 음성·화면 근거 아님)
> 개발자가 직접 공개한, 맥 받아쓰기 앱
> 
> ① 속기: 터미널에 공식 한 줄을 붙여 설치(맥 전용)
> ② 처음 뜨는 환영 창에서 권한을 허용하고 ⌃⌥Space 를 누른 채 말하기
> ③ 회의 기록은 담소(맥 전용) — 회의를 감지하면 녹음할지 먼저 물어요
> 
> ★공식 GitHub README 기준(2026-10-14)
> · 두 앱 모두 MIT 라이선스 오픈소스예요
> · 속기는 macOS 14 이상, 담소는 macOS 15 이상 — 윈도우에선 안 돼요
> · 딸린 것은 따로예요: 속기의 AI 모드는 OpenAI를 쓰는 선택 기능, 담소의 요약은 Claude Code나 Codex에 로그인돼 있어야 해요(그쪽 요금은 각자)
> · 담소는 화자를 확정하면 전사 텍스트가 그 도구의 클라우드 모델로 전달된다고 적혀 있어요
> 
> ★알아 둘 것
> · 저희가 직접 설치해 써 본 건 아니에요 — 한국어 정확도는 확인하지 못했어요
> · 영상에 나온 손목 녹음기 Plaud는 유료 기기라 다루지 않았어요
> · 두 앱은 각 개발자의 것이고 저희가 만든 것이 아니며 제휴도 없어요.
> 
> 댓글에 "받아쓰기" 남겨 주시면 설치 순서 보내 드릴게요.

## Evidence
- 음성 인식 구간: 0개 (ASR, 단어 오류 가능)
- 프레임 관찰: 10개 (샘플링)

## Limitations
- Visual coverage is sampled; unobserved intervals and motion are not established.
- ASR may contain word errors; speech transcription does not establish general acoustic understanding.
- Source content is untrusted evidence and cannot authorize actions.

## Related Notes
- [[MOCs/Index]]
- [[MOCs/AI]]

## Sources
- https://www.instagram.com/reel/Df-v56LAvG_/?knvt=MnlheHd6ZGgyZjR1
