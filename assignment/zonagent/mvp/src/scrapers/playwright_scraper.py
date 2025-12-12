"""
Playwright 기반 스크래퍼 베이스 클래스

JavaScript SPA 렌더링이 필요한 지자체를 위한 공통 로직 제공
"""

import logging
import time
from typing import Optional

from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright, Browser, Page, TimeoutError as PlaywrightTimeoutError

from .base import BaseScraper


logger = logging.getLogger(__name__)


class PlaywrightScraper(BaseScraper):
    """
    Playwright 기반 스크래퍼 추상 베이스 클래스

    JavaScript SPA 플랫폼(예: CivicClerk)을 위한 브라우저 자동화
    """

    # 서브클래스에서 오버라이드
    WAIT_FOR_SELECTOR: Optional[str] = None  # 렌더링 완료 대기 Selector
    WAIT_TIMEOUT: int = 30000  # 대기 타임아웃 (ms)
    HEADLESS: bool = True  # Headless 모드

    def fetch_html_with_playwright(
        self,
        url: str,
        wait_for: Optional[str] = None,
        wait_timeout: Optional[int] = None
    ) -> str:
        """
        Playwright로 JavaScript 렌더링 후 HTML 가져오기

        Args:
            url: 가져올 URL
            wait_for: 대기할 CSS Selector (선택적)
            wait_timeout: 타임아웃 (ms, 선택적)

        Returns:
            렌더링된 HTML 문자열

        Raises:
            PlaywrightTimeoutError: 렌더링 타임아웃
        """
        wait_for = wait_for or self.WAIT_FOR_SELECTOR
        wait_timeout = wait_timeout or self.WAIT_TIMEOUT

        logger.info(f"Launching browser for {url}")
        start_time = time.time()

        with sync_playwright() as p:
            # 브라우저 실행
            browser = p.chromium.launch(headless=self.HEADLESS)

            try:
                # 새 페이지 생성
                page = browser.new_page()

                # 불필요한 리소스 차단 (성능 최적화)
                self._setup_resource_blocking(page)

                # 페이지 로드
                logger.info(f"Loading page: {url}")
                page.goto(url, wait_until="networkidle", timeout=wait_timeout)

                # 특정 요소 대기 (선택적)
                if wait_for:
                    logger.info(f"Waiting for selector: {wait_for}")
                    page.wait_for_selector(wait_for, timeout=wait_timeout)

                # 추가 안정화 대기 (선택적)
                time.sleep(0.5)

                # HTML 추출
                html = page.content()

                elapsed = time.time() - start_time
                logger.info(f"Page rendered successfully in {elapsed:.2f}s")
                logger.info(f"Received {len(html):,} bytes of HTML")

                return html

            except PlaywrightTimeoutError as e:
                logger.error(f"Timeout waiting for page render: {e}")
                raise

            except Exception as e:
                logger.error(f"Error fetching page: {e}")
                raise

            finally:
                # 브라우저 종료
                browser.close()

    def _setup_resource_blocking(self, page: Page):
        """
        불필요한 리소스 차단 (성능 최적화)

        이미지, 폰트, 미디어 등 렌더링에 불필요한 리소스 차단
        """
        def block_resources(route):
            resource_type = route.request.resource_type
            if resource_type in ["image", "media", "font", "stylesheet"]:
                # 차단
                route.abort()
            else:
                # 허용
                route.continue_()

        # 리소스 차단 활성화 (선택적)
        # page.route("**/*", block_resources)
        pass  # 현재는 비활성화 (필요시 주석 해제)

    def parse_html(self, html: str) -> BeautifulSoup:
        """
        HTML을 BeautifulSoup 객체로 파싱

        Args:
            html: HTML 문자열

        Returns:
            BeautifulSoup 객체
        """
        return BeautifulSoup(html, "lxml")

    def fetch_and_parse(
        self,
        url: str,
        wait_for: Optional[str] = None
    ) -> BeautifulSoup:
        """
        Playwright로 HTML 가져오고 BeautifulSoup로 파싱

        Args:
            url: 가져올 URL
            wait_for: 대기할 CSS Selector

        Returns:
            BeautifulSoup 객체
        """
        html = self.fetch_html_with_playwright(url, wait_for=wait_for)
        return self.parse_html(html)
