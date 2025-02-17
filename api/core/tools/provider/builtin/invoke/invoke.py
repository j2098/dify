from typing import Any

import httpx

from core.tools.errors import ToolProviderCredentialValidationError
from core.tools.provider.builtin_tool_provider import BuiltinToolProviderController


class InvokeProvider(BuiltinToolProviderController):
    def _validate_credentials(self, credentials: dict[str, Any]) -> None:
        base_url = credentials.get("base_url")
        api_key = credentials.get("api_key")
        if not base_url or not api_key: 
            raise ToolProviderCredentialValidationError("base_url and api_key are required")

        res = httpx.get(url=f'{base_url}/api/v1/checked', headers={"Authorization": f"Bearer {api_key}"})
        if res.status_code != 200:
            raise ToolProviderCredentialValidationError("invalid api_key")
