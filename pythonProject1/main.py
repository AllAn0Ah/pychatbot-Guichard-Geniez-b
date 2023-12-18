from fonctions import *



def afficher_menu():
    print("1. Afficher la liste des mots les moins importants dans le corpus de documents.")
    print("2. Afficher le(s) mot(s) ayant le score TD-IDF le plus élevé.")
    print("3. Indiquer le(s) mot(s) le(s) plus répété(s) par le président Chirac.")
    print("4. Indiquer le(s) nom(s) du (des) président(s) qui a (ont) parlé de la  Nation et celui qui l’a répété le plus de fois")
    print("5. Indiquer le(s) nom(s) du (des) président(s) qui a (ont) parlé du climat et/ou de l’écologie")



def principal():
    directory = "./speeches"
    nom_fichiers = list_of_files(directory, "txt")
    mettre_en_minuscule(nom_fichiers)
    traiter_fichiers(nom_fichiers)
    noms_presidents = extraire_noms_presidents(nom_fichiers)
    mots = tf(nom_fichiers)
    idf(nom_fichiers)
    liste_tf_idf = tf_idf(nom_fichiers)
    mots_non_importants(liste_tf_idf, mots)
    mots_importants(liste_tf_idf, mots)
    noms_presidents = extraire_noms_presidents(nom_fichiers)
    prenoms_presidents = associer_prenom(noms_presidents)
    chirac_index = prenoms_presidents.index("Jacques Chirac")
    chirac_tfidf_scores = liste_tf_idf[chirac_index]

    # Récupérer les mots les plus fréquents pour Chirac (en excluant les mots non importants)
    mots_importants_chirac = mots_importants([chirac_tfidf_scores], mots)

    # Calculer le nombre de fois où "Nation" a été mentionnée par chaque président
    nb_nation = {}
    nation_index = list(mots.keys()).index('nation') if 'nation' in mots else None

    if nation_index is not None:
        for i, president in enumerate(prenoms_presidents):
            if nation_index < len(liste_tf_idf[i]):
                nb_nation[president] = liste_tf_idf[i][nation_index]


    # Calculer le nombre de fois où "climat" ou "écologie" ont été mentionnés par chaque président
    nb_climat_ecologie = {}
    climat_index = list(mots.keys()).index('climat') if 'climat' in mots else None
    ecologie_index = list(mots.keys()).index('écologie') if 'écologie' in mots else None

    if climat_index is not None or ecologie_index is not None:
        for i, president in enumerate(prenoms_presidents):
            nb = 0
            if climat_index is not None and climat_index < len(liste_tf_idf[i]):
                nb += liste_tf_idf[i][climat_index]
            if ecologie_index is not None and ecologie_index < len(liste_tf_idf[i]):
                nb += liste_tf_idf[i][ecologie_index]
            if nb > 0:
                nb_climat_ecologie[president] = nb

    continuer = True
    while continuer:
        print()
        print()
        afficher_menu()
        choix = input("Entrez le numéro de l'action que vous souhaitez effectuer (0 pour quitter) : ")
        if choix == "1":
            print(mots_non_importants(liste_tf_idf, mots))
        elif choix == "2":
            print(mots_importants(liste_tf_idf, mots))
        elif choix == "3":
            print("Les mots les plus fréquents pour Jacques Chirac (hors mots non importants) :", mots_importants_chirac)
        elif choix == "4":
            if nb_nation:
                president_max_nation = max(nb_nation, key=nb_nation.get)
                print(f"Le président ayant le plus parlé de la 'Nation' est {president_max_nation}.")
            if president_max_nation:
                print(f"Nombre de fois où la 'Nation' a été mentionnée par {president_max_nation}: {nb_nation[president_max_nation]}")
        elif choix == "5":
            print(climat(nom_fichiers))
        elif choix == "6":
            documents = str(input("Saisir une question :"))
            questions = nettoyer_et_tokeniser(documents)
            tf_dict = calculer_tf_question(questions)
            print(calculer_tfidf_question(nom_fichiers, documents, tf_dict))
        elif choix == "0":
            print("fin")
            continuer = False
        else:
            print("Choix invalide. Veuillez entrer un numéro valide.")


if __name__ == "__main__":
    principal()


