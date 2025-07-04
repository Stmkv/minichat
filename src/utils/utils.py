import logging

logger = logging.getLogger("sender")


def logging_user_data(response):
    json_response_for_logging = response.copy()
    json_response_for_logging["account_hash"] = "***"
    logger.info(json_response_for_logging)
