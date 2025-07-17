# HTTP 프로토콜에 대한 이해
Hyper Text Transfer Protocol
- HTML, TEXT
- Image, 음성, 영상, 파일
- Json, XML (API)
- 거의 모든 형태의 데이터 전송 가능
- 서버 간 데이터를 주고 받을 때도 대부분 HTTP 사용


History
HTTP/0.9 1991 : GET method 지원, Header X
HTTP/1.0 1996 : method, header 추가
HTTP/1.1 1997 : 가장 많이 사용
- RFC2068(1997)
f- RFC2616(1999)
- RFC7230~7235(2014)
HTTP/2  2015 : 성능 개선
HTTP/3 ing : TCP 대신 UDP 사용, 성능 개선


기반 프로토콜
TCP : HTTP/1.1, HTTP/2
UDP : HTTP/3
현재 HTTP/1.1 주로 사용, 점점 2, 3 증가하는 중

Flow
1. 웹 브라우저가 HTTP 메시지 생성
2. SOCKET 라이브러리를 통해 전달
	- TCP/IP 연결(IP,PORT)
	- 데이터 전달
3. TCP/IP 패킷 생성, HTTP 메시지 전달


http 요청에 대한 req & res
https://www.google.com:443/search?q=hello&hl=ko

REQUEST
GET /search?q=hello&hl=ko HTTP/1.1    //Start Line
Host: www.google.com                            //header

start-line = request-line / status-line
request-line = method SP(공백) request-target SP HTTP-version CRLF(엔터)

method = HTTP 메서드(GET)
- GET
- POST
- PUT
- DELETE
request-target = (/search?q=hello&hl=ko)
- absolute-path[?query]
- 절대경로 ="/"로 시작하는 경로
- 다른 방법도 있긴 함
HTTP-version
- HTTP/1.1

RESPONSE
HTTP/1.1 200 OK                                             //Start Line
Content-Type: text/html;charset=UTF-8     //Header
Content-Length: 3423                                   //Header
                                                                          //CRLF(Empty Line)
`<html>`                                                              //Message Body
	``<body>...</body>
``</html>


start-line = request-line / status-line
status-line = HTTP-version SP status-code SP reason-phrase CRLF

HTTP-version
HTTP status-code = 요청 성공, 실패를 나타냄
- 200 : 성공
- 400 : 클라이언트 요청 오류
- 500 : 서버 내부 요류
이유 문구 : 사람이 이해할 수 있는 짧은 상태 코드 설명글

header-field = field-name":" OWS field-value OWS (OWS : 띄어쓰기 허용)
field-name 은 대소문자 구분 x

HTTP 헤더의 용도
- HTTP 전송에 필요한 모든 부가정보
- 표준 헤더가 너무 많음
- 필요 시 임의의 헤더 추가 가능
	- helloWorld: hihi

HTTP 메시지 바디의 용도
- 실제 전송할 데이터

정리
- 메시지에 모든 것을 전송
- HTTP/1.1을 기준으로 학습
- 클라이언트-서버 구조
- Stateless Protocol
- 단순함
- 확장 가능

HTTP Method를 이용해서 사용하기 애매한 경우
Control URI 사용

HTTP API - 컬렉션
- POST 기반 등록
- 서버가 리소스 URI 결정

HTTP API - 스토어
- PUT 기반 등록
- 클라이언트가 리소스 URI 결정
HTML FORM 사용
- 순수 HTML + HTML form 사용
- GET, POST만 지원