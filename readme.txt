-Une personne doit lancer le fichier serveur et tous ceux qui veulent utiliser le chat devrait
lancer  le client en arrière-plan (essentielement pour qu'on sache qui est en ligne).
*->EDIT: il est maintenant possible d'acceder au fonctions Serveur/Client 
grace a ProjComP.py. Le serveur cepandant doit etre lancé separément (cmd:py ProjComR.py server)
('py ProjComR.py client' est maintenant accesoire mais reste fonctionel)

-Il est toujours possible de lancer le client et de communiquer avec le serveur de cette manière
pour cela il faut lancer le serveur et puis le client (cmd: py ProjComR.py client)
--> une fois lancé il sera possible de communiquer avec le serveur grace a une interface proposant
differentes fonctions

-Lorsqu'un client communiqe avec le serveur celui ci lui offre 6 possibilitées (6 fonctions).
Les fonctions ci-dessous sont protegées par un mot de passe (echo1234).
	*2. Verifier la base de données
	*6. Fermer le serveur

-Pour communiquer il faut utiliser le reseau/serveur pour obtenir l'addresse IP de la personne
avec laquelle on veut communiquer (ProjComP.py: /IP ou ProjComR.py: fonction 1)

-On ne peut quitter le serveur qu'en utilisant la fonctions 6 (ceci fermera le serveur et il ne sera
plus accesible du tout). Ci on souhaite juste quitter le chat, il faut utiliser la foction 5
(ci on quittais d'une autre manière la base de donné nous considereras toujours comme 'en ligne')

-On suppose qu'une machine ne change pas d'addresse IP après c'être connecté au serveur

-On suppose que les appareils qui ce connecte au serveur seront tous nommés differaments
(avoir 2 "ordininateur-de-benjamin" poserai problème car les clients sont stockées dans un dictionnaire)

-Lorsequ'on utilise le code principale (ProjComP.py), ci on ne mentionne rien le socket ce connectera a l'appareil
que vous utiliser sur le port 5000. Mais il est possible de changer l'hote est le numero de port ci on le 
lance avec cmd. Exm: (cmd:) py ProjComP.py ordinateur3 6000, host= ordinateur3, port= 6000

-Ci on écrit * a la place de 'ordinateur3' dans l'exemple précedent On utilisera automatiquement
le nom de l'appareil qu'on utilise (py ProjComP.py * 6000 ----> connecté a Mioznitnirn : 6000)

-Le code principale contient une commande '/help' qui affiche toutes les commandes possibles

-Il est possible de se donner un pseudo et les autres clients peuvent rechercher un address IP
grace a ce pseudo

-ProjComP.py contient une fonction list mais celle-ci ne ce rapelle que des gens auxquels on c'est
connecté recemment (Il oublie tous une fois qu'on quitte)

-la base de donné contient un dictionaire {hostname: [pseudo, addressIP, en ligne?]}

(-Le code est assez lent dû a des time.sleep() et des timeouts calculés)