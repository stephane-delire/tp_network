class Packet():
    def __init__(self, size):
        # Attention size en octets
        self.size = size
        # Délais d'émission
        self.start_time_host = 0
        # Délais de propagation + d'émission
        self.end_time_router = 0
        # Délais end_time routeur + queueing + émission
        self.start_time_router = 0
        # Délais de propagation du lien L2 + start_time_router
        self.end_time_host = 0
        self.pos = -1
        self.dropped = False