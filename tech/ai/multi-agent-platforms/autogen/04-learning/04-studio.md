# 4-4. AutoGen Studio (노코드 GUI)

## 🎨 설치
```bash
pip install -U autogenstudio
autogenstudio ui --port 8081
```

브라우저: `http://localhost:8081`

## 🧱 구성요소
- **Models**: LLM 백엔드 등록 (OpenAI, Azure, Anthropic)
- **Tools**: function 또는 LangChain tool 카탈로그
- **Agents**: AssistantAgent 정의 (drag-and-drop)
- **Teams**: GroupChat 구성
- **Sessions**: 실제 실행 + 대화 시각화
- **Gallery**: 공유 가능한 컴포넌트 모음

## 🔄 Export to Code
Studio에서 만든 Team을 Python 코드로 export 가능 → 그대로 FastAPI에 임베드.

## ⚠️ 보안 경고
> "AutoGen Studio is meant to help you rapidly prototype multi-agent workflows" — 공식 문서가 production-ready 아님 명시.

- 인증 없음 (기본)
- 코드 실행 = 호스트 권한
- Tailscale 등으로 격리 필수

## ✅ Studio가 좋은 케이스
- 비기술 PM에게 워크플로우 시연
- 빠른 A/B 비교 (다른 selector, prompt)
- 학습용 first hands-on
- Gallery에서 커뮤니티 자산 가져오기

## 🚫 Studio가 부족한 케이스
- 프로덕션 운영
- CI/CD 통합
- 버전 관리 (Studio는 JSON 저장)
- 대규모 협업

## 🔗 다음 → [../05-projects.md](../05-projects.md)
