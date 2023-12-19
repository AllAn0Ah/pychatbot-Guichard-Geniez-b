"""

My First Chatbot par Noah Guichard et Gabriel Geniez.
Ceci est le fichier fonctions.py, il est le fichier qui sert à regrouper l'ensemble de nos fonctions qui nous permettent de répondre aux questions.


"""



import os
import math

def list_of_files(directory, extension):

     files_names = []
     for filename in os.listdir(directory):
        if filename.endswith(extension):
            files_names.append(filename)
     return files_names

def liste_des_fichiers(directory, extension):
    noms_fichiers = []
    for filename in os.listdir(directory):
        if filename.endswith(extension):
            noms_fichiers.append(filename)
    return noms_fichiers

def extraire_noms_presidents(files_names):
    noms_presidents = []
    for fichier in files_names:
        if "1" in fichier or "2" in fichier:
            noms_presidents.append(fichier[11:-5])
        else:
            noms_presidents.append(fichier[11:-4])
    return noms_presidents

def associer_prenom(noms_presidents):
    noms_presidents_reels = ["Jacques Chirac", "Emmanuel Macron", "Nicolas Sarkozy", "François Hollande", "François Mitterrand", "Valery", "Giscard dEstaing"]
    prenoms = []
    for i in noms_presidents_reels:
        for j in noms_presidents:
            if j in i:
                prenoms.append(i)
    return prenoms

def mettre_en_minuscule(files_names):
    for nom_fichier in files_names:
        with open("./speeches/" + nom_fichier, "r", encoding='utf-8') as f:
            contenu = f.read()

        # Convertir le texte en minuscules
        resultat = ''
        for caractere in contenu:
            if 65 <= ord(caractere) <= 90:
                resultat += chr(ord(caractere) + 32)
            else:
                resultat += caractere

        #si le dossier ./cleaned/ n'existe pas, on le créé
        if not os.path.exists("./cleaned"):
            os.mkdir("./cleaned")

        with open("./cleaned/" + nom_fichier, "w", encoding='utf-8') as f:
            f.write(resultat)

def traiter_fichiers(files_names):
    if not os.path.exists("./cleaned"):
        os.mkdir("./cleaned")

    for nom_fichier in files_names:
        with open("./cleaned/" + nom_fichier, "r", encoding='utf-8') as f:
            contenu = f.read()
        contenu_nettoye = ''
        #on enlève tous les caractère spéciaux et ponctuation du texte
        for caractere in contenu:
            if ('z' < caractere <= '~') or ('!' <= caractere < 'a'):
                contenu_nettoye += ' '
            else:
                contenu_nettoye += caractere

        with open("./cleaned/" + nom_fichier, "w", encoding='utf-8') as f:
            f.write(contenu_nettoye)

def tf(files_names):
    chaine = ''
    for nom_fichier in files_names:
        with open("./cleaned/" + nom_fichier, "r", encoding='utf-8') as f:
            contenu = f.read()
            chaine += contenu
    #création d'un dictionnaire qui donne le nombre de répétition des mots dans l'ensemble des textes.
    mots = {}
    mots_list = chaine.split()
    for word in mots_list:
        mots[word] = mots.get(word, 0) + 1

    return mots

def idf(files_names):
    Score = []

    for nom_fichier in files_names:
        with open("./cleaned/" + nom_fichier, "r", encoding='utf-8') as file:
            chaine = file.read()
            mots = chaine.split()
            mots_sans_doublons = []
            ensemble_mots = set()

            for mot in mots:
                if mot not in ensemble_mots:
                    ensemble_mots.add(mot)
                    mots_sans_doublons.append(mot)

            dico = {}
            # Initialise un dictionnaire vide
            liste_mot = chaine.split()
            # Met tout les mots de la châine dans une liste
            for mot in liste_mot:
                if mot in dico:
                    dico[mot] += 1
                else:
                    dico[mot] = 1
            # Si le mot est dans le dico, on augmente sa valeur de 1, sinon on l'ajoute
            Score.append(dico)



    nb_doc = len(files_names)
    #calcule du idf avec le nombre de documents du corpus et la fréquences des mots dans le corpus
    IDF = {}
    for mot in mots_sans_doublons:
        compteur = 0
        for i in range(nb_doc):
            if mot in Score[i].keys():
                compteur += 1
        # Pour chaqun des mots, on compte dans combien de doc il apparait
        IDF[mot] = math.log(nb_doc / compteur)
    return IDF

def tf_idf(files_names):
    Score = []
    for nom_fichier in files_names:
        with open("./cleaned/" + nom_fichier, "r", encoding='utf-8') as file:
            chaine = file.read()
            dico = {}
            # Initialise un dictionnaire vide
            liste_mot = chaine.split()
            # Met tout les mots de la châine dans une liste
            for mot in liste_mot:
                if mot in dico:
                    dico[mot] += 1
                else:
                    dico[mot] = 1
            # Si le mot est dans le dico, on augmente sa valeur de 1, sinon on l'ajoute
            Score.append(dico)
    IDF = idf(files_names)
    TF_IDF = [[], [], [], [], [], [], [], []]
    nb_doc = len(Score)
    for mot in IDF.keys():
        for i in range(nb_doc):
            if mot not in Score[i].keys():
                TF_IDF[i].append(0)
            else:
                TF_IDF[i].append(IDF[mot] * Score[i][mot])
    return TF_IDF

def mots_non_importants(liste_tf_idf, mots):
    mots_non_importants = set()
    # Créer un dictionnaire pour stocker la somme des valeurs pour chaque index
    somme_par_index = {}

    for i in range(len(liste_tf_idf)):
        for j in range(len(liste_tf_idf[i])):
            if j not in somme_par_index:
                somme_par_index[j] = 0
            # Calculer la somme pour chaque index j
            somme_par_index[j] += liste_tf_idf[i][j]

    # Parcourir les index et vérifier les mots non importants (somme = 0)
    for index, somme in somme_par_index.items():
        if somme == 0:
            mots_non_importants.add(index)

    # Obtenir la liste des mots non importants en utilisant l'index pour trouver le mot correspondant
    liste_mots = list(mots.keys())
    mots_non_importants_liste = [liste_mots[index] for index in mots_non_importants if index < len(liste_mots)]

    return mots_non_importants_liste

def mots_importants(liste_tf_idf, mots):
    listmotimportants = []
    somme_max = -1  # Initialisation de la somme maximale trouvée

    # Parcours de la liste de TF-IDF pour trouver la somme maximale
    for i in range(len(liste_tf_idf)):
        for j in range(len(liste_tf_idf[i])):
            somme = sum(liste_tf_idf[k][j] for k in range(len(liste_tf_idf)) if j < len(liste_tf_idf[k]))
            if somme > somme_max:
                somme_max = somme

    # Parcours à nouveau pour récupérer les indices des mots ayant la somme maximale
    for i in range(len(liste_tf_idf)):
        for j in range(len(liste_tf_idf[i])):
            somme = sum(liste_tf_idf[k][j] for k in range(len(liste_tf_idf)) if j < len(liste_tf_idf[k]))
            if somme == somme_max and j not in listmotimportants:
                listmotimportants.append(j)

    liste_de_mots = list(mots.keys())
    mots_importants = [liste_de_mots[index] for index in listmotimportants if index < len(liste_de_mots)]
    return mots_importants


def climat(files_names):
    climat_mot = ["climat", "eclologie"]
    nb_climat_ecologie = []
    for nom_fichier in files_names:
        with open("./cleaned/" + nom_fichier, "r", encoding='utf-8') as file:
            contenu = file.read().split()
            a = 0
            for mots in contenu:
                for word in climat_mot:
                    if mots == word:
                        if a == 0:
                            nb_climat_ecologie.append(nom_fichier)
                        a += 1
    return nb_climat_ecologie

def nation(files_names):
    fichier_nations = []
    somme = []
    for nom_fichier in files_names:
        with open("./cleaned/" + nom_fichier, "r", encoding='utf-8') as file:
            contenu = file.read().split()
            a = 0
            for mots in contenu:
                if mots == "nation":
                    if a == 0:
                        fichier_nations.append(nom_fichier)
                    a += 1
        somme.append(a)
    b = 0  # Trouver le maximum de la liste somme
    for i in range(len(somme)):
        if somme[i] >= b:
            b = somme[i]
        if somme[i] == b:
            e = i
    fichier_nation = fichier_nations[e]
    return fichier_nations, fichier_nation, b

def nettoyer_et_tokeniser(texte):
    texte = texte.lower()  # Convertir en minuscules
    # Enlever la ponctuation et diviser en mots
    mots = ''.join(char if char.isalnum() else ' ' for char in texte).split()
    return mots

# Fonction pour calculer la fréquence des termes (TF)
def calculer_tf_question(mots):
    tf_dict = {}
    total_mots = len(mots)
    for mot in mots:
        tf_dict[mot] = tf_dict.get(mot, 0) + 1
    for mot in tf_dict:
        tf_dict[mot] = tf_dict[mot] / total_mots
    return tf_dict


# Fonction pour calculer TF-IDF
def calculer_tfidf_question(files_names, document, tf_dict):
    mots_du_document = nettoyer_et_tokeniser(document)
    IDF = idf(files_names)
    TF_IDF = []
    for mot in IDF.keys():
        if mot in mots_du_document:
            TF_IDF.append(IDF[mot] * tf_dict[mot])
    return TF_IDF
