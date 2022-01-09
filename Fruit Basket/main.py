'''
Lucas BARREAU                                                11/05/2020
Gaetan ANDRE

****************************FRUIT BASKET***************************************

Bienvenue dans le fichier main de notre projet.

L'ensemble de la documentation est redige sans accents et carateres speciaux
pour etre sur de ne pas generer de probleme d'encoding.

Nous utilisons la version 3.3.6 de Spyder et codons en Python 3.7.

Dans ce fichier, vous pourrez trouver notre boucle principale "jeu" et nos deux
sous-boucle "menu" et "gameplay".
Nous avons prit beaucoup de plaisir a travailler l'aspect du jeu en exploitant
le module pygame. Notre jeu fonctionne correctement : le seul bemol est que le
timer ne s'actualise pas pendant la trajectoire du fruit.
Sinon, nous vous laissons juger des problemes que nous n'aurions pas remarques.

Pour une experience de jeu optimale, nous vous recommandons de jouer avec un pc
branche sur secteur, ou un PC portable branche par cable. Sur certains pc, le
fait qu'il ne soit pas branche bride la quantite d'images par secondes et donne
un rendu qui n'est pas fluide.

Si une variable globale ne vous parrait pas claire, consultez la procedure 
var_init du script fonctions.py, tout y est precise !

Si vous voulez tester l'ensemble des fruits et le mecanisme de changement des 
fruits, nous vous invitons a passer en commentaire la condition 
"while delta_t<0 :" situe au debut de la boucle "gameplay".

Si vous voulez relance le jeu ou qu'une erreur survient, veuillez redemarer le 
noyau.

Bon test et bon courage pour la lecture, essayez de battre notre score !

Cordialement,

Documents et references :
    openclassroom sur pygame
    https://www.pygame.org/
    https://stacko
    verflow.com/

'''

import pygame
from pygame.locals import *
import fonctions as fct
import time

pygame.init()
pygame.mixer.init()

#INITIALISATION DES VARIABLES
touche,affiche_regle,regle,regle_position,son_gameover,son_score,bande_principale,son_panier,son_lance,v0,alpha,position,valide,dedans,jouer,menu,frame_menu,niveau,jeu,delta_t,lance,score,liste_fruit_init,liste_fruit,fruit,fruit_position_init,fruit_position,panier,panier_position,dino1,dino2,dino,dino_position_init,dino_position,font_type_huge,font_type_big,font_type_normal,font_type_little,score_text,score_text_pos,time_txt,time_text_pos,quit_txt,quit_text_pos,gameover_txt,gameover_text_pos,restart,high_score_txt,high_score_text_pos=fct.var_init()


#FENETRE ET FOND
fenetre = pygame.display.set_mode((1100, 909),flags = pygame.FULLSCREEN)#on met la fenetre en plein ecran
fond=pygame.image.load("fichier source/images/fond.png")
fenetre.blit(fond,(0,0))
pygame.display.set_caption("Fruit Basket") #titre de la fenetre

# on colle sur la fenêtre les images de base

#FRUIT
fenetre.blit(fruit,fruit_position)

#PANIER
fenetre.blit(panier,panier_position)

#DINO
fenetre.blit(dino,dino_position)

#REGLE
fenetre.blit(regle[0],regle_position[0])

#POLICE ET ECRITURE
fenetre.blit(score_text,score_text_pos)

fenetre.blit(time_txt,time_text_pos)

fenetre.blit(quit_txt,quit_text_pos)

fenetre.blit(high_score_txt,high_score_text_pos)

#ACTUALISATION
pygame.display.flip()


"""

FENETRE GLOBALE

"""
while jeu :
    pygame.mixer.music.set_volume(0.3) #diminue le volume de la musique(on s'entend plus sinon !)
    pygame.mixer.music.play() #lance la bande principale
    """
    
    FENETRE MENU
    
    Affiche le titre le fond le dino le panier et le premier fruit
    
    """
    while menu :
        fenetre.blit(fond,(0,0))
        fenetre.blit(regle[0],regle_position[0])
        if frame_menu==3 : #il n'y a que 3 frames gerees par une boucle pour (0,1,2)
            frame_menu=0 #on remet a 0 le compteur pour ne pas sortir du range de la boucle pour
        menu_titre_frame=[pygame.image.load("fichier source/images/menu_titre1.png"),pygame.image.load("fichier source/images/menu_titre2.png"),pygame.image.load("fichier source/images/menu_titre3.png")]
        menu_titre=menu_titre_frame[frame_menu]
        menu_str_start=font_type_normal.render("Appuyez sur 'espace' pour commencer !",True,(255, 255, 255))  
        time.sleep(0.05)# on fait une pause de 50ms dans l'affichage
        fenetre.blit(menu_str_start,(370,820))
        frame_menu+=1 #l'image change et le fait que le temps soit en pause donne une impression d'animation
        fenetre.blit(menu_titre,(250,50))
        fenetre.blit(dino,dino_position)
        fenetre.blit(fruit,fruit_position)
        fenetre.blit(quit_txt,quit_text_pos)
        fenetre.blit(panier,panier_position)
        for event in pygame.event.get() :
            if event.type==KEYDOWN and event.key==K_DELETE or event.type==QUIT :  #si l'utilisateur appuie sur suppr ou ferme la fenetre
                touche.play() #petit son de touche
                pygame.mixer.music.stop() #on coupe la musique
                pygame.display.quit() #on ferme pygame donc le jeu
            elif event.type==KEYDOWN and event.key==K_SPACE and not affiche_regle: #s'il appuie sur espace :
                touche.play() #petit son de touche
                menu=False #on ferme la boucle menu
                jouer=True #on lance la boucle de gameplay
            #si l'utilisateur clic dans le cadre "regles"
            elif event.type == MOUSEBUTTONDOWN and event.button == 1 and event.pos[0]>regle_position[0][0] and event.pos[1]>regle_position[0][1] and event.pos[0]<regle_position[0][0]+200 and event.pos[1]<regle_position[0][1]+79 :
                touche.play() #petit son de touche
                fenetre.blit(regle[1],regle_position[0])
                pygame.display.flip()
                time.sleep(0.25)
                affiche_regle=True
            elif event.type==KEYDOWN and event.key==K_SPACE and affiche_regle==True :
                touche.play() #petit son de touche
                affiche_regle=False
        if affiche_regle : # on affiche les regles detaillees
            fenetre.blit(regle[2],regle_position[1])
            pygame.display.flip()
        pygame.display.flip()
    
    
    """
    
    FENETRE GAMEPLAY
    
    
    """
    while jouer :
        t_init=time.time() #on mesure le temps ecoule initial
        while delta_t > 0 :
            delta_t= 40-(time.time()-t_init) #on retire la partie initiale du temps ecoule au temps ecoule pendant la boucle pour obtenir la duree ecoulee depuis le debut de la boucle
            time_txt=font_type_big.render(str(int(delta_t)),True,(255,255,255)) #on ecrit sur l'ecran le temps restant en entier sur l'ecran
            fenetre.blit(fond,(0,0)) #on reinitialise l'affichage
            fenetre.blit(score_text,score_text_pos)
            fenetre.blit(high_score_txt,high_score_text_pos)
            fenetre.blit(time_txt,time_text_pos)
            fenetre.blit(dino,dino_position)
            fenetre.blit(panier,panier_position)
            fruit=liste_fruit[valide][2]
            fruit_position_init=pygame.Rect(640-position,655,20*liste_fruit[valide][0],20*liste_fruit[valide][0])
            fruit_position=fruit_position_init
            fenetre.blit(fruit,fruit_position)
            pygame.display.flip()
            for event in pygame.event.get() :
                if event.type==KEYDOWN and event.key==K_DELETE or event.type==QUIT :
                    touche.play() #petit son de touche
                    #on reinitialise tout si l'utilisateur quitte
                    touche,affiche_regle,regle,regle_position,son_gameover,son_score,bande_principale,son_panier,son_lance,v0,alpha,position,valide,dedans,jouer,menu,frame_menu,niveau,jeu,delta_t,lance,score,liste_fruit_init,liste_fruit,fruit,fruit_position_init,fruit_position,panier,panier_position,dino1,dino2,dino,dino_position_init,dino_position,font_type_huge,font_type_big,font_type_normal,font_type_little,score_text,score_text_pos,time_txt,time_text_pos,quit_txt,quit_text_pos,gameover_txt,gameover_text_pos,restart,high_score_txt,high_score_text_pos=fct.var_init()
                    #l'utilsateur reviens alors sur la page du menu
                if event.type==MOUSEBUTTONDOWN and  event.button==1: # quand il clique sur l'ecran :
                    dino=dino2 #le dino leve la tete
                    lance=True
                    xm=event.pos[0] # on stock les coordonnees du clic dans ces deux variables
                    ym=event.pos[1]
                    xt,yt,compt=fct.coordonnees(xm,ym,fruit_position,liste_fruit,valide) # on calcule les liste de coordonnees du fruit
                    
            if lance :   
                son_lance.play() # on lance le son du lancer
                for i in range(compt-1): # tant qu'il y a des coordonnees restantes dans les listes :
                    time_txt=font_type_big.render(str(int(delta_t)),True,(255,255,255)) # on affiche le temps restant
                    move_x=(xt[i+1]-xt[i])*5 #on deplace le fruit
                    move_y=(yt[i]-yt[i+1])*10
                    fruit_position=fruit_position.move(move_x,int(move_y)) #on passe le coefficient en entier pour que l'implementation de pixel fonctionne
                    """ 
                    
                    HITBOX 
                    
                    
                    """
                    if not dedans and fruit_position[0]>860 and fruit_position[1]>380 and fruit_position[0]<960-fruit_position[2]/2 and fruit_position[1]<410 : # si le centre du Rect du fruit se trouve dans celui du panier le dino marque
                        #fruit_position[0] est le x du point en haut a gauche du canevas du fruit si il est dans la zone et que le x extreme droit (on retire la largeure du canevas du fruit a l'extremite de la hitbox pour obtenir sa coordonnee) y est aussi
                        #pareil pour les y, alors il y a panier
                        son_panier.play()#on lance le son du panier
                        score+=int(liste_fruit[valide][3]) #on incremente la valeur du fruit au score
                        score_text=font_type_big.render('Score :'+str(score), True, (255, 255, 255))
                        dedans=True #empeche que plusieurs points verifient les conditions de la hitbox
                        valide+=1
                        if valide==3+niveau and len(liste_fruit)==3+niveau : #si tout les fruits correspondants au premier palier sont rentres alors :
                            position=100 #le dino et le fruit passent a la position 2
                            liste_fruit.append([3,0.5,pygame.image.load("fichier source/images/ananas.png"),7])#on ajoute le fruit correspondant a la position
                            valide=0 # on remet le compteur de panier a 0
                        elif valide==4+niveau and len(liste_fruit)==4+niveau: # on repete ce motif autant de fois qu'il y a de positions !
                            position=200
                            liste_fruit.append([1.5,1,pygame.image.load("fichier source/images/banane.png"),4])
                            valide=0
                        elif valide==5+niveau and len(liste_fruit)==5+niveau:
                            position=300
                            liste_fruit.append([1.2,1,pygame.image.load("fichier source/images/pomme.png"),5])
                            valide=0
                        elif valide==6+niveau and len(liste_fruit)==6+niveau : #quand tout les fruits d'un niveau son rentres :
                            valide=0 # on remet le compteur de panier a 0
                            position=0 # on remet la position du dino et du fruit a 0
                            stock=[]
                            stock=liste_fruit_init
                            liste_fruit_init=liste_fruit
                            liste_fruit=stock # on redonne a liste_fruit sa valeur initiale a l'aide d'une permutation de variables
                            niveau+=1 # on passe au niveau suivant !
                            if niveau>=1 : #si le "niveau" est superieur a 1 on ajoute le fruit correspondant a liste_fruit
                                liste_fruit.append([0.5,1.3,pygame.image.load("fichier source/images/fraise.png"),8])
                            if niveau>=2 :
                                liste_fruit.append([1,1,pygame.image.load("fichier source/images/kiwi.png"),6])
                            if niveau==3 : #si le compteur de niveau est egale a 3 :
                                niveau=0 # il reviens a 0
                            # de cette maniere, le jeu est infini, il ne sera donc termine que par le temps !
                                
                            # Nous pouvons noter que l'on peut ajouter aisement une infinite de niveau suplementaire !
                            
                        fruit_position_init=pygame.Rect(640-position,655,20,20) #on reinitialise les coordonnees du fruit et du dino
                        dino_position_init=pygame.Rect(450-position,650,200,150)
                        fenetre.blit(dino,dino_position) #on recolle sur la fenetre l'ensemble des elements
                        fenetre.blit(fruit,fruit_position)
                        fenetre.blit(score_text,score_text_pos)
                        fenetre.blit(time_txt,time_text_pos)
                        pygame.display.flip()
                    
                    if fruit_position[1]<800 : #si "y" du rect du fruit ne touche pas le sol (y=800px) :
                        fenetre.blit(fond,(0,0))
                        fenetre.blit(high_score_txt,high_score_text_pos)
                        fenetre.blit(score_text,score_text_pos)
                        fenetre.blit(time_txt,time_text_pos)
                        fenetre.blit(dino,dino_position)
                        fenetre.blit(fruit,fruit_position)
                        fenetre.blit(panier,panier_position)
                        pygame.display.flip()
                        time.sleep(0.001)# le fruit se deplace selon la trajectoire toutes les 1 ms
                    
                    if fruit_position[1]>=800 or fruit_position[0]>= 1050 : # si le ballon touche le sol ou sort du terrain alors il revient sur la tete du dino
                        dedans=False
                        lance=False
                        dino=dino1# on reassocie sa premiere frame au dino
                        fruit_position=fruit_position_init# on remet le fruit a sa position initiale
                        dino_position=dino_position_init
                        fenetre.blit(fond,(0,0)) #on reimprime l'ensemble des elements sur la fenetre
                        fenetre.blit(high_score_txt,high_score_text_pos)
                        fenetre.blit(score_text,score_text_pos)
                        fenetre.blit(time_txt,time_text_pos)
                        fenetre.blit(dino,dino_position)
                        fenetre.blit(fruit,fruit_position)
                        fenetre.blit(panier,panier_position)
                        pygame.event.clear() # cette methode permet d'empecher l'utilisateur de mitrailler le clic gauche et donc de faire n fois le même lancer
                        pygame.display.flip()
                        break
        if delta_t<=0 :
            time_txt=font_type_big.render("0",True,(255,255,255)) # de cette maniere meme si le temps est depasse de qqs secondes, l'affichage reste "0"
            son_gameover.play() #On annonce avec l'audio que le jeu est fini
            for i in range (75) :
                fenetre.blit(fond,(0,0))#on reimprime l'ensemble des elements sur la fenetre
                fenetre.blit(high_score_txt,high_score_text_pos)
                fenetre.blit(quit_txt,quit_text_pos)
                fenetre.blit(score_text,score_text_pos)
                fenetre.blit(time_txt,time_text_pos)
                fenetre.blit(dino,dino_position)
                fenetre.blit(fruit,fruit_position)
                fenetre.blit(panier,panier_position)
                pygame.display.flip()
                fenetre.blit(gameover_txt,gameover_txt.get_rect(center=(550, -100+6*i))) #a chaque iteration de la boucle le texte va "descendre" de 6 pixels vers le bas !
                time.sleep(0.001) #toutes les 1ms
                pygame.display.flip()
            while not restart :
                if score>fct.ScoreChargement() : #si le nouveau score est plus grand que le score stocke :
                    son_score.play() #on felicite le joueur avec le son
                    fct.ScoreSauvegarde(score) # on sauvegarde le nouveau meilleur score !
                    new_high_score_txt=font_type_big.render("Nouveau record !!!", True, (255,255,0))
                    fenetre.blit(new_high_score_txt,new_high_score_txt.get_rect(center=(550, 450)))
                    pygame.display.flip()
                restart_txt=font_type_normal.render("Appuyez sur 'espace' pour continuer",True,(255,255,255))
                fenetre.blit(restart_txt,(370,820))
                pygame.display.flip()
                for event in pygame.event.get() :
                    if event.type==KEYDOWN and event.key==K_SPACE:
                        touche.play() #petit son de touche
                        restart=True
                    elif event.type==KEYDOWN and event.key==K_DELETE :
                        touche.play() #petit son de touche
                        pygame.mixer.music.stop() #on coupe la musique
                        pygame.display.quit() #on quitte le jeu
            if restart : #on reinitialise toutes les variables
                touche,affiche_regle,regle,regle_position,son_gameover,son_score,bande_principale,son_panier,son_lance,v0,alpha,position,valide,dedans,jouer,menu,frame_menu,niveau,jeu,delta_t,lance,score,liste_fruit_init,liste_fruit,fruit,fruit_position_init,fruit_position,panier,panier_position,dino1,dino2,dino,dino_position_init,dino_position,font_type_huge,font_type_big,font_type_normal,font_type_little,score_text,score_text_pos,time_txt,time_text_pos,quit_txt,quit_text_pos,gameover_txt,gameover_text_pos,restart,high_score_txt,high_score_text_pos=fct.var_init()
        fenetre.blit(fond,(0,0)) #on reimprime l'ensemble des elements sur la fenetre
        fenetre.blit(high_score_txt,high_score_text_pos)
        fenetre.blit(quit_txt,quit_text_pos)
        fenetre.blit(score_text,score_text_pos)
        fenetre.blit(time_txt,time_text_pos)
        fenetre.blit(dino,dino_position)
        fenetre.blit(fruit,fruit_position)
        fenetre.blit(panier,panier_position)
        pygame.display.flip()