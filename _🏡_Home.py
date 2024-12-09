import pandas as pd
import numpy as np
import streamlit as st

import mysql.connector

db=mysql.connector.connect(
    host='localhost',
    user='root',
    password='',
    database='classicmodels'
)

st.set_page_config(
    page_title='La mia App💻',
    layout="wide", 
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help':'https://dbdmg.polito.it/',
        'Report a Bug': 'https://dbdmg.polito.it/',
        'About':'# La mia *App*'
    })

st.title('La mia :red[App]')
st.header(':blue[Progetto iniziale]')
st.subheader('Rivendita di modellini di automobili in scala :car:')
st.logo('polito_white.png',link='https://www.polito.it/', size='large')


cursor=db.cursor()
cursor.execute('SELECT lat,lon FROM offices')
points=pd.DataFrame(cursor)
points[['lat','lon']]=points[[0,1]]
points.drop([0,1],inplace=True, axis=1)
points['lat'] = pd.to_numeric(points['lat'], errors='coerce')
points['lon'] = pd.to_numeric(points['lon'], errors='coerce')
st.map(points, size=70, width=20, color='#00FFFF')

