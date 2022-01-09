'''
Lucas BARREAU                                                11/05/2020
Gaetan ANDRE

****************************FRUIT BASKET***************************************

Bienvenue dans le fichier fonctions de notre projet.

Dans ce fichier, vous pourrez trouver nos fonctions.

Toutes les variables globales sont decrites dans la procedure var_init

'''
import math
import pygame

def trajectoire(x,g,v0,alpha):
    
    """
     Cette fonctions prend en arguments :
        x : un entier
        g : un reel, la constante d'acceleration gravitationnelle (elle est en 
        argument pour un eventuel ajout d'extension sur la Lune ou autre)
        v0,alpha : deux reels, conditions initiales
    
    Le but de cette fonction est de calculer les coordonnees d'un objet suivant 
    une trajectoire parabolique sans frottements
    
    Cette fonction renvoie le y associe au x en entree
    
    
    """
    
    y=-0.5*g*(x/(v0*math.cos(alpha)))**2+math.tan(alpha)*x
    return y

def coordonnees(xm,ym,fruit_position,liste_fruit,valide):
    """
    Cette fonction prend en arguments :
        xm,ym : les coordonnees du point ou l'utilisateur a clique
        fruit_position : le Rect du fruit
        liste_fruit : la liste globale de l'ensemble des fruits et leur caracteristiques
        valide : un entier qui permet de selectionner le fruit que lance le dino
    
    Le but de cette fonction est de calculer les coordonnees du fruit en fonction 
    de l'angle alpha entre le point en haut a gauche du fruit et le point ou l'utilisateur 
    a clique, ainsi que la longueur entre ces deux points correspondant a v0.
    
    Cette fonction renvoie 3 objets :
        xt,yt : les listes des coordonnees de chaque point de la trajectoire du fruit
        compt : un entier representant le nombre de points

    """
    xt,yt,compt=[],[],0
    v0=liste_fruit[valide][1]*math.sqrt((xm-fruit_position[0])**2+(ym-fruit_position[1])**2)/10 #calcul de la norme de v0 via les methodes de geometrie
    alpha=math.acos((xm-fruit_position[0])/(v0*10/liste_fruit[valide][1])) #calcul de alpha grace aux methodes de trigonometrie
    while 1 :
        xt.append(compt)
        yt.append(float(trajectoire(compt, 9.81, v0, alpha)))
        compt+=1
        if yt[compt-1]<-30 :
            break
    return xt,yt,compt

def ScoreSauvegarde(score):
    
    """
    Son argument est un entier correspondant au nouveau meilleur score
    
    Cette fonction ouvre le fichier texte et ecrit le nouveau meilleur score
    
    """
    high_score=score
    save= open("fichier source/save/high_score.txt", "w", encoding="utf8") #Ouverture du fichier en mode "w" write ecriture
    save.write('{0}'.format(high_score)) #ecrase l'ancien meilleur score
    save.close() #ferme le fichier

def ScoreChargement():      
    
    """
    Cette procedure lit le fichier de sauvegarde cree par la fonction de sauvegarde
    
    Elle retourne le score avec la valeur lue sur le fichier sauvegarde par la fonction ScoreSauvegarde
    """
    load_score=None #on cree une variable de stockage locale
    with open("fichier source/save/high_score.txt", "r",encoding="utf8") as f_load:#Ouverture du fichier en mode "r" read lire
        for line in f_load:
            line = line.strip()  #On supprime les retour charriot en fin de ligne
            if line:
                 list_score= [str(a) for a in line]  #On recupere notre score sous forme d'une liste de caracteres
        load_score=int("".join(list_score)) #on converti la liste en chaine de caracteres puis en nombre entier
    return load_score


def var_init() :
    """
    
    Cette procedure, comme son nom l'indique, reinitialise l'ensemble des variables
    globales du programme.
    
    Les variables sont de differents types precises au cas par cas
    
    Elle retourne l'ensemble des variables initialisees
    
    """
    
    
    #VARIABLES GLOBALES
    
    #VARIABLES NUMERIQUES
    v0=0 #vitesse initiale
    alpha=0 #angle
    position=0 #position initiale du dino et du fruit sur le terrain
    valide=0 #compteur de panier pour passer d'un fruit a l'autre
    delta_t=40 #timer
    niveau=0 #compteur de niveau
    frame_menu=0 #compteur de l'indice de la frame
    score=0 #score du joueur
    
    #BOOLEENS
    dedans=False #limite le nombre de validation du tir si plusieurs points sont dans le rect du panier
    jouer=False #lance la fenêtre de jeu
    menu=True #lance la fenêtre de menu
    jeu=True #valide la boucle principale comprenant les deux fenetre jouer et menu
    lance=False #lance la trajectoire du fruit quand le joueur clique
    restart=False #relance une partie
    affiche_regle=False #affiche les regles quand vrai
    
    #FRUITS
    """
    Les fruits sont geres de cette maniere, ils sont tous dans une meme liste mais partagent 4 criteres differents :
        0 --> leur taille geree par une variable modifiant la taille des canevas (Rect) de ces derniers
        1 --> leur masse geree par un coefficient par lequel sera multiplie v0 en fonction du poid du fruit : v0 sera augmente ou diminue
        2 --> leur image qui sera importee au sein de la liste
        4 --> leur valeur qui varie d'un fruit a l'autre d'apres la consigne
        
    Nous poserons une norme liee au premier fruit, le citron, pour chacun des parametres. 
    """
    liste_fruit_init=[[1,1,pygame.image.load("fichier source/images/citron.png"),3],[0.5,1.5,pygame.image.load("fichier source/images/framboise.png"),4],[2,0.7,pygame.image.load("fichier source/images/melon.png"),9]]
    liste_fruit=[[1,1,pygame.image.load("fichier source/images/citron.png"),3],[0.5,1.5,pygame.image.load("fichier source/images/framboise.png"),4],[2,0.7,pygame.image.load("fichier source/images/melon.png"),9]]
    fruit=liste_fruit[0][2]
    fruit_position_init=pygame.Rect(640,655,20*liste_fruit[valide][0],20*liste_fruit[valide][0])
    fruit_position=pygame.Rect(640,655,20*liste_fruit[valide][0],20*liste_fruit[valide][0])
    
    #REGELES
    regle=[pygame.image.load("fichier source/images/regle1.png"),pygame.image.load("fichier source/images/regle2.png"),pygame.image.load("fichier source/images/regle3.png")]
    regle_position=[(447,500),(330,450)]
    
    #PANIER
    panier=pygame.image.load("fichier source/images/panier de basket.png")
    panier_position=pygame.Rect(880,400,88,96)
    
    #DINO
    dino1=pygame.image.load("fichier source/images/dino1.png") #frames dino
    dino2=pygame.image.load("fichier source/images/dino2.png")
    dino=dino1
    dino_position_init=pygame.Rect(450,650,200,150)
    dino_position=pygame.Rect(450,650,200,150)
    
    #POLICE ET ECRITURE
    font_type_huge = pygame.font.Font('fichier source/divers/impact.ttf', 90) #ici on initialise nos polices pour plus d'ergonomie
    font_type_big = pygame.font.Font('fichier source/divers/impact.ttf', 50)
    font_type_normal=pygame.font.Font('fichier source/divers/impact.ttf', 25)
    font_type_little=pygame.font.Font('fichier source/divers/impact.ttf', 12)
    
    score_text=font_type_big.render('Score: '+str(score), True, (255, 255, 255))
    score_text_pos=(45,60)
    
    time_txt=font_type_big.render(str(int(delta_t)),True,(255,255,255))
    time_text_pos=(955,60)
    
    quit_txt=font_type_little.render("Quitter = 'Suppr'", True,(255,255,255))
    quit_text_pos=(955,840)
    
    gameover_txt=font_type_huge.render("GAME OVER",True,(255,255,255))
    gameover_text_pos = gameover_txt.get_rect(center=(550, -100))
    
    high_score_txt=font_type_big.render("High Score: "+str(ScoreChargement()),True,(255,255,255))
    high_score_text_pos=(413, 60)
    
    #SONS
    bande_principale=pygame.mixer.music.load("fichier source/sons/bande.wav")
    son_panier=pygame.mixer.Sound("fichier source/sons/ding.wav")
    son_lance=pygame.mixer.Sound("fichier source/sons/lance.wav")
    son_score=pygame.mixer.Sound("fichier source/sons/score.wav")
    son_gameover=pygame.mixer.Sound("fichier source/sons/gameover.wav")
    touche=pygame.mixer.Sound("fichier source/sons/touche.wav")
    
    
    return touche,affiche_regle,regle,regle_position,son_gameover,son_score,bande_principale,son_panier,son_lance,v0,alpha,position,valide,dedans,jouer,menu,frame_menu,niveau,jeu,delta_t,lance,score,liste_fruit_init,liste_fruit,fruit,fruit_position_init,fruit_position,panier,panier_position,dino1,dino2,dino,dino_position_init,dino_position,font_type_huge,font_type_big,font_type_normal,font_type_little,score_text,score_text_pos,time_txt,time_text_pos,quit_txt,quit_text_pos,gameover_txt,gameover_text_pos,restart,high_score_txt,high_score_text_pos
