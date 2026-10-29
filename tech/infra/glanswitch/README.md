---
date: 2026-10-29
tags: [tech]
type: tech-tool-study
status: draft
---

# Glanswitch Tool Study

> **한 줄 정의**: Glanswitch는 독립 제품명이 확인된 용어가 아니라 조달 문서에서 보이는 **GLAN (Gigabit LAN) switch** 용례로 해석하며, Ethernet frame을 MAC address 기반으로 전달하고 PoE 모델은 data와 전력을 함께 제공하는 장비다.

## Overview

이 노트는 `GLANSwitch`라는 표기가 특정 제품·프로젝트임을 전제하지 않는다. 공개 용례의 문맥을 따라 **Gigabit Ethernet switch**, 특히 AP·camera·VoIP에 쓰이는 managed PoE switch를 학습 대상으로 삼는다.

핵심은 port 수가 아니라 VLAN 분리, loop 방지, uplink 설계, PoE budget, 관리·관측성이다. L2 switch는 VLAN 사이를 routing하지 않으므로 router/firewall 또는 L3 switch가 별도 경계가 된다.

## Learning Path

- [ ] [[tech/infra/glanswitch/01-overview|Overview]] — MAC forwarding, VLAN, PoE의 역할 이해
- [ ] [[tech/infra/glanswitch/02-ecosystem|Ecosystem]] — unmanaged부터 L3/campus switch까지 비교
- [ ] [[tech/infra/glanswitch/03-references|References]] — 공식 문서와 표준 근거 확인
- [ ] [[tech/infra/glanswitch/04-learning/01-getting-started|Getting Started]] — management VLAN, access/trunk 구성
- [ ] [[tech/infra/glanswitch/04-learning/02-deep-dive|Deep Dive]] — STP, security, PoE budget, telemetry 심화
- [ ] [[tech/infra/glanswitch/05-projects|Projects]] — 사무실·CCTV·지점 표준화 프로젝트
- [ ] [[tech/infra/glanswitch/cheatsheet|Cheatsheet]] — 설계·운영 점검표 복습

## When To Use

- PC, AP, IP camera, VoIP phone, IoT를 유선으로 집선해야 할 때
- VLAN으로 corporate, guest, camera, POS 같은 broadcast domain을 분리할 때
- AP·camera에 별도 AC outlet 없이 PoE를 공급할 때
- port statistics, SNMP/syslog, ACL/QoS, 802.1X 같은 운영·보안 기능이 필요할 때

## When Not To Use

- 단일 endpoint 하나를 Internet에 연결하는 WAN edge 역할만 필요할 때
- inter-VLAN routing, NAT, stateful inspection을 access switch만으로 해결하려 할 때
- 실제 PoE budget·cable 길이·장비 전력 요구를 검증하지 않은 상태에서 고전력 PD를 붙일 때
- 단순 flat LAN이면 충분한데 policy와 운영 역량 없이 고급 managed switch 기능을 도입할 때

## Related Notes

- [[MOCs/Index]]
- [[MOCs/Infra]]
- [[tech/infra/kubernetes/README|Kubernetes]]
- [[tech/infra/glanswitch/01-overview|Glanswitch Overview]]

## Sources

- https://smlouvy.gov.cz/smlouva/soubor/11721259/SOD.PDF
- https://www.cisco.com/c/en/us/td/docs/switches/lan/c9000/infra/poe/poe-configuration-guide/g-poe/c-poe.html
- https://www.juniper.net/documentation/us/en/software/junos/multicast-l2/topics/topic-map/bridging-and-vlans.html
- https://help.ui.com/hc/en-us/articles/33402927617047-UniFi-Switch-Settings
