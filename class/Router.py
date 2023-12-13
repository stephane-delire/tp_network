class Router():
    def __init__(self, queue_max_size):
        # queue_max_size en octets
        # La mémoire du routeur est calculée en octets
        self.queue = []
        self.queue_max_size = queue_max_size
        
        # Memory est une liste de paquets qui est passé par le routeurs.
        # C'est utilisé dans le cadre de la simulation, pour savoir si un paquet
        # doit être droppé ou non.
        self.memory = []
        self.strategy = "tail_drop"
        
        # bit/sec queueing delay
        self.bandwidth = 4096

    def enqueue(self, packet):
        if self.strategy == "tail_drop":
            if self.queue_max_size > self.get_queue_size():
                packet.start_time_router = self.current_time
                self.queue.append(packet)
                self.memory.append(packet)
            else:
                packet.dropped = True
                self.memory.append(packet)
        else:
            packet.start_time_router = self.current_time
            self.queue.append(packet)
            self.memory.append(packet)

    def dequeue(self):
        if self.queue:
            packet = self.queue.pop(0)
            packet.end_time_router = self.current_time
            return packet
        else:
            return None

    def attach_linkA(self, link):
        self.linkA = link
    
    def attach_linkB(self, link):
        self.linkB = link
    
    def calculate_time(self, packet):
        time = packet.size / self.bandwidth
        return time
    
    def receive_packet(self, packet):
        packet.start_time_router = self.current_time
        self.enqueue(packet)
    
    def send_packet(self, packet):
        self.linkB.receive_packet(packet)
        self.dequeue()

