1차 다운로드 이후 2차 요청 부터는 캐시를 먼저 찾아봄
캐시 적용
- 캐시 덕분에 캐시 가능 시간동안 네트워크를 사용하지 않아도 됨
- 비싼 네트워크 사용량 줄일 수 있음
- 브라우저 로딩 속도 빠름
- 빠른 사용자 경험
- 캐시가 만료되면 다시 다운로드됨
	- 서버 데이터를 변경하지 않은 경우
		- 검증 헤더에 따라 요청 X
	- 서버 데이터가 변경된 경우
		- 다시 다운로드

- cache-control: max-age=60

검증 헤더
캐시 데이터와 서버 데이터가 같은지 검증하는 데이터
Last-Modified, ETag
- 1초 미만 단위로 캐쉬 조정 불가능
- 날짜 기반의 로직 사용
- 데이터를 수정해서 날짜가 다르지만, 같은 데이터를 수정해서 결과가 같은 경우
- 서버에서 별도의 캐시 로직을 관리하고 싶은 경우
	- 스페이스나 주석처럼 크게 영향이 없는 환경에서 캐시를 유지하고 싶은 경우

검증 헤더로 조건에 따른 분기
- Last-Modified: ~~~
	- 첫 다운로드 시 res로 받은 최종 수정시간
-  if-modified-since: ~~~
	- 전달받은 최종 수정일만 req
	- 304 Not Modified
		- cache-contrtol: max-age=60
		- Last-Modified: ~~
		- Body 없음
- If-None-Match: ETag 사용
	- 조건이 만족하면 200 OK
	- 조건이 만족하지 않으면 304 Not Modified

검증 헤더와 조건부 요청
- 캐시 유효기간이 초과해도 서버의 데이터가 갱신되지 않으면
	- 304 Not Modified + 헤더 메타정보 응답(body X)
	- 클라이언트는 서버가 보낸 응답 헤더 정보로 캐시의 메타 정보 갱신
	- 클라이언트는 캐시에 저장되어 있는 데이터 재활용
	- 결과적으로 용량이 적은 헤더 정보만 다운로드 

ETag
- res 때 반환
- 캐시용 데이터에 임의의 고유한 버전 이름을 달아둠
- 데이터가 변경되면 이름을 바꾸어서 변경
- 단순하게 ETag만 보내서 같으면 유지, 다르면 다시 받기
- 캐시 제어 로직을 서버에서 완전히 관리
- 클라이언트는 단순히 이 값을 서버에 제공
- App 배포 주기에 맞춰 ETag 모두 갱신

- Cache-Control: max-age
- 캐시 유효 시간, 초 단위
- Cache-Control: no-cache
	- 데이터는 캐시해도 되지만, 항상 원(origin) 서버에 검증하고 사용
- Cache-Control: no-store
	- 데이터에 민감한 정보가 있으므로 저장하면 안 됨(메모리에서 사용하고 최대한 빨리 삭제)
- Pragma: no-cache
	- Http1.0 하위 호환
- Expires
	- 캐시 만료일을 정확한 날짜로 지정
	- HTTP1.0부터 사용
	- 더 유연한 Cache-Control: max-age 권장
	- 함께 사용할 경우 Expires 무시


- Cache-Control: public
	- 응답이 public 캐시에 저장되어도 됨
- Cache-Control: private
	- 응답이 해당 사용자만을 위한 것임. private 캐시에 저장해야 함(기본값)
- Cache-Control: s-maxage
	- 프록시 캐시에만 적용되는 max-age
- Age: 60 (HTTP 헤더)
	- 오리진 서버에서 응답 후 프록시 캐시 내에 머문 시간

캐시 무효화
- Cache-Control: no-cache, no-store, must-revalidate
- Pragma: no-cache
	- HTTP 1.0 하위 호환


캐시 지시어(directives) - 확실한 캐시 무효화
- Cache-Control: no-cache
	- 데이터는 캐시해도 되지만, 항상 원(origin) 서버에 검증하고 사용
	- 원 서버 접근 실패 시 오류가 발생하지 않을 수 있음 - 200 OK
- Cache-Control: no-store
	- 데이터에 민감한 정보가 있으므로 저장하면 안 됨(메모리에서 사용하고 최대한 빨리 삭제)
- Cache-Control: must-revalidate
	- 캐시 만료 후 최초 조회 시 원 서버에 검증해야함
	- 원 서버 접근 실패 시 오류가 발생해야함 - 504(GW timeout)
	- must-revalidate는 캐시 유효 시간이라면 캐시를 사용함
- Pragma: no-cache
	- Http1.0 하위 호환

