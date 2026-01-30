"""Base HTTP client for API calls."""

import httpx


class BaseClient:
    """基础 HTTP 客户端 / Base HTTP Client"""

    def __init__(self, timeout: float = 10.0):
        """Initialize HTTP client.

        Args:
            timeout: Request timeout in seconds
        """
        self.client = httpx.Client(
            timeout=timeout,
            headers={
                "User-Agent": (
                    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) "
                    "Chrome/120.0.0.0 Safari/537.36"
                )
            },
            follow_redirects=True,
        )

    def get(self, url: str, **kwargs) -> httpx.Response:
        """发送 GET 请求 / Send GET request.

        Args:
            url: Target URL
            **kwargs: Additional arguments for httpx.get

        Returns:
            HTTP response

        Raises:
            httpx.HTTPError: If request fails
        """
        return self.client.get(url, **kwargs)

    def __del__(self):
        """关闭客户端连接 / Close client connection."""
        if hasattr(self, "client"):
            self.client.close()
