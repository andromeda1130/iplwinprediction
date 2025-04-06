import streamlit as st
import pickle
import pandas as pd

teams = ['Royal Challengers Bengaluru',
 'Mumbai Indians',
 'Kolkata Knight Riders',
 'Rajasthan Royals',
 'Chennai Super Kings',
 'Sunrisers Hyderabad',
 'Delhi Capitals',
 'Punjab Kings',
 'Lucknow Super Giants',
 'Gujarat Titans']

cities = ['Kolkata', 'Mumbai', 'Delhi', 'Lucknow', 'Jaipur', 'Dharamsala',
       'Chandigarh', 'Hyderabad', 'Abu Dhabi', 'Pune', 'Bangalore',
       'Mohali', 'Chennai', 'Centurion', 'Cuttack', 'Bengaluru',
       'Guwahati', 'Navi Mumbai', 'Raipur', 'Cape Town', 'Visakhapatnam',
       'Indore', 'Ahmedabad', 'Johannesburg', 'East London', 'Durban',
       'Bloemfontein', 'Port Elizabeth', 'Nagpur', 'Kimberley', 'Ranchi',
       'Dubai', 'Sharjah']

pipe = pickle.load(open('ipl_win_predictor.pkl','rb'))
st.title('IPL Win Predictor')

col1, col2 = st.columns(2)


with col1:
    batting_team = st.selectbox('Select the batting team',sorted(teams))
with col2:
    bowling_team = st.selectbox('Select the bowling team',sorted(teams))

selected_city = st.selectbox('Select host city',sorted(cities))

target = st.number_input('Target')

col3,col4,col5 = st.columns(3)

with col3:
    score = st.number_input('Score')
with col4:
    overs = st.number_input('Overs completed')
with col5:
    wickets_out = st.number_input('Wickets out')

if st.button('Predict Probability'):
    runs_left = target - score
    balls_left = 120 - (overs*6)
    wickets_left = 10 - wickets_out
    if overs == 0:
        crr = 0
    else:
        crr = score / overs
    rrr = (runs_left*6)/balls_left

    input_df = pd.DataFrame({'batting_team':[batting_team],'bowling_team':[bowling_team],'city':[selected_city],'runs_left':[runs_left],'balls_left':[balls_left],'wickets_left':[wickets_left],'total_runs_x':[target],'crr':[crr],'rrr':[rrr]})

    result = pipe.predict_proba(input_df)
    loss = result[0][0]
    win = result[0][1]
    st.header(batting_team + "- " + str(round(win*100)) + "%")
    st.header(bowling_team + "- " + str(round(loss*100)) + "%")