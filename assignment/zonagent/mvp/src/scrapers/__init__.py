"""
스크래퍼 모듈

BaseScraper와 각 지자체별 스크래퍼 구현을 포함합니다.
"""

from .base import BaseScraper
from .cherokee import CherokeeScraper
from .marietta import MariettaScraper
from .alpharetta import AlpharettaScraper
from .holly_springs import HollySpringScraper

__all__ = [
    "BaseScraper",
    "CherokeeScraper",
    "MariettaScraper",
    "AlpharettaScraper",
    "HollySpringScraper",
]


def get_scraper(jurisdiction_name: str):
    """
    지자체 이름으로 스크래퍼 인스턴스 생성 (팩토리 패턴)

    Args:
        jurisdiction_name: 지자체 코드 ("cherokee", "marietta", "alpharetta", "holly_springs")

    Returns:
        BaseScraper 인스턴스

    Raises:
        ValueError: 지원하지 않는 지자체
    """
    scrapers = {
        "cherokee": CherokeeScraper,
        "marietta": MariettaScraper,
        "alpharetta": AlpharettaScraper,
        "holly_springs": HollySpringScraper,
    }

    scraper_class = scrapers.get(jurisdiction_name.lower())
    if not scraper_class:
        raise ValueError(
            f"Unsupported jurisdiction: {jurisdiction_name}. "
            f"Supported: {', '.join(scrapers.keys())}"
        )

    return scraper_class()
