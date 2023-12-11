
def send_packet(router, packet):
    if router.queue and router.queue[-1].end_time > packet.start_time:
        packet.pos = len(router.queue)
        router.queue.append(packet)
    elif len(router.queue) < router.bandwidth:
        packet.pos = len(router.queue)
        router.queue.append(packet)
    else:
        packet.dropped = True
        packet.pos = -1

def receive_packet(router):
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

        send_packet(router, packet)

        while router.queue and router.queue[0].end_time <= packet.end_time:
            packet = receive_packet(router)

def main():
    links = [Link(1000, 200000000, 1000000), Link(1000, 200000000, 1000000)]
    router = Router(1000000)
    size = 1000
    time_between_packets = 0.00001
    simulate(links, router, size, time_between_packets)

if __name__ == "__main__":
    main()