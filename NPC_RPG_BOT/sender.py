# Sender.py

# ==========================================================
# Sender
# ==========================================================

class Sender:
    last_id = 0

    def __init__(self):
        Sender.last_id += 1
        self._sender_id = f"sender_{Sender.last_id}"

    def get_id(self):
        return self._sender_id
