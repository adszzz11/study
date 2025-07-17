프로젝트명 예시
- DN ATT (TT Fragile Fragile)
- QA Box

배경 : 기존 수기로 진행하던 소프트웨어 테스팅을 자동화하기 위함

AS-IS
- FLOW
1. 운영 담당자가 직접 코드 분석 및 테스트서버(QA) 배포
2. Application Build 시(TUNA 제외) Unit Test 및 Function Test 진행
3. 테스트서버에 접근 Or 외부 툴 사용(Postman, Atom, 등)하여 통합 테스트
4. 테스트 완료 시 작업 계획 작성 & 해당일 작업
- 문제점
	1. 담당자의 실수로 인한 장애가 발생할 수 있다.
	2. 테스트 환경을 전부 담당자가 직접 관리하기에, black hole이 발생할 수 있다.
	3. 추가 및 변경에도 용이하지 않고, 테스트 진행 속도와 관련해서도 여러 변수가 생길 수 있다.

TO-BE
- FLOW
	1. 코드 Release Branch 혹은 Test Branch 등에 Merge Request 되면 Jenkins가 다운로드 후 build, Container Image 생성
		- Jenkins로 download, Build(Unit Test, Function Test 진행 가능, Junit @Test 활용)
	2. Image ImageHub(ex : dockerhub)에 push (hook으로 3 자동 실행)
		: ImageHub는 생성된 Image의 버전 관리 할 수 있음. Image 기반으로 설계 시 언제든 버전 FW 및 Rollback 가능
	3. Push 된 Image 다운로드 받아 이미지 기반의 Container instance 생성
	4. 테스팅 application으로 기본 기능 테스트
		**금번 설계해야할 테스팅 자동화 툴**
	5. 테스트 결과 REPORT
	6. **실제 배포 작업 또한 자동화 가능**
![[DN_ATT.jpeg]]

- 제한점
	1. 서버 별 설정(dev, prod, qa)이 다를 것. 파일을 따로 관리해줘야함
	2. Container Structure가 있는 Server필요
	3. On-Prem 형식의 Structure 사용 시 비용 논의 필요
	4. Web 서버의 경우, Application으로 Test가 제한됨. 
		- Selenium을 이용한 화면 Record를 이용하여 Test 하면 용이할 것으로 보임.


TO-BE의 기능 명세
1. 서비스 별 TestCase 방법 분류 & 저장
	- 서비스 & TC번호를 PK로 한 Table에 저장 예상
2. Network Connect Client 구성
	- 서비스 별로 Request 하는 방식이 다르므로 여러 Client 설치가 가능하도록 확장성 있게 구성 필요
3. 요청 시 해당 TestCase 모음 실행
	- 컨테이너 Build 수행 시 해당 APP으로 요청하면, APP에서 Test를 자동화할 수 있게끔 구성
4. TestCase 수기 동작, CRUD 구성 필요
	- 담당자가 UI를 통하여 테스트케이스를 조작할 수 있도록 구성


이 외
- Postman + CircleCI를 이용한 테스트케이스 자동화 구현
https://circleci.com/blog/testing-an-api-with-postman/?utm_source=google&utm_medium=sem&utm_campaign=sem-google-dg--japac-en-dsa-tROAS-auth-brand&utm_term=g_-_c__dsa_&utm_content=&gclid=CjwKCAiA3pugBhAwEiwAWFzwdf2BbL2EUCduMexS1Btxaw-aMy4VfoIY0lMeinUzAIbHDLAPfejtHhoC_X8QAvD_BwE

- Postman CLI(for Linux) 사용 검토