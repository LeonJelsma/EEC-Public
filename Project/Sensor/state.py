import ujson


class State:

    def __init__(self, state_location='state.json'):
        self.state_location = state_location
        self.create_state_if_not_exists()
        self.state = None
        self.load_state()

    def create_state_if_not_exists(self):
        try:
            f = open(self.state_location, 'r')
            f.close()
        except OSError:
            f = open(self.state_location, 'w')
            f.write(ujson.dumps(self.get_empty_state()))
            f.close()

    @staticmethod
    def get_empty_state():
        empty_state = {
            'SSiD': '',
            'NetworkPassword': ''
        }
        return empty_state

    def is_configured(self):
        return not self.state['SSiD'] == ''

    def load_state(self):
        f = open(self.state_location, 'r')
        new_state = f.read()
        f.close()
        self.state = ujson.loads(new_state)

    def save_state(self, new_state=None):
        if new_state is None:
            new_state = self.state
        f = open(self.state_location, 'w')
        f.write(ujson.dumps(new_state))
        f.close()

    def get_value(self, key):
        self.load_state()
        try:
            value = self.state[key]
        except KeyError:
            return None
        return value

    def save_value(self, key, value):
        self.state[key] = value
        self.save_state()

