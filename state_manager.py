class StateManager:
    def __init__(self):
        self.states = {}

    def get_context(self, user_id):
        if user_id not in self.states:
            self.user_states[user_id] = {}
        return self.user_states[user_id]

    def set_context(self, user_id, context):
        self.user_states[user_id] = context