from .service import Service

class NodeParameters(Service):

    def __init__(self, id, alias, device):
        Service.__init__(self, 'NodeParameters', id, alias, device)
        self._parameters = [None,None,None]
        self._alias = alias 

    def receiveParameters(self):
        self._push_value('send_param', True)

    def stopReceiveParameters(self):
        self._push_value('send_param', False)

    @property
    def max_motor_nb(self):
        """ Maximum Motor Number. """
        return self._parameters[0]

    @property
    def id_ring(self):
        """ Ring ID to know on wich ring the node is. """
        return self._parameters[1]

    @property
    def id_disk(self):
        """ Disk ID to know on wich disk the node is. """
        return self._parameters[2]

    def _update(self, new_state):
        Service._update(self, new_state)
        # print(self._alias)
        # print('new_state = ',new_state)
        if 'node_parameters' in new_state:
            self._parameters = new_state['node_parameters']
        
        