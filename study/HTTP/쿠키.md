Set-Cookie : 서버에서 클라이언트로 쿠키 전달(응답)
Cookie : 클라이언트가 서버에서 받은 쿠키 저장, HTTP 요청 시 서버로 전달

set-cookie: sessionId=asdf; expires=~ GMT; path=/; domain=.google.com; Secure
- 사용처
	- 사용자 로그인 세션 관리
	- 광고 정보 트래킹
- 쿠키 정보는 항상 서버에 전송됨
	- 네트워크 트래픽 추가 유발
	- 최소한의 정보만 사용(Session Id, 인증 토큰)
	- 서버에 전송하지 않고, 웹 브라우저 내부에 데이터를 저장하고 싶으면 웹 스토리지(localStorage, sessionStorage) 참고
- 보안에 민감한 데이터는 저장하면 안 됨
생명주기
- expires : 만료일이 되면 쿠키 삭제(GMT 기준)
- max-age : 기간이 지나면 쿠키 삭제(초), 0이나 음수를 지정하면 쿠키 삭제
- 세션 쿠키 : 만료 날짜를 생략하면 브라우저 종려 시 까지만 유지
- 영속 쿠키 : 만료 날짜를 입력하면 해당 날짜까지 유지
도메인
명시한 문서 기준 도메인 + 서브 도메인 포함
- domain=example.org
	- example.org
	- dev.example.org
- domain 생략
	- example.org에서만 접근 가능
	- dev.example.org 접근 불가
경로
path=/home
경로를 포함한 하위 경로 페이지만 쿠키 접근
일반적으로 루트 지정(path=/)
Secure
- 쿠키는 http, https를 구분하지 않고 전송
- Secure를 적용하면 https인 경우에만 전송
HttpOnly
- XSS 공격 방지
- 자바스크립트 에서 접근 불가(document.cookie)
- HTTP 전송에만 사용
SameSite
- XSRF 공격 방지
- 요청 도메인과 쿠키에 설정된 도메인이 같은 경우만 쿠키 전송