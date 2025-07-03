import asyncio
import aiofiles
from datetime import datetime

CHAT_HOST = 'minechat.dvmn.org'
CHAT_PORT = 5000
MAX_READE_BYTES = 100


async def write_file(message):
    async with aiofiles.open('message.txt', 'a') as file:
        time_now = datetime.today().strftime("[%d.%m.%Y %H:%M]")
        await file.write(f"{time_now} {message}")


async def tcp_echo_client():
    reader, writer = await asyncio.open_connection(
        host=CHAT_HOST,
        port=CHAT_PORT,
    )
    try:
        while True:
            data = await reader.read(MAX_READE_BYTES)
            if not data:
                break
            try:
                decode_message = data.decode(encoding="utf-8")
                print(decode_message.replace("\n", ""))
                await write_file(decode_message)
            except UnicodeDecodeError:
                continue
    finally:
        writer.close()
        await writer.wait_closed()


async def main():
    await tcp_echo_client()


try:
    asyncio.run(main())
except KeyboardInterrupt:
    print("👋")
