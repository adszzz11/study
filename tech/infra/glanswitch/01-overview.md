---
date: 2026-10-29
tags: [tech]
type: tech-tool-study
status: draft
---

# Glanswitch Overview

## What

`GLANSwitch`는 공개 자료에서 독립 제품명을 가리킨다고 확인되지 않았다. 이 학습에서는 조달 문서의 표기를 **Gigabit LAN (GLAN) switch**로 읽고, Ethernet LAN의 L2 switch를 뜻하는 일반 용어로 사용한다.

Switch는 ingress frame의 source MAC address와 들어온 port를 MAC/CAM table에 학습한다. 이후 destination MAC을 아는 경우 해당 egress port로만 forwarding하고, unknown unicast·broadcast·일부 multicast는 VLAN 범위에서 flood한다. Hub처럼 모든 port에 반복하는 방식보다 불필요한 traffic과 collision domain을 줄인다.

## Why

현대 access LAN에는 PC뿐 아니라 Wi-Fi AP, IP camera, VoIP phone, POS, IoT가 함께 있다. switch는 다음 요구를 access layer에서 수행한다.

| 요구 | switch 기능 | 주의점 |
|---|---|---|
| traffic 분리 | VLAN, access/trunk port | VLAN은 routing·security policy 자체가 아니다 |
| AP/camera 전력 | PoE PSE | 총 PoE budget과 cable loss를 확인한다 |
| 장애 억제 | STP/RSTP, BPDU Guard | 이중 연결은 loop 방지가 먼저다 |
| 가시성 | SNMP, syslog, port counter | baseline 없이 counter만 보면 원인 판단이 어렵다 |
| access 보안 | ACL, 802.1X, DHCP snooping, port isolation | 모델별 지원 범위와 license를 확인한다 |

## 핵심 아키텍처

```text
Internet/WAN
    │
Router / Firewall ── 802.1Q trunk ── GLAN Switch
                                      ├─ access VLAN 10: employee PC
                                      ├─ access VLAN 20 + PoE: Wi-Fi AP
                                      ├─ access VLAN 30 + PoE: IP camera
                                      └─ access VLAN 40 + PoE: VoIP phone
```

- **Forwarding plane**: source MAC 학습과 destination MAC lookup으로 frame을 전달한다.
- **VLAN / trunk**: access port는 보통 하나의 untagged VLAN에 연결되고, trunk는 여러 VLAN을 802.1Q tag로 uplink에 운반한다. VLAN은 broadcast domain 경계다.
- **Loop prevention / aggregation**: STP/RSTP가 L2 loop를 차단하고, LAG는 redundancy와 bandwidth 확장에 사용한다.
- **PoE power plane**: PSE(switch)가 PD(AP/camera/phone)를 감지·classify해 전력을 제공한다.
- **Management plane**: Web UI, CLI, controller, SNMP, syslog를 통해 configuration과 telemetry를 다룬다.
- **L3 boundary**: VLAN 간 traffic은 router/firewall 또는 L3 switch의 SVI/IRB가 policy와 함께 처리한다.

## PoE 등급과 budget

IEEE 802.3af(Type 1)는 PSE port당 최대 15.4 W, 802.3at(Type 2)는 30 W다. 802.3bt는 Type 3/4에서 각각 60 W/90 W 등급으로 확장한다. endpoint에서 실제로 쓸 수 있는 전력은 cable loss 때문에 더 작다. 예를 들어 802.3af PD 가용 전력은 최대 12.95 W로 계산한다.

`필요 budget = 동시 동작 PD의 설계 전력 합계 + 여유분`으로 산정한다. 단순히 `port 수 × 최대 W`만 보거나, switch의 총 PoE budget과 per-port limit을 혼동하지 않는다.
