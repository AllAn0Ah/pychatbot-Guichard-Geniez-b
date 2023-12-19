"""

My First Chatbot par Noah Guichard et Gabriel Geniez.
Ceci est le fichier main.py, il est le fichier principal du projet et est celui qu'il faut lancer pour faire fonctionner le projet.


"""



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
            resultat = nation(nom_fichiers)
            print(f"les fichier qui ont le termes 'nation' sont :  {resultat[0]}")
            print(f"Le fichier avec le plus grand nombre d'occurrences du mot 'nation' est : {resultat[1]}")
            print(f"Nombre total d'occurrences du mot 'nation' dans ce fichier : {resultat[2]}")
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


