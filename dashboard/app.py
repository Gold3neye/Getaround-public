import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from datetime import datetime
import openpyxl

### Configuration de la page
st.set_page_config(
    page_title="Dashboard GetAround",
    page_icon="🚗",
    layout="wide"
)

# URL pour télécharger les données
DATA_URL = ('https://full-stack-assets.s3.eu-west-3.amazonaws.com/Deployment/get_around_delay_analysis.xlsx')

### Application
# Le contenu sera affiché linéairement sur le tableau de bord
st.title("Dashboard GetAround")

st.markdown("""
    Analyse des données concernant les retours tardifs des voitures et leurs impacts sur les utilisateurs et l'entreprise. Ce tableau de bord a été créé par Melchior Pedro-Rousselin.
""")

st.markdown("---")


# Utiliser `st.cache` pour stocker les données en cache pour éviter de les recharger à chaque actualisation de l'application
@st.cache
def load_data(nrows=''):
    data = pd.DataFrame()
    if (nrows == ''):
        data = pd.read_excel(DATA_URL)
    else:
        data = pd.read_excel(DATA_URL, nrows=nrows)

    # Considérer qu'un délai négatif (en minutes) signifie que le véhicule a été retourné en avance
    # Donc le véhicule a été retourné à l'heure, on met donc les valeurs négatives à 0
    data["delay_at_checkout_in_minutes"] = data["delay_at_checkout_in_minutes"].apply(lambda x: 0 if x < 0 else x)

    return data


data_load_state = st.text('Chargement des données...')
data = load_data()
data_load_state.text("")  # changer le texte de "Loading data..." à "" une fois que la fonction load_data a été exécutée

# Explications en Markdown
st.subheader("À propos des données")
st.markdown(f"""
    Les données sont un échantillon de **{data["rental_id"].size}** enregistrements de locations. Regardons la proportion de retours tardifs.
""")

# Graphique montrant les proportions de checkouts tardifs
fig = px.histogram(
    data["delay_at_checkout_in_minutes"].apply(lambda x: "En retard"
if
x > 0 else "À l'heure ou en avance").rename("Checkouts en retard"),
x = "Checkouts en retard"
)
st.plotly_chart(fig)

st.markdown("""
    En se concentrant uniquement sur les retours tardifs, voici la répartition des retards au checkout.
""")
# Graphique montrant le temps écoulé en minutes avant un checkout tardif
fig = px.histogram(
    data[
        (data["delay_at_checkout_in_minutes"] > 0) &
        (data["delay_at_checkout_in_minutes"] < 1000)
        ]["delay_at_checkout_in_minutes"].rename("Retard au checkout en minutes"),
    x="Retard au checkout en minutes"
)
st.plotly_chart(fig, use_container_width=True)

### Focus sur les locations enchaînées
st.subheader("Locations enchaînées")

# Joindre la table avec elle-même pour ajouter des informations sur la location précédente pour chaque ligne
data_chain = pd.merge(data, data, how='inner', left_on='previous_ended_rental_id', right_on='rental_id')
data_chain = data_chain.drop(
    [
        "delay_at_checkout_in_minutes_x",
        "rental_id_y",
        "car_id_y",
        "time_delta_with_previous_rental_in_minutes_y",
        "previous_ended_rental_id_y"
    ],
    axis=1
)
data_chain.columns = [
    'rental_id',
    'car_id',
    'checkin_type',
    'state',
    'previous_ended_rental_id',
    'time_delta_with_previous_rental_in_minutes',
    'prev_rent_checkin_type',
    "prev_rent_state",
    'prev_rent_delay_at_checkout_in_minutes',
]

# Supprimer les lignes où prev_rent_delay_at_checkout_in_minutes est NaN
data_chain = data_chain[~data_chain["prev_rent_delay_at_checkout_in_minutes"].isnull()]

## Comptage des checkins retardés
chained_rentals_nb = data_chain["rental_id"].size
st.markdown(f"""
    Concentrons-nous maintenant sur les locations enchaînées.
    Deux locations sont enchaînées si la voiture est utilisée par deux utilisateurs différents dans une courte période.
    Dans ce cas, le retard au checkout d'un client peut ou non impacter le checkin du client suivant.
    
    Il y a **{chained_rentals_nb}** cas utilisables de locations enchaînées dans les données (location ni annulée ni manquant une valeur "delay_at_checkout").
""")
# Taguer les lignes où le checkin a été retardé à cause d'un retour tardif
data_chain["delay_at_checkin"] = (data_chain["time_delta_with_previous_rental_in_minutes"] - data_chain[
    "prev_rent_delay_at_checkout_in_minutes"]).apply(lambda x: x if x > 0 else 0)
data_chain["delayed_checkin"] = data_chain["delay_at_checkin"].apply(lambda x: "Retardé" if x > 0 else "À l'heure")

fig = px.histogram(
    data_chain["delayed_checkin"].rename("Checkins retardés"),
    x="Checkins retardés"
)
st.plotly_chart(fig)

## Temps de retard aux checkins
pb_in_data = data_chain["delayed_checkin"].value_counts()["Retardé"]
st.markdown(f"""
    Il y a **{pb_in_data}** cas problématiques de locations enchaînées. Visualisons combien de temps les checkins ont été retardés.
""")
## 3 Graphiques montrant le retard au checkin (total, et segmenté moins et plus de 90min)
fig = px.histogram(
    data_chain[data_chain["delay_at_checkin"] > 0]["delay_at_checkin"].rename("Retard au checkin en minutes"),
    x="Retard au checkin en minutes"
)
st.plotly_chart(fig, use_container_width=True)
col1, col2 = st.columns(2)
with col1:
    fig = px.histogram(
        data_chain[(data_chain["delay_at_checkin"] > 0) & (data_chain["delay_at_checkin"] <= 100)][
            "delay_at_checkin"].rename("Retard au checkin en minutes (moins de 100min)"),
        x="Retard au checkin en minutes (moins de 100min)")
    st.plotly_chart(fig)
with col2:
    fig = px.histogram(
        data_chain[data_chain["delay_at_checkin"] > 100]["delay_at_checkin"].rename(
            "Retard au checkin en minutes (plus de 100min)"),
        x="Retard au checkin en minutes (plus de 100min)")
    st.plotly_chart(fig)
st.markdown(f"""
    Notez que les pics observés peuvent provenir de la manière dont les données ont été recueillies, plutôt que d'habitudes des clients d'être en retard de manière exacte par multiples de 30min. Des enquêtes plus approfondies seraient nécessaires pour conclure.
""")

### Seuil: temps minimum entre deux locations
st.subheader("Test du seuil")

## Référence
st.markdown(f"""
    Utilisez le formulaire ci-dessous pour appliquer différents délais minimums entre deux locations et visualiser son effet sur les données.

    À titre de référence, sans seuil il y a:
    - **{pb_in_data}** cas problématiques
    - **{chained_rentals_nb}** locations enchaînées au total
""")

## Formulaire de seuil
with st.form("threshold_testing"):
    threshold = st.number_input("Seuil en minutes", min_value=0, step=1)
    checkin_type = st.selectbox("Types de checkin", ["Mobile et Connect", "Connect uniquement", "Mobile uniquement"])
    submit = st.form_submit_button("Appliquer")

    if submit:
        # Se concentrer uniquement sur le type de checkin sélectionné
        data_chain_all = data_chain.iloc[:, :]
        if checkin_type == "Connect uniquement":
            data_chain_all = data_chain_all[data_chain_all["checkin_type"] == "connect"]
        elif checkin_type == "Mobile uniquement":
            data_chain_all = data_chain_all[data_chain_all["checkin_type"] == "mobile"]

        # Nombre de problèmes résolus
        pb_solved = 0
        try:
            pb_solved = data_chain_all[data_chain_all["delayed_checkin"] == "Retardé"]["delay_at_checkin"].apply(
                lambda x: "Retardé" if x > threshold else "À l'heure").value_counts()["À l'heure"]
        except:
            pb_solved = 0  # il n'y avait pas de checkin "À l'heure"

        # Nombre de cas affectés
        affected_cases = 0
        try:
            affected_cases = data_chain_all["time_delta_with_previous_rental_in_minutes"].apply(
                lambda x: "Affecté" if x < threshold else "Non affecté").value_counts()["Affecté"]
        except:
            affected_cases = 0  # il n'y avait pas de location "Affectée"
        st.markdown(f"""
            Avec un seuil de **{threshold}**min pour **{checkin_type}** il y a:
            - **{pb_solved}** cas problématiques résolus ({round(pb_solved / pb_in_data * 100, 1)}% résolus)
            - **{affected_cases}** locations affectées ({round(affected_cases / chained_rentals_nb * 100, 1)}% de toutes les locations)
        """)