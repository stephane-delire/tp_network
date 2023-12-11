class Router():
    def __init__(self, queue_max_size):
        # queue_max_size en octets
        # La mémoire du routeur est calculée en octets
        self.queue = []
        self.queue_max_size = queue_max_size
        self.strategy = "tail_drop"
        
        # bit/sec queueing delay
        self.bandwidth = 4096

    def enqueue(self, packet):
        actual_size = 0
        for p in self.queue:
            actual_size += p.size
        if actual_size + packet.size < self.queue_max_size:
            self.queue.append(packet)
        else:
            packet.dropped = True
            packet.pos = -1
    
    def dequeue(self):
        if self.queue:
            return self.queue.pop(0)
        else:
            return None
    def attach_linkA(self, link):
        self.linkA = link
    
    def attach_linkB(self, link):
        self.linkB = link
    
    def calculate_time(self, packet):
        time = packet.size / self.bandwidth
        return time

