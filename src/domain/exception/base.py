class BaseError(Exception):
    msg_template = "{msg}"

    def __init__(self, **kwargs):
        self.msg = self.msg_template.format(**kwargs)
        super().__init__(self.msg)

class DomainError(BaseError):
    """"""

class EntityNotCreated(DomainError):
    """"""

class BdError(DomainError):
    """"""

class EntityNotFound(DomainError):
    """"""