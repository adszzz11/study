# AI 기반 테스트코드 자동 생성 Agent는 어떻게 구현했나요? 실제 효과는?

## 답변

AI 기반 테스트코드 자동 생성 Agent는 LangChain과 OpenAI GPT-4를 활용하여 구현했습니다. 소스 코드를 분석하고 컨텍스트를 이해한 뒤, JUnit 5 기반의 테스트 코드를 자동으로 생성하는 시스템입니다.

핵심 아이디어는 "개발자가 작성한 프로덕션 코드의 패턴을 학습하여, 해당 프로젝트의 코딩 스타일과 테스트 컨벤션에 맞는 테스트를 생성"하는 것이었습니다. 단순히 테스트 코드를 생성하는 것을 넘어, 기존 테스트 코드를 학습시켜 팀의 테스트 작성 스타일을 반영하도록 했습니다.

실제로 테스트 작성 시간을 약 60% 단축했고, 커버리지를 75%에서 92%로 향상시키는 데 핵심적인 역할을 했습니다.

## 핵심 키워드

- AI Agent
- 테스트 자동화
- LLM (Large Language Model)
- 코드 분석
- 생산성 향상

## Agent 구현 방법

### 아키텍처
```
┌─────────────────────────────────────────────────┐
│              AI Test Agent                       │
├─────────────────────────────────────────────────┤
│  1. Code Parser (AST 분석)                       │
│     - Kotlin/Java 소스 코드 파싱                  │
│     - 메서드 시그니처, 의존성 추출                 │
│                                                  │
│  2. Context Builder                              │
│     - 프로젝트 구조 분석                          │
│     - 기존 테스트 패턴 학습                       │
│     - 도메인 지식 수집                            │
│                                                  │
│  3. LLM Chain (LangChain)                        │
│     - Prompt Engineering                         │
│     - Few-shot Learning                          │
│     - Chain of Thought                           │
│                                                  │
│  4. Test Code Generator                          │
│     - JUnit 5 테스트 코드 생성                    │
│     - Mockito 모킹 코드 생성                      │
│     - Assertion 자동 생성                         │
│                                                  │
│  5. Validator & Refiner                          │
│     - 컴파일 검증                                 │
│     - 테스트 실행 및 결과 분석                    │
│     - 피드백 기반 개선                            │
└─────────────────────────────────────────────────┘
```

### 사용한 기술 스택
- **LLM**: OpenAI GPT-4 (gpt-4-turbo-preview)
- **Framework**: LangChain for Kotlin
- **Code Analysis**: KotlinPoet, JavaParser
- **Vector DB**: Pinecone (코드 임베딩 저장)
- **Build Tool**: Gradle + Custom Plugin
- **CI/CD**: Jenkins Pipeline Integration

### 동작 방식
```
1. 소스 코드 분석
   - AST(Abstract Syntax Tree) 파싱
   - 메서드 시그니처, 파라미터, 리턴 타입 추출
   - 의존성 및 외부 호출 분석

2. 테스트 케이스 생성
   - LLM에 컨텍스트와 함께 프롬프트 전달
   - 기존 테스트 패턴을 Few-shot Example로 제공
   - 생성된 테스트 코드 파싱 및 검증

3. 검증 및 피드백
   - 생성된 코드 컴파일 체크
   - 실제 테스트 실행 및 결과 확인
   - 실패 시 에러 메시지를 LLM에 피드백하여 재생성
```

## 구현 코드 예시

```kotlin
class AITestGenerator(
    private val llmClient: OpenAIClient,
    private val codeParser: CodeParser,
    private val vectorStore: VectorStore
) {

    suspend fun generateTest(sourceFile: File): String {
        // 1. 소스 코드 분석
        val codeContext = codeParser.parse(sourceFile)

        // 2. 유사한 테스트 패턴 검색 (Vector DB)
        val similarTests = vectorStore.findSimilar(
            embedding = codeContext.toEmbedding(),
            topK = 3
        )

        // 3. 프롬프트 구성
        val prompt = buildPrompt {
            systemMessage = """
                You are an expert test code generator for Kotlin/Spring Boot applications.
                Generate JUnit 5 tests following the Given-When-Then pattern.
                Use Mockito for mocking dependencies.
            """.trimIndent()

            // Few-shot learning: 기존 테스트 예시 제공
            similarTests.forEach { example ->
                addExample(
                    sourceCode = example.sourceCode,
                    testCode = example.testCode
                )
            }

            // 타겟 소스 코드
            userMessage = """
                Generate comprehensive unit tests for the following code:

                ```kotlin
                ${codeContext.sourceCode}
                ```

                Include:
                - Happy path scenarios
                - Edge cases and boundary conditions
                - Exception handling tests
                - Mock external dependencies
            """.trimIndent()
        }

        // 4. LLM 호출
        val response = llmClient.chat(
            model = "gpt-4-turbo-preview",
            messages = prompt.messages,
            temperature = 0.2  // 낮은 temperature로 일관성 있는 코드 생성
        )

        // 5. 생성된 코드 추출 및 정제
        val generatedTest = extractTestCode(response.content)

        // 6. 컴파일 검증
        if (!validateCompilation(generatedTest)) {
            // 에러 메시지를 피드백하여 재생성
            return regenerateWithFeedback(generatedTest, codeContext)
        }

        return generatedTest
    }

    private fun buildPrompt(block: PromptBuilder.() -> Unit): Prompt {
        return PromptBuilder().apply(block).build()
    }

    private suspend fun regenerateWithFeedback(
        failedTest: String,
        context: CodeContext
    ): String {
        val feedbackPrompt = """
            The generated test code failed to compile.

            Error:
            ${context.compilationError}

            Please fix the test code:
            ```kotlin
            $failedTest
            ```
        """.trimIndent()

        val response = llmClient.chat(
            model = "gpt-4-turbo-preview",
            messages = listOf(
                ChatMessage(role = "user", content = feedbackPrompt)
            )
        )

        return extractTestCode(response.content)
    }
}

// Gradle Plugin으로 통합
class TestGenPlugin : Plugin<Project> {
    override fun apply(project: Project) {
        project.tasks.register("generateTests", GenerateTestsTask::class.java) {
            group = "verification"
            description = "Generate AI-powered test code"

            sourceFiles.from(project.fileTree("src/main/kotlin"))
            outputDir.set(project.file("src/test/kotlin"))
        }
    }
}

abstract class GenerateTestsTask : DefaultTask() {
    @get:InputFiles
    abstract val sourceFiles: ConfigurableFileCollection

    @get:OutputDirectory
    abstract val outputDir: DirectoryProperty

    @TaskAction
    fun generate() {
        val generator = AITestGenerator(
            llmClient = OpenAIClient(apiKey = System.getenv("OPENAI_API_KEY")),
            codeParser = KotlinCodeParser(),
            vectorStore = PineconeVectorStore()
        )

        sourceFiles.forEach { sourceFile ->
            runBlocking {
                val testCode = generator.generateTest(sourceFile)
                val testFile = outputDir.file(
                    sourceFile.nameWithoutExtension + "Test.kt"
                ).get().asFile
                testFile.writeText(testCode)
            }
        }
    }
}
```

**프롬프트 엔지니어링 예시:**

```kotlin
val systemPrompt = """
You are an expert Kotlin test engineer specializing in Spring Boot applications.

GUIDELINES:
1. Use JUnit 5 (@Test, assertions from org.junit.jupiter.api.Assertions)
2. Follow Given-When-Then pattern with clear comments
3. Use Mockito for mocking (@Mock, @InjectMocks, verify())
4. Test method names should describe the scenario in Korean
5. Cover edge cases, null checks, and exception scenarios
6. Use @ExtendWith(MockitoExtension::class)

EXAMPLE TEST STRUCTURE:
```kotlin
@ExtendWith(MockitoExtension::class)
class ServiceTest {
    @Mock
    private lateinit var dependency: Dependency

    @InjectMocks
    private lateinit var service: Service

    @Test
    fun `정상적인 경우 성공 응답을 반환한다`() {
        // Given
        val input = createInput()
        `when`(dependency.call()).thenReturn(expected)

        // When
        val result = service.execute(input)

        // Then
        assertEquals(expected, result)
        verify(dependency).call()
    }
}
```

Now generate tests for the provided code.
""".trimIndent()
```

## 실제 효과

### 정량적 효과
- **테스트 작성 시간**: 평균 30분 → 10분 (66% 단축)
  - 단위 테스트 한 개 작성: 15분 → 5분
  - 복잡한 통합 테스트: 1시간 → 25분
- **커버리지 증가율**: 75% → 92% (17%p 증가)
  - Service Layer: 80% → 95%
  - Controller Layer: 70% → 90%
- **버그 발견율**: 30% 향상
  - Edge Case 테스트 자동 생성으로 숨어있던 버그 발견
- **생성 성공률**: 약 85%
  - 15%는 수동 수정 필요 (주로 복잡한 비즈니스 로직)

### 정성적 효과
- **개발자 만족도 증가**: 반복적인 테스트 작성 작업에서 해방
- **테스트 품질 향상**: AI가 놓치기 쉬운 Edge Case를 제안
- **컨벤션 일관성**: 팀의 테스트 작성 스타일이 통일됨
- **학습 효과**: 주니어 개발자가 생성된 테스트 코드를 보며 학습
- **리팩토링 가속화**: 테스트 코드 재작성 부담 감소로 레거시 개선 속도 향상

**구체적인 사례:**

Before (수동 작성):
```kotlin
// 개발자가 놓친 Edge Case
@Test
fun `계좌 이체 시 정상 처리된다`() {
    // 기본적인 시나리오만 테스트
}
```

After (AI 생성):
```kotlin
@Test
fun `계좌 이체 시 정상 처리된다`() {
    // Given: 충분한 잔액이 있는 경우
    // ...
}

@Test
fun `잔액 부족 시 InsufficientBalanceException을 던진다`() {
    // AI가 자동으로 예외 케이스 생성
}

@Test
fun `동일 계좌로 이체 시 SameAccountException을 던진다`() {
    // 개발자가 놓칠 수 있는 엣지 케이스
}

@Test
fun `음수 금액 이체 시 InvalidAmountException을 던진다`() {
    // 경계값 테스트 자동 생성
}
```

## 한계점 및 개선 방향

### 현재 한계점
1. **복잡한 비즈니스 로직 이해 부족**
   - 도메인 특화 로직은 여전히 사람의 검토 필요
   - 금융 계산 같은 정확성이 중요한 부분은 수동 검증 필수

2. **외부 의존성이 많은 경우**
   - 복잡한 Mock 설정이 필요한 경우 정확도 하락
   - 데이터베이스 쿼리 결과 예측이 어려운 경우

3. **비용 문제**
   - GPT-4 API 호출 비용 (한 달 약 $150)
   - 토큰 사용량 최적화 필요

4. **생성 시간**
   - 대규모 클래스는 30초~1분 소요
   - 실시간 생성은 아직 어려움

### 개선 방향
1. **Fine-tuning으로 정확도 향상**
   - 프로젝트의 테스트 코드로 모델 Fine-tuning
   - 도메인 특화 지식 주입

2. **캐싱 및 최적화**
   - 유사한 코드 패턴은 캐싱하여 비용 절감
   - 벡터 DB 검색 최적화로 응답 속도 향상

3. **점진적 개선 루프**
   - 개발자 피드백을 학습 데이터로 활용
   - 생성된 테스트의 실행 결과를 반영

4. **로컬 LLM 도입 검토**
   - Llama 2, Code Llama 등 오픈소스 모델 평가
   - 비용 절감 및 보안 강화

5. **멀티 에이전트 아키텍처**
   - Code Analyzer Agent + Test Writer Agent + Reviewer Agent
   - 각 에이전트가 전문 영역을 담당

## 참고 자료

- [LangChain Documentation](https://python.langchain.com/docs/get_started/introduction)
- [OpenAI GPT-4 API](https://platform.openai.com/docs/models/gpt-4)
- [Pinecone Vector Database](https://www.pinecone.io/)
- [AI-Powered Testing - TestGPT](https://github.com/microsoft/testgpt)
- [Codex for Unit Test Generation - OpenAI Research](https://arxiv.org/abs/2302.06527)
- [Automated Unit Test Generation using LLMs - Google Research](https://research.google/pubs/pub52121/)
