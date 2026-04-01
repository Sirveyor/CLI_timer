

class Timer:
    def __init__(self, duration_seconds: int, message: str, verbose: bool = False, silent: bool = False):
        self.duration_seconds = duration_seconds
        self.message = message
        self.verbose = verbose
        self.silent = silent

    def start(self):
        pass
    