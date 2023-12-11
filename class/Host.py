class Host():
    def __init__(self, type):
        self.type = type
        self.queue = []
        self.link = None
        self.router = None
        self.time_between_packets = 0
        
        # bit/sec
        self.bandwidth = 1024

    def add_packet(self, packet):
        self.queue.append(packet)
        packet.pos = len(self.queue)
    
    def remove_packet(self, packet):
        self.queue.remove(packet)
    
    def attach_link(self, link):
        self.link = link
    
    def calculate_time(self, packet):
        time = packet.size / self.bandwidth
        return time
