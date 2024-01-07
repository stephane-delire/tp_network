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
        self.pos = 0
    
    def __str__(self):
        """
        Méthode d'affichage de la classe Packet.
        """
        return self.name