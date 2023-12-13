class Router():
    """
    Objet représentant un routeur.
    """
    def __init__(self, queue_max_size=1024):
        """
        Constructeur de la classe Router.
        """
        # Liste de la file d'attente du routeur
        self.queue = []
        # Taille maximale de la file d'attente du routeur (bits)
        self.queue_max_size = queue_max_size
        # Liste des liens du routeur
        self.pointA = None
        self.pointB = None
        # Compteur de temps
        self.current_time = 0
        # Vitesse de transmission du routeur bits/sec
        self.speed = 1024
        
        # Mémoire du routeur :
        # la mémoire ne permet que de sauvegarder la liste des paquets
        # qui sont passés par le routeur. (temps d'entrée et de sortie).
        # Cela permet lors de la simulation de savoir si un paquet doit être
        # droppé ou non.
        # La mémoire est une list de tuple : 
        # (temps d'entrée, temps de sortie, taille, nom)
        self.memory = []

    def __str__(self):
        """
        Méthode d'affichage de la classe Router.
        """
        s = "Router memory : \n"
        for p in self.memory:
            s += str(p) + "\n"
        return s

    def attach_pointA(self, point):
        """
        Attache un point d'entrée au routeur.
        """
        self.pointA = point
    def attach_pointB(self, point):
        """
        Attache un point de sortie au routeur.
        """
        self.pointB = point

    def calculate_time(self, packet):
        """
        Calcule le temps de transmission d'un paquet.
        Dépendant du lien de sortie ! (pas du routeur)
        """
        time = self.pointB.calculate_time(packet)
        return time
    
    def send_packet(self, packet):
        """
        Envoie un paquet.
        """
        self.pointB.receive_packet(packet)

    def receive_packet(self, packet):
        """
        Reçoit un paquet.
        """

        # sauvegarde temps d'arrivée et de sortie théorique du paquet
        packet_in = packet.times[-1]
        packet_out = packet_in + self.calculate_time(packet)
        # Vérification de la mémoire du routeur
        memory_left = self.queue_max_size
        for p in self.memory:
            # p[0] = temps d'entrée du paquet
            # p[1] = temps de sortie du paquet
            # p[2] = taille du paquet
            
            # Vérification de collision
            if packet_in >= p[0] and packet_in <= p[1]:
                # Si le paquet est en collision avec un autre paquet
                # on diminue la mémoire restante
                memory_left -= p[2]
        # Si plus assez de mémoire, on drop le paquet
        if memory_left < packet.size:
            packet.dropped = True
        else:
            # Ajout du paquet dans la mémoire
            self.memory.append((packet_in, packet_out, packet.size, packet.name))
        
        # Ajout du délais de transmission
        # packet.times.append(packet_out)
        # Pas ici... Dans un routeur c'est négligeable
        # la latence doit venir du lien de sortie...

        # On renvoie le paquet au lien de sortie
        self.pointB.receive_packet(packet)
        # A voir si il faut l'envoyer dans le cas de la simulation
        # ou pas... (si il est droppé dans la réalité, il ne faut pas...)

                

