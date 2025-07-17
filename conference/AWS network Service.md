# AWS Network service 톺아보기 conference


AWS Region과 가용용역
: 물리적 위치
AWS VPC, Subnet, Routing Table
- VPC : 사설망
- Subnet : 부분망
- Routing Table : 트래픽 경로


NACL, SecurityGroub, Gateway
- NACL
	- ACL, Subnet 단위 트래픽 제어
	- stateless
	- Unknown Port 열어야함(단점)
- SecurityGroup
	- 보안 그룹,Service 트래픽 제어
	- 인바운드, 아웃바운드 트래픽 **허용** (제거 안돼)
	- stateful
- Internet & NAT Gateway
	- 입구/출구
	- VPC - Internet 간 통신
	- Routing 목적지
	- Private 서브넷과 인터넷 간 아웃바운드 통신을 할 수 있게 해줌





