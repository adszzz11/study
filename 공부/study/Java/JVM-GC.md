Minor GC : Young GC
- Eden
- Survivor
Major GC : Full GC, Old GC
- Old
- Permanent -> Metaspace 
![[Pasted image 20241222230627.png]]

GC 종류
- Serial Collector
	- CPU가 1개일 때 사용했던 GC
	- GC를 단일 쓰레드로 실행
	- 쓰레드 간 GC 오버헤드가 발생하지 않음
	- Client에 적합함
- Parallel Collector
	- Server에 적합한 GC
	- 여러 쓰레드로 실행
	- Compaction 작업을 기본적으로 수행함
		- 조각나 있는 메모리를 한 곳으로 모으기
		- 작업 시간과 CPU를 많이 사용
- Garbage-First(G1) Garbage Collector
	- 복제 시간 감소
	- 바둑판
- Shenandoah GC
	- RedHat 개발
	- OpenJDK 12에 추가
	- Low-pause GC
	- Concurrent Compaction
	- CPU 많이 씀
- The Z Garbage Collector
	- 확장 가능한 빠른 가비지 컬렉터
	- 힙 8MB ~ 16TB
	- 밀리초 단위의 대기시간 목표

XX : 자주 바뀜
X : 좀 덜바뀜
any : 거의 안바뀜

JVM : Java Runtime Environment의 일부분

- ClassLoader
- Class Area
- Heap
- Stack
- PC Register
- Stack
- Execution Engine
- Native Method Interface
- Java Native Libraries

JVM 메모리 영역
- Method Area
	- class info
- Heap Area
	- new Object() 시 저장
- Stack Area
	- thread 별 임시 보관
	- 지역변수
	- runtime method call 순서
	- printStackTrace()와 같음
- PC Registers
	- Thread Execution instruction 정보 위치
- Native Method Stacks
	- 자바 코드가 아닌 native 메소드 정보 저장

Classload 절차
- Loading
	- .class 파일 읽기
	- 바이너리 코드 읽어서 method area 저장
		- package.class
		- 부모 class
		- class, interface, enum 여부
		- 접근제어자, 변수, method 정보
	- Heap 메모리에 class 타입 객체 저장
- Linking
	- Verification
		- .class 파일이 제대로 된 class파일인지 검증
		- ByteCodeVerifier라는 Component를 통해 진행
		- 이 단계가 끝나면 컴파일 준비 끝
	- Preparation
		- class에 있는 static 변수들을 기본값으로 메모리에 할당
	- Resolution
		- 해당 타입의 기호 참조(symbolic references)를 직접 참조(direct references)로 변경
		- 참조되는 엔티티들은 method area를 검색하여 수행
- Initializing
	- static 변수들의 값을 static 블록에서 선언한 값으로 지정
	- class 위에서부터 아래로 내려가면서 진행
	- 부모 class를 처리한 후 자식 class 처리

classLoader 종류
- Bootstrap class loader
	- /jre/lib에 있는 파일 로드
	- bootstrap path라고 부름
	- c, c++과 같은 native 언어로 된 것들도 많음
- Extension class loader
	- Bootstrap class loader의 자식 class loader
	- /lib/ext에 있는 파일 업로드
	- sun.misc.Launcher$ExcClassLoader를 통해 작업 수행
- System/Application clas sloader
	- Extension class loader의 자식 class loader
	- application의 classpath에 지정된 class load
	- sun.misc.Launcher$AppClassLoader 를 통해 작업 수행

BCI : Byte Code Instrumentation
Class 파일을 로딩할 때 내용을 변조하는 기술
- APM
- AOP(Aspect Oriented Programming)

Execution Engine
- Interpreter
	- 바이트코드 라인 단위로 읽어 번역 및 실행
	- 반복 상관없음
- Just-In-Time Compiler(JIT)
	- 효율적인 interpreter 사용
	- 바이트코드 컴파일 후, 네이티브 코드로 변경
	- interpreter가 반복적인 메소드 호출이 있을 때, JIT에서 해당 부분에 대한 native code 제공
- Garbage Collector
	- 미사용 객체 정