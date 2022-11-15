import streamlit as st
import pandas as pd

import tournamentReport as tR
import playerReport as pR
import matchReport as mR

from pymongo import MongoClient
import pymongo
import pandas as pd
import json

import os
from dotenv import load_dotenv

load_dotenv()

client = MongoClient(f"mongodb+srv://orectique:{os.getenv('DB_P')}@orectique.ixj7l.mongodb.net/?retryWrites=true&w=majority")

db = client['chessOlympiad']

page_title = "Welcome to Gambit"
page_icon = ':horse:'
layout = 'centered'
st.set_page_config(page_title = page_title, page_icon = page_icon, layout = layout)
st.title(page_title + " " + page_icon)
st.subheader("A Chess Olympiad Reporting System")
st.write("A Chess Olympiad is a large-scale event with several internationally-recognized rules governing it and professional matches extending for hours on end. Hence, it can be assumed that there will be a large amount of unorganized information that must be processed. ​Gambit is a software system that equips its users with a systematic way to create, retrieve and update relevant data through a curated SQL database. ​ ")
opt = st.selectbox("Select by: ",['Tournament','Year','Player Name','Player ID','Match ID'])

tournament = pd.read_csv("./Data Files/tournament.csv")
player = pd.read_csv("./Data Files/player.csv")
country = pd.read_csv("./Data Files/country.csv")
matches = pd.read_csv("./Data Files/match.csv")

#tournament.columns.to_list()
year = list((pd.DatetimeIndex(tournament['Start_Date']).year).unique()) 
player_id = player["Player_ID"]
player_name = player["Player_Name"]
country = country['Country_Name']
tournament_name = tournament["Tournament_Name"]
match_id = matches["Match_ID"]

if opt == "Tournament":
    
    t = st.selectbox("Select tournament: ", tournament_name)
    tournament = db['Tournament'].find_one({"Tournament_Name": t})
    st.dataframe(pd.DataFrame(list(tournament)))

    if st.button('Generate Report'):
        tR.generateReport(db, t)
        st.success("Report generated!", icon = '♟️')

        with open('./Outs/tournReport.pdf', 'rb') as f:
            btn = st.download_button(
                label="Download Report",
                data=f,
                file_name=f'{t}.pdf',
                mime='application/pdf'
            )        
# elif opt == "Country":
#     c = st.selectbox("Select country: ", country)
#     df_selection = country.query("Country_Name == @c")
#     st.dataframe(df_selection)
# elif opt == "Year":
#     y = st.selectbox("Select year: ", year)
#     tournament['Year'] = pd.DatetimeIndex(tournament['Start_Date']).year
#     df_selection = tournament.query("Year == @y")
#     st.dataframe(df_selection)
elif opt == "Player Name":
    p = st.selectbox("Select player: ", player_name)
    player = db['Player'].find_one({"Player_Name": p})
    st.dataframe(pd.DataFrame(list(player)))

    if st.button('Generate Report'):
        pR.generateReport(db, p)
        st.success("Report generated!", icon = '♟️')

        with open('./Outs/playerReport.pdf', 'rb') as f:
            btn = st.download_button(
                label="Download Report",
                data=f,
                file_name=f'{p}.pdf',
                mime='application/pdf'
            )      

# elif opt == "Player ID":
#     pid = st.selectbox("Select player ID: ", player_id)
#     df_selection = player.query("Player_ID == @pid")
#     st.dataframe(df_selection)
elif opt == "Match ID":
    mid = st.selectbox("Select Match ID: ", match_id)
    match = db['Match'].find_one({"Match_ID": mid})
    st.dataframe(pd.DataFrame(list(match)))

    if st.button('Generate Report'):
        mR.generateReport(db, mid)
        st.success("Report generated!", icon = '♟️')

    with open('./Outs/matchReport.pdf', 'rb') as f:
        btn = st.download_button(
            label="Download Report",
            data=f,
            file_name=f'{mid}.pdf',
            mime='application/pdf'
        )    