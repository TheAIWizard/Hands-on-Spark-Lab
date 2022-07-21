# TP 0 — Partie 1: Découverte d'Onyxia et de son datalab SSP Cloud

[TOC]

## Objectifs

Dans un premier temps, ce TP a pour but de prendre en main l'interface du datalab SSP Cloud, une instance du logiciel open source Onyxia. Puis, de vous représenter globalement, en toute simplicité, le contexte Spark. Qu'est ce qui se passe quand j'utilise Spark ? C'est quoi déjà ? Qu'est ce que je peux faire avec ? En quoi c'est stylé ? Bon allez, c'est parti on y va !

Pendant ce TP vous allez :

- Créer un compte sur le SSP Cloud si ce n'est pas déjà fait 
- Copier des données dans votre espace de stockage MinIO (S3)
- Lancer un service
- Exécuter différentes commandes de base 
  - `ls` pour lister les documents dans un dossier
  - `cd` pour change directory pour naviguer dans une arborescence de fichiers
  - `yum` pour installer un package
  - `mc cp` pour copier des fichiers depuis un bucket MinIO (S3)
  - `chmod` pour changer les permissions d'un fichier
  - `time [commande]` pour mesurer la temps d'exécution d'une commande
  - `kubectl get pods` pour lister les services/pods en cours de lancement
- Eteindre votre service


## 1. Création d'un compte sur le SSP Cloud d'Onyxia

Il est nécessaire de disposer d’un compte personnel SSP Cloud pour en utiliser les services. Si vous n’avez pas de compte sur le SSP Cloud, vous pouvez vous en créer un en cliquant sur ce lien (https://datalab.sspcloud.fr/home) puis suivre les indications dans l'onglet `Connexion`. Deux points sont importants à noter :
- vous devez utiliser votre adresse mail ENSAI
- votre nom d’utilisateur ne doit contenir ni caractères accentués, ni caractère spécial, ni signe de ponctuation. Ce point est essentiel, car votre compte ne fonctionnera pas si votre nom d’utilisateur comprend l’un de ces caractères. Par exemple, si vous vous appelez Jérôme-Gérard L’Hâltère, votre nom d’utilisateur pourra être jeromegerardlhaltere.

Par défaut, l’interface du SSP Cloud est en anglais. Pour choisir le français, vous avez le choix entre:
  - cliquer en bas à droite de la fenêtre puis choisir le français dans les options proposées
  - cliquer sur `My account` dans le menu de gauche puis dans l’onglet `Interface preferences` vous pouvez changer la langue dans la fenêtre qui s’affiche.

![](img/00_choisir_langue.png)

## 2. Exploration

Mais d'abord, pourquoi parle t-on de Datalab ? Un Datalab est un espace dédié à l’expérimentation de nouveaux outils. Il permet d’explorer des jeux de données, de la traiter, et de tester différents algorithmes de machine learning par exemple. 

Le SSP Cloud est un datalab. Cette plateforme permet aux statisticiens d’utiliser un grand nombre de logiciels de data science dans un environnement informatique ergonomique et performant.

Et Onyxia alors ? Késako ? Onyxia est le nom du projet open source sur lequel est construit le datalab SSP Cloud. Vous pouvez tout à fait créer votre propre Datalab en créant une autre instance d'Onyxia pour votre organisation, entreprise, association, communauté ou une utilisation personnelle par exemple. Quelque part, on parle toujours d'Onyxia.

![](img/datalab.png)

Dans l'onglet “**Catalogue de services**”, vous trouverez, entre autres :

- VS Code, votre éditeur de code préféré 
- R Studio, l'environnement phare pour manipuler R 
- Postgresql, bien pratique pour vos bases de données
- Bien d'autres services dédiés à _l'analyse de données_, à la _Dataviz_, aux _calculs distribués_, au _data engineering_, au _DevOps_, au _ML Ops_, au _machine-learning_...


## 3 Accès à votre espace de stockage MinIO : l'alternative open source à Amazon Simple Storage Service (S3)

Le système S3 (Simple Storage System) est un système de stockage développé par Amazon et qui est maintenant devenu une référence pour le stockage en ligne. Il s’agit d’une architecture à la fois sécurisée (données cryptées, accès restreints) et performante. Il y a plus d'un moyen d'utiliser ce fameux système.

**Amazon Simple Storage Service** (S3) est la solution de base que propose AWS pour stocker vos données de manière pérenne. Amazon dit assurer une durabilité de vos données de 99,999999999 %. Cela signifie que si vous stockez 10 000 000 fichiers avec Amazon S3, vous pouvez vous attendre à perdre en moyenne un objet unique une fois tous les 10 000 ans. Assurer votre stockage est payant sur AWS et ce, à coût relativement élevé. :credit_card: :persevere: :coffin:

L'implémentation de S3 est payante mais sa spécification est gratuite !

**MinIO** fournit une implementation open source de S3. Vous pouvez donc stocker vos données sur MinIO comme si elles étaient sur S3 et ce, gratuitement. :brain: :money_with_wings: :star_struck:

Tous les services du datalab d'Onyxia peuvent nativement lire depuis et écrire vers S3 (MinIO) si vous cochez la case correspondante, au moment de lancer votre service. Ainsi, les programmes que vous exécutez et les données que vous traitez peuvent être importés/exportés dans S3. Chaque élément hébergé dans S3, appelé "objet", est accessible par une URL **unique**. Vous pouvez restreindre ou au contraire étendre les droits d'accès à vos objets.

Patience ! Nous verrons comment lancer un service après cet aparté sur MinIO. L'image ci-dessous vous sert seulement de petit encas pour illustrer mon propos. Ce qui vient d'être expliqué peut par exemple s'appliquer à un service Rstudio.

![](img/coche_s3_lancement_service.png)

- [ ] Cliquez sur ce lien https://minio-console.lab.sspcloud.fr et connectez vous avec votre compte du datalab SSP Cloud 

![](img/MinIO_Console.png)

- [ ] Vous pouvez voir deux "compartiments" (en anglais "bucket") 

![](img/MinIO_Console_Buckets.png) 

- [ ] Votre compartiment est celui marqué par votre identifiant. **Vous seul pouvez remplir ou vider votre bucket donc vous ne pouvez pas modifier ceux des autres utilisateurs**

## 4. Copie des données dans votre espace de stockage

* [ ] Cliquez sur le compartiment marqué par votre identifiant. 

  ![](img/MinIO_Console_Inside_Bucket.png)

- [ ] À partir du bouton `Upload`, ajoutez le fichier zip du lab0 disponible sur Moodle.

![](img/s3_upload_file.png)

- [ ] Une fois le chargement terminé cliquez sur votre fichier. Le lien pour accéder à votre fichier se trouvera à gauche du bouton `Create new path`. 

Félicitations ! Vous savez déposer un fichier sur votre bucket perso sur MinIO.

## 5. Lancement d'un service

- [ ] Cliquer sur l’onglet “**Catalogue de services**” qui est accessible à gauche 

- [ ] Choisissez le service que vous souhaitez lancer dans le catalogue. Prenons Rstudio un logiciel que nous connaissons bien. 

- [ ]  Si besoin, vous choisissez ensuite la configuration de votre service dans `Configuration 'nom du service'`. Par exemple, vous pouvez choisir les ressources alloués à votre conteneur (RAM, CPU) dans l'onglet `Resources`. Si vous souhaitez accéder à votre service depuis n'importe quel ordinateur (adresse IP plus précisément), décochez `Enable IP protection` dans l'onglet `Security` comme le montre l'image ci-dessous: 

  ![](img/enable_ip_protection_service_rstudio.png)

- [ ] Puis cliquez sur `Launch` et c'est parti ! Une vidéo de 34 secondes vaut mieux qu'un long discours 

https://user-images.githubusercontent.com/37664429/179776774-0e4b779f-a841-4269-81a4-eeb5cb44c09f.mp4

- [ ] Satisfait ?

- [ ] Félicitations ! Votre service est en cours de lancement. Si vous avez oubliez le mot de passe de votre service, pas de panique à bord ! Vous pouvez toujours retourner dans `Mes services` et cliquer sur `copier le mot de passe`.

## 7. Ouvrir un terminal sur son service

- [ ] Lancez un service VS Code en configurant dans l'option `Configuration VS Code > Kubernetes`, **admin** comme Role.

Plusieurs services comme Jupyter offrent la possibilité d'ouvrir un terminal. Le plus commode est de lancer un service VS Code et d'ouvrir un terminal comme suit:

![](img/terminal_vscode.png)

###  Petite mise en contexte: 
 
<img src="img/Docker-friends.png" width="500" height="500"> <img src="img/Docker-Symbole.png" width="500" height="300">

Un service est en fait un conteneur ou un conteneur Docker pour les plus intimes c'est-à-dire que le service enveloppe l’application d’un logiciel dans une boîte invisible isolée du reste avec tout ce dont il a besoin pour s’exécuter. 

![](img/happy-docker.png)

Notre VS Code est donc isolé des autres services qui ont pu être lancé. 

![](img/isolement-service.png)

Exemple: si vous lancez 2 VS Code et que vous installez la librairie _emoji_ ![](img/emoji-world.png) dans l'un, il ne sera pas disponible dans l'autre.

Comme les services tournent sur le datalab, n'essayez pas de chercher localement dans vos documents où se trouve les fichiers que vous avez pu créer parce qu'il n'y a aucun lien ! :scream_cat: :clown_face: Votre code s'execute sur un cluster kubernetes distant.

![](img/lost-files.png)

Sans entrer dans les détails, Kubernetes est un orchestrateur qui permet de lancer et gérer plusieurs conteneurs à la volée dans le cloud. C'est ce qui permet à Onyxia de lancer plusieurs services facilement en quelques clicks. Un cluster kubernetes est donc un cluster qui répartit les services que vous voyez sur le datalab dans les différentes machines ou "workers" du cluster.

![](img/orchestrateur.png) ![](img/kuberneteslogo.png)

- [ ] Tapez dans le terminal `kubectl get pods`. Caliente ! Vous pouvez voir tous les services en cours de lancement.
- [ ] Pourquoi pod ? Vous le verrez l'année prochaine mais pour le moment vous pouvez vous dire un pod = un conteneur. Même s'il y a une nuance, c'est souvent le cas en pratique.
- [ ] Pour les très curieux, `kubectl` comme kube controller: un controller contrôle l'état du cluster en permanence. On peut donc contrôler les services qui tournent dans chaque worker et en particulier avoir les pods d'où `get pods`
- [ ] Pour les très très curieux qui souhaitent voir sur quels workers les pods tournent: tapez `kubectl get pods -o wide` et vous verrez une colonne supplémentaire correspondant aux workers. Il faudra être patient pour la suite ...

Avantages: 
  - Votre code ne dépend pas de l'environnemnent de votre machine donc fini les problèmes du type "c'est pas juste :sob: ça ne marche pas sur ma machine mais chez toi si ! :salt: :salt: :salt: "
  - Trop smart :point_right: Vous lancez un service pour chaque appli au lieu de tout installer sur une VM et de perdre toute votre installation quand votre VM s'éteindra :yawning_face: 
  - Vous n'avez pas peur de "casser" votre service car vous pouvez en recréer un autre sans émotion à tout moment contrairement à la VM donc expérimentez au max ! 

Les conteneurs\services ont donc forcément vocation à être éphémères. D'ailleurs, je ne vous l'ai pas dit mais leur durée de vie est de 24 heures environ.
Si vous codez dessus, une bonne pratique est de déposer son code sur git mais ce n'est pas le sujet de ce TP.

## 8. Jouer avec son service

Le but de cette section est de vous faire manipuler quelques commandes de base en bash et de reproduire un benchmark des langages comme fait en cours. Vous allez :

1. Récupérer tous les fichiers nécessaires au benchmark
2. Installer R et un package pour python
3. Réaliser le benchmark.

Pour rappel ce benchmark se base sur le calcul de la température max annuelle à partir des données météo étatsunienne. Chaque fichier contient les données d'une année, avec chaque ligne contenant les données d'une mesure. Les différents programmes font tous la même chose, ils lisent les fichiers pour extraire la température maximum et l'afficher. Mais chaque langage à ses spécificités :

- python : langage typé dynamiquement, compilé à la volée puis interprété python
- java : langage typé statiquement, compilé en byte code à l'avance puis interprété par java
- C : langage typé statiquement, compilé en code machine à l'avance puis exécuté
- script bash :  pas de notion au sens python/java/C, interprété par votre OS. 

###  8.1 Mise en place des fichiers du TP 

Vous vous rappelez de ce fameux fichier TP0 disponible sur notre bon vieux Moodle ? Comme vous êtes trop fort, vous l'avez déjà déposé dans un serveur de stockage distant compatible S3. Si vous ne vous en rappellez pas, c'était à la partie 4.

- [ ] Téléchargez vos fichiers stockés sur S3. Pour ce faire vous allez saisir la commande suivante `mc cp --recursive [s3/uri] [output/folder]`.  Pour récupérer l'URI de votre objet S3, retournez sur MinIO, ouvrez votre bucket, cliquez sur le fichier à uploader et copier le chemin à gauche de `Create new path` comme expliqué précedemment dans la partie 4 . Pour `output/folder`, vous allez utiliser le répertoire courant avec un `.`. Vous devriez obtenir une commande et une sortie similaire à celle-ci :

  ```
  (basesspcloud) coder@vscode-520883-6dff9c886f-6pwpc:~/work$ mc cp --recursive s3/votre-identifiant/fichier TP.zip
  ...dentifiant/fichier TP.zip:  15.84 KiB / 15.84 KiB
  ```

- [ ] Avec la commande `ls` (*list*) vérifiez que vous avez bien téléchargé les fichiers sur S3 dans le répertoire courant. Vous devriez le voir apparaître dans le gestionnaire de donnéees de VS Code.

- [ ] Vous allez maintenant extraire les fichiers de l'archive avec la commande `unzip [nom de votre fichier]`. Vérifiez que cela à bien fonctionné avec la commande `ls`

- [ ] Pour des raisons de sécurité, vos fichiers ne peut être exécuté pour le moment. Utilisez la commande

  `chmod 764 get_data.sh awk.sh GetMaxTempC`

  Pour les rendre exécutable. Pour plus de détails sur la autorisation et la commande chmod (*change mode*) la page [wikipedia](https://fr.wikipedia.org/wiki/Chmod) est une bonne documentation.

- [ ] Maintenant que vous avez vos fichiers, vous allez exécuter le script `get_data.sh`. Pour ce faire tapez `./get_data.sh`.  Ce script va récupérer les fichier depuis les serveurs de la NOAA (= météo France étatsunienne) et les mettre en forme pour le TP.

### 8.2 Installer R et un package python

La machine virtuelle que vous avez crée ne dispose pas tous les programmes nécessaires au benchmark.

- [ ] **Installation de python-dev** : `python-devel` est nécessaire pour créez des extension python. Pour l'installer, vous allez utiliser `yum`, un gestionnaire de packages pour certaines distributions linux (un équivalent au `apt` d'ubuntu). La commande à utiliser est `sudo yum install -y python3-devel.x86_64` (`sudo` pour dire que vous exécuter la commande en super user, `yum` pour dire que vous utiliser le gestionnaire de package, `install` pour dire que vous voulez installez un package, `-y` pour valider l'installation, et `python3-devel.x86_64` le nom du package)
  - [ ] Installez `Cython` avec `pip3 ` et compilez le code cython en faisant :
    - [ ] `cd cythond_code` pour *change directory* qui permet de se déplacer dans votre arborescence
    - [ ] `python3 setup.py` pour lancer la compilation
    - [ ] `cd ../` pour retourner dans la dossier parent.

- [ ] **Installation de R** : pour l'installer R vous allez utiliser le gestionnaire de package d'amazon `amazon-linux-extras`,  avec la ligne de commande suivante : `sudo amazon-linux-extras install R4 -y`.  Le terminal va se remplir de texte pendant quelques minutes n'y prêtez pas attention, c'est juste la machine qui vous dit ce qu'elle fait. 

### 8.2 Benchmark des langages

Dans cette partie vous allez reproduire l'expérience du cours consistant à tester la vitesse de traitement de différents langages. Cela va se faire essentiellement avec la commande `time`. La commande `time` permet de mesurer la temps d'exécution d'une commande passer en argument. Exemple `time chmod 764 get_data.sh` permet de mesurez le temps nécessaire pour pour changer les permission du fichier get_data.sh. Notez chacun des résultats et vérifiez qu'ils sont cohérents avec ceux du cours. Si ce n'est pas les cas, essayez de comprendre pourquoi.

- [ ] Pour lancer le code C compilé et le script bash vous devez faire `time ./[file]` 
- [ ] Pour lancer le code java compilé en jar vous devez utiliser la commande `time java -jar [file.jar]`
- [ ] Pour les codes python utilisez la commande `time python3 [file.py]`
- [ ] Pour lancer un script R vous devez saisir `time Rscript [filename.R]` dans votre terminal.

### 8.3 Un shell dans le navigateur

- [ ] Fermez votre terminal et retournez sur la page de votre instance EC2. Nous allons maintenant nous y connecter via un *cloud shell*. Pour ce faire cliquez sur `Se connecter`
  ![](img/ec2_se_connecter.png)
  Vous allez arriver sur une page similaire à celle ci-dessous. Cliquez sur `Se connecter`
  ![](img/ec2_se_connecter 2.png)
  Après quelques instants vous allez arriver sur votre *cloud shell*
- [ ] ![](img/cloud_shell.png)

Depuis cette écran vous êtes connecté à votre machine distante. Par exemple tapez la commande suivante `ls` pour voir que vous avez bien vos fichiers, puis tentez de les réexécuter.

## 9. Eteindre son service

Une fois le taff fait, n'oubliez pas d'éteindre vos services ! **Pour ne pas gaspiller les ressources !**

Pour éteindre votre service, allez sur l'onglet `Mes services`. Vous pouvez éteindre à tout moment, le service que vous souhaitez à coup de click sur l'icône poubelle.
- [ ] ![](img/arret_service.png)


## Author
- [Nathan Randriamanana](https://github.com/TheAIWizard)

## Version AWS du TP by Rémi Pépin
- [Lab 0 AWS](https://github.com/HealerMikado/panorama_big_data_2021/blob/main/labs/lab%200%20-%20first%20steps%20with%20cloud%20computing/TP%200%20%20D%C3%A9couverte%20de%20l'interface%20d'Amazon%20Web%20Service%20(AWS).md)