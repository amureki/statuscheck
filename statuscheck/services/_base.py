import logging

logger = logging.getLogger(__name__)


# class BaseSummary(NamedTuple):
#     status: str
#     incidents: list
#     components: list
#
#     @classmethod
#     def _get_components(cls, summary):
#         raise NotImplementedError
#
#     @classmethod
#     def _get_incidents(cls, summary):
#         raise NotImplementedError
#
#     @classmethod
#     def from_summary(cls, summary):
#         raise NotImplementedError


class BaseServiceAPI:
    data = {}

    @property
    def _module_name(self):
        module_relpath = self.__class__.__module__
        return module_relpath.rsplit('.', 1)[1]

    def get_summary(self):
        raise NotImplementedError

    def capture_log(self, status, extra=None):
        message = f'Failed to assign status type for {status} [{self._module_name}]'
        if extra:
            message += f'. Data: {extra}'

        logger.warning(message)
