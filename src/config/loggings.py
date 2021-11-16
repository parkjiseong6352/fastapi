import os

from src.config.settings import get_settings

settings = get_settings()

BASE_DIR = settings.BASE_DIR
LOG_DIR = os.path.join(BASE_DIR, 'logs/')

if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR, exist_ok=True)


logging_config = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'default': {
            'format': '[%(asctime)s] - %(name)s - [%(levelname)s] - %(message)s'
        }
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'level': 'INFO',
            'formatter': 'default',
        },
        'file': {
            'class': 'logging.handlers.RotatingFileHandler',
            'level': 'INFO',
            'formatter': 'default',
            'filename': f'{LOG_DIR}/api.log',
        }
    },
    'loggers': {
        'fastapi.request': {
            'handlers': ['console', 'file'],
            'level': 'DEBUG',
            'propagate': False,
        },
    }
}
