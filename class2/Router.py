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
        self.bandwidth = 1024
        
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
        s = "\nRouter memory : \n"
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
        Et du délais de réception de l'hôte.
        Le délais de reception de l'hôte est retrouvé au bout du lien de sortie.
        Dans notre cas objet : self.pointB.pointB...
        """
        time = self.pointB.calculate_time(packet) + self.pointB.pointB.calculate_time(packet)
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

        # Le paquet arrive dans le routeur, il faut donc imprimer à l'intérieur
        # le temps qu'il a mis pour arriver.
        # le calcul est le délais de transmission (min entre celui de l'émetteur et du routeur)
        # + le temps de propagation du lien d'entrée.
        if self.bandwidth < self.pointA.pointA.bandwidth:
            bandwidth_a = self.bandwidth
        else:
            bandwidth_a = self.pointA.pointA.bandwidth
        propagation_a = self.pointA.calculate_time(packet)
        transmission_a = packet.size / bandwidth_a
        # 2eme valeur demandé dans le tp. (temps d'entrée dans le routeur)
        packet.times.append(propagation_a + transmission_a + packet.times[-1])

        # calcul du délais de transmission vers l'hôte de sortie
        if self.bandwidth < self.pointB.pointB.bandwidth:
            bandwidth_b = self.bandwidth
        else:
            bandwidth_b = self.pointB.pointB.bandwidth
        transmission_b = packet.size / bandwidth_b
        # transmission_b est donc le temps ou le paquet sort du router.

        # Calcul de la mémoire du routeur.
        # On a besoin théoriquement de garder en mémoire tout les paquets
        # qui sont passés par le routeur. (temps d'entrée et de sortie).
        # Cela permet lors de la simulation de savoir si un paquet doit être
        # droppé ou non. Et de savoir combien de temps il a passé dans le routeur.
        # le paquet actuel :
        packet_in = packet.times[-1]
        packet_out = packet_in + transmission_b

        # ---
        # on regarde les packets déja enregistrés dans la mémoire du routeur
        # pour voir si il y a des collisions.
        # Besoin d'une mémoire temporaire car il se peut que plusieurs paquets
        # soient déja dans la mémoire du routeur.
        temp_memory = self.queue_max_size
        # Besoin d'un compteur pour savoir la position du paquet dans la mémoire.
        count = 0
        # Besoin de récupérer également le temps de sortie du paquet précédent
        # occasionnant une collision.
        last_packet_out = 0
        for p in self.memory :
            # on regarde si il y a collision ou non.
            if packet_in >= p[0] and packet_in < p[1] and not p[5]:
                # il y a collision, on décrémente la mémoire temporaire.
                temp_memory -= p[2]
                # on augmente le compteur pour placer le paquet derrière.
                count += 1
                # on récupère le temps de sortie du dernier paquet.
                if p[1] > last_packet_out:
                    last_packet_out = p[1]
                # Si on a encore de la mémoire, on peut ajouter le paquet dans la mémoire
                # du routeur.
                if temp_memory >= packet.size:
                    # on imprime la position dans le paquet
                    packet.pos = count
                # Sinon, on drop le paquet.
                else:
                    packet.dropped = True
        self.memory.append((packet_in, packet_out, packet.size, packet.name, packet.pos, packet.dropped))
        
        # ---
        # On imprime le temps passé dans le routeur, ce qui est la troisième valeur
        # demandé dans le tp.
        # Si un paquet a la position 0 il est renvoyé directement.
        if packet.pos == 0:
            packet.times.append(packet_out)
        # Sinon, il faut calculer son le temps qu'il a passé dans le routeur.
        else:
            # on a la variable last_packet_out qui contient le temps de sortie du paquet précédent.
            # et il suffit de lui ajouter le délais de transmission vers l'hôte de sortie.
            packet.times.append(last_packet_out + packet_out)


        # ---
        # Il ne reste qu'à vérifier si le paquet a été droppé ou non.
        if packet.dropped:
            pass
        else:
            # Le paquet n'a pas été droppé, on peut l'envoyer vers le lien de sortie.
            self.send_packet(packet)

                

