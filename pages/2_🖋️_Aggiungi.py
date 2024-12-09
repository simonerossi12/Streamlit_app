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

st.set_page_config(layout="wide")
st.title("Aggiungi nuovo prodotto: ")
st.logo('polito_white.png',link='https://www.polito.it/', size='large')

cursor=db.cursor()

with st.form('form'):
    st.subheader(':blue[Inserisci nuovo prodotto:]')
    cod=st.text_input('Codice Prodotto')
    name=st.text_input('Nome Prodotto')
    cat=st.selectbox('Categoria Prodotto',('Classic Cars','Motorcycles','Planes','Ships','Trains','Trucks and Buses','Vintage Cars'))
    scala=st.selectbox('Scala Prodotto',('1:10','1:12','1:18','1:24','1:32','1:50','1:700','1:72'))
    prod=st.selectbox('Produttore',('Autoart Studio Design','Carousel DieCast Legends','Classic Metal Creations','Exoto Designs','Gearbox Collectibles','Highway 66 Mini Classics','Min Lin Diecast','Motor City Art Classics','Red Start DieCast','Second Gear Diecast','Studio M Art Models','Unimax Art Galleries','Welly Diecast Productions'))
    desc=st.text_area('Descrizione prodotto')
    qty=st.slider('Quantità',8,10080)
    price=st.number_input('Prezzo')
    msrp=st.number_input('MSRP')
    submitted=st.form_submit_button('Submit')

if submitted:
    if cod and cat and name and scala and prod and desc and qty and price and msrp:
        cursor.execute('INSERT INTO products(productCode, productName, productLine, productScale, productVendor, productDescription, quantityInStock, buyPrice, MSRP) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)', (cod, name, cat, scala, prod, desc, qty, price, msrp))
        db.commit()
        st.success('Dati inseriti con successo')
    else:
        st.error('Compila i dati obbligatori')