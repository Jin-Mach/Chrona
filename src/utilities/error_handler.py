from src.utilities.logging_provider import get_logger


# noinspection PyBroadException
class Errorhandler:
    logger = get_logger()

    @staticmethod
    def handle_error(class_name: str, exception: Exception) -> None:
        if Errorhandler.logger is None:
            return
        try:
            Errorhandler.logger.error(f"{class_name}: {exception}", exc_info=True)
        except Exception:
            pass