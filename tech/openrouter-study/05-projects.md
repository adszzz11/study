# OpenRouter 실전 프로젝트

> 실제 프로젝트에 OpenRouter 적용하기

## 프로젝트 1: 스마트 챗봇

### 개요
다중 모델 폴백과 비용 최적화가 적용된 챗봇

### 구현

```python
import os
from openai import OpenAI
from typing import Optional

class SmartChatbot:
    def __init__(self):
        self.client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=os.environ["OPENROUTER_API_KEY"]
        )
        self.conversation = []
        self.total_cost = 0.0

        # 모델 설정
        self.models = {
            "fast": "openai/gpt-4o-mini",
            "balanced": "anthropic/claude-3-haiku",
            "quality": "anthropic/claude-sonnet-4",
            "free": "meta-llama/llama-3.1-8b:free"
        }

    def set_system_prompt(self, prompt: str):
        """시스템 프롬프트 설정"""
        self.conversation = [{"role": "system", "content": prompt}]

    def chat(
        self,
        message: str,
        mode: str = "balanced",
        max_tokens: int = 500
    ) -> str:
        """메시지 전송 및 응답 받기"""
        self.conversation.append({"role": "user", "content": message})

        model = self.models.get(mode, self.models["balanced"])

        try:
            response = self.client.chat.completions.create(
                model=model,
                messages=self.conversation,
                max_tokens=max_tokens,
                extra_body={
                    "route": "fallback",
                    "models": [
                        model,
                        self.models["balanced"],
                        self.models["free"]
                    ]
                }
            )

            assistant_message = response.choices[0].message.content
            self.conversation.append({
                "role": "assistant",
                "content": assistant_message
            })

            # 비용 추적 (간단한 추정)
            tokens = response.usage.total_tokens
            self.total_cost += tokens * 0.000001  # 대략적 추정

            return assistant_message

        except Exception as e:
            return f"오류 발생: {e}"

    def clear_history(self):
        """대화 기록 초기화"""
        system = self.conversation[0] if self.conversation else None
        self.conversation = [system] if system else []

    def get_stats(self) -> dict:
        """통계 반환"""
        return {
            "messages": len(self.conversation),
            "estimated_cost": f"${self.total_cost:.4f}"
        }


# 사용 예시
if __name__ == "__main__":
    bot = SmartChatbot()
    bot.set_system_prompt("당신은 친절한 한국어 AI 어시스턴트입니다.")

    while True:
        user_input = input("You: ")
        if user_input.lower() in ["quit", "exit"]:
            break

        response = bot.chat(user_input, mode="fast")
        print(f"Bot: {response}\n")

    print(bot.get_stats())
```

---

## 프로젝트 2: 문서 분석 파이프라인

### 개요
PDF/이미지 문서를 분석하고 요약하는 파이프라인

### 구현

```python
import base64
import json
from pathlib import Path

class DocumentAnalyzer:
    def __init__(self, api_key: str):
        self.client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=api_key
        )

    def _encode_file(self, file_path: str) -> tuple[str, str]:
        """파일을 base64로 인코딩"""
        path = Path(file_path)
        ext = path.suffix.lower()

        with open(file_path, "rb") as f:
            content = base64.b64encode(f.read()).decode("utf-8")

        if ext in [".png", ".jpg", ".jpeg"]:
            mime = f"image/{ext.replace('.', '')}"
            return content, mime
        elif ext == ".pdf":
            return content, "application/pdf"
        else:
            raise ValueError(f"지원하지 않는 형식: {ext}")

    def analyze_image(self, image_path: str, prompt: str) -> str:
        """이미지 분석"""
        content, mime = self._encode_file(image_path)

        response = self.client.chat.completions.create(
            model="anthropic/claude-sonnet-4",
            messages=[{
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {
                        "type": "image_url",
                        "image_url": {"url": f"data:{mime};base64,{content}"}
                    }
                ]
            }]
        )

        return response.choices[0].message.content

    def analyze_pdf(self, pdf_path: str, prompt: str) -> str:
        """PDF 분석"""
        content, mime = self._encode_file(pdf_path)

        response = self.client.chat.completions.create(
            model="anthropic/claude-sonnet-4",
            messages=[{
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {
                        "type": "file",
                        "file": {"url": f"data:{mime};base64,{content}"}
                    }
                ]
            }]
        )

        return response.choices[0].message.content

    def extract_structured_data(
        self,
        file_path: str,
        schema: dict
    ) -> dict:
        """구조화된 데이터 추출"""
        prompt = f"""이 문서에서 다음 구조로 데이터를 추출해주세요.
JSON 형식으로만 응답하세요:

{json.dumps(schema, ensure_ascii=False, indent=2)}"""

        ext = Path(file_path).suffix.lower()

        if ext in [".png", ".jpg", ".jpeg"]:
            result = self.analyze_image(file_path, prompt)
        elif ext == ".pdf":
            result = self.analyze_pdf(file_path, prompt)
        else:
            raise ValueError(f"지원하지 않는 형식: {ext}")

        try:
            return json.loads(result)
        except json.JSONDecodeError:
            return {"raw_response": result}

    def batch_analyze(
        self,
        file_paths: list[str],
        prompt: str
    ) -> list[dict]:
        """여러 문서 일괄 분석"""
        results = []

        for file_path in file_paths:
            try:
                ext = Path(file_path).suffix.lower()

                if ext in [".png", ".jpg", ".jpeg"]:
                    content = self.analyze_image(file_path, prompt)
                elif ext == ".pdf":
                    content = self.analyze_pdf(file_path, prompt)
                else:
                    content = f"지원하지 않는 형식: {ext}"

                results.append({
                    "file": file_path,
                    "status": "success",
                    "content": content
                })
            except Exception as e:
                results.append({
                    "file": file_path,
                    "status": "error",
                    "error": str(e)
                })

        return results


# 사용 예시
if __name__ == "__main__":
    analyzer = DocumentAnalyzer(os.environ["OPENROUTER_API_KEY"])

    # 영수증 데이터 추출
    schema = {
        "store_name": "가게 이름",
        "date": "날짜",
        "items": [{"name": "품목", "price": "가격"}],
        "total": "총액"
    }

    data = analyzer.extract_structured_data("receipt.jpg", schema)
    print(json.dumps(data, ensure_ascii=False, indent=2))
```

---

## 프로젝트 3: 코드 리뷰 봇

### 개요
Git diff를 분석하여 코드 리뷰를 제공하는 봇

### 구현

```python
import subprocess
from typing import Optional

class CodeReviewBot:
    def __init__(self, api_key: str):
        self.client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=api_key
        )

    def get_git_diff(self, base_branch: str = "main") -> str:
        """Git diff 가져오기"""
        result = subprocess.run(
            ["git", "diff", base_branch],
            capture_output=True,
            text=True
        )
        return result.stdout

    def review_code(
        self,
        diff: str,
        focus: Optional[str] = None
    ) -> str:
        """코드 리뷰 수행"""
        system_prompt = """당신은 시니어 소프트웨어 엔지니어입니다.
코드 리뷰를 수행하고 다음 관점에서 피드백을 제공해주세요:
1. 버그 또는 잠재적 문제
2. 성능 개선점
3. 코드 스타일 및 가독성
4. 보안 취약점
5. 테스트 필요성

리뷰는 건설적이고 구체적으로 작성해주세요."""

        user_prompt = f"다음 코드 변경사항을 리뷰해주세요:\n\n```diff\n{diff}\n```"

        if focus:
            user_prompt += f"\n\n특히 다음 부분에 집중해주세요: {focus}"

        response = self.client.chat.completions.create(
            model="anthropic/claude-sonnet-4",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            max_tokens=2000
        )

        return response.choices[0].message.content

    def suggest_improvements(self, code: str, language: str) -> str:
        """코드 개선 제안"""
        prompt = f"""다음 {language} 코드의 개선점을 제안해주세요.
개선된 코드와 설명을 함께 제공해주세요.

```{language}
{code}
```"""

        response = self.client.chat.completions.create(
            model="anthropic/claude-sonnet-4",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=2000
        )

        return response.choices[0].message.content

    def explain_code(self, code: str, detail_level: str = "normal") -> str:
        """코드 설명"""
        levels = {
            "simple": "초보자도 이해할 수 있게 간단히",
            "normal": "일반 개발자 수준으로",
            "detailed": "모든 세부사항을 포함하여 상세히"
        }

        prompt = f"""{levels.get(detail_level, levels['normal'])} 다음 코드를 설명해주세요:

```
{code}
```"""

        response = self.client.chat.completions.create(
            model="openai/gpt-4o-mini",  # 설명은 저렴한 모델로
            messages=[{"role": "user", "content": prompt}],
            max_tokens=1000
        )

        return response.choices[0].message.content


# 사용 예시
if __name__ == "__main__":
    bot = CodeReviewBot(os.environ["OPENROUTER_API_KEY"])

    # Git diff 리뷰
    diff = bot.get_git_diff("main")
    if diff:
        review = bot.review_code(diff)
        print("=== 코드 리뷰 ===")
        print(review)

    # 특정 코드 개선 제안
    code = """
def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)
"""
    improvements = bot.suggest_improvements(code, "python")
    print("\n=== 개선 제안 ===")
    print(improvements)
```

---

## 프로젝트 4: API 래퍼 서비스

### 개요
OpenRouter를 감싸는 Flask API 서비스

### 구현

```python
from flask import Flask, request, jsonify
from functools import wraps
import os

app = Flask(__name__)

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.environ["OPENROUTER_API_KEY"]
)

# 간단한 API 키 인증
def require_api_key(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        api_key = request.headers.get("X-API-Key")
        if api_key != os.environ.get("MY_API_KEY"):
            return jsonify({"error": "Unauthorized"}), 401
        return f(*args, **kwargs)
    return decorated


@app.route("/chat", methods=["POST"])
@require_api_key
def chat():
    """채팅 엔드포인트"""
    data = request.json

    messages = data.get("messages", [])
    model = data.get("model", "openai/gpt-4o-mini")
    max_tokens = data.get("max_tokens", 500)

    try:
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            max_tokens=max_tokens
        )

        return jsonify({
            "response": response.choices[0].message.content,
            "usage": {
                "total_tokens": response.usage.total_tokens
            }
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/models", methods=["GET"])
def list_models():
    """사용 가능한 모델 목록"""
    models = {
        "fast": "openai/gpt-4o-mini",
        "balanced": "anthropic/claude-3-haiku",
        "quality": "anthropic/claude-sonnet-4",
        "free": "meta-llama/llama-3.1-8b:free"
    }
    return jsonify(models)


@app.route("/health", methods=["GET"])
def health():
    """헬스 체크"""
    return jsonify({"status": "ok"})


if __name__ == "__main__":
    app.run(debug=True, port=5000)
```

### 클라이언트 사용

```python
import requests

API_URL = "http://localhost:5000"
API_KEY = "your-api-key"

def chat(message: str, model: str = "fast") -> str:
    response = requests.post(
        f"{API_URL}/chat",
        headers={"X-API-Key": API_KEY},
        json={
            "messages": [{"role": "user", "content": message}],
            "model": model
        }
    )
    return response.json()["response"]

# 사용
print(chat("안녕하세요!"))
```

---

## Best Practices

### 1. 에러 처리

```python
from openai import APIError, RateLimitError, AuthenticationError
import time

def safe_completion(messages, max_retries=3):
    """안전한 API 호출"""
    for attempt in range(max_retries):
        try:
            response = client.chat.completions.create(
                model="openai/gpt-4o-mini",
                messages=messages
            )
            return response.choices[0].message.content

        except RateLimitError:
            wait = 2 ** attempt
            print(f"Rate limit, waiting {wait}s...")
            time.sleep(wait)

        except AuthenticationError:
            raise Exception("API 키가 유효하지 않습니다")

        except APIError as e:
            if attempt == max_retries - 1:
                raise
            print(f"API 에러: {e}, 재시도 중...")

    raise Exception("최대 재시도 횟수 초과")
```

### 2. 환경 분리

```python
import os

class Config:
    @staticmethod
    def get_model(purpose: str) -> str:
        env = os.environ.get("ENVIRONMENT", "development")

        if env == "production":
            models = {
                "chat": "anthropic/claude-sonnet-4",
                "analysis": "anthropic/claude-sonnet-4",
                "simple": "openai/gpt-4o-mini"
            }
        else:
            models = {
                "chat": "meta-llama/llama-3.1-8b:free",
                "analysis": "openai/gpt-4o-mini",
                "simple": "meta-llama/llama-3.1-8b:free"
            }

        return models.get(purpose, models["simple"])
```

### 3. 로깅 및 모니터링

```python
import logging
from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("openrouter")

def logged_completion(messages, model, purpose=""):
    """로깅이 포함된 API 호출"""
    start = datetime.now()

    try:
        response = client.chat.completions.create(
            model=model,
            messages=messages
        )

        elapsed = (datetime.now() - start).total_seconds()

        logger.info(
            f"model={model} "
            f"tokens={response.usage.total_tokens} "
            f"latency={elapsed:.2f}s "
            f"purpose={purpose}"
        )

        return response

    except Exception as e:
        logger.error(f"model={model} error={e} purpose={purpose}")
        raise
```

### 4. 프롬프트 관리

```python
class PromptManager:
    """프롬프트 템플릿 관리"""

    templates = {
        "summarize": "다음 텍스트를 {length}로 요약해주세요:\n\n{text}",
        "translate": "{text}\n\n위 텍스트를 {target_lang}로 번역해주세요.",
        "code_review": "다음 {language} 코드를 리뷰해주세요:\n\n```{language}\n{code}\n```",
    }

    @classmethod
    def get(cls, template_name: str, **kwargs) -> str:
        template = cls.templates.get(template_name)
        if not template:
            raise ValueError(f"템플릿 없음: {template_name}")
        return template.format(**kwargs)


# 사용
prompt = PromptManager.get(
    "summarize",
    length="3문장",
    text="긴 텍스트..."
)
```

### 5. 테스트 전략

```python
import unittest
from unittest.mock import Mock, patch

class TestChatbot(unittest.TestCase):

    @patch('openai.OpenAI')
    def test_chat_returns_response(self, mock_client):
        # Mock 응답 설정
        mock_response = Mock()
        mock_response.choices = [Mock(message=Mock(content="테스트 응답"))]
        mock_response.usage = Mock(total_tokens=10)

        mock_client.return_value.chat.completions.create.return_value = mock_response

        bot = SmartChatbot()
        result = bot.chat("테스트")

        self.assertEqual(result, "테스트 응답")

    def test_model_selection(self):
        bot = SmartChatbot()
        self.assertEqual(bot.models["fast"], "openai/gpt-4o-mini")
        self.assertEqual(bot.models["free"], "meta-llama/llama-3.1-8b:free")
```

---

## 핵심 요약

```
프로젝트 패턴:
1. 스마트 챗봇: 폴백 + 비용 최적화
2. 문서 분석: 멀티모달 활용
3. 코드 리뷰: 특화 프롬프트
4. API 서비스: Flask 래퍼

Best Practices:
- 재시도 로직 (지수 백오프)
- 환경별 모델 분리
- 로깅 및 모니터링
- 프롬프트 템플릿 관리
- 테스트 작성
```

---

## 관련 노트

- [[04-learning/01-quickstart|Quick Start]]
- [[04-learning/06-cost-management|비용 관리]]
- [[cheatsheet|치트시트]]
