"""
Alpharetta (CivicClerk) 스크래퍼

CivicClerk SPA 플랫폼 지원 (JavaScript 렌더링 필요)
"""

import logging
import re
from datetime import datetime, date
from typing import Optional
from urllib.parse import urljoin

from bs4 import BeautifulSoup

from ..models import Document, DocumentType, Jurisdiction, DocumentList
from .playwright_scraper import PlaywrightScraper


logger = logging.getLogger(__name__)


class AlpharettaScraper(PlaywrightScraper):
    """
    Alpharetta - CivicClerk SPA 플랫폼 스크래퍼

    JavaScript 렌더링이 필요한 Modern SPA
    """

    # 지자체 정보
    JURISDICTION = Jurisdiction.ALPHARETTA
    BASE_URL = "https://alpharettaga.portal.civicclerk.com"

    # Playwright 설정 - 실제 HTML 구조에 맞춤
    WAIT_FOR_SELECTOR = "a[data-id]"  # 이벤트 링크들이 로드될 때까지 기다림
    WAIT_TIMEOUT = 30000  # 30초
    HEADLESS = True

    def __init__(self):
        """Initialize Alpharetta scraper"""
        super().__init__(Jurisdiction.ALPHARETTA)

    def get_base_url(self) -> str:
        """베이스 URL 반환"""
        return self.BASE_URL

    def scrape(self, limit: Optional[int] = None) -> DocumentList:
        """
        CivicClerk 플랫폼에서 문서 스크래핑

        Args:
            limit: 최대 수집 개수 (회의 수 제한)

        Returns:
            Document 리스트
        """
        logger.info(f"Starting scrape for {self.JURISDICTION.value}")

        # Playwright로 페이지 로드 및 파싱
        logger.info(f"Fetching page: {self.BASE_URL}")
        soup = self.fetch_and_parse(
            self.BASE_URL,
            wait_for=self.WAIT_FOR_SELECTOR
        )

        # 회의 목록 추출
        documents = self._parse_meetings(soup, limit=limit)

        logger.info(f"Successfully parsed {len(documents)} documents")
        return documents

    def _parse_meetings(self, soup: BeautifulSoup, limit: Optional[int] = None) -> DocumentList:
        """
        회의 목록 파싱

        Args:
            soup: BeautifulSoup 객체
            limit: 최대 수집할 회의 개수

        Returns:
            Document 리스트
        """
        documents: DocumentList = []

        # 이벤트 링크 찾기: <a data-id="..." href="/event/.../files">
        event_links = soup.select('a[data-id][href*="/event/"][href*="/files"]')

        if not event_links:
            logger.warning("No event links found")
            return documents

        logger.info(f"Found {len(event_links)} events")

        # 제한 적용
        if limit:
            event_links = event_links[:limit]

        # 각 이벤트 링크 처리
        for event_link in event_links:
            try:
                docs = self._parse_event_link(event_link, soup)
                documents.extend(docs)
            except Exception as e:
                logger.error(f"Error parsing event: {e}", exc_info=True)
                continue

        return documents

    def _parse_event_link(self, event_link, soup: BeautifulSoup) -> DocumentList:
        """
        개별 이벤트 링크 파싱

        Args:
            event_link: BeautifulSoup 이벤트 링크 요소
            soup: 전체 페이지 BeautifulSoup

        Returns:
            해당 이벤트의 Document 리스트
        """
        documents: DocumentList = []

        # 이벤트 ID 추출
        event_id = event_link.get("data-id")
        if not event_id:
            logger.warning("No event ID found")
            return documents

        # 이벤트 URL 추출
        event_url = event_link.get("href")
        if not event_url:
            logger.warning(f"No URL for event {event_id}")
            return documents

        # 절대 URL로 변환
        event_url = urljoin(self.BASE_URL, event_url)

        # 이벤트 행 찾기: id="eventListRow-{event_id}" 또는 data-testid="row"인 div
        event_row = soup.find("div", id=f"eventListRow-{event_id}")
        if not event_row:
            logger.warning(f"No event row found for event {event_id}")
            return documents

        # 날짜 추출 - data-date 속성 (ISO format: "2025-12-02T17:30:00Z")
        date_str = event_row.get("data-date")
        meeting_date = None
        if date_str:
            try:
                # ISO 8601 형식 파싱
                meeting_date = datetime.fromisoformat(date_str.replace('Z', '+00:00')).date()
            except Exception as e:
                logger.warning(f"Failed to parse date {date_str}: {e}")

        # 제목 추출 - id="eventListRow-{event_id}-title"인 h3 요소
        title_elem = soup.find("h3", id=f"eventListRow-{event_id}-title")
        meeting_title = title_elem.get_text(strip=True) if title_elem else f"Event {event_id}"

        # 문서 타입은 PACKET으로 통일 (files 페이지에 모든 문서가 있음)
        doc = Document(
            url=event_url,
            title=f"{meeting_title} - Files",
            doc_type=DocumentType.PACKET,
            meeting_date=meeting_date,
            jurisdiction=self.JURISDICTION,
        )
        documents.append(doc)

        return documents
