from .service import Service

class NodeParameters(Service):

    def __init__(self, id, alias, device):
        Service.__init__(self, 'NodeParameters', id, alias, device)
        self._max_motor_nb = 1

    @property
    def max_motor_nb(self):
        """ Maximum Motor Number. """
        return self._max_motor_nb

    @max_motor_nb.setter
    def max_motor_nb(self, new_val):
        self._max_motor_nb = new_val
        self._push_value('max_motor_nb', new_val)

    def _update(self, new_state):
        Service._update(self, new_state)
        if 'max_motor_nb' in new_state:
            print('new_state = ',new_state)
            self._max_motor_nb = new_state['max_motor_nb']

