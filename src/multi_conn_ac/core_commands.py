import json
from typing import Any
import aiohttp

from multi_conn_ac.basic_types import Port
from multi_conn_ac.async_utils import sync_or_async


class CoreCommands:

    _BASE_URL: str = "http://127.0.0.1"

    def __init__(self, port: Port):
        self.port: Port = port

    @sync_or_async
    async def post_command(self, command: str, parameters: dict | None = None) -> dict[str, Any]:
        if parameters is None:
            parameters = {}
        url = f"{self._BASE_URL:}:{self.port}"
        json_str = json.dumps({"command": command,
                               "parameters": parameters}).encode("utf8")
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=json.loads(json_str)) as response:
                result = await response.text()
                return json.loads(result)

    @sync_or_async
    async def post_tapir_command(self, command: str, parameters: dict | None = None) -> dict[str, Any]:
        if parameters is None:
            parameters = {}
        return await self.post_command(
                command="API.ExecuteAddOnCommand",
                parameters={"addOnCommandId": {
                                "commandNamespace": 'TapirCommand',
                                "commandName": command},
                            'addOnCommandParameters': parameters})


