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

st.set_page_config(layout="wide")  # Layout ampio

def formato_abbreviato(numero):
    if numero >= 1_000_000_000:
        return f"{numero / 1_000_000_000:.1f}B"  # Abbreviazione in miliardi
    elif numero >= 1_000_000:
        return f"{numero / 1_000_000:.1f}M"  # Abbreviazione in milioni
    elif numero >= 1_000:
        return f"{numero / 1_000:.1f}k"  # Abbreviazione in migliaia
    else:
        return str(numero)

st.title("Analisi :chart_with_upwards_trend:")
prodotti, staff, clienti= st.tabs(['Prodotti', 'Staff','Clienti'])
st.logo('polito_white.png',link='https://www.polito.it/', size='large')

cursor=db.cursor()
cursor.execute('SELECT * from employees')
data=cursor.fetchall()
columns=[col[0] for col in cursor.description]
employees=pd.DataFrame(data, columns=columns)

cursor=db.cursor()
cursor.execute('SELECT * from orderdetails')
data=cursor.fetchall()
columns=[col[0] for col in cursor.description]
orderdetails=pd.DataFrame(data, columns=columns)

cursor.execute('SELECT * from products')
p=cursor.fetchall()
Colp=[col[0] for col in cursor.description]
products=pd.DataFrame(p,columns=Colp)

cursor.execute('SELECT * from payments')
pay=cursor.fetchall()
colPay=[col[0] for col in cursor.description]
payments=pd.DataFrame(pay,columns=colPay)

cursor.execute('SELECT * from customers')
cus=cursor.fetchall()
colPay=[col[0] for col in cursor.description]
customers=pd.DataFrame(cus,columns=colPay)

tot= int(payments['amount'].sum())
tot='$ '+formato_abbreviato(tot)

max=int(payments['amount'].max())
max='$ '+formato_abbreviato(max)

mean=int(payments['amount'].mean())
mean='$ '+formato_abbreviato(mean)

col1,col2,col3=prodotti.columns(3)
col1.metric('Importo totale:',tot)
col2.metric('Importo massimo:',max)
col3.metric('Importo medio:', mean)

with prodotti.expander('Panoramica prodotti',expanded=True):
    prodotti.header('I nostri prodotti')
    s1,s2=prodotti.columns(2)
    scelta=s1.radio('Ordina per: ', ['code','name','quantity','price'],)
    ord=s2.selectbox('Ordinamento',['Crescente','Decrescente'])
    if ord=='Crescente':
        bo=True
    else:
        bo=False
    if prodotti.button('Mostra',type='primary'):
        if scelta=='code':
           prodotti.dataframe(products.sort_values(by='productCode',ascending=bo))
        elif scelta=='name':
            prodotti.dataframe(products.sort_values(by='productName',ascending=bo))
        elif scelta=='quantity':
            prodotti.dataframe(products.sort_values(by='quantityInStock',ascending=bo))
        elif scelta=='price':
            prodotti.dataframe(products.sort_values(by='buyPrice',ascending=bo))  


with prodotti.expander('Pagamenti',expanded=True):
    prodotti.header('Pagamenti:')
    payments['paymentDate']=pd.to_datetime(payments['paymentDate'])
    paymonth=payments[['amount','paymentDate']]
    paymonth['amount']=pd.to_numeric(paymonth['amount'])
    date=prodotti.date_input('Seleziona il range di date', value=(paymonth['paymentDate'].min(),paymonth['paymentDate'].max()))
    if isinstance(date, tuple) and len(date) == 2:
        start = pd.Timestamp(date[0]) 
        end = pd.Timestamp(date[1])   
        if start <= end:
            paymonth = paymonth[(paymonth['paymentDate'] >= start) & (paymonth['paymentDate'] <= end)]
            if not paymonth.empty:
                prodotti.line_chart(paymonth.set_index('paymentDate')['amount'])
            else:
                prodotti.warning("Nessun dato disponibile per il range selezionato.")
        else:
            prodotti.error("La data di inizio deve essere antecedente o uguale alla data di fine.")
    else:
        prodotti.warning("Seleziona un intervallo di date valido.")
        

pr, vp = staff.columns(2)


pres = employees[employees['jobTitle'] == 'President'][['lastName', 'firstName']].iloc[0]
presName = f"{pres['firstName']} {pres['lastName']}"


vp_emp = employees[employees['jobTitle'] == 'VP Sales'][['lastName', 'firstName']].iloc[0]
vpName = f"{vp_emp['firstName']} {vp_emp['lastName']}"


pr.metric(':blue[PRESIDENT]', presName)
vp.metric(':green[VP SALES]', vpName)

employees_group=employees.groupby(by='jobTitle')
staff.bar_chart(employees_group['firstName'].count(), x_label='Job Title',y_label='Num Dipendenti')


country, limit= clienti.columns(2)

country.subheader('Distribuzione clienti nel mondo')
custWorld = customers.groupby(by='country').count()
custWorld = custWorld['customerNumber'].sort_values(ascending=False)
custWorld = custWorld.rename('Numero clienti') 
country.dataframe(custWorld,use_container_width=True)

limit.subheader('Clienti con maggior *credit limit* negli USA')
credit=customers[customers['country']=='USA'].sort_values(by='creditLimit',ascending=False)
creditNew=credit[['customerName','state','creditLimit']]
limit.dataframe(creditNew,use_container_width=True)