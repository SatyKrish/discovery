"""Client that calls the Temporal DeepAgent tool over MCP Streamable HTTP."""

import asyncio
from mcp.client.streamable_http import streamablehttp_client
from mcp.client.session import ClientSession


async def main() -> None:
    async with streamablehttp_client("http://127.0.0.1:8000/mcp") as (
        read_stream,
        write_stream,
        _,
    ):
        async with ClientSession(read_stream, write_stream) as session:
            await session.initialize()
            result = await session.call_tool(
                "ask",
                {"question": "List available banking tables"},
            )
            for item in result.content:
                if hasattr(item, "text"):
                    print(item.text)


if __name__ == "__main__":
    asyncio.run(main())
