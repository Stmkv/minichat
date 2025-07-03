import asyncio

CHAT_HOST = 'minechat.dvmn.org'
CHAT_PORT = '5000'
MAX_READE_BYTES = 100

async def tcp_echo_client():
    reader, writer = await asyncio.open_connection(
        host=CHAT_HOST,
        port=CHAT_PORT,
    )
    while True:
        data = await reader.read(MAX_READE_BYTES)
        try:
            decode_data = data.decode(encoding="utf-8")
            print(decode_data.replace('\n', ''))
        except UnicodeDecodeError:
            continue
        if not data:
            break

    print('Close the connection')
    writer.close()
    await writer.wait_closed()


async def main():
    await tcp_echo_client()


try:
    asyncio.run(main())
except KeyboardInterrupt:
    print("👋")
