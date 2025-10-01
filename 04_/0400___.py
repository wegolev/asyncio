import aiohttp
import asyncio

async def websocket_client():
    session = aiohttp.ClientSession()
    async with session.ws_connect('http://localhost:8080/ws') as ws:
        await ws.send_str("Hello, server")
        async for msg in ws:
            if msg.type == aiohttp.WSMsgType.TEXT:
                print(f"Message from server: {msg.data}")
                break

    await session.close()

asyncio.run(websocket_client())