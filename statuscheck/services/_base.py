import logging

logger = logging.getLogger(__name__)


class BaseServiceAPI:
    summary = None

    @property
    def _module_name(self):
        module_relpath = self.__class__.__module__
        return module_relpath.rsplit('.', 1)[1]

    def __init__(self):
        self.summary = self.get_summary()

    def get_summary(self):
        raise NotImplementedError

    def capture_log(self, status, extra=None):
        message = f'Failed to assign status type for {status} [{self._module_name}]'
        if extra:
            message += f'. Data: {extra}'

        logger.warning(message)
