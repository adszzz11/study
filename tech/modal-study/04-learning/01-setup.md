---
date: 2026-02-02
tags:
  - tech
  - modal
  - setup
  - tutorial
parent: "[[../README]]"
---

# Modal - 설치 및 첫 배포

> [[../03-references|이전: 참고자료]] | [[../README|목차]] | [[02-functions|다음: Function 정의]]

---

## 1. 사전 준비

### 요구 사항

| 항목 | 요구 사항 |
|------|----------|
| Python | 3.9 이상 |
| pip | 최신 버전 권장 |
| 인터넷 | 클라우드 연결 필요 |
| 계정 | Modal 계정 (무료) |

### 계정 생성

1. [modal.com](https://modal.com) 접속
2. "Sign Up" 클릭
3. GitHub 또는 Google 계정으로 가입
4. **매달 $30 무료 크레딧** 자동 제공

---

## 2. 설치하기

### pip 설치

```bash
# Modal 클라이언트 설치
pip install modal

# 버전 확인
modal --version
```

### 인증 설정

```bash
# Modal 인증 (브라우저 열림)
modal setup
```

실행하면:
1. 브라우저가 자동으로 열림
2. Modal 로그인/승인
3. 터미널에 "Authentication successful" 표시

### 설치 확인

```bash
# 설치 확인
modal --help

# 계정 정보 확인
modal profile current
```

---

## 3. Hello World

### 첫 번째 Modal 앱 작성

`hello.py` 파일 생성:

```python
import modal

# 앱 정의
app = modal.App("hello-modal")

# 클라우드에서 실행될 함수
@app.function()
def hello(name: str = "World"):
    print(f"Hello, {name}!")
    return f"Hello, {name}!"

# 로컬 진입점 (modal run 시 실행)
@app.local_entrypoint()
def main():
    # .remote()로 클라우드에서 실행
    result = hello.remote("Modal")
    print(f"결과: {result}")
```

### 실행하기

```bash
# 앱 실행
modal run hello.py
```

출력 예시:
```
✓ Created objects.
├── Function hello.hello (1 container)
Hello, Modal!
결과: Hello, Modal!
```

---

## 4. 기본 명령어

### modal CLI 명령어

| 명령어 | 설명 |
|--------|------|
| `modal run app.py` | 앱 실행 (개발 모드) |
| `modal deploy app.py` | 앱 배포 (상시 실행) |
| `modal serve app.py` | 웹 엔드포인트 로컬 개발 |
| `modal shell app.py` | 컨테이너 쉘 접속 |
| `modal app list` | 배포된 앱 목록 |
| `modal app stop <name>` | 앱 중지 |

### 실행 모드 비교

```
modal run  → 개발/테스트 (일회성 실행)
modal deploy → 프로덕션 배포 (상시 대기)
modal serve → 로컬 웹 개발 (핫 리로드)
```

---

## 5. 개발 환경 설정

### VS Code 설정

```json
// settings.json
{
  "python.analysis.extraPaths": [],
  "python.linting.enabled": true
}
```

### 추천 확장

- Python
- Pylance (타입 힌트)

### 프로젝트 구조

```
my-modal-project/
├── app.py           # 메인 앱
├── requirements.txt # 의존성
├── .gitignore       # modal 캐시 제외
└── README.md        # 프로젝트 설명
```

`.gitignore` 예시:
```
__pycache__/
.modal/
*.pyc
.env
```

---

## 6. 첫 배포 실습

### 간단한 계산 함수 배포

`compute.py`:

```python
import modal

app = modal.App("my-compute")

@app.function()
def add(a: int, b: int) -> int:
    """두 숫자를 더합니다"""
    return a + b

@app.function()
def multiply(a: int, b: int) -> int:
    """두 숫자를 곱합니다"""
    return a * b

@app.local_entrypoint()
def main():
    # 클라우드에서 실행
    sum_result = add.remote(10, 20)
    print(f"10 + 20 = {sum_result}")

    mul_result = multiply.remote(10, 20)
    print(f"10 * 20 = {mul_result}")
```

실행:
```bash
modal run compute.py
```

출력:
```
10 + 20 = 30
10 * 20 = 200
```

---

## 7. 트러블슈팅

### 자주 발생하는 문제

| 문제 | 원인 | 해결 |
|------|------|------|
| `modal: command not found` | 설치 안 됨 | `pip install modal` |
| `Authentication failed` | 인증 만료 | `modal setup` 재실행 |
| `ModuleNotFoundError` | 의존성 누락 | Image에 패키지 추가 |
| 연결 타임아웃 | 네트워크 문제 | 인터넷 연결 확인 |

### 인증 문제 해결

```bash
# 토큰 초기화
modal token delete

# 재인증
modal setup
```

### 로그 확인

```bash
# 앱 로그 보기
modal app logs <app-name>
```

---

## 8. 체크리스트

### 설치 완료 확인

- [ ] Python 3.9+ 설치됨
- [ ] `pip install modal` 완료
- [ ] `modal setup` 인증 완료
- [ ] Hello World 실행 성공
- [ ] modal CLI 명령어 이해

### 다음 단계 준비

- [ ] 프로젝트 폴더 생성
- [ ] Git 저장소 초기화
- [ ] VS Code 설정 완료

---

## 다음 단계

> [!tip] 다음으로
> 설치가 완료되었다면 [[02-functions|Function 정의와 데코레이터]]를 학습하세요.

---

## References

- [Modal 설치 가이드](https://modal.com/docs/guide/install)
- [Modal CLI Reference](https://modal.com/docs/reference/cli)
