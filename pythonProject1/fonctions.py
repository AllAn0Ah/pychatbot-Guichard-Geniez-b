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
    word_doc_count = {}

    for nom_fichier in files_names:
        with open("./cleaned/" + nom_fichier, "r", encoding='utf-8') as file:
            mots = file.read().split()
            mots_sans_doublons = []
            ensemble_mots = set()

            for mot in mots:
                if mot not in ensemble_mots:
                    ensemble_mots.add(mot)
                    mots_sans_doublons.append(mot)


            for word in mots_sans_doublons:
                word_doc_count[word] = word_doc_count.get(word, 0) + 1

    nb_doc = len(files_names)
    #calcule du idf avec le nombre de documents du corpus et la fréquences des mots dans le corpus
    IDF = {}
    for word, count in word_doc_count.items():
        IDF[word] = math.log10(nb_doc / count)

    return IDF

def tf_idf(files_names):
    TF_IDF = []  # Initialize TF_IDF inside the function for each set of documents
    IDF = idf(files_names)
    for nom_fichier in files_names:
        Score = tf([nom_fichier])
        tfidf_scores = [] #pour chaque document on calcule le tf_idf
        for word, tf_score in IDF.items():
            if word in Score:
                tfidf_scores.append(tf_score * IDF[word])
            else:
                tfidf_scores.append(0)#si le mot n'est pas dans le documents, on lui attribut la valeur 0

        TF_IDF.append(tfidf_scores)

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
