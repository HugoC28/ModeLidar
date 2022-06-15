# ModeLidar

## Introduction
  L'objectif de ce projet est de concevoir un robot roulant télécommandé équipé d'un LiDAR (Light Detection And Ranging) dans le but de réaliser une modélisation 3D de notre école. Ce projet couvre ainsi un large domaine de compétences, notamment en informatique et en électronique de puissance. 

![plan_projet](https://user-images.githubusercontent.com/103205458/173843100-479ac1ec-ba7d-4a71-9c8a-24d99744ac7c.png)

  Le concept initial était de piloter la base roulante *4WD Wild Thumper*, équipa du *Velodyne LiDAR Puck Hi-Res* à l'aide d'un joystick *Miscrosoft SideWinder Force Feedback Pro*. Nous avons fait le choix d'utiliser un Raspberry Pi 4 pour le pupitre de commande et un pour la base mobile. Nous avons utiliser pour relier tous ces éléments le système *ROS*, qui est un environnement Open Source permettant de centraliser les différents composants d'un robot et les faire fonctionner ensemble.
  Pour communiquer et suivre l'avancement de notre projet, nous avons choisi d'utiliser l'outil de gestion de projet *Microsoft Office Planner*.
  
  Après quelques recherches en électronique de puissance, j'ai pour ma part beaucoup travaillé sur la partie informatique de ce projet, notamment sur la compréhension du système ROS. 
  
## Electronique de puissance
  J'ai en effet dans un premier temps consulté les documentations de tous les composants de notre robot pour savoir quelle batterie était nécessaire pour les alimenter. Nous avons donc choisi une batterie *Gens Ace 5000mAh 7,4V 2S2P 60C* pour être sûrs d'avoir une capacité suffisante, toute en évitant les échauffements.
  
## Informatique

### Système ROS
  *ROS (Robot Operating Système)* est un ensemble d'outils et de librairies permettant de développer un environnement dédié à la conception de robots. La puissance de cette technologie vient de la grande communauté de développeurs qui améliorent et mettent à jour continuellement la grande variété d'outils Open Source qui composent ROS.
  
  Il nous a donc fallu comprendre le fonctionnement de cet outil qui est dans un premier temps assez difficile à appréhender.
  
  ROS est basé sur un système de *noeuds*. Chaque élément du robot correspond à un *noeud*, et les *noeuds* communiquent ensuite entre eux. Chaque *noeud* peut publier des messages vers un *topic* ou souscrire à un *topic*. C'est ainsi que les différents *noeuds* communiquent entre eux.
  
![schema_noeud_ros](https://user-images.githubusercontent.com/103205458/173875267-c52c2caa-596b-4210-a816-4c0d5e57705d.png)
  
  Dans notre cas, il fallait ainsi créer 2 *noeuds*, l'un pour publier les informations du joystick depuis la Raspberry du pupitre de commande, et l'autre pour souscrire au même *topic* et récupérer ces informations sur la Raspberry de la partie mobile pour commander les moteurs.
  
  Pour fonctionner, ROS a besoin qu'un programme nommé *Roscore* soit exécuté. Il doit y avoir un seul *Roscore* pour tout le robot, et il faut ensuite spécifier à chaque *noeud* l'adresse IP du *MASTER* (système sur lequel *Roscore* est exécuté).


### Joystick Miscrosoft SideWinder Force Feedback Pro

  L'objectif initial était d'utiliser le *Miscrosoft SideWinder Force Feedback Pro* que nous avions à disposition pour piloter le robot. Après quelques recherches, nous avons trouvé un [projet GitHub](https://github.com/MaZderMind/SidewinderInterface) consistant à récupérer les trames envoyées par le joystick sur une carte Arduino. Après quelques essais à l'oscilloscope, nous avons obtenus des résultats relativement différents de ceux obtenus dans ce projet. Nous ne pouvions donc pas réutiliser ce travail et il nous a alors fallu développer notre propre système de récupération des trames. Se rendant compte de la complexité et du temps nécessaire pour le réaliser, nous avons décider de séparer l'équipe Joystick en 2, l'une continuera de travailler sur ce joysctick, et l'autre cherchera une autre solution.

### Joystick Raspberry 

![joystick_ensea](https://user-images.githubusercontent.com/103205458/173899441-7979b14d-e491-4cc3-a532-80b8bbc70d78.jpg)

  Nous avons trouvé un joystick réalisé précédemment par d'autres étudiants de l'ENSEA. Il est composé de 2 joysticks reliées à une STM32, qui transmet elle-même les informations à une Raspberry Pi 4 via le port série.

![schema_structure_ros](https://user-images.githubusercontent.com/103205458/173882049-1ec95fe3-31d3-4c5e-93f1-4d4217272456.png)

## Conclusion

![robot_assemble](https://user-images.githubusercontent.com/103205458/173899096-43156983-8215-45ce-88db-b7e5d52e1cae.jpg)


### Remerciements
