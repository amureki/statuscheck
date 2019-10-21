import logging

logger = logging.getLogger(__name__)


class BaseServiceAPI:
    name: str = None
    summary = None

    @property
    def _module_name(self):
        module_relpath = self.__class__.__module__
        return module_relpath.rsplit(".", 1)[1]

    def __init__(self):
        self.summary = self.get_summary()

    def get_summary(self):
        raise NotImplementedError
