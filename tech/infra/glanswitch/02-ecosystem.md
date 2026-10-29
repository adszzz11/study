---
date: 2026-10-29
tags: [tech]
type: tech-tool-study
status: draft
---

# Glanswitch Ecosystem

## 선택지 비교

| 구분 | 구성·기능 | 적합한 경우 | 한계 |
|---|---|---|---|
| Unmanaged GLAN switch | Plug-and-play, 기본 MAC forwarding | 단일 flat LAN, 소규모 port 확장 | VLAN, QoS, telemetry, security policy 부재 |
| Smart / easy-managed | Web UI, 기본 VLAN·QoS | 소규모 사무실의 경량 segmentation | CLI, 고급 ACL, 관측성이 제한적 |
| Managed L2/L2+ PoE | VLAN, QoS, ACL, 802.1X, SNMP, per-port PoE | AP·camera·VoIP·IoT가 공존하는 SMB·지점 | 설계·운영 역량 필요 |
| L3 / campus switch | inter-VLAN routing, routing protocol, stacking/fabric | 다수 VLAN의 distribution/core | 비용과 복잡도 증가 |
| Router / firewall | WAN edge, NAT, stateful security, routing | Internet/WAN 경계와 policy enforcement | 고밀도 LAN port·PoE access 대체재가 아님 |

## 대표 ecosystem

- **Cisco Catalyst**: enterprise access/distribution, 광범위한 IOS XE 운영·보안 ecosystem에 적합하다.
- **Juniper EX**: 1GbE access와 10/25GbE uplink, PoE+, Virtual Chassis·EVPN-VXLAN 같은 확장 선택지를 제공한다.
- **Ubiquiti UniFi**: controller에서 Native/Tagged VLAN, PoE, mirroring, aggregation, STP/RSTP를 일관되게 다루기 좋다.
- **TP-Link Omada**: controller 기반 SMB/지점 운영에서 managed switch와 AP ecosystem을 함께 구성하기 쉽다.
- **NETGEAR**: unmanaged부터 Smart Managed Pro까지 소규모 환경의 폭넓은 선택지를 제공한다.

## 비교 기준

구매 전에는 marketing 용어보다 다음을 모델 datasheet에서 확인한다.

1. 필요한 port speed와 uplink(SFP/SFP+, 10/25GbE), switching capacity
2. VLAN, RSTP/MSTP, LACP, ACL, 802.1X, DHCP snooping의 실제 지원 여부
3. 총 PoE budget, per-port PSE limit, 802.3af/at/bt class, 전원 redundancy
4. standalone CLI/Web UI인지, controller/cloud 의존성이 있는지
5. SNMP, syslog, streaming telemetry, firmware lifecycle과 support policy

> [!tip]
> Vendor를 섞어도 802.1Q, RSTP, LACP 같은 표준 protocol은 상호 운용될 수 있다. 단, stacking·controller adoption·proprietary fabric은 같은 vendor 영역으로 남는 경우가 많다.
