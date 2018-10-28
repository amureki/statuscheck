import logging

logger = logging.getLogger(__name__)


class BaseServiceAPI:
    data = {}

    @property
    def _module_name(self):
        module_relpath = self.__class__.__module__
        return module_relpath.rsplit('.', 1)[1]

    def _get_status_data(self):
        raise NotImplementedError

    def get_status(self):
        raise NotImplementedError

    def get_type(self):
        raise NotImplementedError

    def get_active_incident(self):
        raise NotImplementedError

    def capture_log(self, status, extra=None):
        message = f'Failed to assign status type for {status} [{self._module_name}]'
        if extra:
            message += f'. Data: {extra}'

        logger.warning(message)
