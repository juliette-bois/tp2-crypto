# TP2 : stéganographie, signature

---------

L'objectif du TP est de fournir un prototype pour les outils nécessaires à un service de création de diplômes numériques afin d'en vérifier la faisabilité.

Ce diplôme sera constitué d'une image avec les caractéristiques suivantes :
- il contiendra une information visible : le nom de l'étudiant ainsi que sa moyenne
- il contiendra une information cachée par stéganographie : la signature de la concaténation d'un mot de passe + Nom Prénom de l'étudiant + sa moyenne
- il contiendra une signature venant de l'université NIHCAMCURT

### Introduction
Nous avons utilisé le langage Python car ce TP ne demande pas une grosse puissance de calcul.
De plus, Python propose plusieurs librairies pour simplifier le traitement de l'image.

**Comment installer le projet ?**    
A la racine du projet, vous pouvez lancer les commandes suivantes dans votre terminal afin d'installer les dépendances nécessaires.
```
# Pillow
python3 -m pip install --upgrade pip
python3 -m pip install --upgrade Pillow

# PyOpenSSL
pip install pyOpenSSL

# QRCode
pip install qrcode

# CV2
pip install opencv-python
```

Le dossier `tests` contient tous les tests des questions 1 à 3.
En effet, ces questions sont des POC.
Tandis que les questions 4 et 5 réutilisent ces POC afin de proposer un prototype complet du service de création de diplômes numériques.

-------------

### Question 1
L'objectif est de cacher un message dans une image et de le récupérer.
Pour simplifier les choses et pour permettre de stocker un grand nombre de caractères dans l'image, on stocke un caractère par pixel.   
4 bits dans rouge et 4 bits dans vert.   
Afin d'éviter d'utiliser un paramètre `nb_bytes`, on stocke la taille du texte dans les 4 premiers pixels de l'image car on en a besoin pour récupérer les données à la lecture.

Pour tester cette première partie, vous pouvez lancer cette commande dans votre console :
```
python3 hide_in_image.py images/chablais-orig.png testQ1.png "coucou j'adore la crypto"
```
Cela va vous générer une image `testQ1.png` dans laquelle un message est caché.

Puis, vous pouvez vérifier l'existence de ce message en lançant cette commande :
```
python3 read_from_image.py testQ1.png
```
Le message caché devrait s'afficher dans votre console.

-------------

### Question 2
La question 2 représente un POC de signature de fichier.
Pour créer une paire clé publique / clé privée pour pouvoir signer des données, nous avons lancé cette commande :
```
#génération de la clée privée
openssl genrsa -aes256 -out .private_key.pem 4096

#génération de la clée publique à partir de la clé privée
openssl rsa -in .private_key.pem -pubout -out public_key.pem
```

Vous n'avez pas besoin de relancer ces commandes, car nous vous fournissons déjà la paire de clés.

Nous avons utilisé la librairie Python `pyOpenSSL`. Cela nous a permis d'utiliser la paire de clés privée/publique générée précédemment, afin de
signer un fichier puis de vérifier sa signature.
Nous avons choisi d'utiliser l'algorithme de signature SHA256 car c'est l'un des plus utilisés et il est assez sécurisé dans le sens où il faudrait une machine très performante pour casser un tel chiffrement.

Pour tester cette partie, vous pouvez lancer cette commande :
```
python3 data_signature.py testQ1.png
```
Cela va signer le fichier `testQ1.png` et vous retourner un message de vérification de la signature.
Si tout va bien, vous devriez voir apparaître le message `Verified OK` dans votre console.

-------------

### Question 3
La question 3 permet de générer un diplôme simple (sans composant cryptographique) en utilisant une image de fond.
Pour cela, nous avons utilisé la librairie Python `Pillow` qui nous a permis de gérer facilement l'écriture sur une image.

Pour tester cette partie, vous pouvez lancer cette commande dans votre terminal :
```
python3 generate_basic_diploma.py "Pierre Hyvernat" 17,3 testQ3.png
```

-------------

### Question 4
La question 4 permet de générer un diplôme pour n'importe quel étudiant, de signer le diplôme et de cacher la signature dans le fichier.
Pour cela, nous avons repris le code des 3 questions précédentes.

Pour tester cette partie, vous pouvez lancer cette commande dans votre terminal :
```
 python3 generate_signed_diploma.py "Pierre Hyvernat" 17,3 testQ4.png
```

-------------

### Question 5
La question 5 permet d'extraire l'information cachée dans un diplôme et vérifie que l'information n'a pas été corrompue ou modifiée. En l'occurrence, ici il s'agit de la signature.

Pour tester cette partie, vous pouvez lancer cette commande dans votre terminal :
```
python3 verify_signed_diploma.py testQ4.png
```
Si tout va bien, vous devriez voir apparaître le message `Diploma Verified` dans votre console.

-------------

### Fonction supplémentaire : ajout d'un QR-code

Nous avons choisi d'implémenter en plus un QR Code sur le diplôme.
Pour cela, nous avons utilisé les librairies Python `opencv-python` et `python-qrcode`

Nous avons stocké des données dans le QRCode. 
Nous vérifions que les données dans le QR code sont identiques à celles qui sont stockées par stéganographie sur le diplôme.
Cela permet d'ajouter une sécurité supplémentaire au niveau des données stockées afin d'être plus sûrs qu'elles ne soient pas modifiées et que donc le diplôme n'a pas été falsifié.

-------------

### Conclusion sur la faisabilité et l'intérêt du service + Pistes d'amélioration
#### 1. Faisabilité
Dans la vraie vie, un tel prototype ne serait pas envisageable car le service de création de diplômes numériques ne serait pas assez sécurisé.
De plus, la stéganographie mise en place est trop "lourde" et son implémentation est trop "simpliste".

### 2. Intérêt du service
En revanche, l'idée de mettre en place un service de création de diplômes numériques serait très intéressante à mettre en place.
Cela permettrait d'avoir des diplômes numériques officiels, non reproductibles, non falsifiables et uniques pour chaque étudiant.

### 3. Améliorations
Voici quelques pistes d'améliorations :
- pour la stéganographie, on pourrait s'adapter à la taille du texte (adapter le nombre de pixels utilisés pour stocker un caractère)
- pour la stéganographie, on pourrait stoker les caractères au moyen d'une suite mathématique et non de manière linéaire
- gérer le placement du texte sur le diplôme de manière dynamique, afin de gérer toutes les tailles de texte (si le nom d'un étudiant est trop long par exemple)