import logging
import requests as rq


logger = logging.getLogger('RequestsLogger')
logger.setLevel(logging.DEBUG)


class InfoFilter(logging.Filter):
    def filter(self, record):
        return record.levelno == logging.INFO


class WarningFilter(logging.Filter):
    def filter(self, record):
        return record.levelno == logging.WARNING


class ErrorFilter(logging.Filter):
    def filter(self, record):
        return record.levelno == logging.ERROR


info_handler = logging.FileHandler('success_responses.log', 'w')
info_handler.setLevel(logging.INFO)
info_format = logging.Formatter('%(asctime)s | %(levelname)s: %(message)s')
info_handler.setFormatter(info_format)
logger.addHandler(info_handler)
info_handler.addFilter(InfoFilter())


warning_handler = logging.FileHandler('bad_responses.log', 'w')
warning_handler.setLevel(logging.WARNING)
warning_format = logging.Formatter('%(asctime)s | %(levelname)s: %(message)s')
warning_handler.setFormatter(warning_format)
logger.addHandler(warning_handler)
warning_handler.addFilter(WarningFilter())


error_handler = logging.FileHandler('blocked_responses.log', 'w')
error_handler.setLevel(logging.ERROR)
error_format = logging.Formatter('%(asctime)s | %(levelname)s: %(message)s')
error_handler.setFormatter(error_format)
logger.addHandler(error_handler)
error_handler.addFilter(ErrorFilter())


sites = ['https://www.youtube.com/', 'https://instagram.com', 'https://wikipedia.org', 'https://yahoo.com',
         'https://yandex.ru', 'https://whatsapp.com', 'https://twitter.com', 'https://amazon.com', 'https://tiktok.com',
         'https://www.ozon.ru']

for site in sites:
    try:
        response = rq.get(site, timeout=3)
        if response.status_code == 200:
            logger.info(f"{site}, response - 200")
        else:
            logger.warning(f"{site}, response - {response.status_code}")
    except rq.exceptions.ConnectTimeout:
        logger.error(f"{site}, NO CONNECTION")
    except rq.exceptions.Timeout:
        logger.error(f"{site}, TIMEOUT")
    except rq.exceptions.RequestException as e:
        logger.error(f"{site}, REQUEST FAILED: {e}")

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)