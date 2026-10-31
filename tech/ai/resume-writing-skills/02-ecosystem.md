---
date: 2026-09-29
tags: [tech]
type: tech-tool-study
status: draft
---

# 이력서 작성 Skills: Ecosystem

> [[README|목차로 돌아가기]] · [[03-references|다음: References]]

| 방식 | 강점 | 한계 | 적합한 경우 |
|---|---|---|---|
| Ad-hoc ChatGPT/Claude prompt | 즉시 시작, 대화형 수정 | 재현성·사실 검증·version 관리가 약함 | 단발성 초안 |
| Resume-writing Agent Skill | 공고별 workflow·QA·privacy rule 재사용 | Skill 설계와 source data 정리가 필요 | 반복 지원, coach, 팀 표준화 |
| Community Claude Skill | 설치 뒤 빠른 활용, CAR·지역 규칙 등을 참고 가능 | maintainer 품질·보안·최신성 검증 필요 | 개인 실험, rule reference |
| RenderCV + Skill | YAML source-of-truth, Git diff, deterministic output | CLI/YAML 학습 필요 | 엔지니어·연구자·다수 version |
| ATS SaaS | parsing/score UI가 편리 | opaque scoring, 개인정보·구독 비용 우려 | 비기술 사용자의 빠른 점검 |

## 선택 기준

| 질문 | 권장 |
|---|---|
| 한 공고의 빠른 초안인가? | 대화형 prompt 후 수동 fact check |
| 지원 공고가 여러 개인가? | fact base + Skill + jobs별 folder |
| 산출물 재현과 diff가 중요한가? | RenderCV 같은 declarative renderer 병행 |
| 외부 service에 개인정보를 둘 수 없는가? | local files, 최소 입력, provider policy 검토 |
| ATS 점수가 목표인가? | score가 아닌 requirement coverage와 readability를 검토 |

## 공개 구현을 읽는 법

`StephanieKoehl/resume-best-practices`의 `/optimize-resume`은 ATS, bullet impact, quantification, keyword match scorecard와 JD의 missing keyword를 제시하는 공개 사례다. 이를 quality checklist의 출발점으로 사용하되, score는 community-maintained heuristic이지 공식 ATS benchmark가 아니다.

`jezweb/claude-skills`의 Resume & Cover Letter Writer는 CAR 방식과 정량 결과를 강조하는 사례다. 설치·실행 전에는 instructions가 개인 data를 어디로 보내는지, scripts가 무엇을 하는지, maintainer와 revision이 신뢰 가능한지 확인한다.

## Sources

- https://github.com/StephanieKoehl/resume-best-practices
- https://github.com/jezweb/claude-skills/blob/main/plugins/writing/skills/resume-cover-letter/SKILL.md
- https://docs.rendercv.com/user_guide/yaml_input_structure/
