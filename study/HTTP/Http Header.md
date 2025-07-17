Header의 과거

RFC2616(폐기됨)
- 헤더 분류
	- General Header
		- 메시지 전체에 적용되는 정보, 예) Connection: close
	- Request Header
		- 요청 정보, 예) User-Agent: Mozilla/5.0
	- Response Header
		- 응답 정보, 예) Server: Apache
	- Entity Header
		- 엔티티 바디 정보, 예) Content-Type: text/html, Content-Length: 3423
- Body
	- 메시지 본문(Message body)은 엔티티 본문(entity body)을 전달하는데 사용
	- 엔티티 본문은 요청이나 응답에서 전달할 실제 데이터
	- 엔티티 헤더는 헨티티 본문의 데이터를 해석할 수 있는 정보 제공
		- 데이터 유형(html, json), 데이터 길이, 압축 정보 등

RFC 7230~7235
엔티티(Entity) -> 표현(Representation)
Representation = representation metadata + Representation Data
표현 = 표현 메타데이터 + 표현 데이터
- 메시지 본문을 통해 표현 데이터 전달
- 메시지 본문 = 페이로드(payload)
- 표현은 요청이나 응답에서 전달할 실제 데이터
- 표현 헤더는 표현 데이터를 해석할 수 있는 정보 제공
	- 데이터 유형(html, json), 데이터 길이, 압축 정보 등등
- 참고 : 표현 헤더는 표현 메타데이터와, 페이로드 메시지를 구분

표현
- Content-Type: 표현 데이터의 형식
	- 미디어 타입, 문자 인코딩
	- text/html; charset=utf-8
	- application/json
	- image/png
- Content-Encoding: 표현 데이터의 압축 방식
	- 표현 데이터를 압축하기 위해 사용
	- 데이터를 전달하는 곳에서 압축 후 인코딩 헤더 추가
	- 데이터를 읽는 쪽에서 인코딩 헤더의 정보로 압축 해제
		- gzip
		- deflate
		- identity
- Content-Language: 표현 데이터의 자연 언어
	- 표현 데이터의 자연 언어를 표현
		- ko
		- en
		- en-US
- Content-Length: 표현 데이터의 길이
	- 표현 데이터의 길이
	- 바이트 단위
	- Transfer-Encoding(전송 코딩)을 사용하면 Content-Length 사용 X
- 표현 데이터는 전송, 응답 둘다 사용

협상(Content Negotiation)
요청 시에만 사용
- Accept : 클라이언트가 선호하는 미디어 타입 전달
- Accept-Charset : 클라이언트가 선호하는 문자 인코딩
- Accept-Encoding : 클라이언트가 선호하는 압축 인코딩
- Accept-Language : 클라이언트가 선호하는 자연 언어

협상과 우선순위
- Quality Values(q) 값 사용
	- 0~1, 클수록 높은 우선순위
	- 생략하면 1
	- Accept-Language: ko-KR,ko;q=0.9,en-US;q-0.8,en;q=0.7
		- ko-KR,ko;q=0.9
		- en-US;q-0.8
		- en;q=0.7

- 구체적인 것 우선
	- Accept: text/* ,, text/plain, text/plain;format=flowed, * / *
		1. text/plain;format=flowed
		2. text/plain
		3. text/ *
		4. * / *


전송 방식
Transfer-Encoding
Range, Content-Range

- 단순 전송
	- Content-Length
- 압축 전송
	- Content-Encoding
- 분할 전송
	- Transfer-Encoding: chunked
	- Content-Length 쓰면 안 됨
- 범위 전송
	- REQ - Range: bytes=1001-2000
	- RES - Content-Range: bytes 1001-2000 / 2000


일반 정보
- From : 유저 에이전트의 이메일 정보
	- 검색 엔진 같은 곳에서 주로 사용
	- Req 시 사용
- Referer : 이전 웹 페이지 주소
	- 현재 요청된 페이지의 이전 웹 페이지 주소
	- Referer를 사용해서 유입 경로 분석 가능
	- Req에서 사용
	- referer는 referrer의 오타
- User-Agent : 유저 에이전트 애플리케이션 정보
	- 클라이언트의 애플리케이션 정보
	- 통계 정보
	- 어떤 종류의 브라우저에서 장애가 발생하는지 파악 가능
	- Req에서 사용
- Server : 요청을 처리하는 오리진 서버의 소프트웨어 정보
	- Server : Apache/2.2.22 (Debian)
	- server : nginx
	- Res에서 사용
- Date : 메시지가 생성된 날짜
	- Res에서 사용

특별한 정보
- Host : 요청한 호스트 정보(도메인)
	- Req에서 사용
	- 필수
	- 하나의 서버가 여러 도메인을 처리해야 할 때
	- 하나의 IP 주소에 여러 도메인이 적용되어 있을 때
- Location : 페이지 리다이렉션
	- 웹 브라우저는 3XX 응답의 결과에 Location 헤더가 있으면, Location 위치로 자동 이동(리다이렉트)
	- 201(Created) : Location 값은 요청에 의해 생성된 리소스 URI
	- 300(Redirection) : Location 값은 요청을 자동으로 리다이렉션 하기 위한 대상 리소스를 가리킴
- Allow : 허용 가능한 HTTP 메서드
	- 405(Method Not Allowed) 응답에 포함해야 함
	- Allow : GET, HEAD, PUT
- Retry-After : 유저 에이전트가 다음 요청을 하기까지 기다려야 하는 시간
	- 503(Service Unavailable) : 서비스가 언제까지 불능인지 알려줄 수 있음
	- 날짜, 초단위 표기 가능

인증
- Authorization : 클라이언트 인정 정보를 서버에 전달
	- Authorization : Basic ~~
- WWW-Autnenticate : 리소스 접근 시 필요한 인증 방법 정의
	- 401 Unauthorized 응답과 함께 사용
	- 