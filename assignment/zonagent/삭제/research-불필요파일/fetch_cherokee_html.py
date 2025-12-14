#!/usr/bin/env python3
"""
Cherokee County Granicus 포털 HTML 구조 분석 스크립트

목적:
- 서버 렌더링된 HTML 직접 파싱
- CSS Selector 패턴 추출
- 문서 링크 구조 파악
- Playwright 불필요 (httpx + BeautifulSoup만 사용)
"""

import httpx
from bs4 import BeautifulSoup
from pathlib import Path
from datetime import datetime
import re
from typing import Dict, List, Optional


def fetch_and_analyze():
    """Cherokee County Granicus 포털 분석"""

    url = "https://cherokeega.granicus.com/ViewPublisher.php?view_id=1"
    output_dir = Path(__file__).parent / "html_samples"
    output_dir.mkdir(exist_ok=True)

    print("=" * 60)
    print("Cherokee County Granicus HTML 구조 분석 도구")
    print("=" * 60)

    # 1. HTML 가져오기 (httpx - 간단!)
    print(f"\n📡 페이지 가져오기: {url}")

    try:
        response = httpx.get(url, timeout=30.0, follow_redirects=True)
        response.raise_for_status()
        html_content = response.text

        print(f"✅ HTML 수신 완료")
        print(f"   상태 코드: {response.status_code}")
        print(f"   파일 크기: {len(html_content):,} bytes")

    except Exception as e:
        print(f"❌ 오류 발생: {e}")
        return

    # 2. HTML 파일 저장
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    html_file = output_dir / f"cherokee_granicus_{timestamp}.html"
    html_file.write_text(html_content, encoding="utf-8")
    print(f"✅ HTML 저장: {html_file}")

    # 3. BeautifulSoup으로 파싱
    print("\n🔍 HTML 구조 분석:")
    soup = BeautifulSoup(html_content, "html.parser")

    # 4. 테이블 찾기
    table = soup.find("table", class_="listingTable")
    if not table:
        print("❌ listingTable을 찾을 수 없습니다.")
        return

    print(f"✅ 회의 테이블 발견: <table class='listingTable'>")

    # 5. 헤더 분석
    header_row = table.find("tr", class_="listHeader")
    if header_row:
        headers = [th.get_text(strip=True) for th in header_row.find_all("td")]
        print(f"✅ 테이블 헤더: {headers}")

    # 6. 회의 행 분석
    meeting_rows = table.find_all("tr", class_="listingRow")
    print(f"✅ 회의 행 발견: {len(meeting_rows)}개")

    if not meeting_rows:
        print("⚠️  회의 데이터가 없습니다.")
        return

    # 7. 첫 번째 회의 상세 분석
    print("\n📋 첫 번째 회의 상세 분석:")
    first_row = meeting_rows[0]

    cells = first_row.find_all("td", class_="listItem")
    if len(cells) >= 5:
        print(f"  이름: {cells[0].get_text(strip=True)}")
        print(f"  날짜: {cells[1].get_text(strip=True)}")

        # Agenda 링크
        agenda_link = cells[2].find("a")
        if agenda_link:
            print(f"  Agenda: {agenda_link.get('href', 'N/A')}")

        # Minutes 링크
        minutes_link = cells[3].find("a")
        if minutes_link:
            print(f"  Minutes: {minutes_link.get('href', 'N/A')}")

        # Video 링크
        video_link = cells[4].find("a")
        if video_link:
            print(f"  Video: {video_link.get('href', 'N/A')}")

    # 8. 샘플 행 HTML 저장
    sample_file = output_dir / f"cherokee_sample_row_{timestamp}.html"
    sample_file.write_text(str(first_row), encoding="utf-8")
    print(f"\n✅ 샘플 행 저장: {sample_file}")

    # 9. CSS Selector 추출 및 검증
    print("\n🎯 CSS Selector 검증:")

    selectors = {
        "meeting_table": "table.listingTable",
        "header_row": "tr.listHeader",
        "meeting_rows": "tr.listingRow",
        "meeting_name": "td.listItem:nth-child(1)",
        "meeting_date": "td.listItem:nth-child(2)",
        "agenda_link": "td.listItem:nth-child(3) a",
        "minutes_link": "td.listItem:nth-child(4) a",
        "video_link": "td.listItem:nth-child(5) a",
    }

    for name, selector in selectors.items():
        try:
            elements = soup.select(selector)
            print(f"  ✅ {name:20s}: {selector:40s} → {len(elements)}개")
        except Exception as e:
            print(f"  ❌ {name:20s}: {selector:40s} → 오류: {e}")

    # 10. 날짜 패턴 분석
    print("\n📅 날짜 형식 분석:")

    date_pattern = r"(\w+)\s+(\d{1,2}),\s+(\d{4})\s+-\s+(\d{1,2}):(\d{2})\s+(AM|PM)"
    dates_found = []

    for row in meeting_rows[:5]:  # 처음 5개만
        date_cell = row.find_all("td", class_="listItem")[1]
        date_text = date_cell.get_text(strip=True)

        match = re.match(date_pattern, date_text)
        if match:
            dates_found.append({
                "text": date_text,
                "month": match.group(1),
                "day": match.group(2),
                "year": match.group(3),
                "hour": match.group(4),
                "minute": match.group(5),
                "ampm": match.group(6),
            })

    if dates_found:
        print(f"  ✅ 날짜 패턴 매칭: {len(dates_found)}/{min(5, len(meeting_rows))}")
        print(f"  예시: {dates_found[0]['text']}")
        print(f"  정규식: {date_pattern}")
    else:
        print("  ⚠️  날짜 패턴 매칭 실패")

    # 11. 링크 패턴 분석
    print("\n🔗 문서 링크 패턴 분석:")

    link_patterns = {
        "agenda": [],
        "minutes": [],
        "video": [],
    }

    for row in meeting_rows[:10]:  # 처음 10개만
        cells = row.find_all("td", class_="listItem")

        if len(cells) >= 5:
            # Agenda
            agenda = cells[2].find("a")
            if agenda and agenda.get("href"):
                link_patterns["agenda"].append(agenda["href"])

            # Minutes
            minutes = cells[3].find("a")
            if minutes and minutes.get("href"):
                link_patterns["minutes"].append(minutes["href"])

            # Video
            video = cells[4].find("a")
            if video and video.get("href"):
                link_patterns["video"].append(video["href"])

    for doc_type, links in link_patterns.items():
        unique_patterns = set()
        for link in links:
            # URL 패턴 추출 (파라미터 제외)
            if "?" in link:
                base = link.split("?")[0]
                unique_patterns.add(base)
            else:
                unique_patterns.add(link)

        print(f"\n  {doc_type.upper()}:")
        print(f"    총 {len(links)}개 링크")
        if links:
            print(f"    예시: {links[0][:80]}")
            if len(unique_patterns) > 1:
                print(f"    패턴: {len(unique_patterns)}가지")

    # 12. 통계
    print("\n📊 분석 통계:")
    print(f"  전체 회의: {len(meeting_rows)}개")
    print(f"  Agenda 링크: {len(link_patterns['agenda'])}개")
    print(f"  Minutes 링크: {len(link_patterns['minutes'])}개")
    print(f"  Video 링크: {len(link_patterns['video'])}개")

    # 13. 결과 요약 저장
    summary_file = output_dir / f"cherokee_analysis_{timestamp}.txt"
    with summary_file.open("w", encoding="utf-8") as f:
        f.write("Cherokee County Granicus 분석 결과\n")
        f.write("=" * 60 + "\n\n")
        f.write(f"URL: {url}\n")
        f.write(f"분석 시간: {datetime.now()}\n\n")
        f.write(f"전체 회의: {len(meeting_rows)}개\n")
        f.write(f"Agenda: {len(link_patterns['agenda'])}개\n")
        f.write(f"Minutes: {len(link_patterns['minutes'])}개\n")
        f.write(f"Video: {len(link_patterns['video'])}개\n\n")
        f.write("CSS Selectors:\n")
        for name, selector in selectors.items():
            f.write(f"  {name}: {selector}\n")
        f.write(f"\n날짜 정규식: {date_pattern}\n")

    print(f"\n✅ 분석 요약 저장: {summary_file}")
    print("\n✅ 분석 완료!")


if __name__ == "__main__":
    fetch_and_analyze()
