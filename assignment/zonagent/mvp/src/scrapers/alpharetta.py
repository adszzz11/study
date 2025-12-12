"""
Alpharetta (CivicClerk) 스크래퍼

CivicClerk SPA 플랫폼 지원 (JavaScript 렌더링 필요)
"""

import logging
import re
from datetime import datetime, date
from typing import Optional

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

    # Playwright 설정
    WAIT_FOR_SELECTOR = ".meeting-list, [data-meetings], .meetings, .agenda-list"  # 여러 후보
    WAIT_TIMEOUT = 30000  # 30초
    HEADLESS = True

    # CSS Selectors (로컬 테스트 후 조정 필요)
    # CivicClerk의 일반적인 패턴 가정
    SELECTORS = {
        # 회의 목록 컨테이너 (여러 후보)
        "meeting_container": ".meeting-list, [data-meetings], .meetings, .agenda-list, main",

        # 개별 회의 아이템 (여러 후보)
        "meeting_items": ".meeting-item, .meeting, article, .agenda-item, [data-meeting]",

        # 회의 날짜
        "meeting_date": ".meeting-date, .date, time, .meeting-time, [data-date]",

        # 회의 제목
        "meeting_title": ".meeting-title, .title, h2, h3, .meeting-name",

        # 문서 링크 컨테이너
        "documents_container": ".documents, .attachments, .files, .meeting-documents",

        # 개별 문서 링크
        "document_links": "a[href*='agenda'], a[href*='minutes'], a[href*='packet'], a[href*='.pdf']",
    }

    # 날짜 파싱 패턴 (다양한 형식 지원)
    DATE_PATTERNS = [
        # "December 12, 2025" 또는 "Dec 12, 2025"
        (r"(\w+)\s+(\d{1,2}),?\s+(\d{4})", "%B %d %Y"),
        # "12/12/2025"
        (r"(\d{1,2})/(\d{1,2})/(\d{4})", "%m/%d/%Y"),
        # "2025-12-12"
        (r"(\d{4})-(\d{2})-(\d{2})", "%Y-%m-%d"),
    ]

    def get_base_url(self) -> str:
        """베이스 URL 반환"""
        return self.BASE_URL

    def scrape(self, limit: Optional[int] = None) -> DocumentList:
        """
        CivicClerk 플랫폼에서 문서 스크래핑

        Args:
            limit: 최대 수집 개수 (선택적)

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
        documents = self._parse_meetings(soup)

        # 제한 적용
        if limit:
            documents = documents[:limit]
            logger.info(f"Limited to {limit} documents")

        logger.info(f"Successfully parsed {len(documents)} documents")
        return documents

    def _parse_meetings(self, soup: BeautifulSoup) -> DocumentList:
        """
        회의 목록 파싱

        Args:
            soup: BeautifulSoup 객체

        Returns:
            Document 리스트
        """
        documents: DocumentList = []

        # 회의 컨테이너 찾기 (여러 Selector 시도)
        container = None
        for selector in self.SELECTORS["meeting_container"].split(", "):
            container = soup.select_one(selector.strip())
            if container:
                logger.info(f"Found meeting container with selector: {selector}")
                break

        if not container:
            logger.warning("No meeting container found")
            return documents

        # 회의 아이템 찾기 (여러 Selector 시도)
        meeting_items = []
        for selector in self.SELECTORS["meeting_items"].split(", "):
            meeting_items = container.select(selector.strip())
            if meeting_items:
                logger.info(f"Found {len(meeting_items)} meetings with selector: {selector}")
                break

        if not meeting_items:
            logger.warning("No meeting items found")
            return documents

        # 각 회의 아이템 처리
        for item in meeting_items:
            try:
                item_docs = self._parse_meeting_item(item)
                documents.extend(item_docs)
            except Exception as e:
                logger.error(f"Error parsing meeting item: {e}", exc_info=True)
                continue

        return documents

    def _parse_meeting_item(self, item) -> DocumentList:
        """
        개별 회의 아이템 파싱

        Args:
            item: BeautifulSoup 회의 아이템

        Returns:
            해당 회의의 Document 리스트
        """
        documents: DocumentList = []

        # 회의 날짜 추출
        meeting_date = self._extract_meeting_date(item)
        if not meeting_date:
            logger.warning("No meeting date found, skipping item")
            return documents

        # 회의 제목 추출
        meeting_title = self._extract_meeting_title(item)
        if not meeting_title:
            meeting_title = "Untitled Meeting"

        # 문서 링크 추출
        doc_links = self._extract_document_links(item)

        # 각 문서 링크를 Document 객체로 변환
        for link in doc_links:
            href = link.get("href", "")
            if not href:
                continue

            # 상대 URL -> 절대 URL
            if href.startswith("/"):
                href = self.BASE_URL.rstrip("/") + href
            elif not href.startswith("http"):
                href = self.BASE_URL.rstrip("/") + "/" + href.lstrip("/")

            # 문서 타입 판별
            doc_type = self._determine_doc_type(href, link)
            if not doc_type:
                continue

            # 문서 제목
            doc_title = link.get_text(strip=True) or f"{meeting_title} - {doc_type.value}"

            # Document 객체 생성
            doc = Document(
                url=href,
                title=doc_title,
                doc_type=doc_type,
                meeting_date=meeting_date,
                jurisdiction=self.JURISDICTION,
            )
            documents.append(doc)

        return documents

    def _extract_meeting_date(self, item) -> Optional[date]:
        """
        회의 날짜 추출 및 파싱

        Args:
            item: BeautifulSoup 회의 아이템

        Returns:
            datetime.date 객체 또는 None
        """
        # 날짜 요소 찾기 (여러 Selector 시도)
        date_elem = None
        for selector in self.SELECTORS["meeting_date"].split(", "):
            date_elem = item.select_one(selector.strip())
            if date_elem:
                break

        if not date_elem:
            return None

        # 텍스트 추출
        date_text = date_elem.get_text(strip=True)

        # datetime 속성 확인 (HTML5 time 태그)
        if date_elem.name == "time" and date_elem.get("datetime"):
            date_text = date_elem["datetime"]

        # 여러 패턴으로 파싱 시도
        for pattern, fmt in self.DATE_PATTERNS:
            match = re.search(pattern, date_text)
            if match:
                try:
                    # 전체 매치 텍스트 사용
                    date_str = match.group(0)
                    parsed_date = datetime.strptime(date_str, fmt).date()
                    return parsed_date
                except ValueError:
                    continue

        logger.warning(f"Could not parse date: {date_text}")
        return None

    def _extract_meeting_title(self, item) -> Optional[str]:
        """
        회의 제목 추출

        Args:
            item: BeautifulSoup 회의 아이템

        Returns:
            회의 제목 또는 None
        """
        # 제목 요소 찾기 (여러 Selector 시도)
        for selector in self.SELECTORS["meeting_title"].split(", "):
            title_elem = item.select_one(selector.strip())
            if title_elem:
                return title_elem.get_text(strip=True)

        return None

    def _extract_document_links(self, item) -> list:
        """
        문서 링크 추출

        Args:
            item: BeautifulSoup 회의 아이템

        Returns:
            링크 요소 리스트
        """
        # 문서 컨테이너 찾기 (선택적)
        doc_container = item
        for selector in self.SELECTORS["documents_container"].split(", "):
            container = item.select_one(selector.strip())
            if container:
                doc_container = container
                break

        # 문서 링크 찾기
        links = doc_container.select(self.SELECTORS["document_links"])
        return links

    def _determine_doc_type(self, href: str, link_elem) -> Optional[DocumentType]:
        """
        URL과 링크 텍스트로 문서 타입 판별

        Args:
            href: 링크 URL
            link_elem: BeautifulSoup 링크 요소

        Returns:
            DocumentType 또는 None
        """
        href_lower = href.lower()
        text_lower = link_elem.get_text(strip=True).lower()

        # Minutes
        if "minutes" in href_lower or "minutes" in text_lower:
            return DocumentType.MINUTES

        # Packet
        if "packet" in href_lower or "packet" in text_lower:
            return DocumentType.PACKET

        # Agenda (기본값)
        if "agenda" in href_lower or "agenda" in text_lower:
            return DocumentType.AGENDA

        # PDF 파일이지만 타입 불명확 -> Agenda로 가정
        if ".pdf" in href_lower:
            return DocumentType.AGENDA

        # 알 수 없음
        logger.warning(f"Unknown document type: {href}")
        return None
