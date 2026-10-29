---
date: 2026-10-29
tags: [tech]
type: tech-tool-study
status: draft
---

# Glanswitch Getting Started

## 학습 목표

- management VLAN과 switch management IP의 목적을 설명한다.
- access port와 trunk port를 구분해 VLAN 10/20/30을 구성한다.
- inter-VLAN policy가 switch port 설정과 별개임을 확인한다.
- PoE consumption과 오류 counter의 baseline을 수집한다.

## 1. 실습 전 설계

8-port managed Gigabit switch 또는 virtual lab을 준비한다. 실제 환경에 적용하기 전, 현재 uplink의 native VLAN, allowed VLAN, management access 경로를 기록하고 console/rollback 경로를 확보한다.

| VLAN | 이름 | endpoint | 기본 policy |
|---:|---|---|---|
| 10 | employee | PC | 업무 서비스만 허용 |
| 20 | guest | guest AP SSID | Internet만 허용 |
| 30 | IoT | camera, IoT | 필요한 controller/NVR만 허용 |

## 2. management VLAN과 port 역할

switch vendor의 UI/CLI에서 management VLAN과 관리 IP를 지정한다. 관리 workstation에서만 Web UI/SSH/SNMP에 접근하도록 firewall ACL을 둔다.

```text
port 1: router/firewall uplink  → trunk, tagged VLAN 10/20/30
port 2: employee PC            → access, untagged VLAN 10
port 3: guest AP               → trunk 또는 vendor AP profile, PoE enabled
port 4: IP camera              → access, untagged VLAN 30, PoE enabled
```

AP가 여러 SSID/VLAN을 전달한다면 AP port는 하나의 access port가 아니라 tagged VLAN을 허용하는 trunk가 될 수 있다. native/untagged VLAN과 allowed VLAN 목록을 양 끝단에서 일치시킨다.

## 3. routing과 policy 검증

VLAN 생성만으로 traffic이 완전히 격리되는 것은 아니다. VLAN 사이 packet은 router/firewall 또는 L3 switch로 보내고 최소 허용 정책을 적용한다.

```text
guest (VLAN 20) ──X──> employee (VLAN 10)
IoT   (VLAN 30) ──X──> employee (VLAN 10)
IoT   (VLAN 30) ─────> NVR / DNS / NTP (필요한 대상만)
```

각 VLAN의 test host에서 DHCP, DNS, Internet, 허용 대상, 차단 대상 순으로 검증한다. ping 성공만으로 application policy가 안전하다고 판단하지 않는다.

## 4. PoE와 baseline

AP/camera를 연결한 뒤 port별 negotiated class, 실제 consumption, switch 전체 PoE budget, link speed/duplex를 확인한다. 802.3af의 PSE 최대 출력은 15.4 W지만 PD 가용 전력은 최대 12.95 W임을 기준값으로 기록한다.

마지막으로 interface error, discard, CRC, utilization, flap 횟수와 STP state를 같은 시점에 수집한다. 이 값이 정상 상태의 baseline이 된다.
