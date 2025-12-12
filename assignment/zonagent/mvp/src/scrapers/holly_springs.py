"""
Holly Springs (CivicClerk) 스크래퍼

Alpharetta와 동일한 CivicClerk 플랫폼 (코드 재사용)
"""

import logging

from ..models import Jurisdiction
from .alpharetta import AlpharettaScraper


logger = logging.getLogger(__name__)


class HollySpringScraper(AlpharettaScraper):
    """
    Holly Springs - CivicClerk SPA 플랫폼 스크래퍼

    Alpharetta와 100% 동일한 플랫폼
    URL만 변경하여 모든 로직 재사용
    """

    # 지자체 정보 (오버라이드)
    JURISDICTION = Jurisdiction.HOLLY_SPRINGS
    BASE_URL = "https://hollyspringsga.portal.civicclerk.com"

    # 나머지는 모두 Alpharetta 상속
    # - WAIT_FOR_SELECTOR
    # - SELECTORS
    # - DATE_PATTERNS
    # - 모든 파싱 메서드

    # 필요 시 Selector 오버라이드 가능
    # SELECTORS = {
    #     **AlpharettaScraper.SELECTORS,
    #     "meeting_items": ".custom-selector",  # Holly Springs 특화
    # }
