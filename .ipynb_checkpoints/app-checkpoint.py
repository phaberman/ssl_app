# packages
import streamlit as st
import pandas as pd
import numpy as np
import random

# data
folder = 'data/'
file = 'ssl_stats_clean.pkl'
path = folder + file
df = pd.read_pickle(path)
df = df.reset_index(drop = True)

st.sidebar.title('Filters')

# team selector
teams = pd.Series(df.Team.unique())
team_choice = st.sidebar.selectbox(label = 'Select a Team', options = teams)
filtered_team = df.loc[df['Team'] == team_choice].reset_index(drop = True)

# stat sorter
stats = df.columns.tolist()[2:]
sort_choice = st.sidebar.selectbox(label = f"Sort the {team_choice} by Stat", options = stats)
# sorted_df = filtered_team.sort_values(by = sort_choice, ascending = False).reset_index(drop = True)
sorted_df = filtered_team.sort_values(by = sort_choice, ascending = False).drop(columns = {'Team'}).set_index('Name')

st.subheader(f"Team: {team_choice}")
st.dataframe(data = sorted_df, height = 200, width = 800)

# name selector
players = pd.Series(filtered_team.Name.unique())
player_choice = st.sidebar.selectbox(label = f"Select a Player from the {team_choice}", options = players)
filtered_player = filtered_team.loc[filtered_team['Name'] == player_choice].reset_index(drop = True).drop(columns = {'Team'}).set_index('Name')
filtered_player2 = filtered_team.loc[filtered_team['Name'] == player_choice].reset_index(drop = True) # for displaying name_only

name_only = filtered_player2.iloc[0][1]

st.subheader(f"Full Stat Line")
st.dataframe(data = filtered_player)

# stat selector
stat_choice = st.sidebar.multiselect(label = f"Select a Stat for {name_only}", options = stats, default = ['GP', 'AVG'])
filtered_stat = filtered_player[stat_choice].reset_index(drop = True)
filtered_stat['Name'] = filtered_player2.Name
filtered_stat = filtered_stat.set_index('Name')
                                                        
st.subheader(f"Selected Stats")
st.dataframe(data = filtered_stat)

st.subheader(f"This Week the {team_choice} Superstar...Will...Be..")
if st.button('Find Out!'):
    superstar_prediction = random.choice(players)
    st.write('OH SHIT! ' + superstar_prediction.upper() + '!')
