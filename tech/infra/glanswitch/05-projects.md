---
date: 2026-10-29
tags: [tech]
type: tech-tool-study
status: draft
---

# Glanswitch Projects

## 1. 소형 사무실 segmentation

managed PoE switch 한 대에 corporate, guest, IoT VLAN을 만들고 AP와 VoIP phone을 연결한다. firewall에서 guest·IoT의 corporate 접근은 deny하고 필요한 DNS, NTP, Internet만 허용한다.

**완료 기준**: VLAN별 DHCP/DNS와 정책 검증표, switch config backup, PoE·interface baseline이 남아 있다.

## 2. CCTV deployment

camera 전용 VLAN과 NVR 접근 policy를 만들고, camera별 normal/peak 전력을 기준으로 PoE budget을 산정한다. NVR uplink의 bandwidth를 계산하고, 필요 시 QoS와 camera-port isolation을 검토한다.

**완료 기준**: 모든 camera가 장애·재부팅 시에도 power denied 없이 동작하며, NVR 외 VLAN에서 camera management에 접근하지 못한다.

## 3. 지점 표준화

UniFi/Omada 같은 controller 기반 환경에서 VLAN, port profile, firmware window, SNMP/syslog destination을 template화한다. 지점별 예외는 명시적으로 문서화하고 공통 baseline과 비교한다.

**완료 기준**: 새 지점 배포 checklist와 rollback plan으로 일관된 policy를 재현할 수 있다.

## 4. 관측성 실습

SNMP로 interface utilization·errors·discards와 PoE draw를 수집하고, syslog의 link flap/STP event를 dashboard 또는 log search에서 상관 분석한다. 정상 baseline, 의도적인 cable disconnect, 과부하 상황을 비교한다.

**완료 기준**: alert threshold가 임의의 숫자가 아니라 측정한 baseline과 서비스 영향에 근거한다.
