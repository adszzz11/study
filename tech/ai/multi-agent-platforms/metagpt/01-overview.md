# Part 1. MetaGPT 개요

## 📌 핵심 철학: "Code = SOP(Team)"

> 사람 회사가 효율적으로 일하는 비결은 **명문화된 SOP**. LLM 팀에도 같은 SOP를 입히면 협업이 잘 된다.

## 🎭 역할 (Role) 5종

| 역할 | 책임 |
|------|------|
| **Product Manager** | 요구사항 분석, PRD 작성, 경쟁 분석 |
| **Architect** | 시스템 설계, 데이터 구조, API spec |
| **Project Manager** | 작업 분할, 일정 |
| **Engineer** | 실제 코드 작성 |
| **QA** | 테스트, 코드 리뷰, 버그 발견 |

각 Role은 `Role` 클래스 상속:
```python
class Engineer(Role):
    name: str = "Alex"
    profile: str = "Engineer"
    actions: list = [WriteCode, RunCode, DebugError]
```

## ⚡ Action

작업 단위. Role이 수행하는 구체적 행동.

```python
class WriteCode(Action):
    PROMPT_TEMPLATE = """Given the system design and tasks, write code..."""
    
    async def run(self, context):
        # LLM 호출
        return generated_code
```

## 📡 Environment + Messages

```
Environment (메시지 버스)
   │
   ├─ Role A publish message
   ├─ Role B subscribe (조건 매칭)
   └─ Role C subscribe
```

각 Role이 어떤 메시지를 구독할지 선언 → 자동으로 협업 흐름 형성.

## 🚀 실행 흐름 예시

```
사용자: "할 일 관리 앱"
   │
   ▼
PM: WritePRD → "PRD.md 작성"
   │ publish
   ▼
Architect: WriteDesign → "설계 + 데이터 모델 + API"
   │ publish
   ▼
ProjectManager: WriteTasks → "할 일 분해"
   │ publish
   ▼
Engineer: WriteCode → "각 파일 작성"
   │ publish
   ▼
QA: ReviewCode → "버그 발견 시 Engineer로 다시"
   │
   ▼
완성된 프로젝트 폴더
```

## 🧠 Data Interpreter (특수 모드)

```bash
metagpt --debug "내 매출 CSV 분석해서 인사이트 + 시각화"
```

코드 생성·실행·디버깅을 LLM이 자동 반복. Kaggle 등 데이터 사이언스 워크플로우.

## ⚖️ 장단점

### ✅ 장점
- **소프트웨어 회사 메타포 직관적** — 비기술자도 흐름 이해
- **풍부한 산출물** — PRD부터 코드까지
- **SOP 명문화** — 결과 재현성 ↑
- **Data Interpreter** — DS 시나리오 강력
- **68.2k★** — 가장 큰 SW 자동화 생태계 중 하나

### ❌ 단점
- **코드 생성 외 활용 어려움** — 가족 비서 같은 케이스엔 부적합
- **결과 코드 품질 편차** — 작은 데모는 OK, 큰 시스템은 사람 검토 필수
- **비용 큼** — 한 번 돌릴 때 PM/Arch/PM/Eng/QA 각자 LLM 호출
- **메시지 라우팅 디버깅 어려움**
- 한국어 PRD/문서는 품질 좀 떨어짐 (영어가 안정)

## 🎯 적합도

| 상황 | 적합 |
|------|------|
| 프로토타입·MVP 코드 자동 생성 | ⭐⭐⭐⭐⭐ |
| 작은 사이드 프로젝트 빠른 시작 | ⭐⭐⭐⭐ |
| 데이터 분석 자동화 (Data Interpreter) | ⭐⭐⭐⭐⭐ |
| 개인 비서 / 멀티 도메인 자동화 | ⭐⭐ (다른 프레임워크 추천) |
| 프로덕션 코드 곧장 사용 | ⭐⭐ (사람 검토 필수) |

## 🔗 다음 → [02-ecosystem.md](02-ecosystem.md)
