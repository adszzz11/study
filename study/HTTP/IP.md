# IP란
사전적 의미 : OSI의 Layer 3(Network Layer)와 Internet Protocol Suite의 Layer 3(Internet Layer)에 위치하는 프로토콜, E2E 통신을 책임진다.
- 지정한 IP 주소(IP Address)에 데이터 전달
- 패킷(Packet) 이라는 통신 단위로 데이터 전달

한계
- 비연결성
	: 패킷을 받을 대상이 없거나 서비스 불능 상태여도 전송한다.
- 비신뢰성
	- 패킷 소실
	- 패킷 순서성 보장 x
- 프로그램 구분