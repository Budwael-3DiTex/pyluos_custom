from .service import Service

class AppBttnMotor(Service):

    def __init__(self, id, alias, device):
        Service.__init__(self, 'AppBttnMotor', id, alias, device)
        self._alias = alias
        
    def _update(self, new_state):
        Service._update(self, new_state)