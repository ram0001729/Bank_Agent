class EmergencyStopSwitch:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(EmergencyStopSwitch, cls).__new__(cls)
            cls._instance.is_stopped = False
        return cls._instance

    def trigger_stop(self):
        self.is_stopped = True

    def reset(self):
        self.is_stopped = False

    def check_active(self) -> bool:
        return not self.is_stopped
