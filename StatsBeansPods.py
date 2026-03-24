import streamlit as st
import numpy as np 
from matplotlib import pyplot as plt
from pandas import read_csv
import pandas as pd 
import seaborn as  sns
from pandas.plotting import scatter_matrix

st.sidebar.title(" Statistiques descrptives: ")
menu = st.sidebar.selectbox("Navigation",[ 'Les Données','Aperçu du Jeu de Données','Statistiques','Corrélations','Visualisations','Rapport & Recommandations'])

st.markdown("""
    <div style='
        text-align: center;
        background: linear-gradient(135deg, #3e2723, #6d4c41);
        padding: 30px;
        border-radius: 15px;
        margin-bottom: 20px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.3);
    '>
        <h1 style='color: #fff8f1; font-size: 2.8rem; margin: 0;'>
             Beans & Pods
        </h1>
        <p style='color: #d7ccc8; font-size: 1.2rem; margin-top: 10px;'>
            Analyse Descriptive des Ventes
        </p>
        <p style='color: #a1887f; font-size: 0.95rem; margin-top: 5px;'>
            Rapport préparé pour <strong style='color:#ffccbc'>Angeli VC</strong>
        </p>
    </div>
""", unsafe_allow_html=True)

chemin = 'BeansDataSet.csv'
data=read_csv(chemin)
ligne=[f'Vente{x}' for x in range(1,len(data)+1)]
data.index=ligne

if menu == "Les Données":
    st.header('Affichage des donnees:')
    st.dataframe(data)
elif menu == "Aperçu du Jeu de Données":
    st.header('Aperçu du Jeu de Données')

    st.write('Les dimensions :',data.shape)
    
    st.write('Le nombre d\'individus:',data.shape[0])
    st.write('Le nombre de descripteur:',data.shape[1])


    st.subheader('Les 5 pemieres lignes')
    st.write(data.head())
          
    st.subheader('Les 5 dernieres lignes')
    st.write(data.tail(8))

    st.header('Les types de donnees:')
    st.write(data.dtypes)

    st.header('Distribution par region ')
  

    figure,ax=plt.subplots()
    data['Region'].value_counts().plot(kind='bar' , color=['beige','brown'],ax=ax)
    ax.set_xlabel('Regions')
    ax.set_ylabel('Commandes')
    st.pyplot(figure)                               

    st.header('Distribution par Channel ')

    figure,ax=plt.subplots()
    data['Channel'].value_counts().plot(kind='pie' , colors=['beige','brown'],ax=ax)
    ax.set_ylabel('')
    st.pyplot(figure)  

elif menu== 'Statistiques':
        st.header('Statistiques descriptives')
        st.write(data.describe())
        
        st.header('La moyenne')
        st.write(data.select_dtypes(include='number').mean())

        st.header('Statistiques groupées par Channel')
        st.write(data.groupby('Channel').mean(numeric_only=True))

        st.header('Statistiques groupées par Région')
        st.write(data.groupby('Region').mean(numeric_only=True))

elif menu == 'Corrélations':
    figure,ax=plt.subplots(figsize=(15,15))
    sns.heatmap(data.corr(method='pearson',numeric_only=True),annot=True,fmt='.2f',cmap='coolwarm',ax=ax)
    st.pyplot(figure)  

elif menu == 'Visualisations':     
    st.header('Techniques de visualisation')
    st.subheader('Histogramme des variables:')
    data.hist(bins=20, figsize=(15,10), grid=True, layout=(2,3))
    st.pyplot(plt.gcf())

    st.subheader("Histogramme de Robusta:")
    figure, ax = plt.subplots(figsize=(15,15))
    ax.hist(data['Robusta'], bins=20)
    st.pyplot(figure)

    st.subheader('Graphes de densite :')
    data.plot(kind='density', layout=(2,3), figsize=(15,10), subplots=True, sharex=False, sharey=False)  
    st.pyplot(plt.gcf())

    st.subheader('Scatter Matrice  :')
    scatter_matrix(data,figsize=(25,25),c='g')
    st.pyplot(plt.gcf())


    st.subheader('Les pairplots:')
    sns.pairplot(data,hue='Channel')
    st.pyplot(plt.gcf())

    st.subheader('Les pairplots:')
    sns.pairplot(data,hue='Channel',vars=['Robusta','Arabica'])
    st.pyplot(plt.gcf())


    st.subheader('Les Boites a moustaches:')
    data.plot(kind='box',layout=(2,3),figsize=(15,10),subplots=True,sharex=False,sharey=False)
    st.pyplot(plt.gcf())    

    st.subheader('Les Valeurs aberrantes')
    df = data.select_dtypes(include="number")
    resultat=[]

    for col in df.columns:

        Q1=np.percentile(df[col],25)
        Q2=np.percentile(df[col],50)
        Q3=np.percentile(df[col],75)


        IQR=  Q3- Q1
        born_inf=Q1-1.5* IQR
        born_sup=Q1+1.5* IQR
        nb_out_inf=np.sum(df<born_inf)
        nb_out_sup=np.sum(df>born_sup)
        nb_total= nb_out_inf +nb_out_sup

        resultat.append({
            "Col" : col,
            "Q1" : Q1,
            "Q2" : Q2,
            "Q3" : Q3,
            "born_inf" : born_inf,
            "born_sup" : born_sup,
            "nb_out_inf" :nb_out_inf,
            "nb_out_sup" : nb_out_sup,
            "Total" : nb_total

        })

    resultat_df = pd.DataFrame(resultat)

    # Sécurité : convertir Total en nombre
    resultat_df["Total"] = pd.to_numeric(resultat_df["Total"], errors="coerce")

    # Tri
    resultat_df = resultat_df.sort_values(by="Total", ascending=True)   
    st.dataframe(resultat_df)
else:
    st.header("Rapport d'analyse & Recommandations")

    st.subheader("Résumé")
    st.write("""
    Beans & Pods a enregistré 439 transactions de vente réparties sur 2 canaux (Store et Online) 
    et 3 régions (North, Central, South). 
    Le produit le plus vendu est le Robusta et le moins vendu est le Latte.
    La majorité des ventes provient du canal Store et de la région South.
    Les clients Online achètent plus de capsules que les clients en magasin.
    """)

    st.subheader("Recommandations")
    st.write("""
     — Faire plus de publicité sur internet pour vendre plus de capsules en ligne.
    
     — Lancer des promotions dans la région Central car elle commande moins que les autres.
    
     — Mettre le Robusta et l'Espresso en avant dans les publicités car ce sont les produits les plus achetés.
    
     — Proposer des packs grains + capsules à prix réduit pour que les clients achètent plus.
    
     — Offrir une réduction aux clients fidèles du North pour qu'ils continuent à acheter.
    """)

    st.subheader("Informations à collecter dans le futur")
    st.write("""
    - Le prix de chaque produit vendu
    - La date de chaque achat
    - Un numéro pour identifier chaque client
    - Le coût d'achat des produits

    """)


