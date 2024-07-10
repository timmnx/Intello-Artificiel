from datetime import timedelta, datetime, date, time
import pygame
# Programme contenant les fonctions de l'IA 

class Label:
    def __init__(self, position :tuple, police :object, surface :object) -> None:
        self.position   :tuple  = position
        self.police     :object = police
        self.surface    :object = surface
        self.score_1    :int    = 0
        self.score_2    :int    = 0
        self.tour       :int    = 0
        self.couleur    :tuple  = (255,255,255)
        self.mettre_a_jour(self.score_1, self.score_2, self.tour)

    def faire_le_texte(self) -> None:
        tour    :str    = "C'est à votre tour"
        if self.tour==2:
            tour        = "C'est au tour de l'ordinateur"
        elif self.tour==0:
            tour        = "Partie Finie"
        texte   :str    = f'''SCORES :;- Joueur        : {self.score_1};- Ordinateur : {self.score_2}; ;{tour}'''
        coords  :tuple  = self.position
        for ligne in texte.split(";"):
            coords      = self.surface.blit(self.police.render(ligne, True, self.couleur), coords).bottomleft

    def mettre_a_jour(self, joueur_1, joueur_2, tour) -> None:
        ancien  :tuple  = (self.score_1, self.score_2, self.tour)
        self.score_1    = joueur_1
        self.score_2    = joueur_2
        self.tour       = tour
        if ancien != (self.score_1, self.score_2, self.tour):
            pygame.draw.rect(self.surface, "black",(self.position[0], self.position[1], 1000,1000))
            self.faire_le_texte()


class Chrono:
    def __init__(self, position :tuple, police :object, surface :object) -> None:
        self.position   :tuple  = position
        self.police     :object = police
        self.surface    :object = surface
        self.chrono     :object = datetime.combine(date.today(), time(0,0))
        self.couleur    :tuple  = (255, 255, 255)
        self.texte      :object = self.faire_le_chrono()
        self.rect       :object = self.texte.get_rect(topleft=self.position)
        self.tempsPause :int    = 0

    def faire_le_chrono(self) -> object:
        """
        Crée une Surface représentant le temps du chrono
        """
        return self.police.render(self.chrono.strftime("%H : %M : %S"),True, self.couleur)

    def mettre_a_jour(self, dt) -> None:
        """
        Mise à jour du temps écoulé.
        dt est le nombre de millisecondes
        """
        old_chrono      :object = self.chrono
        self.rect       = self.texte.get_rect(topleft=self.position)
        self.chrono     += timedelta(milliseconds=dt)
        visibleChrono   :object = self.chrono - timedelta(milliseconds=self.tempsPause)
        # Comme le chrono n'indique pas les fractions de secondes,
        # on ne met à jour le texte que si quelque chose de visible a changé
        if old_chrono.second != self.chrono.second:
            self.texte = self.faire_le_chrono()

    def dessiner(self) -> None:
        pygame.draw.rect(self.surface, "black",(self.position[0], self.position[1], 250,50))
        self.surface.blit(self.texte, self.rect)


class Grille:
    def __init__(self, grille : list) -> None:
        self.grille :list   = grille #Liste de listes représentant la grille de jeu
        self.cote   :int    = len(self.grille) #Longueur des côtés

    def creer(cote : int) -> list:
        '''
        Cette fonction renvoie une grille dans l'état de base du jeu.
        Celle-ci n'est appelée théoriquement qu'à l'initialisation du jeu.
        '''
        lst :list   = []
        for _ in range(cote):
            miniLst :list   = []
            for _ in range(cote):
                miniLst += [0]
            lst += [miniLst]
        
        lst[int(cote/2-1)][int(cote/2-1)], lst[int(cote/2)][int(cote/2-1)] = 1, 2
        lst[int(cote/2-1)][int(cote/2)],   lst[int(cote/2)][int(cote/2)]   = 2, 1
        return lst

    def afficher(self) -> None:
        '''
        Cette fonction affiche la grille dans la console.
        '''
        print() #Créé un espace pour améliorer la lisibilité
        for e in self.grille:
            print(e)

    def clone(self) -> object:
        '''
        Cette fonction permet de copier une liste sans que la liste
        originelle ne soit modifiée. Cela revient à faire un deepcopy.
        '''
        return Grille(list(list(t) for t in (tuple(tuple(l) for l in self.grille))))

    def case_horiz(self, adversaire : int, jeton : tuple) -> tuple: # position = (y, x)
        '''
        Fonction secondaire appelée par la fonction primaire obj.jouer() :
        Elle sert à dessiner les pions horizontaux (droite d'équation y = 0).
        jeton est un tuple de sa position
        '''
        lst :list   = []
        for sens in (-1,1):
            i       :int    = sens
            fini    :bool   = False
            joue    :bool   = False
            while not fini:
                if jeton[1]+i in range(0, 8):
                    case    :int    = self.grille[jeton[0]][jeton[1]+i]
                    case_p  :int    = self.grille[jeton[0]][jeton[1]+i-sens]
                    if case == adversaire:
                        i += sens
                    elif case == 0 and case_p == adversaire:
                        fini = True
                        joue = True
                    else:
                        fini = True
                else:
                    fini = True
            if joue == True:
                lst += [(jeton[0],jeton[1]+i)]
        return lst

    def case_verti(self, adversaire : int, jeton : tuple) -> tuple: # position = (y, x)
        '''
        Fonction secondaire appelée par la fonction primaire obj.jouer() :
        Elle sert à dessiner les pions verticaux (droite d'équation x = 0).
        '''
        lst :list   = []
        for sens in (-1,1):
            i       :int    = sens
            fini    :bool   = False
            joue    :bool   = False
            while not fini:
                if jeton[0]+i in range(0, 8):
                    case    :int    = self.grille[jeton[0]+i][jeton[1]]
                    case_p  :int    = self.grille[jeton[0]+i-sens][jeton[1]]
                    if case == adversaire:
                        i += sens
                    elif case == 0 and case_p == adversaire:
                        fini = True
                        joue = True
                    else:
                        fini = True
                else:
                    fini = True
            if joue == True:
                lst += [(jeton[0]+i,jeton[1])]
        return lst

    def case_diag1(self, adversaire : int, jeton : tuple) -> tuple: # position = (y, x)
        '''
        Fonction secondaire appelée par la fonction primaire obj.jouer() :
        Elle sert à dessiner les pions diagonaux (droite d'équation y = -x).
        '''
        lst :list   = []
        for sens in (-1,1):
            i       :int    = sens
            fini    :bool   = False
            joue    :bool   = False
            while not fini:
                if jeton[0]+i in range(0, 8) and jeton[1]+i in range(0, 8):
                    case    :int    = self.grille[jeton[0]+i][jeton[1]+i]
                    case_p  :int    = self.grille[jeton[0]+i-sens][jeton[1]+i-sens]
                    if case == adversaire:
                        i += sens
                    elif case == 0 and case_p == adversaire:
                        fini = True
                        joue = True
                    else:
                        fini = True
                else:
                    fini = True
            if joue == True:
                lst += [(jeton[0]+i,jeton[1]+i)]
        return lst

    def case_diag2(self, adversaire : int, jeton : tuple) -> tuple: # position = (y, x)
        '''
        Fonction secondaire appelée par la fonction primaire obj.jouer() :
        Elle sert à dessiner les pions diagonaux (droite d'équation y = x).
        '''
        lst :list   = []
        for sens in (-1,1):
            i       :int    = sens
            fini    :bool   = False
            joue    :bool   = False
            while not fini:
                if jeton[0]-i in range(0, 8) and jeton[1]+i in range(0, 8):
                    case    :int    = self.grille[jeton[0]-i][jeton[1]+i]
                    case_p  :int    = self.grille[jeton[0]-i+sens][jeton[1]+i-sens]
                    if case == adversaire:
                        i += sens
                    elif case == 0 and case_p == adversaire:
                        fini = True
                        joue = True
                    else:
                        fini = True
                else:
                    fini = True
            if joue == True:
                lst += [(jeton[0]-i,jeton[1]+i)]
        return lst

    def case(self, joueur : int) -> list:
        '''
        Cette fonction renvoie une liste de tuple représentant les
        coordonnées auxquelles il est possible de jouer un pion.
        '''
        lst         :list   = []
        adversaire  :int    = 2 if joueur==1 else 1
        for y in range(len(self.grille)):
            for x in range(len(self.grille[y])):
                if self.grille[y][x]==joueur:
                    lst += self.case_horiz(adversaire, (y,x))
                    lst += self.case_verti(adversaire, (y,x))
                    lst += self.case_diag1(adversaire, (y,x))
                    lst += self.case_diag2(adversaire, (y,x))
        lst2 :list = []
        for e in lst:
            if e not in lst2 and e != None:
                lst2 += [e]
        return lst2

    def fini(self) -> bool:
        '''
        Renvoie si True plus personne ne peut jouer, ce qui revient à une fin de partie.
        '''
        if len(self.case(1)) == 0 and len(self.case(2)) == 0:
            return True
        else:
            return False

    def gagne(self, joueur :int) -> bool:
        '''
        Cette fonction renvoie True si le joueur j a gagné.
        '''
        j1 :int = self.compter(1)
        j2 :int = self.compter(2)
        if (joueur == 1 and j1 > j2) or (joueur == 2 and j2 > j1):
            return True
        else:
            return False

    def quiGagne(self) -> int:
        '''
        Fonction qui n'est appelée qu'une fois la partie terminée pour savoir qui a gagné
        '''
        if self.gagne(1) == True:
            return 1
        elif self.gagne(2) == True:
            return 2
        else:
            return 0

    def compter(self, joueur : int) -> int:
        '''
        Renvoie le nombre de points du joueur j dans la grille actuelle.
        '''
        compteur :int = 0
        for y in self.grille:
            for x in y:
                if x == joueur:
                    compteur += 1
        return compteur

    def nb_voisines(self, case :tuple) -> int:
        '''
        Cette fonction permet de savoir combien de voisines a une case.
        Cette fonction sert dans l'euristique
        '''
        compteur :int = 0
        for i in (-1,0,1):
            for j in (-1,0,1):
                y :int = case[0]+j
                x :int = case[0]+i
                if y in range(0,8):
                    if x in range(0,8):
                        if case != (y, x):
                            compteur += 1
        return compteur

    def diff(self, joueur :int) -> int:
        '''
        Renvoie la différence de points entre le joueur et l'autre joueur.
        '''
        compteur :int = 0
        for y in range(len(self.grille)):
            for x in range(len(self.grille[y])):
                if self.grille[y][x] == 0:
                    compteur += 0
                elif self.grille[y][x] == joueur:
                    compteur += 2**(8-self.nb_voisines((y,x)))
                else:
                    compteur -= 2**(8-self.nb_voisines((y,x)))
        return compteur        

    def jouer_horiz(self, joueur : int, position : tuple) -> list: # position = (y, x)
        '''
        Fonction secondaire appelée par la fonction primaire obj.jouer() :
        Elle sert à dessiner les pions horizontaux (droite d'équation y = 0).
        '''
        lst :list = []
        for i in (-1, 1):
            if position[1]+i in range(0,self.cote):
                if self.grille[position[0]][position[1]+i] not in (0, joueur):
                    localLst  :list = []
                    n         :int  = 1
                    continuer :bool = True
                    while position[1] + i*n in range(8) and continuer:
                        y :int = position[0]
                        x :int = position[1]+i*n
                        if self.grille[y][x] not in (0, joueur):
                            localLst.append((y, x))
                            n += 1
                        elif self.grille[y][x] == joueur:
                            lst += localLst
                            continuer = False
                        elif self.grille[y][x] == 0:
                            continuer = False
        return lst

    def jouer_verti(self, joueur : int, position : tuple) -> list: # position = (y, x)
        '''
        Fonction secondaire appelée par la fonction primaire obj.jouer() :
        Elle sert à dessiner les pions verticaux (droite d'équation x = 0).
        '''
        lst :list = []
        for i in (-1, 1):
            if position[0]+i in range(0,self.cote):
                if self.grille[position[0]+i][position[1]] not in (0, joueur):
                    localLst  :list = []
                    n         :int  = 1
                    continuer :bool = True
                    while position[0] + i*n in range(8) and continuer:
                        y :int = position[0]+i*n
                        x :int = position[1]
                        if self.grille[y][x] not in (0, joueur):
                            localLst.append((y, x))
                            n += 1
                        elif self.grille[y][x] == joueur:
                            lst += localLst
                            continuer = False
                        elif self.grille[y][x] == 0:
                            continuer = False
        return lst

    def jouer_diag1(self, joueur : int, position : tuple) -> list: # position = (y, x)
        '''
        Fonction secondaire appelée par la fonction primaire obj.jouer() :
        Elle sert à dessiner les pions diagonaux (droite d'équation y = -x).
        '''
        lst :list = []
        for i in (-1, 1):
            if position[0]+i in range(0,self.cote) and position[1]+i in range(0,self.cote):
                if self.grille[position[0]+i][position[1]+i] not in (0, joueur):
                    localLst  :list = []
                    n         :int  = 1
                    continuer :bool = True
                    while position[0] + i*n in range(8) and position[1] + i*n in range(8) and continuer:
                        y :int = position[0]+i*n
                        x :int = position[1]+i*n
                        if self.grille[y][x] not in (0, joueur):
                            localLst.append((y, x))
                            n += 1
                        elif self.grille[y][x] == joueur:
                            lst += localLst
                            continuer = False
                        elif self.grille[y][x] == 0:
                            continuer = False
        return lst

    def jouer_diag2(self, joueur : int, position : tuple) -> list: # position = (y, x)
        '''
        Fonction secondaire appelée par la fonction primaire obj.jouer() :
        Elle sert à dessiner les pions diagonaux (droite d'équation y = x).
        '''
        lst :list = []
        for i in (-1, 1):
            if position[0]+i in range(0,self.cote) and position[1]-i in range(0,self.cote):
                if self.grille[position[0]+i][position[1]-i] not in (0, joueur):
                    localLst  :list = []
                    n         :int  = 1
                    continuer :bool = True
                    while position[0] + i*n in range(8) and position[1] - i*n in range(8) and continuer:
                        y :int = position[0]+i*n
                        x :int = position[1]-i*n
                        if self.grille[y][x] not in (0, joueur):
                            localLst.append((y, x))
                            n += 1
                        elif self.grille[y][x] == joueur:
                            lst += localLst
                            continuer = False
                        elif self.grille[y][x] == 0:
                            continuer = False
        return lst

    def jouer(self, joueur : int, position : tuple) -> None: #position = (y, x)
        '''
        Fonction qui appelle les fonctions jouant les pions dans chaque directions.
        Elle modifie directement les cases concernant dans la grille "grille" de l'objet.
        '''
        lst :list   = [position]
        lst         += self.jouer_horiz(joueur, position)
        lst         += self.jouer_verti(joueur, position)
        lst         += self.jouer_diag1(joueur, position)
        lst         += self.jouer_diag2(joueur, position)
        for e in lst:
            self.grille[e[0]][e[1]] = joueur
