# HTTP 특징
Request-Response 구조
- 클라이언트는 서버에 요청을 보내고, 응답 대기
- 서버가 요청에 대한 결과를 만들어서 응답
- stateless 구조
	- Stateful : 상태 유지
	- Stateless : 상태 유지 X
- Connectionless
	- TCP/IP 연결을 새로 맺어야 함 -> 3 way handshake 시간 추가
	- HTTP 지속 연결(Persistent Connections)로 문제 해결
	- HTTP/2, HTTP/3에서 더 많은 최적화