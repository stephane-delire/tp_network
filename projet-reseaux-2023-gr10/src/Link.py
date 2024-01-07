class Link():
    """
    Objet représentant un lien entre deux objets.
    """
    def __init__(self, length=1000, speed=200000000):
        """
        Constructeur de la classe Link.
        """
        self.length = length
        self.speed = speed
        # point d'entrée du lien
        self.pointA = None
        # point de sortie du lien
        self.pointB = None

    def calculate_time(self, packet):
        """
        Calcule le temps de propagation d'un paquet.
        """
        time = packet.size * self.length / self.speed
        return time
    
    def attach_pointA(self, point):
        """
        Attache un point d'entrée au lien.
        """
        self.pointA = point
    
    def attach_pointB(self, point):
        """
        Attache un point de sortie au lien.
        """
        self.pointB = point
    
    def send_packet(self, packet):
        """
        Envoie un paquet.
        """
        self.pointB.receive_packet(packet)
    
    def receive_packet(self, packet):
        """
        Reçoit un paquet.
        """
        self.send_packet(packet)