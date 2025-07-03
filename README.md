# Minichat

Утилита для асинхронного взаимодействия подключения к чату.

## Установка

```bash
uv sync
source .venv/bin/activate
```

## Использование

```bash
minichat --host minechat.dvmn.org --port 5000 --history minechat.history
```

Для изменения конфигурации используйте файл `argparse_config.txt`. После изменения конфигурации под себя можно не указывать параметры командной строки