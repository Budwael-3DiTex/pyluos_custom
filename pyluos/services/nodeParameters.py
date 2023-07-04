from .service import Service

class NodeParameters(Service):

    def __init__(self, id, alias, device):
        Service.__init__(self, 'NodeParameters', id, alias, device)
        self._max_motor_nb = None
        self._id_ring = None
        self._id_disk = None

    def receiveParameters(self):
        self._push_value('send_param', True)

    @property
    def max_motor_nb(self):
        """ Maximum Motor Number. """
        return self._max_motor_nb

    @max_motor_nb.setter
    def max_motor_nb(self, new_val):
        self._max_motor_nb = new_val
        self._push_value('max_motor_nb', new_val)

    @property
    def id_ring(self):
        """ Ring ID to know on wich ring the node is. """
        return self._id_ring

    @property
    def id_disk(self):
        """ Disk ID to know on wich disk the node is. """
        return self._id_disk

    def _update(self, new_state):
        Service._update(self, new_state)
        if 'max_motor_nb' in new_state:
            print('new_state = ',new_state)
            self._max_motor_nb = new_state['max_motor_nb']
        if 'id_ring' in new_state:
            self._id_ring = new_state['id_ring']
        if 'id_disk' in new_state:
            self._id_disk = new_state['id_disk']