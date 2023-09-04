# -*- coding: utf-8 -*-
"""
Created on Tue Dec  7 14:33:28 2021

@author: team caribou
"""

#%%
import pandas as pd
from ast import literal_eval



#on importe le csv movies_metadata et on en fait un dataframe
df_movies = pd.read_csv("movies_metadata.csv", low_memory=False, \
                        usecols = ["title", "vote_average", "genres","vote_count", \
                                   "original_title", "original_language", "runtime", \
                                       "tagline", "release_date",\
                                           "production_countries", "overview", "id"]).dropna()

#on importe le csv credits et on en fait un dataframe    
df_credits = pd.read_csv("credits.csv").dropna()


# on convertit les string en liste de dictionnaires pour df_credits
columns = ['cast', 'crew']
for col in columns:
    df_credits[col] = df_credits[col].apply(literal_eval)

# on convertit les string en liste de dictionnaires pour df_movies
# on utilise literal_eval plutôt qu'eval() car la methode eval est plus dangereuse.
columns_movies = ['genres', 'production_countries']
for col in columns_movies:
    df_movies[col] = df_movies[col].apply(literal_eval)

# on convertit la colonne id de df_movies en int    
df_movies["id"] = df_movies["id"].apply(int)

# on fait une jointure externe (outer join) des deux tables sur la colonne id. 
# reset_index permet d'éviter les soucis d'index suite au dropna.
table_global = pd.merge(df_credits, df_movies, how="outer", on=["id", "id"]).dropna().reset_index(drop=True)


#%%
def obtain_values_cast():
    """
    Cette fonction permet de transformer la liste de dictionnaires dans la colonne cast en liste de string
    des acteurs

    """
    list_of_lists=[]
    for i in range(table_global.index.size):
        list_actors=[]
        list_char = table_global.iloc[i]["cast"]
        for j in range(len(list_char)):
            list_actors.append(list_char[j]["name"].casefold())        
        list_of_lists.append(list_actors)
    return pd.Series(list_of_lists)
    
table_global["cast"] = obtain_values_cast()

#%%
def obtain_values_genre():
    """
    Cette fonction permet de transformer la liste de dictionnaires dans la colonne genre en liste de string
    des genres

    """
    list_of_lists=[]
    for i in range(table_global.index.size):
        list_genres=[]
        list_init = table_global.iloc[i]["genres"]
        for j in range(len(list_init)):
            list_genres.append(list_init[j]["name"].casefold())        
        list_of_lists.append(list_genres)
    return pd.Series(list_of_lists)
    
table_global["genres"] = obtain_values_genre()

#%%
# on ordonne les films par leur note de la meilleure à la moins bonne
#table_global = table_global.sort_values(by = "vote_average", ascending=False)


#%%
def get_actor(actor):
    """
    cette fonction permet de rechercher les 5 meilleurs films dans lesquels un acteur a joué
    pour chaque film, on parcourt la liste d'acteurs et on compare à l'acteur cherché
    si le titre original et le titre americain sont différents, on affiche les 2 titres.
    le compteur total_films permet de s'arrêter à 5 films.

    Parameters
    ----------
    actor : l'acteur qu'on va rechercher.

    Returns
    -------
    None.

    """
    i = 0
    total_films = 0
    while ((i < table_global.index.size) and (total_films < 5)):
        if actor.casefold() in table_global.iloc[i]["cast"]:
            if(table_global.iloc[i]["title"] != table_global.iloc[i]["original_title"]):
                print("{} - {}".format(table_global.iloc[i]["title"], table_global.iloc[i]["original_title"]))
            else:
                print(table_global.iloc[i]["title"])
                total_films += 1
        i += 1
    if(total_films==0):
        print("Aucun film n'a été trouvé")
        
def get_language(langue):
    """
    Cette fonctions affiche les 5 premiers films correspondant à "langue".

    Parameters
    ----------
    langue : la langue recherchée 

    Returns
    -------
    None.

    """
    df_result = table_global.loc[table_global["original_language"]==langue.casefold()][["title", "original_title"]].head()
    if(df_result.empty):
        print("Aucun film n'a été trouvé")
    else:
        print(df_result)
        
    
def get_runtime(runtime):
    """
    Cette fonctions affiche les 5 premiers films correspondant à "runtime".

    Parameters
    ----------
    runtime : la durée recherchée 

    Returns
    -------
    None.

    """
    
    df_result = table_global.loc[table_global["runtime"]==int(runtime)][["title", "original_title"]].head()
    if(df_result.empty):
        print("Aucun film n'a été trouvé")
    else:
        print(df_result)
   
        
def get_genre(genre):
    """
    cette fonction permet de rechercher les 5 meilleurs films correspondant au genre recherché.
    pour chaque film, on parcourt la liste de genres et on compare au genre cherché
    si le titre original et le titre americain sont différents, on affiche les 2 titres.
    le compteur total_films permet de s'arrêter à 5 films.

    Parameters
    ----------
    actor : l'acteur qu'on va rechercher.

    Returns
    -------
    None.

    """
    i = 0
    total_films = 0
    while ((i < table_global.index.size) and (total_films < 5)):
        if genre.casefold() in table_global.iloc[i]["genres"]:
            if(table_global.iloc[i]["title"] != table_global.iloc[i]["original_title"]):
                print("{} - {}".format(table_global.iloc[i]["title"], table_global.iloc[i]["original_title"]))
            else:
                print(table_global.iloc[i]["title"])
                total_films += 1
        i += 1
    if(total_films==0):
        print("Aucun film n'a été trouvé")

#%%           
        
def filter_genre(genre):
    list_films=[]
    for i in range(table_global.index.size):
        if genre.casefold() in table_global.iloc[i]["genres"]:
            list_films.append(table_global.iloc[i]['id'])
    return list_films


def filter_runtime(runtime):
    list_films=[]
    for i in range(table_global.index.size):
        if(table_global["runtime"].iloc[i] == runtime):
            list_films.append(table_global["id"].iloc[i])    
    return list_films

def filter_language(language):
    list_films=[]
    for i in range(table_global.index.size):
        if(table_global["original_language"].iloc[i].casefold()==language.casefold()):
            list_films.append(table_global["id"].iloc[i])            
    return list_films

def search_filter(elements):
    list_genre=[]
    list_runtime=[]
    list_language=[]
    list_final=[]
    
    if (elements[0] != ""):
        list_genre = filter_genre(elements[0])
    if (elements[1] != ""):
        list_runtime = filter_runtime(int(elements[1]))
    if (elements[2] != ""):
        list_language = filter_language(elements[2])      

    
    # ensuite on assemble les listes
    if (elements[0] != "" and elements[1] != "" and elements[2] != ""):
        list_final = set(list_genre).intersection(set(list_runtime), set(list_language))
    elif (elements[0] == "" and elements[1] != "" and elements[2] != ""):
        list_final = set(list_runtime).intersection(set(list_language))
    elif (elements[0] != "" and elements[1] == "" and elements[2] != ""):
        list_final = set(list_genre).intersection(set(list_language))
    elif (elements[0] != "" and elements[1] != "" and elements[2] == ""):
        list_final = set(list_genre).intersection(set(list_runtime))
    elif (elements[0] != "" and elements[1] == "" and elements[2] == ""):
        list_final = list_genre
    elif (elements[0] == "" and elements[1] != "" and elements[2] == ""):
        list_final = list_runtime  
    elif (elements[0] == "" and elements[1] == "" and elements[2] != ""):
        list_final = list_language
    
    
    for id_film in list_final:
        if(table_global["title"].loc[table_global["id"]==id_film].iloc[0] != table_global["original_title"].loc[table_global["id"]==id_film].iloc[0]):
            print("{} - {}".format(table_global["title"].loc[table_global["id"]==id_film].iloc[0], table_global["original_title"].loc[table_global["id"]==id_film].iloc[0]))
        else:
            print(table_global["title"].loc[table_global["id"]==id_film].iloc[0])

#%%
#On enregistre la table utilisateur df_data_user en csv
def update_user_csv(df_data_user, username, histo_genre, histo_actor, histo_language, histo_runtime):
         
        
        df_data_user.loc[df_data_user["username"]==username, ["genre"]] = str(histo_genre)
        
        df_data_user.loc[df_data_user["username"]==username, ["actor"]] = str(histo_actor)
        
        df_data_user.loc[df_data_user["username"]==username, ["language"]] = str(histo_language)
        
        df_data_user.loc[df_data_user["username"]==username, ["runtime"]] = str(histo_runtime)
        
        df_data_user.to_csv("user_data.csv", index = False, header = True, encoding ="utf-8", sep=",")
        

        
#%%


#On importe le csv user_data
df_data_user = pd.read_csv("user_data.csv", sep=",", usecols = ["username","genre","actor","language","runtime","connection_count"]).dropna()
df_data_user["genre"] = df_data_user["genre"].apply(literal_eval)
df_data_user["actor"] = df_data_user["actor"].apply(literal_eval)
df_data_user["language"] = df_data_user["language"].apply(literal_eval)
df_data_user["runtime"] = df_data_user["runtime"].apply(literal_eval)
list_users = list(df_data_user["username"])

#on lit le nombre total de connexions dans le fichier txt, on incrémente et on enregistre
with open('total_use_count.txt') as f:
    total_count = int(f.readlines()[0])
total_count += 1
f.close()
f = open('total_use_count.txt', "w")
f.write(str(total_count))
f.close()

run_program = True
username =""


histo_genre =[]
histo_actor =[]
histo_runtime=[]
histo_language=[]
connection_count_user = 0

keep_user = True

while(run_program):
    
    if(username==""):
        username = input("Créer un utilisateur ou se connecter à un utilisateur existant. Veuillez rentrer un nom d'utilisateur.\n")
        if (username not in list_users):
            list_users.append(username)
            df_temp = pd.DataFrame([[username,[],[],[],[],1]], columns=["username", "genre", "actor", "language", "runtime", "connection_count"])
            #print(df_temp)
            df_data_user = df_data_user.append(df_temp, ignore_index=False)
            #print(df_data_user)
        else:
            histo_genre = df_data_user["genre"].loc[df_data_user["username"]==username].iloc[0]
            histo_actor = df_data_user["actor"].loc[df_data_user["username"]==username].iloc[0]
            histo_runtime = df_data_user["runtime"].loc[df_data_user["username"]==username].iloc[0]
            histo_language = df_data_user["language"].loc[df_data_user["username"]==username].iloc[0]
            df_data_user.at[df_data_user["username"]==username, "connection_count"] = df_data_user["connection_count"].loc[df_data_user["username"]==username] + 1

    choice = input("Bonjour {}, bienvenue dans le catalogue Netflix. Veuillez choisir une option \n \
                   1 - Recherchez un film \n \
                   2 - Filtrez les films selon des critères spécifiques \n \
                   3 - Statistiques \n \
                   4 - Interface utilisateur \n \
                   5 - Interface administrateur \n \
                   q - Quitter le programme \n".format(username))
          
    
        
    if(choice == "1"):
        choice = input("\n \
                   1 - Recherchez par genre \n \
                   2 - Recherchez par acteur \n \
                   3 - Recherchez par durée \n \
                   4 - Recherchez par langue d'origine \n \
                   r - Retour au menu \n \
                   q - Quitter le programme \n")
                   
        if(choice == "1"):
            genre = input("Choisissez un genre (Animation Adventure Action Comedy Romance Family History Drama Crime Science Fiction Fantasy Thriller Documentary Horror Mystery) \n")
            histo_genre.append(genre.casefold())
            get_genre(genre)
        elif(choice == "2"):
            actor = input("Recherchez un acteur\n")
            histo_actor.append(actor.casefold())
            get_actor(actor)
        elif(choice == "3"):
            runtime = input("Recherchez une durée en minutes\n")            
            histo_runtime.append(int(runtime))
            get_runtime(runtime)
        elif(choice == "4"):
            language = input("Recherchez une langue (fr, en, zh, it, es, ar, de, nl, sv, ja, cy, hu, ro, sr, pt, he, bn, ko) \n")
            histo_language.append(language.casefold())
            get_language(language)
        
        
    elif(choice == "2"):
        elements_filtre = ["","",""]
        elements_filtre[0] = input("Vous pouvez filtrer par genre (Animation Adventure Action Comedy Romance Family History Drama Crime Science Fiction Fantasy Thriller Documentary Horror Mystery). \nLaissez vide sinon.\n")
        elements_filtre[1] = input("Vous pouvez filtrer par durée du film.\nLaissez vide sinon.\n")
        elements_filtre[2] = input("Vous pouvez filtrer par pays (fr, en, zh, it, es, ar, de, nl, sv, ja, cy, hu, ro, sr, pt, he, bn, ko.\nLaissez vide sinon.\n")
        search_filter(elements_filtre)
        
    #Zone statistiques 
    elif(choice == "3"):
        print(f"Voici des stats {username} \n")
        choice = input("\n \
                   1 - Nombre total de films \n \
                   2 - Nombre total d'heures de films \n \
                   3 - Nombre de langues \n \
                   r - Retour au menu \n \
                   q - Quitter le programme \n")
                   
        if(choice == "1"):
            total_film = table_global.index.size
            print(f"Il y'a au total {total_film} films dans notre base de données.")
           
        elif(choice == "2"):
            heures_total = sum(table_global["runtime"])
            jours = heures_total/24
            annees = jours/365
            print(f"Il y'a au total {heures_total:.2f} heures, soit {jours:.2f} jours, soit {annees:.0f} années de film dans notre base de données. ")
            
        elif(choice == "3"):
            liste_langue =[]
            for i in range(table_global.index.size):
                liste_langue.append(table_global["original_language"].iloc[i])
            
            total_langue = len(set(liste_langue))
            print(f"Il y'a {total_langue} langues dans notre base de données. ")
            
    # options utilisateur
    elif(choice == "4"):
        choice = input("Options utilisateur. Que désirez-vous faire ?\n \
                       1 - Afficher son historique de recherche \n \
                       2 - Statistiques personnelles \n \
                       3 - Supprimer compte \n \ " )
                          
                  
                       
        if choice == "1":
            print(f"{username} , voici vos données : ")   
            print(df_data_user["genre"].loc[df_data_user["username"]==username])
            print(df_data_user["actor"].loc[df_data_user["username"]==username])
            print(df_data_user["language"].loc[df_data_user["username"]==username])
            print(df_data_user["runtime"].loc[df_data_user["username"]==username])
            
        if choice =="2":
            print(f"{username}, voici votre total de connexions : ")
            print(df_data_user["connection_count"].loc[df_data_user["username"]==username])
        
        if choice == "3":
            accord_final = input(f"Attention {username}, vous êtes sur le point d'effacer entièrement vos données ! \n\
                                 Etes vous sur de vouloir disparaitre à jamais ? (O/N) ? : ")
            if accord_final == "O":
               df_data_user = df_data_user[df_data_user.username != username]
               keep_user = False
               run_program = False
            
            else :
                print(f"Le meilleur choix de votre vie {username} ! ")
    # options administrateur     
    elif(choice == "5"):
        print("Attention simple mortel, vous entrez dans la zone administateur. ")
        sainte_cle = input("Veuillez rentrer la sainte clé : ")
        if sainte_cle == "admin":
            choice = input("\n \
                   1 - Nombre total de connexions utilisateur \n \
                   2 - Nombre total de compte utilisateur \n \
                   3 - Noms de langues \n \
                   r - Retour au menu \n \
                   q - Quitter le programme \n")
                   
            if choice == "1":
                print(f"Il y'a eu {total_count} connexions sur notre super base de films ! ")
                
            elif choice == "2":
                total_user = df_data_user.index.size
                print(f"Il y'a {total_user} merveilleux utilisateurs . ")
                
            elif choice == "3":
                total_nom_langue =[]
                for i in range(table_global.index.size):
                    total_nom_langue.append(table_global["original_language"].iloc[i])
                    nom_langue = set(total_nom_langue)
                print(f"Voici la liste des langues, la Tour de Babel n'a qu'a bien se tenir : \n {nom_langue}")
            
                   
        else:
            print("Essaie encore {username}, le Paradis n'est pas loin.")
    if(choice == "r"):
            continue    
    if(choice == "q"):
        run_program = False

if(keep_user):        
    update_user_csv(df_data_user, username, histo_genre, histo_actor, histo_language, histo_runtime)
else:
    df_data_user.to_csv("user_data.csv", index = False, header = True, encoding ="utf-8", sep=",")
            
        
#%%

