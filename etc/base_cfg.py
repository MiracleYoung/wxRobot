#!/usr/bin/env python
# encoding: utf-8
# @Time    : 2018/10/17 上午6:26

__author__ = 'Miracle'

import os

PROJ_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOG_DIR = os.path.join(PROJ_ROOT, 'log')
TMP_DIR = os.path.join(PROJ_ROOT, 'tmp')
STATIC_ROOT = os.path.join(PROJ_ROOT, 'static')
WX_IMG_DIR = os.path.join(STATIC_ROOT, 'img/app')

DEFAULT_LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': '%(asctime)s - %(filename)s[%(lineno)d] - %(levelname)s : %(message)s'
        },
    },
    'handlers': {
        'console': {
            'level': 'INFO',
            'formatter': 'standard',
            'class': 'logging.StreamHandler',
        },
        'file_handler': {
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'level': 'INFO',
            'formatter': 'standard',
            'filename': os.path.join(LOG_DIR, 'PIP.log'),
            #        suffix: "%Y%m%d_%H%M%S.log"
            'when': 'D',
            'interval': 7,
            'backupCount': 4,
            'encoding': 'utf8'
        },
        'error_file_handler': {
            'class': 'logging.handlers.RotatingFileHandler',
            'level': 'ERROR',
            'formatter': 'standard',
            'filename': os.path.join(LOG_DIR, 'error.log'),
            'maxBytes': 104857600,  # 10MB
            'backupCount': 20,
            'encoding': 'utf8',
        }

    },
    'loggers': {
        'myhandler': {
            'handlers': ['console', 'file_handler', 'error_file_handler'],
            'level': 'INFO',
            'propagate': True
        },
    },
    'root': {
        'level': 'INFO',
        'handlers': ['console', 'file_handler'],
    }
}
