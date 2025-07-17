# URI
: Uniform Resource Identifier

Uniform : 리소스 식별하는 통일된 방식
Resource : 자원, URI로 식별할 수 있는 모든 것(제한 없음)
Identifier : 다른 항목과 구분하는데 필요한 정보

- URI
 : Uniform Resource Identifier
	- Locator, Name 또는 둘 다 추가로 분류될 수 있다
	- https://www.ietf.org/rfc/rfc3986.txt
	- 
- URL
: Uniform Resource Locator, 리소스가 있는 위치를 지정
- URN
: Uniform Resource Name, 리소스에 이름을 부여


`scheme://[userinfo@]host[:port][/path][?query][#fragment]`

https://www.google.com:443/search?q=hello&hl=ko

Scheme
주로 프로토콜 사용
프로토콜 : 어떤 방식으로 자원에 접근할 것인가? 를 정하는 약속
- HTTP, HTTPS, FTP, etc..
- http는 80, https는 443 주로 사용, 약속된 포트의 경우 생략 가능

Userinfo
URL에 사용자 정보를 포함해서 인증
- FTP 외에는 거의 사용하지 않음

Host
호스트명
- 도메인 또는 IP 사용

Port
접속 포트
- 약속된 포트의 경우 생략 가능

Path
리소스 경로, 계층적 구조
- /home/apache/https_home/test/test.php

Query
key=value의 형태
- ?로 시작, & 로 추가 가능
- query parameter, query string 등으로 불림, 웹 서버에 제공하는 파라미터, 문자 형태.

Fragment
Html 내부 북마크 등에 사용
- 서버에 전송되는 정보 아님

