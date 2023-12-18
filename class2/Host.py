class Host():
    """
    Objet représentant les hôtes du réseau.
    """
    def __init__(self, queue=[], link=None):
        """
        Constructeur de la classe Host.
        """
        self.queue = queue
        # lien par lequel on envoie/reçoit les paquets
        self.link = link
        # Compteur de temps
        self.current_time = 0
        # Vitesse de transmission de l'hôte bits/sec
        self.bandwidth = 1024

    def attach_link(self, link):
        """
        Attache un lien à l'hôte.
        """
        self.link = link

    def add_packet(self, packet):
        """
        Ajoute un paquet à la queue de l'hôte.
        """
        self.queue.append(packet)

    def remove_packet(self, packet):
        """
        Retire un paquet de la queue de l'hôte.
        """
        self.queue.remove(packet)

    def attach_link(self, link):
        """
        Attache un lien à l'hôte.
        """
        self.link = link

    def calculate_time(self, packet):
        """
        Calcule le temps de transmission d'un paquet.
        ! Il faut prendre le minimum entre la bandwidth de l'hôte et celle du routeur.
        """
        if self.bandwidth < self.link.pointA.bandwidth:
            time = packet.size / self.bandwidth
        else:
            time = packet.size / self.link.pointA.bandwidth
        return time
    
    def receive_packet(self, packet):
        """
        Reçoit un paquet.
        On imprime les résultats qui sont dans le paquet.
        + Ajout du délais de réception du paquet.
        """

        # Il ne reste que le délais de propagation du lien à ajouter
        # pour avoir le temps total du paquet.
        #packet.times.append(packet.times[-1] + self.link.calculate_time(packet))
        # UPDATE : pour afficher le paquet qui est droppé, comme dans la simulation
        # C'est l'hote de réception qui print() les résultats, il faut légèrement
        # adapter le code précédent.
        if packet.dropped:
            packet.times.append("False")
        else:
            packet.times.append(packet.times[-1] + self.link.calculate_time(packet))
        

        # Méthode d'affichage des résultats
        # UPDATE : 
        # L'affichage des paquets doit se faire de la sorte (un seul espace entre les données):
        # nom du paquet | depart de l'hôte | arrivée dans le routeur | sortie du routeur | arrivée dans l'hôte | position du paquet | dropped
        print(packet.name, end=" ")
        # Affichage des temps
        # Par question de lisibilité, on affiche les temps avec 3 chiffres après la virgule...
        # Il suffit de modifier le format de la string, pour afficher plus de chiffres si besoin.
        for t in packet.times:
            if t!= "False":
                t = "{0:.3f}".format(t)
            print(t, end=" ")
        # Affichage de la position du paquet dans le routeur
        print(packet.pos, end=" ")
        # Affichage si le paquet est droppé ou non
        print(packet.dropped)

    def send_packet(self, packet):
        """
        Envoie un paquet.
        """
        # Initialisation du temps de départ du paquet
        packet.times.append(self.current_time)
        # Ajout du temps de transmission du paquet
        self.current_time += self.calculate_time(packet)
        # Envoie du paquet
        self.link.receive_packet(packet)
        # Retrait du paquet de la queue
        self.remove_packet(packet)
