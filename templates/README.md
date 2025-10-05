# Obsidian 템플릿 사용 가이드

이 폴더에는 Obsidian에서 사용할 수 있는 노트 템플릿들이 포함되어 있습니다.

## 템플릿 설정 방법

### 1. Obsidian Templates 플러그인 설정

1. Obsidian 설정 (⚙️) → **Core plugins** 열기
2. **Templates** 플러그인 활성화
3. Templates 설정에서 **Template folder location** 을 `templates`로 지정

### 2. 템플릿 사용하기

1. 새 노트 생성
2. 명령 팔레트 열기 (`Cmd+P` 또는 `Ctrl+P`)
3. `Templates: Insert template` 검색 후 선택
4. 원하는 템플릿 선택

또는

- 단축키 설정: Settings → Hotkeys → "Templates: Insert template" 검색 → 원하는 단축키 지정 (예: `Cmd+T`)

## 사용 가능한 템플릿

### 📝 컨퍼런스 노트 템플릿

**파일명**: `컨퍼런스-노트-템플릿.md`

**용도**: 컨퍼런스, 밋업, 세미나 참석 후 노트 정리

**주요 섹션**:
- 이벤트 정보 (이벤트명, 발표자, 일시, 장소)
- 핵심 내용 (주제별 정리)
- 인사이트 & 배운 점
- 질의응답 (Q&A)
- 참고 자료
- 개인 회고
- TODO

**사용 예시**:
1. `conference/` 폴더에서 새 노트 생성
2. 템플릿 삽입
3. `{{title}}` 부분을 발표 제목으로 변경
4. YAML frontmatter의 이벤트명, 발표자 등 정보 입력
5. 핵심 내용을 들으면서 실시간으로 작성

## 템플릿 변수

Obsidian Templates 플러그인에서 지원하는 변수:

- `{{date}}` : 현재 날짜
- `{{date:YYYY-MM-DD}}` : 특정 형식의 날짜
- `{{time}}` : 현재 시간
- `{{title}}` : 노트 제목

## 팁

### 1. 실시간 노트테이킹
- 발표를 들으면서 핵심 내용 섹션에 불릿포인트로 바로 작성
- 이해 안 되는 부분은 `TODO`나 `추가 학습이 필요한 부분`에 메모

### 2. 위키링크 활용
- 관련 개념이 나오면 `[[개념명]]` 형식으로 링크 생성
- 나중에 해당 개념 노트를 따로 정리할 때 자동으로 연결됨

### 3. 태그 활용
- YAML frontmatter의 tags에 기술 스택, 주제 등 추가
- 예: `conference`, `backend`, `aws`, `database`, `ai` 등

### 4. 발표 자료 첨부
- Obsidian vault 내 `assets/conference/` 폴더에 PDF나 이미지 저장
- `![발표자료](assets/conference/파일명.png)` 형식으로 삽입

## 커스터마이징

필요에 따라 템플릿을 자유롭게 수정하세요:
- 섹션 추가/제거
- YAML frontmatter 필드 추가
- 본인만의 노트테이킹 스타일로 변경
