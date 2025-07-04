import argparse
import asyncio

import configargparse
import os
import logging
from logger.logger_setup import setup_logging
from dotenv import load_dotenv

setup_logging()
logger = logging.getLogger("sender")

MAX_READE_BYTES = 100


async def login_hash(hash: str, writer):
    writer.write(f"{hash}\n\n".encode())
    await writer.drain()


async def tcp_echo_client(args: argparse.Namespace) -> None:
    reader, writer = await asyncio.open_connection(
        host=args.host,
        port=args.port,
    )

    if args.password:
        await login_hash(args.password, writer)
    else:
        hash = input("Введите хеш для авторизации: \n")
        await login_hash(hash, writer)

    try:
        while True:
            message = input("Введите сообщение для отправки:\n")
            writer.write(f"{message}\n\n".encode())
            await writer.drain()
    finally:
        writer.close()
        await writer.wait_closed()


async def main() -> None:
    current_dir = os.path.dirname(os.path.abspath(__file__))
    config_path = os.path.join(current_dir, 'configs', 'argparse_config_sender.txt')

    load_dotenv()
    parser = configargparse.ArgParser(default_config_files=[config_path])
    parser.add('--host', help='host to connect', default='minechat.dvmn.org')
    parser.add('--port', type=int, help='port number', default=5050)
    parser.add('--password', help='personal hash for chat', default=os.getenv("CHAT_PASSWORD"))
    args, unknown = parser.parse_known_args()
    await tcp_echo_client(args)


try:
    asyncio.run(main())
except KeyboardInterrupt:
    print("👋")
