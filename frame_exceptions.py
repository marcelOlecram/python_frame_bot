class FrameException(Exception):
    """
    Exception class to handle errors when posting the picture
    """
    def __init__(self, message, frame):
        self.frame = frame
        self.message = message
        super().__init__(self, "Coult not post frame")
    
    def get_message(self):
        return f"Frame: {self.frame} - Message: {self.message}"