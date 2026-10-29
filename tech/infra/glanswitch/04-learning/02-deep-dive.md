---
date: 2026-10-29
tags: [tech]
type: tech-tool-study
status: draft
---

# Glanswitch Deep Dive

## 1. L2 loop와 STP/RSTP

L2 Ethernet frame에는 TTL이 없어서 loop가 생기면 broadcast storm, MAC table flapping, packet loss가 빠르게 확산될 수 있다. STP/RSTP는 topology를 계산해 redundant path 일부를 blocking/discarding 상태로 두고, 장애 시 경로를 전환한다.

- root bridge를 우연한 기본 priority에 맡기지 말고 의도적으로 정한다.
- endpoint access port에는 edge/PortFast와 BPDU Guard를 적용해 실수로 switch를 연결했을 때 보호한다.
- trunk/uplink의 allowed VLAN 및 LACP member 상태를 변경 전후로 확인한다.

## 2. Access-layer security

VLAN은 security boundary를 구현하는 한 요소일 뿐이다. 다음 control을 위협 모델과 장비 지원 범위에 맞춰 조합한다.

| Control | 목적 | 운영상 주의 |
|---|---|---|
| 802.1X | 인증된 user/device만 port access | RADIUS 장애 시 fail-open/closed 정책 필요 |
| DHCP snooping | 신뢰되지 않은 DHCP server 억제 | uplink를 trusted로 정확히 지정 |
| Dynamic ARP Inspection | ARP spoofing 완화 | DHCP snooping binding과 연계 |
| Port security | 예상 MAC 수 제한 | phone+PC, AP uplink의 정상 MAC 수 고려 |
| Port isolation | endpoint 간 lateral traffic 제한 | NVR, printer, gateway 예외를 검증 |

## 3. PoE capacity 설계

PD가 부팅 시 peak power를 요구하거나, heater/PTZ 기능이 있는 camera처럼 workload별 소비가 달라질 수 있다. 따라서 다음을 분리해 본다.

1. 각 PD의 standard/class와 정상·peak 소비 전력
2. cable 길이·품질에 따른 PD 가용 전력
3. switch의 총 PoE budget과 port별 maximum
4. 전원 공급 장치와 UPS의 장애·복구 시나리오

우선순위 기반 power policing을 지원하면 critical AP/phone/camera가 저우선순위 PD보다 먼저 보호되도록 설정한다. 전력 부족 alarm과 denied power event도 monitoring 항목에 넣는다.

## 4. Observability와 변경 안전성

SNMP 또는 controller telemetry로 interface utilization, errors, discards, CRC, speed/duplex, PoE draw, temperature, STP topology change를 수집한다. syslog에는 link flap, authentication 실패, STP event, power denied가 남도록 한다.

변경은 backup → 영향받는 VLAN/port 식별 → maintenance window → 한 항목 변경 → management·endpoint·uplink 검증 → rollback 순서를 따른다. remote switch에서 management VLAN을 바꿀 때는 out-of-band console 없이는 고립될 수 있다.
