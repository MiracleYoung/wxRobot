# /usr/bin/env python
# Created by Miracle at 9/11/18

import logging
import logging.config

from etc.base_cfg import DEFAULT_LOGGING

__all__ = ['logger']


def setup_logging(cfg=DEFAULT_LOGGING):
    logging.config.dictConfig(cfg)
    return logging.getLogger(__file__)


logger = setup_logging()
