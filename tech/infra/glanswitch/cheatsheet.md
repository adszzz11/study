---
date: 2026-10-29
tags: [tech]
type: tech-tool-study
status: draft
---

# Glanswitch Cheatsheet

## 용어

| 용어 | 요약 |
|---|---|
| CAM/MAC table | MAC address와 ingress port의 학습 테이블 |
| access port | 보통 한 untagged VLAN의 endpoint port |
| trunk | 여러 802.1Q-tagged VLAN을 운반하는 link |
| PSE / PD | 전력을 공급하는 switch / 전력을 받는 device |
| STP/RSTP | L2 loop를 방지하고 redundancy를 제어하는 protocol |
| LAG/LACP | 여러 physical link를 논리적으로 묶는 aggregation |
| SVI/IRB | L3 switch에서 VLAN에 연결하는 routed interface |

## 빠른 설계 점검

- [ ] 각 VLAN의 목적, gateway, DHCP/DNS, inter-VLAN allowlist가 문서화되어 있는가?
- [ ] access/trunk, native/untagged VLAN, allowed VLAN이 link 양 끝에서 일치하는가?
- [ ] root bridge, RSTP, edge port, BPDU Guard 정책이 의도대로인가?
- [ ] 총 PoE budget, per-port limit, PD peak power, UPS 용량을 계산했는가?
- [ ] management plane은 별도 VLAN·ACL·강한 인증으로 보호되는가?
- [ ] config backup, syslog, SNMP/telemetry, error/discard baseline이 있는가?

## PoE 기억할 값

| IEEE type | PSE port 최대 출력 | 비고 |
|---|---:|---|
| 802.3af / Type 1 | 15.4 W | PD 가용 최대 12.95 W |
| 802.3at / Type 2 | 30 W | PoE+ |
| 802.3bt / Type 3 | 60 W | 고전력 PD용 |
| 802.3bt / Type 4 | 90 W | 고전력 PD용 |

## 장애 확인 순서

1. port admin/oper state, speed/duplex, cable·SFP 상태를 확인한다.
2. VLAN membership, trunk tag/native VLAN, MAC table 학습 위치를 확인한다.
3. STP state·topology change와 LAG member 상태를 확인한다.
4. interface error/CRC/discard, utilization, PoE class/draw/denied event를 확인한다.
5. router/firewall의 gateway·DHCP·DNS·inter-VLAN policy를 확인한다.

## Sources

- https://www.cisco.com/c/en/us/td/docs/switches/lan/c9000/infra/poe/poe-configuration-guide/g-poe/c-poe.html
- https://www.juniper.net/documentation/us/en/software/junos/multicast-l2/topics/topic-map/bridging-and-vlans.html
