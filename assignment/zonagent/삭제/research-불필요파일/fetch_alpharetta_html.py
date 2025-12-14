#!/usr/bin/env python3
"""
Alpharetta CivicClerk 포털 HTML 구조 분석 스크립트

목적:
- JavaScript로 렌더링된 실제 HTML 구조 확인
- CSS Selector 패턴 추출
- 문서 링크 구조 파악
"""

import asyncio
from playwright.async_api import async_playwright
from pathlib import Path
from datetime import datetime


async def fetch_and_save_html():
    """Alpharetta CivicClerk 포털의 렌더링된 HTML 가져오기"""

    url = "https://alpharettaga.portal.civicclerk.com"
    output_dir = Path(__file__).parent / "html_samples"
    output_dir.mkdir(exist_ok=True)

    async with async_playwright() as p:
        print(f"🚀 Playwright 시작...")
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()

        print(f"📡 페이지 로딩: {url}")
        await page.goto(url, wait_until="networkidle")

        # JavaScript 렌더링 대기 (추가 시간)
        print("⏳ JavaScript 렌더링 대기...")
        await page.wait_for_timeout(3000)

        # 전체 HTML 저장
        html_content = await page.content()
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        html_file = output_dir / f"alpharetta_portal_{timestamp}.html"

        html_file.write_text(html_content, encoding="utf-8")
        print(f"✅ HTML 저장 완료: {html_file}")
        print(f"   파일 크기: {len(html_content):,} bytes")

        # 스크린샷 저장 (시각적 확인용)
        screenshot_file = output_dir / f"alpharetta_portal_{timestamp}.png"
        await page.screenshot(path=str(screenshot_file), full_page=True)
        print(f"📸 스크린샷 저장: {screenshot_file}")

        # 기본 구조 분석
        print("\n🔍 페이지 구조 분석:")

        # 회의 항목 찾기 (일반적인 패턴들)
        selectors_to_try = [
            "table.meeting-list tr",
            ".meeting-item",
            ".meeting-row",
            "[data-meeting-id]",
            "ul.meetings li",
            ".agenda-item",
        ]

        for selector in selectors_to_try:
            try:
                elements = await page.query_selector_all(selector)
                if elements:
                    print(f"  ✅ '{selector}': {len(elements)}개 발견")

                    # 첫 번째 항목의 HTML 샘플 저장
                    if elements:
                        first_html = await elements[0].inner_html()
                        sample_file = output_dir / f"sample_meeting_item_{timestamp}.html"
                        sample_file.write_text(first_html, encoding="utf-8")
                        print(f"     샘플 저장: {sample_file}")
            except Exception as e:
                print(f"  ❌ '{selector}': {str(e)}")

        # 링크 분석
        print("\n🔗 문서 링크 분석:")
        links = await page.query_selector_all("a[href*='agenda'], a[href*='minutes'], a[href*='packet']")
        print(f"  문서 관련 링크: {len(links)}개")

        if links:
            for i, link in enumerate(links[:5]):  # 처음 5개만
                href = await link.get_attribute("href")
                text = await link.inner_text()
                print(f"    {i+1}. {text[:50]:50s} -> {href}")

        await browser.close()
        print("\n✅ 분석 완료!")


async def analyze_saved_html():
    """저장된 HTML 파일 분석 (BeautifulSoup)"""
    from bs4 import BeautifulSoup

    output_dir = Path(__file__).parent / "html_samples"
    html_files = sorted(output_dir.glob("alpharetta_portal_*.html"))

    if not html_files:
        print("❌ 저장된 HTML 파일이 없습니다. 먼저 fetch_and_save_html()을 실행하세요.")
        return

    latest_file = html_files[-1]
    print(f"📂 분석 대상: {latest_file.name}")

    html_content = latest_file.read_text(encoding="utf-8")
    soup = BeautifulSoup(html_content, "html.parser")

    print("\n📊 HTML 구조 분석:")
    print(f"  전체 태그 수: {len(soup.find_all(True))}")

    # 주요 컨테이너 찾기
    main_containers = [
        ("main", soup.find_all("main")),
        ("div.container", soup.select("div.container")),
        ("div.content", soup.select("div.content")),
        ("section", soup.find_all("section")),
    ]

    for name, elements in main_containers:
        if elements:
            print(f"  {name}: {len(elements)}개")

    # 테이블 분석
    tables = soup.find_all("table")
    if tables:
        print(f"\n📋 테이블 분석: {len(tables)}개")
        for i, table in enumerate(tables[:3]):
            rows = table.find_all("tr")
            print(f"  테이블 {i+1}: {len(rows)}개 행")

    # 날짜 패턴 찾기
    import re
    date_patterns = [
        r"\d{1,2}/\d{1,2}/\d{4}",  # MM/DD/YYYY
        r"\d{4}-\d{2}-\d{2}",      # YYYY-MM-DD
        r"[A-Z][a-z]+ \d{1,2}, \d{4}",  # January 1, 2024
    ]

    print("\n📅 날짜 패턴 분석:")
    for pattern in date_patterns:
        matches = re.findall(pattern, html_content)
        if matches:
            print(f"  {pattern}: {len(set(matches))}개 고유 날짜")
            print(f"    예시: {list(set(matches))[:3]}")


if __name__ == "__main__":
    print("=" * 60)
    print("Alpharetta CivicClerk HTML 구조 분석 도구")
    print("=" * 60)

    # 1단계: Playwright로 렌더링된 HTML 가져오기
    asyncio.run(fetch_and_save_html())

    # 2단계: BeautifulSoup로 구조 분석
    print("\n" + "=" * 60)
    asyncio.run(analyze_saved_html())
