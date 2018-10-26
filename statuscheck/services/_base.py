import logging

logger = logging.getLogger(__name__)


class BaseServiceAPI:
    data = {}

    def _get_status_data(self):
        raise NotImplementedError

    def get_status(self):
        raise NotImplementedError

    def get_type(self):
        raise NotImplementedError

    def get_active_incident(self):
        raise NotImplementedError

    def capture_log(self, status, extra=None):
        message = f'Failed to assign status type for {status} [{self.api_name}]'
        if extra:
            message += f'. Data: {extra}'

        logger.warning(message)
