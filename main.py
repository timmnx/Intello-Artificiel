###############  Jeux Othello  ###############
import pygame
import pygame.locals
import sys # Pour fermer correctement l'application
import ia
import fonctions as f

def actualiser():
    longueur :range = range(plateau.cote)
    for y in longueur:
        for x in longueur:
            carre :int = dimensions[1]*90/800
            rayon :int = dimensions[1]*40/800
            marge :int = dimensions[1]*5/800
            pos :tuple = (int(marge+cote*x), int(marge+cote*y), carre, carre)
            pygame.draw.rect(screen, "darkgreen", pos)
            if plateau.grille[y][x] == 1:
                pygame.draw.circle(screen, "white", (pos[0]+pos[2]/2, pos[1]+pos[3]/2), rayon)
            elif plateau.grille[y][x] == 2:
                pygame.draw.circle(screen, "black", (pos[0]+pos[2]/2, pos[1]+pos[3]/2), rayon)
            pygame.display.flip()


if __name__ == "__main__":
    print("\n\nBienvenue sur Inthello Artificiel, un jeu d'Othello où vous jouez contre une Intelligence",
          "\nArtificielle. Vous avez le choix entre différentes difficultés, mais attention, plus une",
          "\ndifficulté est élevée, plus l'I.A. sera lente et plus votre PC devra être puissant."
          "\nBon jeu à vous !")
    
    plateau = f.Grille(f.Grille.creer(8))
    dimensions  :tuple  = (700,700)
    accueil     :bool   = True
    difficulte  :int    = 1
    joueur      :int    = 1
    screen      :object = None
    fond        :object = None
    derniere    :tuple  = None
    pause       :bool   = False
    ### Images racines ###
    Rimage      :object = pygame.image.load('images/pause.jpg')
    Ri_joueur   :object = pygame.image.load('images/gagnant_joueur.jpg')
    Ri_ia       :object = pygame.image.load('images/gagnant_ia.jpg')
    Ri_nul      :object = pygame.image.load('images/match_nul.jpg')
    ### Images mises à l'échelle
    image       :object = pygame.transform.scale(Rimage, dimensions)
    i_joueur    :object = pygame.transform.scale(Ri_joueur, dimensions)
    i_ia        :object = pygame.transform.scale(Ri_ia, dimensions)
    i_nul       :object = pygame.transform.scale(Ri_nul, dimensions)
    
    # Chargement de la couleur de fond
    police      :object = None
    fps_clock   :str    = None
    chrono      :object = None
    texte       :object = None
    
    tab         :list   = [i for i in range(0,10)] + [i for i in range(90,100)]
    cote        :float  = (dimensions[0] if dimensions[0]<dimensions[1] else dimensions[1])/8
    
    ### BOUCLE DE JEU  ###
    running     :bool   = True # Variable pour laisser la fenêtre ouverte
    while running == True:
        ### Boucle infini pour laisser la fenêtre ouverte ###

        ### Actualisation de la scène ###
        if accueil == True:
            difficulte = input("Donnez le niveau de l'ordinateur, compris entre 1 et 5 : ")
            if difficulte not in [f"{i+1}" for i in range(5)]:
                print("La difficulté doit être comprise entre 1 et 5 !")
            else:
                # Lancement des modules inclus dans pygame
                difficulte  = int(difficulte)
                pygame.init()
                pygame.mouse.get_pos()
                pygame.display.set_caption("Jeux Othello")
                screen      = pygame.display.set_mode(dimensions, pygame.locals.RESIZABLE)
                fond        = screen.fill("black")
                derniere    = screen.get_size()
                police      = pygame.font.Font(None, 64)
                fps_clock   = pygame.time.Clock()
                chrono      = f.Chrono((dimensions[0]+20, 0), police, screen)
                texte       = f.Label((dimensions[0]+20, 150), police, screen)
                actualiser()
                texte.mettre_a_jour(0, 0, 0)
                accueil = False
        
        else:
            case_jouer  :tuple  = None
            
            ### Gestion des évènements ###
            for event in pygame.event.get():            # Parcours de tous les events pygame dans cette fenêtre
                if event.type == pygame.QUIT:           # Si l'évènement est le clic sur la fermeture de la fenêtre
                    running =  False                    # running est sur False
                    sys.exit()                          # Pour fermer correctement
                ### Gestion du clavier ###
                if event.type == pygame.KEYDOWN:        # Si une touche a été tapée KEYDOWN quand on relache la touche
                    if event.key == pygame.K_ESCAPE:    # Si la touche est échap
                        running = False
                        sys.exit()                      # Pour fermer correctement
                    if event.key == pygame.K_SPACE:     # Si la touche est espace
                        pause = not pause               # (Dés)activer sous-boucle unpause
                        screen.fill("black")            # Remplir l'écran de noir
                        if pause == False:              # Si le jeu repart
                            actualiser()                # On actualise la scène, soit réafficher les cases
                            texte.mettre_a_jour(0, 0, joueur)
                            j1      :int    = plateau.compter(1)
                            j2      :int    = plateau.compter(2)
                            texte.mettre_a_jour(j1, j2, joueur)
            if joueur == 1:
                if pygame.mouse.get_pressed(num_buttons=3)[0]:
                    if pygame.mouse.get_pos()[0]%(cote) not in tab and pygame.mouse.get_pos()[1]%(cote) not in tab:
                        # Tuple contenant les coordonnées de la souris
                        coords      :tuple  = pygame.mouse.get_pos()
                        # Tuple contenant les coordonnées de la case "cliquée"
                        case_jouer  :tuple  = (int(coords[1]//(cote)), int(coords[0]//(cote)))
            
            taille  :int     = screen.get_size()
            if taille != derniere:               # Si la taille d'écran a changée entre la dernière itération de la boucle et celle-ci
                derniere     = taille              # On met à jour l'ancienne taille d'écran
                nouveau :int = int((taille[1]//100)*100)
                dimensions   = (nouveau, nouveau)
                cote         = (dimensions[0] if dimensions[0]<dimensions[1] else dimensions[1])/8
                image        = pygame.transform.scale(Rimage, dimensions)
                i_joueur     = pygame.transform.scale(Ri_joueur, dimensions)
                i_ia         = pygame.transform.scale(Ri_ia, dimensions)
                i_nul        = pygame.transform.scale(Ri_nul, dimensions)
                chrono.position = (nouveau + 20, 0)
                texte.position  = (nouveau + 20, 150)
                actualiser()                    # On actualise la scène, afin de bien redessiner le plateau
                texte.mettre_a_jour(0,0,0)
            
            ### Si le jeu n'est pas en pause ###
            if pause == False:                
                case_1  :list   = plateau.case(1)   # Cases possibles de jeu pour le joueur 1
                case_2  :list   = plateau.case(2)   # Cases possibles de jeu pour le joueur 2
                
                if len(case_1)==0 and len(case_2)==0:   # Si aucun coup n'est possible
                    gagnant :int    = plateau.quiGagne()
                    j1      :int    = plateau.compter(1)
                    j2      :int    = plateau.compter(2)
                    joueur  :int    = 0
                    texte.mettre_a_jour(j1,j2,joueur)
                    avance  :int    = j1-j2 if gagnant==1 else j2-j1
                    
                    if gagnant == 0:
                        screen.blit(i_nul,(0,0))
                    elif gagnant == 1:
                        screen.blit(i_joueur,(0,0))
                    elif gagnant == 2:
                        screen.blit(i_ia,(0,0))
                    chrono.tempsPause += fps_clock.tick(60)
                    chrono.dessiner()
                    
                elif joueur == 1:                           # Sinon, si c'est le tour du joueur 1
                    if len(case_1)==0:                      # Si le joueur 1 ne peut pas jouer
                        joueur = 2                          # C'est au tour du joueur 2
                    elif case_jouer in case_1:              # Sinon, on vérifie que la case sélectionnée est jouable par le joueur 1
                        plateau.jouer(1, case_jouer)        # On fait jouer le joueur 1 sur la case sélectionnée
                        actualiser()                        # On actualise la scène
                        joueur = 2                          # C'est au tour du joueur 2

                elif joueur == 2:                           # Sinon, si c'est le tour du joueur 2
                    if len(case_2) > 0:                     # Si le joueur 2 peut jouer
                        minmax  :object = ia.Arbre(plateau, 2, difficulte, 0)    # L'IA créer l'arbre des possibilitées de jeu
                        coup    :tuple  = minmax.chercher() # L'IA applique l'algorithme MinMax pour chercher son meilleur coup (d'après l'euristique)
                        plateau.jouer(2, coup[1])           # On fait jouer le joueur 2 sur la case sélectionnée
                        actualiser()                        # On actualise la scène
                    joueur = 1                              # C'est au tour du joueur 1

                if not(len(case_1)==0 and len(case_2)==0):  # Si les joueurs pouvaient jouer, on met à jour le chrono et le score
                    dt  :float  = fps_clock.tick(60)
                    chrono.mettre_a_jour(dt)
                    chrono.dessiner()
                    j1      :int    = plateau.compter(1)
                    j2      :int    = plateau.compter(2)
                    texte.mettre_a_jour(j1, j2, joueur)

            ### Si le jeu est en pause ###
            else:
                chrono.tempsPause += fps_clock.tick(60)
                chrono.dessiner()
                screen.blit(image,(0,0))
                texte.mettre_a_jour(0, 0, 0)
                j1      :int    = plateau.compter(1)
                j2      :int    = plateau.compter(2)
                texte.mettre_a_jour(j1, j2, joueur)
            
            ### Quelque soit l'état du jeu, on met à jour l'écran ###
            pygame.display.flip()


# Image mode pause
# https://pixabay.com/fr/photos/le-noir-conseil-traces-de-craie-1072366/ nh