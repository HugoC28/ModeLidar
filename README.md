# ModeLidar

## Introduction
  L'objectif de ce projet est de concevoir un robot roulant télécommandé équipé d'un LiDAR (Light Detection And Ranging) dans le but de réaliser une modélisation 3D de notre école. Ce projet couvre ainsi un large domaine de compétences, notamment en informatique et en électronique de puissance. 

![plan_projet](https://user-images.githubusercontent.com/103205458/174444903-65946355-f00d-41b5-8f76-240362b40eb5.png)


  Le concept initial était de piloter la base roulante *4WD Wild Thumper*, équipée du *Velodyne LiDAR Puck Hi-Res* à l'aide d'un joystick *Miscrosoft SideWinder Force Feedback Pro*. Nous avons fait le choix d'utiliser un *Raspberry Pi 4* pour le pupitre de commande et un pour la base mobile. Nous avons utilisé, pour relier tous ces éléments, le système *ROS*, qui est un environnement Open Source permettant de centraliser les différents composants d'un robot et les faire fonctionner ensemble.
  Pour communiquer et suivre l'avancement de notre projet, nous avons choisi d'utiliser l'outil de gestion de projet *Microsoft Office Planner*.
  
  Après quelques recherches en électronique de puissance, j'ai pour ma part beaucoup travaillé sur la partie informatique et réseaux de ce projet, notamment sur la compréhension du système ROS. 
  
## Electronique de puissance
  J'ai en effet dans un premier temps consulté les documentations de tous les composants de notre robot pour savoir quelle batterie était nécessaire pour les alimenter. Nous avons donc choisi une batterie *Gens Ace 5000mAh 7,4V 2S2P 60C* pour être sûrs d'avoir une capacité suffisante, tout en évitant les échauffements.
  
## Informatique

### Système ROS
  *ROS (Robot Operating Système)* est un ensemble d'outils et de librairies permettant de développer un environnement dédié à la conception de robots. La puissance de cette technologie vient de la grande communauté de développeurs qui améliorent et mettent à jour continuellement la grande variété d'outils Open Source qui composent ROS.
  
  Il nous a donc fallu comprendre le fonctionnement de cet outil qui est dans un premier temps assez difficile à appréhender.
  
  ROS est basé sur un système de *nœuds*. Chaque élément du robot correspond à un *nœud*, et les *nœuds* communiquent ensuite entre eux. Chaque *nœud* peut publier des messages vers un *topic* ou souscrire à un *topic*. C'est ainsi que les différents *nœuds* communiquent entre eux.
  
![schema_noeud_ros](https://user-images.githubusercontent.com/103205458/173875267-c52c2caa-596b-4210-a816-4c0d5e57705d.png)
  
  Dans notre cas, il fallait ainsi créer 2 *nœuds*, l'un pour publier les informations du joystick depuis la Raspberry du pupitre de commande, et l'autre pour souscrire au même *topic* et récupérer ces informations sur la Raspberry de la partie mobile pour commander les moteurs.
  
  Pour fonctionner, ROS a besoin qu'un programme nommé *Roscore* soit exécuté. Il doit y avoir un seul *Roscore* pour tout le robot, et il faut ensuite spécifier à chaque composant l'adresse IP du *MASTER* (système sur lequel *Roscore* est exécuté), ici RPI MOBILE.


### Joystick Miscrosoft SideWinder Force Feedback Pro

  L'objectif initial était d'utiliser le *Miscrosoft SideWinder Force Feedback Pro* que nous avions à disposition pour piloter le robot. Après quelques recherches, nous avons trouvé un [projet GitHub](https://github.com/MaZderMind/SidewinderInterface) consistant à récupérer les trames envoyées par le joystick sur une carte Arduino. Après quelques essais à l'oscilloscope, nous avons obtenus des résultats relativement différents de ceux obtenus dans ce projet. Nous ne pouvions donc pas réutiliser ce travail et il nous a alors fallu développer notre propre système de récupération des trames. Se rendant compte de la complexité et du temps nécessaire pour le réaliser, nous avons décidé de séparer l'équipe Joystick en 2, l'une continuera de travailler sur ce joystick, et l'autre cherchera une autre solution.

### Joystick Raspberry 

![joystick_ensea](https://user-images.githubusercontent.com/103205458/173899441-7979b14d-e491-4cc3-a532-80b8bbc70d78.jpg)

  Nous avons trouvé un joystick réalisé précédemment par d'autres étudiants de l'ENSEA. Il est composé de 2 joysticks reliées à une STM32, qui transmet elle-même les informations à une Raspberry Pi 4 via le port série. La récupération des trames transmises par le port série et leur publication vers le *topic* ROS sont effectués par le programme python [joystick_talker.py](https://github.com/HugoC28/ModeLidar/blob/main/joystick_talker.py). Ces trames sont ensuite reçues par la Raspberry de notre base mobile et transmises à la STM32 pour la commande des moteurs via le programme [proxy.py](https://github.com/HugoC28/ModeLidar/blob/main/proxy.py). Ces fichiers, ainsi que les fichiers [package.xml](https://github.com/HugoC28/ModeLidar/blob/main/package.xml) et [CMakeLists.txt](https://github.com/HugoC28/ModeLidar/blob/main/CMakeLists.txt) sont à placer dans les dossiers des packages ROS préalablement créés ( *joystick_talker.py* dans le package *ensea_modelidar_joy* sur la Raspberry du joystick et *proxy.py* dans le package *ensea_modelidar_robot* sur la Raspberry de la base mobile).
  
  Les extrema de nos joysticks étant différents selon chaque axe, nous avons fait le choix arbitraire de convertir les valeurs de chaque axe en un entier compris entre -100 et +100.

![schema_structure_ros](https://user-images.githubusercontent.com/103205458/173882049-1ec95fe3-31d3-4c5e-93f1-4d4217272456.png)

  L'exécution de notre programme n'étant pas encore automatisée, il faut rentrer au démarrage les lignes de codes suivantes, dans 3 terminaux différents, sur la Raspberry du joystick. Ici, l'adresse IP de notre *MASTER* (base mobile) est 192.168.1.6 et celle de notre joystick 192.168.1.4 .
    
    //terminal 1
    ssh 192.168.1.6
    roscore

    //terminal 2
    ssh 192.168.1.6
    export ROS_MASTER_URI=http://192.168.1.6:11311
    rosrun ensea_modelidar_robot proxy.py
    
    //terminal 3
    export ROS_MASTER_URI=http://192.168.1.6:11311
    export ROS_IP=192.168.1.4
    rosrun ensea_modelidar_joy joystick_talker.py
    

  
## Conclusion

![robot_assemble](https://user-images.githubusercontent.com/103205458/173899096-43156983-8215-45ce-88db-b7e5d52e1cae.jpg)

  Bien que toutes les parties de notre robot fonctionnaient séparément, nous avons malheureusement manqué de temps pour obtenir un robot fonctionnel. Mise à part ces problèmes au moment de l'assemblage, plusieurs améliorations sont possibles comme l'automatisation du démarrage et de la récupération des trames du LiDAR, ou même l'autonomisation totale du robot qui serait possible grâce au LiDAR.
