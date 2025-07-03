import argparse
import asyncio
from datetime import datetime

import aiofiles
import configargparse

MAX_READE_BYTES = 100


async def write_file(message, file_path: str) -> None:
    async with aiofiles.open(file_path, "a") as file:
        time_now = datetime.today().strftime("[%d.%m.%Y %H:%M]")
        await file.write(f"{time_now} {message}")


async def tcp_echo_client(args: argparse.Namespace) -> None:
    reader, writer = await asyncio.open_connection(
        host=args.host,
        port=args.port,
    )
    try:
        while True:
            data = await reader.read(MAX_READE_BYTES)
            if not data:
                break
            try:
                decode_message = data.decode(encoding="utf-8")
                print(decode_message.replace("\n", ""))
                await write_file(decode_message, args.history)
            except UnicodeDecodeError:
                continue
    finally:
        writer.close()
        await writer.wait_closed()


async def main() -> None:
    parser = configargparse.ArgParser(default_config_files=['argparse_config.txt'])
    parser.add('--host', help='host to connect', env_var='MYAPP_HOST', default='minechat.dvmn.org')
    parser.add('--port', type=int, help='port number', default=5000)
    parser.add('--history', help='history file', default='minechat.history')
    args = parser.parse_args()

    await tcp_echo_client(args)


try:
    asyncio.run(main())
except KeyboardInterrupt:
    print("👋")
