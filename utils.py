import logging
import sys


def get_logger(name, level=logging.NOTSET, file=None):
    try:
        if isinstance(level, str):
            level = getattr(logging, level.upper())

        app_log = logging.getLogger(name)
        # 必须设置，否则无法输出
        app_log.setLevel(level)

        # no handler, a new logger, set up it
        if not app_log.handlers:

            # set format        
            format_str = logging.Formatter(fmt="%(asctime)s %(filename)s[%(lineno)d] %(levelname)s %(message)s")

            # create stander output handler
            crit_hand = logging.StreamHandler(sys.stderr)
            crit_hand.setFormatter(format_str)
            crit_hand.setLevel(level)
            app_log.addHandler(crit_hand)

            # create file handler
            if file:
                file_hand = logging.FileHandler(file, 'a')
                file_hand.setFormatter(format_str)
                file_hand.setLevel(level)
                app_log.addHandler(file_hand)

        # 必须设置，否则无法输出
        app_log.setLevel(level)
        app_log.propagate = False

        return app_log
    except Exception as e:
        logging.shutdown()
        raise e


logger = get_logger(__name__, level=logging.INFO)
