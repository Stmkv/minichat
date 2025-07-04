import argparse
import asyncio
import json
import logging
import os

import configargparse
from colorama import Fore, Style, init
from dotenv import load_dotenv

from logger.logger_setup import setup_logging
from utils import logging_user_data

setup_logging()
logger = logging.getLogger("sender")

init(autoreset=True)


async def authorise(
    hash: str, writer: asyncio.StreamWriter, reader: asyncio.StreamReader
) -> None:
    response = await reader.readuntil(b"\n")
    logger.info(response)

    writer.write(f"{hash}\n".encode())
    await writer.drain()

    response = await reader.readuntil(b"\n")
    logger.info(response)
    if response == b"null\n":
        print(
            Fore.RED
            + "Был указан неверный токен, зарегистрируйте нового пользователя, либо измените токен"
        )
        response = await register_with_unknown_hash(writer, reader)
    return response


async def register_with_unknown_hash(
    writer: asyncio.StreamWriter, reader: asyncio.StreamReader
) -> dict:
    """Функция обрабатывает случай когда пользователь ввел неправильный пароль."""
    response = await reader.readuntil(b"\n")
    logger.info(response.decode().strip())

    nickname = input("Введите ник для регистрации:")
    writer.write(f"{nickname}\n".encode())
    await writer.drain()

    response = await reader.readuntil(b"\n")
    json_response = json.loads(response.decode())

    logging_user_data(json_response)

    return json_response


async def register_without_hash(
    writer: asyncio.StreamWriter, reader: asyncio.StreamReader
) -> dict:
    """Функция обрабатывает случай когда пользователь не задал пароль по умолчанию"""
    writer.write(b"\n")
    await writer.drain()

    for _ in range(2):
        response = await reader.readuntil(b"\n")
        logger.info(response.decode().strip())

    nickname = input("Введите ник для регистрации:")
    writer.write(f"{nickname}\n".encode())
    await writer.drain()

    response = await reader.readuntil(b"\n")
    json_response = json.loads(response.decode())

    logging_user_data(json_response)

    return json_response


async def submit_message(writer: asyncio.StreamWriter) -> None:
    while True:
        message = input(Fore.YELLOW + "Введите сообщение:")
        try:
            writer.write(f"{message}\n\n".encode())
            print(Fore.GREEN + "Сообщение успешно отправлено")
        except UnicodeEncodeError as e:
            print(Fore.RED + "Ошибка отправки сообщения")
            logger.error("Не удалось закодировать сообщение", exc_info=True)
        await writer.drain()


async def tcp_echo_client(args: argparse.Namespace) -> None:
    reader, writer = await asyncio.open_connection(
        host=args.host,
        port=args.port,
    )
    token = args.token
    if not token:
        print(Fore.GREEN + "___Регистрация нового пользователя___\n")
        response = await register_without_hash(writer, reader)
        print(
            Fore.GREEN
            + f"""___{response['nickname']} успешно авторизованы___\n
    Ваш токен: {response['account_hash']}, запомните его """
        )
    else:
        response = await authorise(token, writer, reader)
        print(Fore.GREEN + f"___{response['nickname']} успешно авторизованы___\n")
    await submit_message(writer)


async def main() -> None:
    current_dir = os.path.dirname(os.path.abspath(__file__))
    config_path = os.path.join(current_dir, "configs", "argparse_config_sender.txt")

    load_dotenv()
    parser = configargparse.ArgParser(default_config_files=[config_path])
    parser.add("--host", help="host to connect", default="minechat.dvmn.org")
    parser.add("--port", type=int, help="port number", default=5050)
    parser.add(
        "--token", help="personal hash for chat", default=os.getenv("CHAT_PASSWORD")
    )
    args, unknown = parser.parse_known_args()
    await tcp_echo_client(args)


try:
    asyncio.run(main())
except KeyboardInterrupt:
    print("👋")
