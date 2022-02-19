class FrameException(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self, "Coult not post frame")