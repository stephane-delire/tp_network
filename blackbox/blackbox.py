import random
import math
import time

class Packet:
    def __init__(self, size, start_time, end_time):
        self.size = size
        self.start_time = start_time
        self.end_time = end_time
        self.pos = -1
        self.dropped = False

class Link:
    def __init__(self, length, speed, bandwidth):
        self.length = length
        self.speed = speed
        self.bandwidth = bandwidth

class Router:
    def __init__(self, bandwidth):
        self.bandwidth = bandwidth
        self.queue = []

def calculate_time(link, size):
    time = (size / float(link.bandwidth)) * 8.0 / link.speed
    return time

def enqueue(router, packet):
    if router.queue and router.queue[-1].end_time > packet.start_time:
        packet.pos = len(router.queue)
        router.queue.append(packet)
    elif len(router.queue) < router.bandwidth:
        packet.pos = len(router.queue)
        router.queue.append(packet)
    else:
        packet.dropped = True
        packet.pos = -1

def dequeue(router):
    if router.queue:
        return router.queue.pop(0)
    else:
        return None

def simulate(links, router, size, time_between_packets):
    source = 0
    dest = 1

    while True:
        start_time = router.queue[-1].end_time if router.queue else 0
        packet = Packet(size, start_time, start_time + time_between_packets)

        for i in range(len(links) - 1):
            packet.start_time += calculate_time(links[i], size)
            packet.end_time += calculate_time(links[i + 1], size)

        enqueue(router, packet)

        while router.queue and router.queue[0].end_time <= packet.end_time:
            packet = dequeue(router)
            print("{0} {1} {2} {3} {4}".format(packet.size, packet.start_time, packet.end_time, packet.pos, packet.dropped))

        if packet.dropped:
            print("Packet {0} was dropped".format(packet.size))

        time.sleep(time_between_packets)

def main():
    link1 = Link(1, 10, 100)
    link2 = Link(2, 10, 100)
    links = [link1, link2]

    router = Router(100)

    simulate(links, router, 10, 0.001)

if __name__ == "__main__":
    main()