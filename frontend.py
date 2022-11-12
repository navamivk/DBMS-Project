import streamlit as st
import pandas as pd

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
    df_selection = tournament.query("Tournament_Name == @t")
    st.dataframe(df_selection)
elif opt == "Country":
    c = st.selectbox("Select country: ", country)
    df_selection = country.query("Country_Name == @c")
    st.dataframe(df_selection)
elif opt == "Year":
    y = st.selectbox("Select year: ", year)
    tournament['Year'] = pd.DatetimeIndex(tournament['Start_Date']).year
    df_selection = tournament.query("Year == @y")
    st.dataframe(df_selection)
elif opt == "Player Name":
    p = st.selectbox("Select player: ", player_name)
    df_selection = player.query("Player_Name == @p")
    st.dataframe(df_selection)
elif opt == "Player ID":
    pid = st.selectbox("Select player ID: ", player_id)
    df_selection = player.query("Player_ID == @pid")
    st.dataframe(df_selection)
elif opt == "Match ID":
    mid = st.selectbox("Select Match ID: ", match_id)
    df_selection = matches.query("Match_ID == @mid")
    st.dataframe(df_selection)