class Link:
    def __init__(self, length, speed, bandwidth):
        self.length = length
        self.speed = speed
        self.bandwidth = bandwidth
        self.pointA = None
        self.pointB = None
    
    def calculate_time(self, packet):
        time = (packet.size / float(self.bandwidth)) * 8.0 / self.speed
        return time

    def attach_pointA(self, point):
        self.pointA = point

    def attach_pointB(self, point):
        self.pointB = point
    