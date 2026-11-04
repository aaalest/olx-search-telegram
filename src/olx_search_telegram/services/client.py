import httpx
from pydantic import TypeAdapter, ValidationError

from olx_search_telegram.services.models import ScheduleJob


_schedules_adapter = TypeAdapter(list[ScheduleJob])


class SearchApiClientError(Exception):
    """Base exception for API client errors."""


class SearchApiClient:
    def __init__(self, base_url: str, timeout: float = 10.0) -> None:
        self.base_url = base_url.rstrip("/")
        self._client: httpx.AsyncClient | None = None
        self._timeout = timeout

    def is_alive(self) -> bool:
        return not (self._client is None or self._client.is_closed)

    async def start(self) -> None:
        """Initialize the persistent connection pool."""
        if self._client is None or self._client.is_closed:
            self._client = httpx.AsyncClient(
                base_url=self.base_url,
                timeout=self._timeout,
            )

    async def close(self) -> None:
        """Close the underlying connection pool."""
        if self._client and not self._client.is_closed:
            await self._client.aclose()

    async def get_schedules(self) -> list[ScheduleJob]:
        if not self.is_alive():
            raise SearchApiClientError("HTTP client is not started.")

        try:
            response = await self._client.get("/schedules")
            response.raise_for_status()
            data = response.json()
            return _schedules_adapter.validate_python(data)

        except httpx.HTTPStatusError as exc:
            raise SearchApiClientError(
                f"API returned status {exc.response.status_code}"
            ) from exc
        except (httpx.RequestError, ValidationError) as exc:
            raise SearchApiClientError(f"Request failed: {exc}") from exc
