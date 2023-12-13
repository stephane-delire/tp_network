class Packet():
    """
    Objet représentant les paquets du réseau.
    """
    
    def __init__(self, name="", size=1024):
        """
        Constructeur de la classe Packet.
        """
        self.size = size
        self.times = []
        self.name = name
        self.dropped = False
    
    def __str__(self):
        """
        Méthode d'affichage de la classe Packet.
        """
        return "I'm a packet !"