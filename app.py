from ast import IsNot
from flask import Flask, render_template, request, flash, redirect, url_for, session, jsonify
from flask_mysqldb import MySQL, MySQLdb
from flaskext.mysql import MySQL as MySQLext
import bcrypt
import sqlite3
import json
from sqlite3 import Error
import datetime 
import http.client
from difflib import SequenceMatcher as SM
import datetime
import time
from apscheduler.schedulers.background import BackgroundScheduler
import atexit

#Crea objeto Flask
app = Flask(__name__)


P1 = int() 
P2 = int() 
D1 = int() 
D2 = int()
D3 = int() 
D4 = int()
D5 = int()
M1 = int() 
M2 = int()
M3 = int() 
M4 = int()
M5 = int()
A1 = int() 
A2 = int()
A3 = int()
precio_equipo = float()
frecuencia = {}
listaequipo = list()
dicequipo = {}
torneo = str()
ronda = str()

# Las funciones que responden a los procesos solicitados por las paginas------------------------
def abr_name(name):
    nom=name
    nombre = name.split() 
    new = ""
    if nom=='Sergio Henrique Francisco':
        new='Serginho'
        return new
    if nom=='Patricio Julián Rodríguez':
        new='Pato R.'
        return new
    if len(nombre) == 2:
        pal1 = nombre[0]
        pal2 = nombre[1]
        new += (pal1[0]+'.')
        new += pal2
        return new
    elif len(nombre) == 3:
        pal1 = nombre[0]
        pal2 = nombre[1]
        new += (pal1[0]+'.')
        new += pal2
        return new
    elif len(nombre) == 4:
        pal1 = nombre[0]
        pal3 = nombre[2]
        new += (pal1[0]+'.')
        new += pal3
        return new
    elif len(nombre) == 5:
        pal1 = nombre[0]
        pal3 = nombre[2]
        pal4 = nombre[3]
        new += (pal1[0]+'.')
        new += pal3
        new += (pal1[3]+'.')
        return new
    return name

def abr_posi(p):
    pos=p
    if pos=='1':npos='POR'
    elif pos=='2':npos='DEF'
    elif pos=='3':npos='MED'
    elif pos=='4':npos='ATA'
    elif pos==1:npos='POR'
    elif pos==2:npos='DEF'
    elif pos==3:npos='MED'
    elif pos==4:npos='ATA'
    elif pos==None:
        print('¡¡¡Nuevo jugador sin posicion, de momento pos 3!!!')
        npos='MED'
    return npos

def abr_pos(pos):
    if pos == 'Goalkeeper':
        newpos = 'Por'
    elif pos == 'Defender':
        newpos = 'Def'
    elif pos == 'Midfielder':
        newpos = 'Med'
    elif pos == 'Attacker':
        newpos = 'Ata'
    return(newpos)

def carga_equipo(param):
    global P1,P2,D1,D2,D3,D4,D5,M1,M2,M3,M4,M5,A1,A2,A3,frecuencia,precio_equipo,dicequipo,torneo,ronda
        
    #GW = request.form['GW']
    
    app.config['MYSQL_DB'] = torneo
    sQuery = "SELECT team,name,fav,ligas FROM registrados WHERE login_id = %s"
    fQuery = "SELECT %s,name,fav,ligas FROM registrados WHERE login_id = %s"
    cur = mysql.connection.cursor()
    
    ses=session['id']
    if param == None:
        sron=str('team_fecha_'+ronda)
        ron=str('fecha_'+ronda)
        rond=ronda
    else:
        rond=str(int(ronda)+param)
        sron=str('team_fecha_'+rond)
        ron=str('fecha_'+rond)
    cur.execute(fQuery %(sron,ses))
    plantilla=cur.fetchone()
    if plantilla[0] == None:
        cur.execute(sQuery %(ses))
        plantilla=cur.fetchone()
    dicequipo=json.loads(plantilla[0])
    mysql.connection.commit()
    name=plantilla[1]

    P1=dicequipo['P1'];P2=dicequipo['P2']
    D1=dicequipo['D1'];D2=dicequipo['D2'];D3=dicequipo['D3'];D4=dicequipo['D4'];D5=dicequipo['D5']
    M1=dicequipo['M1'];M2=dicequipo['M2'];M3=dicequipo['M3'];M4=dicequipo['M4'];M5=dicequipo['M5']
    A1=dicequipo['A1'];A2=dicequipo['A2'];A3=dicequipo['A3']
    ron_id=str('fecha_'+rond+'.team')
    ron_pl=str('fecha_'+rond+'.player_id')
    dQuery="""SELECT teams.logo,%s.name,player_id,team,pos,pts,imbat,gol,pen,asis,ta,tr 
                FROM %s JOIN teams ON %s=teams.teams_id WHERE %s=%s"""
    eQuery="""SELECT teams.logo,dname,players_id,team,pos
                FROM players JOIN teams ON players.team=teams.teams_id WHERE players_id=%s"""
    jQuery="SELECT precio FROM players WHERE players_id=%s"    
    
    cur.execute(dQuery %(ron, ron, ron_id, ron_pl, dicequipo['P1']))
    jugadorP1 = cur.fetchone()
    if jugadorP1!=None:
        jugadoP1 = list(jugadorP1)
        jugadoP1[4]= abr_posi(jugadoP1[4])
        cur.execute(jQuery %dicequipo['P1'])
        price=cur.fetchone()[0]
        jugadoP1.append(price)
    else:
        cur.execute(eQuery %dicequipo['P1'])
        jugadorP1=cur.fetchone()
        jugadoP1=list(jugadorP1)
        jugadoP1[4]= abr_posi(jugadoP1[4])
        jugadoP1.extend([0,0,0,0,0,0,0])
        cur.execute(jQuery %dicequipo['P1'])
        price=cur.fetchone()[0]
        jugadoP1.append(price)

    cur.execute(dQuery %(ron, ron, ron_id, ron_pl, dicequipo['P2']))
    jugadorP2 = cur.fetchone()
    if jugadorP2!=None:
        jugadoP2 = list(jugadorP2)
        jugadoP2[4]= abr_posi(jugadoP2[4])
        cur.execute(jQuery %dicequipo['P2'])
        price=cur.fetchone()[0]
        jugadoP2.append(price)
    else:
        cur.execute(eQuery %dicequipo['P2'])
        jugadorP2=cur.fetchone()
        jugadoP2=list(jugadorP2)
        jugadoP2[4]= abr_posi(jugadoP2[4])
        jugadoP2.extend([0,0,0,0,0,0,0])
        cur.execute(jQuery %dicequipo['P2'])
        price=cur.fetchone()[0]
        jugadoP2.append(price)
    
    cur.execute(dQuery %(ron, ron, ron_id, ron_pl, dicequipo['D1']))
    jugadorD1 = cur.fetchone()
    if jugadorD1!=None:
        jugadoD1 = list(jugadorD1)
        jugadoD1[4]= abr_posi(jugadoD1[4])
        cur.execute(jQuery %dicequipo['D1'])
        price=cur.fetchone()[0]
        jugadoD1.append(price)
    else:
        cur.execute(eQuery %dicequipo['D1'])
        jugadorD1=cur.fetchone()
        jugadoD1=list(jugadorD1)
        jugadoD1[4]= abr_posi(jugadoD1[4])
        jugadoD1.extend([0,0,0,0,0,0,0])
        cur.execute(jQuery %dicequipo['D1'])
        price=cur.fetchone()[0]
        jugadoD1.append(price)
    cur.execute(dQuery %(ron, ron, ron_id, ron_pl, dicequipo['D2']))
    jugadorD2 = cur.fetchone()
    if jugadorD2!=None:
        jugadoD2 = list(jugadorD2)
        jugadoD2[4]= abr_posi(jugadoD2[4])
        cur.execute(jQuery %dicequipo['D2'])
        price=cur.fetchone()[0]
        jugadoD2.append(price)
    else:
        cur.execute(eQuery %dicequipo['D2'])
        jugadorD2=cur.fetchone()
        jugadoD2=list(jugadorD2)
        jugadoD2[4]= abr_posi(jugadoD2[4])
        jugadoD2.extend([0,0,0,0,0,0,0])
        cur.execute(jQuery %dicequipo['D2'])
        price=cur.fetchone()[0]
        jugadoD2.append(price)
    cur.execute(dQuery %(ron, ron, ron_id, ron_pl, dicequipo['D3']))
    jugadorD3 = cur.fetchone()
    if jugadorD3!=None:
        jugadoD3 = list(jugadorD3)
        jugadoD3[4]= abr_posi(jugadoD3[4])
        cur.execute(jQuery %dicequipo['D3'])
        price=cur.fetchone()[0]
        jugadoD3.append(price)
    else:
        cur.execute(eQuery %dicequipo['D3'])
        jugadorD3=cur.fetchone()
        jugadoD3=list(jugadorD3)
        jugadoD3[4]= abr_posi(jugadoD3[4])
        jugadoD3.extend([0,0,0,0,0,0,0])
        cur.execute(jQuery %dicequipo['D3'])
        price=cur.fetchone()[0]
        jugadoD3.append(price)
    cur.execute(dQuery %(ron, ron, ron_id, ron_pl, dicequipo['D4']))
    jugadorD4 = cur.fetchone()
    if jugadorD4!=None:
        jugadoD4 = list(jugadorD4)
        jugadoD4[4]= abr_posi(jugadoD4[4])
        cur.execute(jQuery %dicequipo['D4'])
        price=cur.fetchone()[0]
        jugadoD4.append(price)
    else:
        cur.execute(eQuery %dicequipo['D4'])
        jugadorD4=cur.fetchone()
        jugadoD4=list(jugadorD4)
        jugadoD4[4]= abr_posi(jugadoD4[4])
        jugadoD4.extend([0,0,0,0,0,0,0])
        cur.execute(jQuery %dicequipo['D4'])
        price=cur.fetchone()[0]
        jugadoD4.append(price)
    cur.execute(dQuery %(ron, ron, ron_id, ron_pl, dicequipo['D5']))
    jugadorD5 = cur.fetchone()
    if jugadorD5!=None:
        jugadoD5 = list(jugadorD5)
        jugadoD5[4]= abr_posi(jugadoD5[4])
        cur.execute(jQuery %dicequipo['D5'])
        price=cur.fetchone()[0]
        jugadoD5.append(price)
    else:
        cur.execute(eQuery %dicequipo['D5'])
        jugadorD5=cur.fetchone()
        jugadoD5=list(jugadorD5)
        jugadoD5[4]= abr_posi(jugadoD5[4])
        jugadoD5.extend([0,0,0,0,0,0,0])
        cur.execute(jQuery %dicequipo['D5'])
        price=cur.fetchone()[0]
        jugadoD5.append(price)
    cur.execute(dQuery %(ron, ron, ron_id, ron_pl, dicequipo['M1']))
    jugadorM1 = cur.fetchone()
    if jugadorM1!=None:
        jugadoM1 = list(jugadorM1)
        jugadoM1[4]= abr_posi(jugadoM1[4])
        cur.execute(jQuery %dicequipo['M1'])
        price=cur.fetchone()[0]
        jugadoM1.append(price)
    else:
        cur.execute(eQuery %dicequipo['M1'])
        jugadorM1=cur.fetchone()
        jugadoM1=list(jugadorM1)
        jugadoM1[4]= abr_posi(jugadoM1[4])
        jugadoM1.extend([0,0,0,0,0,0,0])
        cur.execute(jQuery %dicequipo['M1'])
        price=cur.fetchone()[0]
        jugadoM1.append(price)
    cur.execute(dQuery %(ron, ron, ron_id, ron_pl, dicequipo['M2']))
    jugadorM2 = cur.fetchone()
    if jugadorM2!=None:
        jugadoM2 = list(jugadorM2)
        jugadoM2[4]= abr_posi(jugadoM2[4])
        cur.execute(jQuery %dicequipo['M2'])
        price=cur.fetchone()[0]
        jugadoM2.append(price)
    else:
        cur.execute(eQuery %dicequipo['M2'])
        jugadorM2=cur.fetchone()
        jugadoM2=list(jugadorM2)
        jugadoM2[4]= abr_posi(jugadoM2[4])
        jugadoM2.extend([0,0,0,0,0,0,0])
        cur.execute(jQuery %dicequipo['M2'])
        price=cur.fetchone()[0]
        jugadoM2.append(price)
    cur.execute(dQuery %(ron, ron, ron_id, ron_pl, dicequipo['M3']))
    jugadorM3 = cur.fetchone()
    if jugadorM3!=None:
        jugadoM3 = list(jugadorM3)
        jugadoM3[4]= abr_posi(jugadoM3[4])
        cur.execute(jQuery %dicequipo['M3'])
        price=cur.fetchone()[0]
        jugadoM3.append(price)
    else:
        cur.execute(eQuery %dicequipo['M3'])
        jugadorM3=cur.fetchone()
        jugadoM3=list(jugadorM3)
        jugadoM3[4]= abr_posi(jugadoM3[4])
        jugadoM3.extend([0,0,0,0,0,0,0])
        cur.execute(jQuery %dicequipo['M3'])
        price=cur.fetchone()[0]
        jugadoM3.append(price)
    cur.execute(dQuery %(ron, ron, ron_id, ron_pl, dicequipo['M4']))
    jugadorM4 = cur.fetchone()
    if jugadorM4!=None:
        jugadoM4 = list(jugadorM4)
        jugadoM4[4]= abr_posi(jugadoM4[4])
        cur.execute(jQuery %dicequipo['M4'])
        price=cur.fetchone()[0]
        jugadoM4.append(price)
    else:
        cur.execute(eQuery %dicequipo['M4'])
        jugadorM4=cur.fetchone()
        jugadoM4=list(jugadorM4)
        jugadoM4[4]= abr_posi(jugadoM4[4])
        jugadoM4.extend([0,0,0,0,0,0,0])
        cur.execute(jQuery %dicequipo['M4'])
        price=cur.fetchone()[0]
        jugadoM4.append(price)
    cur.execute(dQuery %(ron, ron, ron_id, ron_pl, dicequipo['M5']))
    jugadorM5 = cur.fetchone()
    if jugadorM5!=None:
        jugadoM5 = list(jugadorM5)
        jugadoM5[4]= abr_posi(jugadoM5[4])
        cur.execute(jQuery %dicequipo['M5'])
        price=cur.fetchone()[0]
        jugadoM5.append(price)
    else:
        cur.execute(eQuery %dicequipo['M5'])
        jugadorM5=cur.fetchone()
        jugadoM5=list(jugadorM5)
        jugadoM5[4]= abr_posi(jugadoM5[4])
        jugadoM5.extend([0,0,0,0,0,0,0])
        cur.execute(jQuery %dicequipo['M5'])
        price=cur.fetchone()[0]
        jugadoM5.append(price)
    cur.execute(dQuery %(ron, ron, ron_id, ron_pl, dicequipo['A1']))
    jugadorA1 = cur.fetchone()
    if jugadorA1!=None:
        jugadoA1 = list(jugadorA1)
        jugadoA1[4]= abr_posi(jugadoA1[4])
        cur.execute(jQuery %dicequipo['A1'])
        price=cur.fetchone()[0]
        jugadoA1.append(price)
    else:
        cur.execute(eQuery %dicequipo['A1'])
        jugadorA1=cur.fetchone()
        jugadoA1=list(jugadorA1)
        jugadoA1[4]= abr_posi(jugadoA1[4])
        jugadoA1.extend([0,0,0,0,0,0,0])
        cur.execute(jQuery %dicequipo['A1'])
        price=cur.fetchone()[0]
        jugadoA1.append(price)
    cur.execute(dQuery %(ron, ron, ron_id, ron_pl, dicequipo['A2']))
    jugadorA2 = cur.fetchone()
    if jugadorA2!=None:
        jugadoA2 = list(jugadorA2)
        jugadoA2[4]= abr_posi(jugadoA2[4])
        cur.execute(jQuery %dicequipo['A2'])
        price=cur.fetchone()[0]
        jugadoA2.append(price)
    else:
        cur.execute(eQuery %dicequipo['A2'])
        jugadorA2=cur.fetchone()
        jugadoA2=list(jugadorA2)
        jugadoA2[4]= abr_posi(jugadoA2[4])
        jugadoA2.extend([0,0,0,0,0,0,0])
        cur.execute(jQuery %dicequipo['A2'])
        price=cur.fetchone()[0]
        jugadoA2.append(price)
    cur.execute(dQuery %(ron, ron, ron_id, ron_pl, dicequipo['A3']))
    jugadorA3 = cur.fetchone()
    if jugadorA3!=None:
        jugadoA3 = list(jugadorA3)
        jugadoA3[4]= abr_posi(jugadoA3[4])
        cur.execute(jQuery %dicequipo['A3'])
        price=cur.fetchone()[0]
        jugadoA3.append(price)
    else:
        cur.execute(eQuery %dicequipo['A3'])
        jugadorA3=cur.fetchone()
        jugadoA3=list(jugadorA3)
        jugadoA3[4]= abr_posi(jugadoA3[4])
        jugadoA3.extend([0,0,0,0,0,0,0])
        cur.execute(jQuery %dicequipo['A3'])
        price=cur.fetchone()[0]
        jugadoA3.append(price)

    return (jugadoP1,jugadoP2,jugadoD1,jugadoD2,jugadoD3,jugadoD4, 
        jugadoD5,jugadoM1,jugadoM2,jugadoM3,jugadoM4,jugadoM5,jugadoA1,jugadoA2,jugadoA3,name, dicequipo)

def carga_equipos(param,login_id):
    global P1,P2,D1,D2,D3,D4,D5,M1,M2,M3,M4,M5,A1,A2,A3,frecuencia,precio_equipo,torneo,ronda
        
    #GW = request.form['GW']
    
    app.config['MYSQL_DB'] = torneo
    sQuery = "SELECT team,name,fav,ligas FROM registrados WHERE login_id = %s"
    fQuery = "SELECT %s,name,fav,ligas FROM registrados WHERE login_id = %s"
    cur = mysql.connection.cursor()
    
    ses=login_id
    if param == None:
        sron=str('team_fecha_'+ronda)
        ron=str('fecha_'+ronda)
        rond=ronda
    else:
        rond=str(int(ronda)+param)
        sron=str('team_fecha_'+rond)
        ron=str('fecha_'+rond)
    cur.execute(fQuery %(sron,ses))
    plantilla=cur.fetchone()
    if plantilla[0] == None:
        cur.execute(sQuery %(ses))
        plantilla=cur.fetchone()
    dicequipo=json.loads(plantilla[0])
    mysql.connection.commit()
    name=plantilla[1]

    P1=dicequipo['P1'];P2=dicequipo['P2']
    D1=dicequipo['D1'];D2=dicequipo['D2'];D3=dicequipo['D3'];D4=dicequipo['D4'];D5=dicequipo['D5']
    M1=dicequipo['M1'];M2=dicequipo['M2'];M3=dicequipo['M3'];M4=dicequipo['M4'];M5=dicequipo['M5']
    A1=dicequipo['A1'];A2=dicequipo['A2'];A3=dicequipo['A3']
    ron_id=str('fecha_'+rond+'.team')
    ron_pl=str('fecha_'+rond+'.player_id')
    dQuery="""SELECT teams.logo,%s.name,player_id,team,pos,pts,imbat,gol,pen,asis,ta,tr 
                FROM %s JOIN teams ON %s=teams.teams_id WHERE %s=%s"""
    eQuery="""SELECT teams.logo,dname,players_id,team,pos
                FROM players JOIN teams ON players.team=teams.teams_id WHERE players_id=%s"""
    jQuery="SELECT precio FROM players WHERE players_id=%s"    
    
    cur.execute(dQuery %(ron, ron, ron_id, ron_pl, dicequipo['P1']))
    jugadorP1 = cur.fetchone()
    if jugadorP1!=None:
        jugadoP1 = list(jugadorP1)
        jugadoP1[4]= abr_posi(jugadoP1[4])
        cur.execute(jQuery %dicequipo['P1'])
        price=cur.fetchone()[0]
        jugadoP1.append(price)
    else:
        cur.execute(eQuery %dicequipo['P1'])
        jugadorP1=cur.fetchone()
        jugadoP1=list(jugadorP1)
        jugadoP1[4]= abr_posi(jugadoP1[4])
        jugadoP1.extend([0,0,0,0,0,0,0])
        cur.execute(jQuery %dicequipo['P1'])
        price=cur.fetchone()[0]
        jugadoP1.append(price)

    cur.execute(dQuery %(ron, ron, ron_id, ron_pl, dicequipo['P2']))
    jugadorP2 = cur.fetchone()
    if jugadorP2!=None:
        jugadoP2 = list(jugadorP2)
        jugadoP2[4]= abr_posi(jugadoP2[4])
        cur.execute(jQuery %dicequipo['P2'])
        price=cur.fetchone()[0]
        jugadoP2.append(price)
    else:
        cur.execute(eQuery %dicequipo['P2'])
        jugadorP2=cur.fetchone()
        jugadoP2=list(jugadorP2)
        jugadoP2[4]= abr_posi(jugadoP2[4])
        jugadoP2.extend([0,0,0,0,0,0,0])
        cur.execute(jQuery %dicequipo['P2'])
        price=cur.fetchone()[0]
        jugadoP2.append(price)
    
    cur.execute(dQuery %(ron, ron, ron_id, ron_pl, dicequipo['D1']))
    jugadorD1 = cur.fetchone()
    if jugadorD1!=None:
        jugadoD1 = list(jugadorD1)
        jugadoD1[4]= abr_posi(jugadoD1[4])
        cur.execute(jQuery %dicequipo['D1'])
        price=cur.fetchone()[0]
        jugadoD1.append(price)
    else:
        cur.execute(eQuery %dicequipo['D1'])
        jugadorD1=cur.fetchone()
        jugadoD1=list(jugadorD1)
        jugadoD1[4]= abr_posi(jugadoD1[4])
        jugadoD1.extend([0,0,0,0,0,0,0])
        cur.execute(jQuery %dicequipo['D1'])
        price=cur.fetchone()[0]
        jugadoD1.append(price)
    cur.execute(dQuery %(ron, ron, ron_id, ron_pl, dicequipo['D2']))
    jugadorD2 = cur.fetchone()
    if jugadorD2!=None:
        jugadoD2 = list(jugadorD2)
        jugadoD2[4]= abr_posi(jugadoD2[4])
        cur.execute(jQuery %dicequipo['D2'])
        price=cur.fetchone()[0]
        jugadoD2.append(price)
    else:
        cur.execute(eQuery %dicequipo['D2'])
        jugadorD2=cur.fetchone()
        jugadoD2=list(jugadorD2)
        jugadoD2[4]= abr_posi(jugadoD2[4])
        jugadoD2.extend([0,0,0,0,0,0,0])
        cur.execute(jQuery %dicequipo['D2'])
        price=cur.fetchone()[0]
        jugadoD2.append(price)
    cur.execute(dQuery %(ron, ron, ron_id, ron_pl, dicequipo['D3']))
    jugadorD3 = cur.fetchone()
    if jugadorD3!=None:
        jugadoD3 = list(jugadorD3)
        jugadoD3[4]= abr_posi(jugadoD3[4])
        cur.execute(jQuery %dicequipo['D3'])
        price=cur.fetchone()[0]
        jugadoD3.append(price)
    else:
        cur.execute(eQuery %dicequipo['D3'])
        jugadorD3=cur.fetchone()
        jugadoD3=list(jugadorD3)
        jugadoD3[4]= abr_posi(jugadoD3[4])
        jugadoD3.extend([0,0,0,0,0,0,0])
        cur.execute(jQuery %dicequipo['D3'])
        price=cur.fetchone()[0]
        jugadoD3.append(price)
    cur.execute(dQuery %(ron, ron, ron_id, ron_pl, dicequipo['D4']))
    jugadorD4 = cur.fetchone()
    if jugadorD4!=None:
        jugadoD4 = list(jugadorD4)
        jugadoD4[4]= abr_posi(jugadoD4[4])
        cur.execute(jQuery %dicequipo['D4'])
        price=cur.fetchone()[0]
        jugadoD4.append(price)
    else:
        cur.execute(eQuery %dicequipo['D4'])
        jugadorD4=cur.fetchone()
        jugadoD4=list(jugadorD4)
        jugadoD4[4]= abr_posi(jugadoD4[4])
        jugadoD4.extend([0,0,0,0,0,0,0])
        cur.execute(jQuery %dicequipo['D4'])
        price=cur.fetchone()[0]
        jugadoD4.append(price)
    cur.execute(dQuery %(ron, ron, ron_id, ron_pl, dicequipo['D5']))
    jugadorD5 = cur.fetchone()
    if jugadorD5!=None:
        jugadoD5 = list(jugadorD5)
        jugadoD5[4]= abr_posi(jugadoD5[4])
        cur.execute(jQuery %dicequipo['D5'])
        price=cur.fetchone()[0]
        jugadoD5.append(price)
    else:
        cur.execute(eQuery %dicequipo['D5'])
        jugadorD5=cur.fetchone()
        jugadoD5=list(jugadorD5)
        jugadoD5[4]= abr_posi(jugadoD5[4])
        jugadoD5.extend([0,0,0,0,0,0,0])
        cur.execute(jQuery %dicequipo['D5'])
        price=cur.fetchone()[0]
        jugadoD5.append(price)
    cur.execute(dQuery %(ron, ron, ron_id, ron_pl, dicequipo['M1']))
    jugadorM1 = cur.fetchone()
    if jugadorM1!=None:
        jugadoM1 = list(jugadorM1)
        jugadoM1[4]= abr_posi(jugadoM1[4])
        cur.execute(jQuery %dicequipo['M1'])
        price=cur.fetchone()[0]
        jugadoM1.append(price)
    else:
        cur.execute(eQuery %dicequipo['M1'])
        jugadorM1=cur.fetchone()
        jugadoM1=list(jugadorM1)
        jugadoM1[4]= abr_posi(jugadoM1[4])
        jugadoM1.extend([0,0,0,0,0,0,0])
        cur.execute(jQuery %dicequipo['M1'])
        price=cur.fetchone()[0]
        jugadoM1.append(price)
    cur.execute(dQuery %(ron, ron, ron_id, ron_pl, dicequipo['M2']))
    jugadorM2 = cur.fetchone()
    if jugadorM2!=None:
        jugadoM2 = list(jugadorM2)
        jugadoM2[4]= abr_posi(jugadoM2[4])
        cur.execute(jQuery %dicequipo['M2'])
        price=cur.fetchone()[0]
        jugadoM2.append(price)
    else:
        cur.execute(eQuery %dicequipo['M2'])
        jugadorM2=cur.fetchone()
        jugadoM2=list(jugadorM2)
        jugadoM2[4]= abr_posi(jugadoM2[4])
        jugadoM2.extend([0,0,0,0,0,0,0])
        cur.execute(jQuery %dicequipo['M2'])
        price=cur.fetchone()[0]
        jugadoM2.append(price)
    cur.execute(dQuery %(ron, ron, ron_id, ron_pl, dicequipo['M3']))
    jugadorM3 = cur.fetchone()
    if jugadorM3!=None:
        jugadoM3 = list(jugadorM3)
        jugadoM3[4]= abr_posi(jugadoM3[4])
        cur.execute(jQuery %dicequipo['M3'])
        price=cur.fetchone()[0]
        jugadoM3.append(price)
    else:
        cur.execute(eQuery %dicequipo['M3'])
        jugadorM3=cur.fetchone()
        jugadoM3=list(jugadorM3)
        jugadoM3[4]= abr_posi(jugadoM3[4])
        jugadoM3.extend([0,0,0,0,0,0,0])
        cur.execute(jQuery %dicequipo['M3'])
        price=cur.fetchone()[0]
        jugadoM3.append(price)
    cur.execute(dQuery %(ron, ron, ron_id, ron_pl, dicequipo['M4']))
    jugadorM4 = cur.fetchone()
    if jugadorM4!=None:
        jugadoM4 = list(jugadorM4)
        jugadoM4[4]= abr_posi(jugadoM4[4])
        cur.execute(jQuery %dicequipo['M4'])
        price=cur.fetchone()[0]
        jugadoM4.append(price)
    else:
        cur.execute(eQuery %dicequipo['M4'])
        jugadorM4=cur.fetchone()
        jugadoM4=list(jugadorM4)
        jugadoM4[4]= abr_posi(jugadoM4[4])
        jugadoM4.extend([0,0,0,0,0,0,0])
        cur.execute(jQuery %dicequipo['M4'])
        price=cur.fetchone()[0]
        jugadoM4.append(price)
    cur.execute(dQuery %(ron, ron, ron_id, ron_pl, dicequipo['M5']))
    jugadorM5 = cur.fetchone()
    if jugadorM5!=None:
        jugadoM5 = list(jugadorM5)
        jugadoM5[4]= abr_posi(jugadoM5[4])
        cur.execute(jQuery %dicequipo['M5'])
        price=cur.fetchone()[0]
        jugadoM5.append(price)
    else:
        cur.execute(eQuery %dicequipo['M5'])
        jugadorM5=cur.fetchone()
        jugadoM5=list(jugadorM5)
        jugadoM5[4]= abr_posi(jugadoM5[4])
        jugadoM5.extend([0,0,0,0,0,0,0])
        cur.execute(jQuery %dicequipo['M5'])
        price=cur.fetchone()[0]
        jugadoM5.append(price)
    cur.execute(dQuery %(ron, ron, ron_id, ron_pl, dicequipo['A1']))
    jugadorA1 = cur.fetchone()
    if jugadorA1!=None:
        jugadoA1 = list(jugadorA1)
        jugadoA1[4]= abr_posi(jugadoA1[4])
        cur.execute(jQuery %dicequipo['A1'])
        price=cur.fetchone()[0]
        jugadoA1.append(price)
    else:
        cur.execute(eQuery %dicequipo['A1'])
        jugadorA1=cur.fetchone()
        jugadoA1=list(jugadorA1)
        jugadoA1[4]= abr_posi(jugadoA1[4])
        jugadoA1.extend([0,0,0,0,0,0,0])
        cur.execute(jQuery %dicequipo['A1'])
        price=cur.fetchone()[0]
        jugadoA1.append(price)
    cur.execute(dQuery %(ron, ron, ron_id, ron_pl, dicequipo['A2']))
    jugadorA2 = cur.fetchone()
    if jugadorA2!=None:
        jugadoA2 = list(jugadorA2)
        jugadoA2[4]= abr_posi(jugadoA2[4])
        cur.execute(jQuery %dicequipo['A2'])
        price=cur.fetchone()[0]
        jugadoA2.append(price)
    else:
        cur.execute(eQuery %dicequipo['A2'])
        jugadorA2=cur.fetchone()
        jugadoA2=list(jugadorA2)
        jugadoA2[4]= abr_posi(jugadoA2[4])
        jugadoA2.extend([0,0,0,0,0,0,0])
        cur.execute(jQuery %dicequipo['A2'])
        price=cur.fetchone()[0]
        jugadoA2.append(price)
    cur.execute(dQuery %(ron, ron, ron_id, ron_pl, dicequipo['A3']))
    jugadorA3 = cur.fetchone()
    if jugadorA3!=None:
        jugadoA3 = list(jugadorA3)
        jugadoA3[4]= abr_posi(jugadoA3[4])
        cur.execute(jQuery %dicequipo['A3'])
        price=cur.fetchone()[0]
        jugadoA3.append(price)
    else:
        cur.execute(eQuery %dicequipo['A3'])
        jugadorA3=cur.fetchone()
        jugadoA3=list(jugadorA3)
        jugadoA3[4]= abr_posi(jugadoA3[4])
        jugadoA3.extend([0,0,0,0,0,0,0])
        cur.execute(jQuery %dicequipo['A3'])
        price=cur.fetchone()[0]
        jugadoA3.append(price)

    return (jugadoP1,jugadoP2,jugadoD1,jugadoD2,jugadoD3,jugadoD4, 
        jugadoD5,jugadoM1,jugadoM2,jugadoM3,jugadoM4,jugadoM5,jugadoA1,jugadoA2,jugadoA3,name, dicequipo)

       
def time_in_range(start, end, current):
    return start <= current <= end

def fechas(now):
    count=0
    app.config['MYSQL_DB'] = 'bolivia2022'
    ahora=now
    antes='2022-01-24T17:01:00'
    fQuery="""SELECT start FROM rounds"""
    #con_db = sqlite3.connect('fantasydb.sqlite')
    #cur = con_db.cursor()
    cur = mysql.connection.cursor()
    cur.execute(fQuery)
    rondas=cur.fetchall()
    mysql.connection.commit()
    #Todo esto deberia llegar de la base de datos llenada por la API pero el futbol nacional es tan chistoso
    #GW1='2022-02-06T15:00:00'
    #GW2='2022-02-11T15:00:00'
    #GW3='2022-02-18T15:00:00'
    #GW4='2022-02-25T15:00:00'
    #GW5='2022-03-04T15:00:00'
    #GW6='2022-03-11T15:00:00'
    #GW7='2022-04-01T15:00:00'
    #rondas=GW1,GW2,GW3,GW4,GW5,GW6,GW7
    
    for ronda in rondas:
        ronda=ronda[0].isoformat()
        print(ronda)
        count=count+1
        if(time_in_range(antes,ronda,ahora))==True:
            print(ronda,'Pertenece a fecha-',count)
            count=str(count)
            return count


def fecha_live():
    app.config['MYSQL_DB'] = 'bolivia2022'
    fQuery="""SELECT start,end FROM rounds"""
    cur = mysql.connection.cursor()
    cur.execute(fQuery)
    rondas=cur.fetchall()
    mysql.connection.commit()
    return rondas
    

    
# Las peticiones API para llenar la base de datos----------------------------------------------
def API_currents(league_id):
    global torneo
    #pedir el season actual del torneo que se desee
    liga=league_id
    current=dict()
    conn = http.client.HTTPSConnection("soccer.sportmonks.com")
    key_tz="?api_token=Sp4hVNvCAOGiMjpKDMWkhVcMmzV7nykqY0Tk3o92NKclrxQrfpFjWu6oFieM"

    headers = {
        'tz': "America/La_Paz",
        'include': "country,season,seasons",
        'x-rapidapi-host': "football-pro.p.rapidapi.com",
        'x-rapidapi-key': "0329e6e9e8msh13e33172622a180p1ddd31jsnd12defe9b2c5"
        }

    conn.request("GET", "/api/v2.0/leagues/"+liga+key_tz)

    res= conn.getresponse()
    data= res.read()
    json_data= json.loads(data)
    data=json_data['data']

    current['logo']=data['logo_path']
    current['season']=data['current_season_id']
    current['round']=data['current_round_id']
    current['stage']=data['current_stage_id']

    app.config['MYSQL_DB'] = torneo
    cur = mysql.connection.cursor()
    jQuery='''CREATE TABLE IF NOT EXISTS registrados (
        login_id INT UNIQUE PRIMARY KEY,
        team VARCHAR(500) NOT NULL,
        name VARCHAR(255) NOT NULL,
        fav VARCHAR(255) NOT NULL,
        ligas VARCHAR(255) NOT NULL,
        detalle VARCHAR(255) NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )  ENGINE=INNODB;''' 
    uQuery='''CREATE TABLE IF NOT EXISTS ultimo (
        login_id INT UNIQUE PRIMARY KEY,
        team VARCHAR(500) NOT NULL,
        name VARCHAR(255) NOT NULL,
        fav VARCHAR(255) NOT NULL,
        ligas VARCHAR(255) NOT NULL,
        detalle VARCHAR(255) NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )  ENGINE=INNODB;'''
    cur.execute(jQuery)
    cur.execute(uQuery)
    mysql.connection.commit()

    sesion=str(current['season'])
    
    return current

def API_season(sesion): 
    global torneo
    conn = http.client.HTTPSConnection("soccer.sportmonks.com")
    season=str(sesion)
    key_tz="&tz=America/La_Paz&api_token=Sp4hVNvCAOGiMjpKDMWkhVcMmzV7nykqY0Tk3o92NKclrxQrfpFjWu6oFieM"
    headers = {
        'x-rapidapi-host': "football-pro.p.rapidapi.com",
        'x-rapidapi-key': "0329e6e9e8msh13e33172622a180p1ddd31jsnd12defe9b2c5"
        }
    
    conn.request("GET", "/api/v2.0/seasons/"+season+"?include=league%2Cstages%2Crounds"+key_tz)

    res = conn.getresponse()
    data = res.read()
    json_data= json.loads(data)
    data=json_data['data']

    app.config['MYSQL_DB'] = torneo
    cur = mysql.connection.cursor()
        
    jQuery='''CREATE TABLE IF NOT EXISTS Stages (
        stages_id INT PRIMARY KEY,
        name VARCHAR(255) NOT NULL,
        type VARCHAR(255) NOT NULL,
        league_id INT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )  ENGINE=INNODB;''' 
    cur.execute(jQuery)
    stages=data['stages']
    cQuery='''INSERT INTO Stages
        (stages_id, name, type, league_id) 
        VALUES 
        (%s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE
        name = %s, type = %s, league_id = %s;'''
    for stage in stages['data']:
        cur.execute(cQuery, (stage['id'],stage['name'],stage['type'],stage['league_id'],
        stage['name'],stage['type'],stage['league_id'] ))
    
    jQuery='''CREATE TABLE IF NOT EXISTS Rounds (
        rounds_id INT PRIMARY KEY,
        name VARCHAR(255) NOT NULL,
        stage_id INT NOT NULL,
        start   DATE,
        end     DATE,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )  ENGINE=INNODB;''' 
    cur.execute(jQuery)
    rounds=data['rounds']
    cQuery='''INSERT INTO Rounds
        (rounds_id, name, stage_id, start, end) 
        VALUES 
        (%s, %s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE
        name = %s, stage_id = %s, start = %s, end = %s ;'''
    for round in rounds['data']:
        cur.execute(cQuery, (round['id'],round['name'],round['stage_id'],round['start'],round['end'],
        round['name'],round['stage_id'],round['start'],round['end'] ))
        
    
    mysql.connection.commit()

def API_teams(sesion):
    global torneo
    conn = http.client.HTTPSConnection("soccer.sportmonks.com")
    team_list=list()
    season=str(sesion)
    key_tz="?tz=America/La_Paz&api_token=Sp4hVNvCAOGiMjpKDMWkhVcMmzV7nykqY0Tk3o92NKclrxQrfpFjWu6oFieM"

    headers = {
        'x-rapidapi-host': "football-pro.p.rapidapi.com",
        'x-rapidapi-key': "0329e6e9e8msh13e33172622a180p1ddd31jsnd12defe9b2c5"
        }

    conn.request("GET", "/api/v2.0/teams/season/"+season+key_tz)

    res = conn.getresponse()
    
    data= res.read()
    json_data= json.loads(data)
    data=json_data['data']

    app.config['MYSQL_DB'] = torneo
    cur = mysql.connection.cursor()
        
    jQuery='''CREATE TABLE IF NOT EXISTS Teams (
        teams_id INT PRIMARY KEY,
        name VARCHAR(255) NOT NULL,
        logo VARCHAR(255) NOT NULL,
        stadium INT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )  ENGINE=INNODB;''' 
    cur.execute(jQuery)
    
    cQuery='''INSERT INTO Teams
        (teams_id, name, logo, stadium) 
        VALUES 
        (%s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE
        name = %s, stadium = %s;'''
    for team in data:
        cur.execute(cQuery, (team['id'],team['name'],team['logo_path'],team['venue_id'],
        team['name'],team['venue_id'] ))
        team_list.append(team['id'])
    
    mysql.connection.commit()
    return(team_list)
 

def API_fixtures(sesion): 
    global torneo
    conn = http.client.HTTPSConnection("soccer.sportmonks.com")
    season=str(sesion)
    key_tz="&tz=America/La_Paz&api_token=Sp4hVNvCAOGiMjpKDMWkhVcMmzV7nykqY0Tk3o92NKclrxQrfpFjWu6oFieM"

    conn.request("GET", "/api/v2.0/seasons/"+season+"?include=fixtures"+key_tz)
    res = conn.getresponse()
    
    data= res.read()
    json_data= json.loads(data)
    jdata=json_data['data']
    fixtures=jdata['fixtures']
    data=fixtures['data']

    app.config['MYSQL_DB'] = torneo
    cur = mysql.connection.cursor()
    
        
    jQuery='''CREATE TABLE IF NOT EXISTS fixtures (
        fixtures_id INT PRIMARY KEY,
        season VARCHAR(255) NOT NULL,
        stage VARCHAR(255) NOT NULL,
        round VARCHAR(255) NOT NULL,
        local VARCHAR(255) NOT NULL,
        l_score VARCHAR(255) NOT NULL,
        visit VARCHAR(255) NOT NULL,
        v_score VARCHAR(255) NOT NULL,
        estado VARCHAR(255) NOT NULL,
        arbitro VARCHAR(255),
        fecha DATE,
        hora TIME,
        l_dt VARCHAR(255),
        l_lineup VARCHAR(500),
        v_dt VARCHAR(255),
        v_lineup VARCHAR(500),
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )  ENGINE=INNODB;''' 
    cur.execute(jQuery)
    cQuery='''INSERT INTO fixtures
        (fixtures_id,season,stage,round,local,l_score,visit,v_score,estado,arbitro,fecha,hora,l_dt,v_dt) 
        VALUES 
        (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
        ON DUPLICATE KEY UPDATE
        season=%s,stage=%s,round=%s,local=%s,l_score=%s,visit=%s,v_score=%s,estado=%s,
        arbitro=%s,fecha=%s,hora=%s,l_dt=%s,v_dt=%s;'''
        
    for fix in data:
        score=fix['scores']
        time=fix['time']
        stime=time['starting_at']
        coaches=fix['coaches']
        cur.execute(cQuery, (fix['id'],fix['season_id'],fix['stage_id'],fix['round_id'],
        fix['localteam_id'],score['localteam_score'],fix['visitorteam_id'],score['visitorteam_score'],
        time['status'],fix['referee_id'],stime['date'],stime['time'],coaches['localteam_coach_id'],coaches['visitorteam_coach_id'],
        fix['season_id'],fix['stage_id'],fix['round_id'],
        fix['localteam_id'],score['localteam_score'],fix['visitorteam_id'],score['visitorteam_score'],
        time['status'],fix['referee_id'],stime['date'],stime['time'],coaches['localteam_coach_id'],coaches['visitorteam_coach_id']))
    mysql.connection.commit()

def API_squads(sesion,equipos):
    global torneo
    conn = http.client.HTTPSConnection("soccer.sportmonks.com")
    season=str(sesion)

    app.config['MYSQL_DB'] = torneo
    cur = mysql.connection.cursor()
    
        
    jQuery='''CREATE TABLE IF NOT EXISTS players (
        players_id BIGINT PRIMARY KEY,
        pos VARCHAR(255),
        injured VARCHAR(255) NOT NULL,
        team VARCHAR(255) NOT NULL,
        fullname VARCHAR(255) NOT NULL,
        dname VARCHAR(255) NOT NULL,
        nacion VARCHAR(255),
        birthdate VARCHAR(255),
        birthplace VARCHAR(255),
        height VARCHAR(255),
        weight VARCHAR(255),
        estado VARCHAR(255),
        min INT(10),
        pj INT(10),
        tit INT(10),
        gol INT(10),
        asi INT(10),
        ta INT(10),
        tr INT(10),
        imb INT(10),
        pts INT(10),
        precio INT(10),
        img VARCHAR(255),
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )  ENGINE=INNODB;''' 
    cur.execute(jQuery)
    cQuery='''INSERT INTO players
        (players_id,pos,injured,team,fullname,dname,nacion,birthdate,birthplace,height,weight,
        min,pj,tit,gol,asi,ta,tr,imb,img) 
        VALUES 
        (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
        ON DUPLICATE KEY UPDATE
        injured=%s,team=%s,fullname=%s,dname=%s,nacion=%s,birthdate=%s,
        birthplace=%s,height=%s,weight=%s,min=%s,pj=%s,tit=%s,gol=%s,asi=%s,ta=%s,tr=%s,imb=%s,img=%s;'''



    key_tz="&tz=America/La_Paz&api_token=Sp4hVNvCAOGiMjpKDMWkhVcMmzV7nykqY0Tk3o92NKclrxQrfpFjWu6oFieM"
    for team in equipos:
        conn.request("GET", "/api/v2.0/squad/season/"+season+"/team/"+str(team)+"?include=player"+key_tz)
        res = conn.getresponse()
        data= res.read()
        json_data= json.loads(data)
        players=json_data['data']
        for player in players:
            p_player=player['player']
            d_player=p_player['data']
            cur.execute(cQuery, (player['player_id'],player['position_id'],player['injured'],team,
            d_player['fullname'],d_player['display_name'],d_player['nationality'],d_player['birthdate'],d_player['birthplace'],
            d_player['height'],d_player['weight'],player['minutes'],player['appearences'],player['lineups'],
            player['goals'],player['assists'],player['yellowcards'],player['redcards'],player['cleansheets'],d_player['image_path'],
            player['injured'],team,
            d_player['fullname'],d_player['display_name'],d_player['nationality'],d_player['birthdate'],d_player['birthplace'],
            d_player['height'],d_player['weight'],player['minutes'],player['appearences'],player['lineups'],
            player['goals'],player['assists'],player['yellowcards'],player['redcards'],player['cleansheets'],d_player['image_path']  ))
    mysql.connection.commit()

def API_events():
    global torneo
    conn = http.client.HTTPSConnection("soccer.sportmonks.com")
    app.config['MYSQL_DB'] = torneo
    cur = mysql.connection.cursor()
    mQuery="SELECT fixtures_id FROM fixtures WHERE estado='FT'"
    cur.execute(mQuery)
    fix_list=cur.fetchall()
    
    jQuery='''CREATE TABLE IF NOT EXISTS events (
            events_id BIGINT PRIMARY KEY,
            team_id VARCHAR(255),
            type VARCHAR(255),
            fixt_id VARCHAR(255),
            round_id VARCHAR(255),
            play_a VARCHAR(255),
            a_name VARCHAR(255),
            play_b VARCHAR(255),
            b_name VARCHAR(255),
            min VARCHAR(255),
            inj VARCHAR(255),
            result VARCHAR(255),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )  ENGINE=INNODB;''' 

    cur.execute(jQuery)
    
    
    key_tz="&tz=America/La_Paz&api_token=Sp4hVNvCAOGiMjpKDMWkhVcMmzV7nykqY0Tk3o92NKclrxQrfpFjWu6oFieM"
    for fix in fix_list:
        fixt=str(fix[0])
        conn.request("GET", "/api/v2.0/fixtures/"+fixt+"?include=events,lineup,round"+key_tz)
        res = conn.getresponse()
        data= res.read()
        json_data= json.loads(data)
        players=json_data['data']
        l_lineup=list()
        v_lineup=list()
        ron=players['round']
        round=ron['data']
        p_player=players['events']
        eventos=p_player['data']
        line=players['lineup']
        lineu=line['data']
        for lineup in lineu:
            if lineup['team_id']==players['localteam_id']: l_lineup.append(lineup['player_id'])
            elif lineup['team_id']==players['visitorteam_id']: v_lineup.append(lineup['player_id'])
        l_lineup=json.dumps(l_lineup)
        v_lineup=json.dumps(v_lineup)
        lQuery='UPDATE fixtures SET l_lineup= %s,v_lineup= %s WHERE fixtures_id= %s'
        cur.execute(lQuery, (l_lineup,v_lineup,int(fixt)))
        for event in eventos:
            cQuery='''INSERT INTO events
                (events_id,team_id,type,fixt_id,play_a,a_name,play_b,b_name,min,inj,result,round_id) 
                VALUES 
                (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
                ON DUPLICATE KEY UPDATE
                team_id=%s,type=%s,fixt_id=%s,play_a=%s,a_name=%s,play_b=%s,b_name=%s,min=%s,inj=%s,result=%s,round_id=%s;'''
            
            cur.execute(cQuery, (event['id'],event['team_id'],event['type'],event['fixture_id'],
            event['player_id'],event['player_name'],event['related_player_id'],
            event['related_player_name'],event['minute'],event['injuried'],event['result'],round['id'],
            event['team_id'],event['type'],event['fixture_id'],
            event['player_id'],event['player_name'],event['related_player_id'],
            event['related_player_name'],event['minute'],event['injuried'],event['result'],round['id'] ))
    mysql.connection.commit()
     
def API_rounds():
    global torneo
    conn = http.client.HTTPSConnection("soccer.sportmonks.com")
    app.config['MYSQL_DB'] = torneo
    cur = mysql.connection.cursor()
    mQuery="SELECT name FROM rounds"
    cur.execute(mQuery)
    rondas=cur.fetchall()
    yQuery="""ALTER TABLE registrados ADD COLUMN IF NOT EXISTS team_%s VARCHAR(500);"""
    aQuery='''CREATE TABLE IF NOT EXISTS %s (
        player_id INT PRIMARY KEY,
        name VARCHAR(255),
        pos INT(10),
        team INT(10),
        round_id INT(10),
        fix_id INT(10),
        min INT(10),
        gol INT(10),
        asis INT(10),
        ta INT(10),
        tr INT(10), 
        imbat INT(10),
        conced INT(10),
        autog INT(10),
        pen INT(10),
        pen_mis INT(10),
        pen_sav INT(10),
        pts INT(10),
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )  ENGINE=INNODB;'''
    
    for ronda in rondas:
        GW= str('fecha_'+ronda[0])
        cur.execute(aQuery %GW)
        cur.execute(yQuery %GW)
    mysql.connection.commit()

def API_last_season():
    global torneo
    app.config['MYSQL_DB'] = torneo
    torn=str('last_'+torneo)
    cur = mysql.connection.cursor()
    cQuery='''CREATE TABLE IF NOT EXISTS pts_bol2021 (
        id INT AUTO_INCREMENT PRIMARY KEY,
        monks_id BIGINT,
        fapi_id INT(10),
        fullname VARCHAR(255),
        apiname VARCHAR(255),
        position INT(10),
        nameteam VARCHAR(255),
        min INT(10),
        imbat INT(10),
        gol INT(10),
        pen INT(10),
        asis INT(10),
        ta INT(10),
        tr INT(10),
        pts INT(10),
        precio INT(10),
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )  ENGINE=INNODB;'''

    cur.execute(cQuery)
    mQuery="SELECT players_id, fullname, pos FROM players"
    cur.execute(mQuery)
    player_list=cur.fetchall()
    con_db = sqlite3.connect('fantasydb.sqlite')
    curs = con_db.cursor()
    curs.execute("SELECT * FROM PlayersTot2021")
    djugador = curs.fetchall()
    con_db.commit()
    sQuery='''INSERT INTO pts_bol2021
                (monks_id,fapi_id,fullname,apiname,position,nameteam,min,imbat,gol,pen,
                asis,ta,tr,pts,precio) 
                VALUES 
                (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);'''
    for player in player_list:
        
        for jug21 in djugador:
            if SM(None, player[1], jug21[1]).ratio() > 0.7:
                cur.execute(sQuery,(player[0],jug21[0],player[1],jug21[1],player[2],jug21[3],jug21[4],
                jug21[5],jug21[6],jug21[7],jug21[8],jug21[9],jug21[10],jug21[11],jug21[12]) )
    mysql.connection.commit()

def img_change():
    global torneo
    app.config['MYSQL_DB'] = torneo
    cur = mysql.connection.cursor()
    mQuery="SELECT players_id,img FROM players"
    cur.execute(mQuery)
    jugadores22=cur.fetchall()
    eQuery="SELECT fapi_id from pts_bol2021 WHERE monks_id=%s"
    iQuery="UPDATE players SET img='https://media.api-sports.io/football/players/%s.png' WHERE players_id= %s"
    for jug22 in jugadores22:
        if jug22[1]=="https://cdn.sportmonks.com/images/soccer/placeholder.png":
            cur.execute(eQuery %jug22[0])
            jugadores21=cur.fetchall()
            for jug21 in jugadores21:
                if jug21[0]!="":
                    cur.execute(iQuery,(jug21[0],jug22[0]))
    mysql.connection.commit()

def precio():
    global torneo
    Nacional=list()
    Nacional.append('11347071')
    Nacional.append('10024')
    app.config['MYSQL_DB'] = torneo
    cur = mysql.connection.cursor()
    mQuery="SELECT players_id,pos,min,pj,tit,gol,asi,ta,tr,imb FROM players"
    cur.execute(mQuery)
    jugadores=cur.fetchall()
    aQuery="UPDATE players SET precio=%s WHERE players_id=%s"
    for j in jugadores:
        precio=0
        if j[1]==None: precio=3.5
        else:
            if int(j[1]) == 1:
                try:
                    
                    if j[5] >= 1:
                        precio+=0.7
                    
                    if j[6] >= 1:
                        precio+=0.4 
                    
                    if j[3]/j[9]<=2:
                        precio+=1.5
                    precio = precio + 4
                except:
                    precio = precio + 4
            elif int(j[1]) == 2:
                try:
                    
                    if j[2]/j[5] <= 180:
                        precio+=1
                    elif j[2]/j[5] <= 360:
                        precio+=0.5
                    if j[2]/j[6] <= 180:
                        precio+=1 
                    elif j[2]/j[6] <= 360:
                        precio+=0.5
                    if j[3]/j[9]<=2:
                        precio+=1.2
                    precio = precio + 4.5
                except:
                    precio = precio + 4.5
            elif int(j[1]) == 3:
                try:
                    
                    if j[2]/j[5] <= 180:
                        precio+=1.8
                    elif j[2]/j[5] <= 360:
                        precio+=0.9
                    if j[2]/j[6] <= 135:
                        precio+= 1.8
                    elif j[2]/j[6] <= 270:
                        precio+= 0.9
                    precio = precio + 5
                except:
                    precio = precio + 5
            elif int(j[1]) == 4:
                try:
                    
                    if j[2]/j[5] <= 135:
                        precio+=1.5
                    elif j[2]/j[5] <= 270:
                        precio+=0.5
                    if j[2]/j[6] <= 270:
                        precio+= 0.3
                    precio = precio + 6
                except:
                    precio = precio + 6 

            if jugadores[0] in Nacional:
                precio = precio + 0.5 
            try:
                if j[3]/j[4] <= 2:
                    precio += 0.3
            except:
                precio=precio-0.1
        cur.execute(aQuery, (precio,j[0]))
    mysql.connection.commit()

def tpuntos():
    app.config['MYSQL_DB'] = torneo
    cur = mysql.connection.cursor()
    mQuery="SELECT players_id,pos,min,pj,tit,gol,asi,ta,tr,imb FROM players"
    aQuery="UPDATE players SET pts=%s WHERE players_id=%s"
    cur.execute(mQuery)
    jugadores=cur.fetchall()
    for jugador in jugadores:
        
        pts_tiempo = 1
        pts_pi = 0
        pts_ingreso = 1
        pts_gol = 0
        pts_asis = 0
        pts_TA = 1
        pts_TR = 3
        puntos=0
        posicion_jugador=jugador[1]
        if posicion_jugador == '4':
            pts_pi = 1
            pts_gol = 4
            pts_asis = 3
        elif posicion_jugador == '3':
            pts_pi = 2
            pts_gol = 5
            pts_asis = 4
        elif posicion_jugador == '2':
            pts_pi = 4
            pts_gol = 6
            pts_asis = 5
        elif posicion_jugador == '1':
            pts_pi = 6
            pts_gol = 10
            pts_asis = 6
        #por ser titular o ingresar
        try:
            puntos+=(jugador[3]*pts_ingreso)
        except:
            puntos+=0
        #por permanencia
        try:
            if jugador[2]/jugador[3]>=60:
                puntos+=(jugador[3]*pts_tiempo)
        except:
            puntos+=0
        #por gol
        try:
            puntos+=(jugador[5]*pts_gol)
        except:
            puntos+=0
        #por asist
        try:
            puntos+=(jugador[6]*pts_asis)
        except:
            puntos+=0
        #por TA
        try:
            puntos-=(jugador[7]*pts_TA)
        except:
            puntos+=0
        #por TR
        try:
            puntos-=(jugador[8]*pts_TR)
        except:
            puntos+=0
        #por porteria imbatida
        try:
            puntos+=(jugador[9]*pts_pi)
        except:
            puntos+=0
        cur.execute(aQuery,(puntos,jugador[0]))
    mysql.connection.commit()

def calc_pts(partido):
    jugador=list()
    jugador=partido
    app.config['MYSQL_DB'] = torneo
    cur = mysql.connection.cursor()
    fQuery="SELECT l_score, local, v_score, visit FROM fixtures WHERE fixtures_id=%s"
    pQuery="SELECT pos,team FROM players WHERE players_id=%s"
    cur.execute(fQuery %jugador[0])
    score=cur.fetchone()
    cur.execute(pQuery %jugador[1])
    jug=cur.fetchone()
    if jug==None:
        conn = http.client.HTTPSConnection("soccer.sportmonks.com")
        key_tz="&tz=America/La_Paz&api_token=Sp4hVNvCAOGiMjpKDMWkhVcMmzV7nykqY0Tk3o92NKclrxQrfpFjWu6oFieM"
        conn.request("GET", "/api/v2.0/players/"+str(jugador[1])+"?include=stats"+key_tz)
        res = conn.getresponse()
        data= res.read()
        json_data= json.loads(data)
        d_player=json_data['data']
        cQuery='''INSERT INTO players
        (players_id,pos,team,fullname,dname,nacion,birthdate,birthplace,height,weight,img) 
        VALUES 
        (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
        ON DUPLICATE KEY UPDATE
        team=%s,fullname=%s,dname=%s,nacion=%s,birthdate=%s,
        birthplace=%s,height=%s,weight=%s,img=%s;'''
        cur.execute(cQuery,(jugador[1],d_player['position_id'],d_player['team_id'],
            d_player['fullname'],d_player['display_name'],d_player['nationality'],d_player['birthdate'],d_player['birthplace'],
            d_player['height'],d_player['weight'],d_player['image_path'],d_player['team_id'],
            d_player['fullname'],d_player['display_name'],d_player['nationality'],d_player['birthdate'],d_player['birthplace'],
            d_player['height'],d_player['weight'],d_player['image_path']))
        mysql.connection.commit()
        jug=list()
        posicion_jugador=d_player['position_id']
        team=d_player['team_id']
        
    else:
        posicion_jugador=jug[0]
        team=jug[1]
    pts_tiempo = 1
    pts_pi = 0
    pts_ingreso = 1
    pts_gol = 0
    pts_asis = 0
    pts_TA = 1
    pts_TR = 3
    goleada=2
    autogol=1
    pen_missed=2
    pen_saved=4
    imbat=0
    puntos=0
    if posicion_jugador == '4':
        pts_pi = 1
        pts_gol = 4
        pts_asis = 3
    elif posicion_jugador == '3':
        pts_pi = 2
        pts_gol = 5
        pts_asis = 4
    elif posicion_jugador == '2':
        pts_pi = 4
        pts_gol = 6
        pts_asis = 5
    elif posicion_jugador == '1':
        pts_pi = 6
        pts_gol = 10
        pts_asis = 6
    #por ser titular o ingresar y permanencia
    try:
        if jugador[2]>=60:
            puntos+=(pts_tiempo + pts_ingreso)
        elif jugador[2]<60:
            puntos+=pts_ingreso
        else: puntos+=0
    except:
        puntos+=0
    #por gol
    try:
        puntos+=(jugador[3]*pts_gol)
    except:
        puntos+=0
    #por asist
    try:
        puntos+=(jugador[4]*pts_asis)
    except:
        puntos+=0
    #por TA
    try:
        puntos-=(jugador[7]*pts_TA)
    except:
        puntos+=0
    #por TR
    try:
        puntos-=(jugador[8]*pts_TR)
    except:
        puntos+=0
    #por porteria imbatida
    try:
        if team == score[1]:
            if score[2]=='0':
                imbat=1 
                puntos+= pts_pi 
        if team == score[3]:
            if score[0]=='0':
                imbat=1
                puntos+= pts_pi 
    except:
        puntos+=0
    
    if jugador[5]>2:puntos-=goleada
    if jugador[6]>0:puntos-=autogol
    try:puntos-=(jugador[10]*pen_missed)
    except:puntos-=0
    try:puntos+=(jugador[11]*pen_saved)
    except:puntos+=0
    return puntos,imbat,posicion_jugador

def calc_pts_job(partido):
    jugador=list()
    jugador=partido
    connect=mysqlext.connect()
    cur = connect.cursor()
    fQuery="SELECT l_score, local, v_score, visit FROM fixtures WHERE fixtures_id=%s"
    pQuery="SELECT pos,team FROM players WHERE players_id=%s"
    cur.execute(fQuery %jugador[0])
    score=cur.fetchone()
    cur.execute(pQuery %jugador[1])
    jug=cur.fetchone()
    if jug==None:
        conn = http.client.HTTPSConnection("soccer.sportmonks.com")
        key_tz="&tz=America/La_Paz&api_token=Sp4hVNvCAOGiMjpKDMWkhVcMmzV7nykqY0Tk3o92NKclrxQrfpFjWu6oFieM"
        conn.request("GET", "/api/v2.0/players/"+str(jugador[1])+"?include=stats"+key_tz)
        res = conn.getresponse()
        data= res.read()
        json_data= json.loads(data)
        d_player=json_data['data']
        cQuery='''INSERT INTO players
        (players_id,pos,team,fullname,dname,nacion,birthdate,birthplace,height,weight,img) 
        VALUES 
        (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
        ON DUPLICATE KEY UPDATE
        team=%s,fullname=%s,dname=%s,nacion=%s,birthdate=%s,
        birthplace=%s,height=%s,weight=%s,img=%s;'''
        cur.execute(cQuery,(jugador[1],d_player['position_id'],d_player['team_id'],
            d_player['fullname'],d_player['display_name'],d_player['nationality'],d_player['birthdate'],d_player['birthplace'],
            d_player['height'],d_player['weight'],d_player['image_path'],d_player['team_id'],
            d_player['fullname'],d_player['display_name'],d_player['nationality'],d_player['birthdate'],d_player['birthplace'],
            d_player['height'],d_player['weight'],d_player['image_path']))
        connect.commit()
        jug=list()
        jug[0]=d_player['position_id']
        jug[1]=d_player['team_id']
        
    else:
        posicion_jugador=jug[0]
        team=jug[1]
    pts_tiempo = 1
    pts_pi = 0
    pts_ingreso = 1
    pts_gol = 0
    pts_asis = 0
    pts_TA = 1
    pts_TR = 3
    goleada=2
    autogol=1
    pen_missed=2
    pen_saved=4
    imbat=0
    puntos=0
    if posicion_jugador == '4':
        pts_pi = 1
        pts_gol = 4
        pts_asis = 3
    elif posicion_jugador == '3':
        pts_pi = 2
        pts_gol = 5
        pts_asis = 4
    elif posicion_jugador == '2':
        pts_pi = 4
        pts_gol = 6
        pts_asis = 5
    elif posicion_jugador == '1':
        pts_pi = 6
        pts_gol = 10
        pts_asis = 6
    #por ser titular o ingresar y permanencia
    try:
        if jugador[2]>=60:
            puntos+=(pts_tiempo + pts_ingreso)
        elif jugador[2]<60:
            puntos+=pts_ingreso
        else: puntos+=0
    except:
        puntos+=0
    #por gol
    try:
        puntos+=(jugador[3]*pts_gol)
    except:
        puntos+=0
    #por asist
    try:
        puntos+=(jugador[4]*pts_asis)
    except:
        puntos+=0
    #por TA
    try:
        puntos-=(jugador[7]*pts_TA)
    except:
        puntos+=0
    #por TR
    try:
        puntos-=(jugador[8]*pts_TR)
    except:
        puntos+=0
    #por porteria imbatida
    try:
        if team == score[1]:
            if score[2]=='0':
                imbat=1 
                puntos+= pts_pi 
        if team == score[3]:
            if score[0]=='0':
                imbat=1
                puntos+= pts_pi 
    except:
        puntos+=0
    
    if jugador[5]>2:puntos-=goleada
    if jugador[6]>0:puntos-=autogol
    try:puntos-=(jugador[10]*pen_missed)
    except:puntos-=0
    try:puntos+=(jugador[11]*pen_saved)
    except:puntos+=0
    return puntos,imbat,jug[0]
   
      
def rpuntos():
    global torneo
    conn = http.client.HTTPSConnection("soccer.sportmonks.com")
    key_tz="&tz=America/La_Paz&api_token=Sp4hVNvCAOGiMjpKDMWkhVcMmzV7nykqY0Tk3o92NKclrxQrfpFjWu6oFieM"
    app.config['MYSQL_DB'] = torneo
    cur = mysql.connection.cursor()
    eQuery="SELECT rounds_id,name FROM rounds"
    mQuery="SELECT fixtures_id FROM fixtures WHERE round=%s"
    rQuery="SELECT name FROM rounds WHERE rounds_id=%s"
    cur.execute(eQuery)
    rounds=cur.fetchall()
    for round in rounds:
        cur.execute(mQuery %round[0])
        fix_list=cur.fetchall()
        cur.execute(rQuery %round[0])
        n_round=cur.fetchone()
        for fixt in fix_list:
            fix=str(fixt[0])
            conn.request("GET", "/api/v2.0/fixtures/"+fix+"?include=lineup,bench"+key_tz)
            res = conn.getresponse()
            data= res.read()
            json_data= json.loads(data)
            players=json_data['data']
            line=players['lineup']
            lineu=line['data']
            
            for lineup in lineu:
                partido=list()
                jugador=lineup['player_id']
                team=lineup['team_id']
                name=lineup['player_name']
                stats=lineup['stats']
                goals=stats['goals']
                gol=goals['scored']
                asis=goals['assists']
                concedidos=goals['conceded']
                autogol=goals['owngoals']
                cards=stats['cards']
                ta=cards['yellowcards']
                tr=cards['redcards']
                other=stats['other']
                pen_scored=other['pen_scored']
                pen_missed=other['pen_missed']
                pen_saved=other['pen_saved']
                min=other['minutes_played']
                partido=(fixt[0],jugador,min,gol,asis,concedidos,autogol,ta,tr,pen_scored,pen_missed,pen_saved)
                puntos,imbat,pos=calc_pts(partido)
                bQuery='''INSERT INTO fecha_%s (player_id,name,pos,team,round_id,
                fix_id,min,gol,asis,ta,tr,imbat,conced,autog,pen,pen_mis,pen_sav,pts) 
                VALUES 
                (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
                ON DUPLICATE KEY UPDATE
                name=%s,pos=%s,team=%s,round_id=%s,fix_id=%s,min=%s,gol=%s,asis=%s,ta=%s,tr=%s,imbat=%s,
                conced=%s,autog=%s,pen=%s,pen_mis=%s,pen_sav=%s,pts=%s;'''
                cur.execute(bQuery, (int(round[1]),jugador,name,pos,team,int(round[0]),fix,min,gol,asis,
                ta,tr,imbat,concedidos,autogol,pen_scored,pen_missed,pen_saved,puntos,
                name,pos,team,int(round[0]),fix,min,gol,asis,
                ta,tr,imbat,concedidos,autogol,pen_scored,pen_missed,pen_saved,puntos))
    hQuery='''CREATE TABLE IF NOT EXISTS puntos (
        login_id INT UNIQUE PRIMARY KEY,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )  ENGINE=INNODB;''' 
    yQuery="""ALTER TABLE puntos ADD COLUMN IF NOT EXISTS pts_%s INT;"""
    mQuery="SELECT name FROM rounds"
    cur.execute(hQuery)
    cur.execute(mQuery)
    rondas=cur.fetchall()
    for ronda in rondas:
        GW= str('fecha_'+ronda[0])
        cur.execute(yQuery %GW)
    mysql.connection.commit()

def crea_ligas():
    app.config['MYSQL_DB'] = torneo
    cur = mysql.connection.cursor()
    jQuery='''CREATE TABLE IF NOT EXISTS Ligas (
        ligas_id INT PRIMARY KEY AUTO_INCREMENT,
        name VARCHAR(255) NOT NULL,
        teams VARCHAR(500),
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )  ENGINE=INNODB;''' 
    cur.execute(jQuery) 
    iQuery="INSERT INTO Ligas (ligas_id,name, teams) VALUES (NULL,%s,%s)"
    uQuery="INSERT iNTO Ligas (ligas_id,name, teams) VALUES (NULL,%s,%s)"
    
    sQuery="SELECT ligas_id FROM Ligas"
    pQuery="""CREATE TABLE registrado_liga (
            registrado_id INT NOT NULL,
            liga_id INT NOT NULL,
            PRIMARY KEY (registrado_id, liga_id),
            FOREIGN KEY (registrado_id) REFERENCES registrados (login_id),
            FOREIGN KEY (liga_id) REFERENCES ligas (ligas_id)
        );"""
    rQuery="INSERT INTO registrado_liga (registrado_id, liga_id) VALUES (%s,%s)"
    gral="General"
    priv="Privada_test"
    ses=session['id']
    cur.execute(iQuery ,(gral,ses))
    cur.execute(uQuery ,(priv,ses))
    cur.execute(sQuery)
    ligas=cur.fetchall()
    cur.execute(pQuery)
    for liga in ligas:
        cur.execute(rQuery ,(ses,liga))
    mysql.connection.commit()

def info_liga(registrado):
    app.config['MYSQL_DB'] = torneo
    cur = mysql.connection.cursor()
    jQuery="SELECT liga_id, ligas.name FROM registrado_liga JOIN ligas ON ligas_id=liga_id WHERE registrado_id=%s"
    cur.execute(jQuery %registrado)
    ligas=cur.fetchall()
    return(ligas)
def estado_liga(liga_id):
    app.config['MYSQL_DB'] = torneo
    cur = mysql.connection.cursor()
    
    jQuery="""SELECT registrados.login_id,registrados.name, puntos.pts_fecha_1 FROM 
    registrado_liga JOIN registrados JOIN puntos ON 
    registrado_id=registrados.login_id AND registrados.login_id=puntos.login_id 
    WHERE liga_id=%s ORDER BY `puntos`.`pts_fecha_1` DESC """
    cur.execute(jQuery %liga_id)
    resultado=cur.fetchall()
    
    return(resultado)
def crea_puntos_ronda():
    app.config['MYSQL_DB'] = torneo
    cur = mysql.connection.cursor()
    sQuery="SELECT login_id FROM registrados"
    cur.execute(sQuery)
    usuarios=cur.fetchall()
    tQuery="SELECT team FROM registrados WHERE login_id=%s"
    pQuery="SELECT pts FROM %s WHERE player_id=%s"
    lQuery="""INSERT INTO puntos (login_id, %s) VALUES (%s,%s) 
            ON DUpLICATE KEY UPDATE
            %s=%s;"""
    for i in range(1,int(ronda)):
        for usuario in usuarios:
            pts_totales=0
            equipo=dict()
            cur.execute(tQuery %usuario)
            equipo_json=cur.fetchone()
            equipo=json.loads(equipo_json[0])
            fecha='fecha_'+str(i)
            for k,v in equipo.items():
                if k!='suplentes':
                    cur.execute(pQuery %(fecha,v))
                    pts_jug_ronda=cur.fetchone()
                    if pts_jug_ronda == None: pts_jug_ronda='0'
                    
                    pts_totales+=int(pts_jug_ronda[0])
                else: print('suplentes wasitos')
            print('El equipo ', usuario[0],' hizo ',pts_totales,' puntos en la ronda',(i))
            jornada='pts_fecha_'+str(i)
            cur.execute(lQuery %(jornada,usuario[0],pts_totales,jornada,pts_totales))
        mysql.connection.commit()




#Establezco llave secreta
app.secret_key="applogin"

#Configura conex a MySQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'dbapp'
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = ''
app.config['MYSQL_DATABASE_DB'] = 'bolivia2022'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
#Crea el objeto MySQL
mysql = MySQL(app)
mysqlext=MySQLext()
mysqlext.init_app(app)

#Llave para encrypt (semilla)
semilla = bcrypt.gensalt()



def print_date_time():
    print(time.strftime("%A, %d. %B %Y %I:%M:%S %p"))


def livescores():
    global torneo
    
    connect=mysqlext.connect()
    curl=connect.cursor()
    
    conn = http.client.HTTPSConnection("soccer.sportmonks.com")
    key_tz="&tz=America/La_Paz&api_token=Sp4hVNvCAOGiMjpKDMWkhVcMmzV7nykqY0Tk3o92NKclrxQrfpFjWu6oFieM"
    app.config['MYSQL_DB'] = torneo
    conn.request("GET", "/api/v2.0/livescores?include=lineup,events"+key_tz)
    res = conn.getresponse()
    data= res.read()
    json_data= json.loads(data)
    data=json_data['data']
    if data=='':
        print('sin partidos hoy')
    else:
        for partido in data:
            fix=partido['id']
            
            line=partido['lineup']
            lineu=line['data']
            round=partido['round_id']
            rQuery="SELECT name FROM rounds WHERE rounds_id=%s"
            curl.execute(rQuery %round)
            round_name=curl.fetchone()[0]
            print ('fixture:',fix,' ronda: ',round_name, 'Alineaciones disponibles y eventos actualizandose')
            if lineu==[]:
                print('Las alineaciones estaran disponibles minutos antes del partido')
            else:
                for lineup in lineu:
                    partido=list()
                    jugador=lineup['player_id']
                    team=lineup['team_id']
                    name=lineup['player_name']
                    stats=lineup['stats']
                    goals=stats['goals']
                    gol=goals['scored']
                    asis=goals['assists']
                    concedidos=goals['conceded']
                    autogol=goals['owngoals']
                    cards=stats['cards']
                    ta=cards['yellowcards']
                    tr=cards['redcards']
                    other=stats['other']
                    pen_scored=other['pen_scored']
                    pen_missed=other['pen_missed']
                    pen_saved=other['pen_saved']
                    min=other['minutes_played']
                    partido=(fix,jugador,min,gol,asis,concedidos,autogol,ta,tr,pen_scored,pen_missed,pen_saved)
                    puntos,imbat,pos=calc_pts_job(partido)
                    bQuery='''INSERT INTO fecha_%s (player_id,name,pos,team,round_id,
                    fix_id,min,gol,asis,ta,tr,imbat,conced,autog,pen,pen_mis,pen_sav,pts) 
                    VALUES 
                    (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
                    ON DUPLICATE KEY UPDATE
                    name=%s,pos=%s,team=%s,round_id=%s,fix_id=%s,min=%s,gol=%s,asis=%s,ta=%s,tr=%s,imbat=%s,
                    conced=%s,autog=%s,pen=%s,pen_mis=%s,pen_sav=%s,pts=%s;'''
                    curl.execute(bQuery, (int(round_name),jugador,name,pos,team,round,fix,min,gol,asis,
                    ta,tr,imbat,concedidos,autogol,pen_scored,pen_missed,pen_saved,puntos,
                    name,pos,team,round,fix,min,gol,asis,
                    ta,tr,imbat,concedidos,autogol,pen_scored,pen_missed,pen_saved,puntos))
        connect.commit()


#scheduler = BackgroundScheduler()

#scheduler.add_job(func=print_date_time, trigger="interval", seconds=20, start_date='2022-03-31 19:59:00' , end_date='2022-03-31 20:00:00')
#scheduler.print_jobs()
#scheduler.start()



# Shut down the scheduler when exiting the app
#atexit.register(lambda: scheduler.shutdown())
#Define ruta principal
@app.route("/")
#Define la funcion Principal
def main():
    #Verifica que haya sesion
    if 'nombre' in session:
        return render_template('inicio.html')
    else:
        return render_template('ingresar.html')

#Define la ruta de index
@app.route("/inicio")
def inicio():
    global ronda, torneo
    if 'nombre' in session:
        #----------------------Nombre del torneo! importante para toda la temporada----------------
        torneo = 'bolivia2022'
        ahora=datetime.datetime.now().isoformat()
        ronda=fechas(ahora)
       
        return render_template('inicio.html', ronda=ronda)
        
    else:
        return render_template('ingresar.html')

@app.route("/ligas")
def ligas():
    
    global ronda, torneo
    if 'nombre' in session:
        #----------------------Nombre del torneo! importante para toda la temporada----------------
        torneo = 'bolivia2022'
        ahora=datetime.datetime.now().isoformat()
        ronda=fechas(ahora)
        ses=session['id']
        ligas=info_liga(ses)
        return render_template('ligas.html', ronda=ronda, ligas=ligas)
        
    else:
        return render_template('ingresar.html')

@app.route("/liga/<liga_id>/")
def liga_user(liga_id):
    
    global ronda, torneo
    if 'nombre' in session:
        #----------------------Nombre del torneo! importante para toda la temporada----------------
        torneo = 'bolivia2022'
        cur = mysql.connection.cursor()
        ahora=datetime.datetime.now().isoformat()
        ronda=fechas(ahora)
        ses=liga_id
        nQuery="SELECT ligas.name FROM ligas WHERE ligas_id=%s"
        cur.execute(nQuery %liga_id)
        nliga=cur.fetchone()
        ligas=estado_liga(ses)
        return render_template('liga.html', ronda=ronda, ligas=ligas,nombre=nliga[0])
        
    else:
        return render_template('ingresar.html')

#Widget SportMonks
@app.route("/live")
def live():
    
    if 'nombre' in session:
        
        return render_template('live.html', ronda=ronda)
        
    else:
        return render_template('ingresar.html')

#definimos la ruta para el registro---------------------------------------------------------
@app.route("/registrar", methods=["GET", "POST"])
def registrar():
    
    if (request.method=="GET"):
        #accesso no concedido 
        if 'nombre' in session:
            return render_template('inicio.html')
        else:
            return render_template("ingresar.html")
    else:
        nombre    = request.form['nmNombreRegistro']
        correo    = request.form['nmCorreoRegistro']
        username  = request.form['nmUsernameRegistro']
        password  = request.form['nmPasswordRegistro']
        password_encode = password.encode("utf-8")
        password_encriptado = bcrypt.hashpw(password_encode, semilla)
        
        app.config['MYSQL_DB'] = 'dbapp'
        #prepara el query
        sQuery = "INSERT into Login (correo, password, nombre, tipo) VALUES (%s, %s, %s, %s)"
        #crea cursor
        cur = mysql.connection.cursor()
        #Ejecuta
        cur.execute(sQuery, (correo,password_encriptado,nombre,'usuario'))
        mysql.connection.commit()

        #registra la sesion
        session['nombre'] = nombre
        lQuery = 'SELECT id FROM login WHERE correo = %s'
        cur.execute(lQuery,[correo])
        usuario = cur.fetchone()
        session['id'] = usuario[0] 
        
        return redirect(url_for('inicio'))

@app.route("/ingresar", methods=["GET","POST"])
def ingresar():
    app.config['MYSQL_DB'] = 'dbapp'
    if (request.method=="GET"):
        if 'nombre' in session:
            return render_template('inicio.html')
        else:
            return render_template('ingresar.html')
    else:
        correo    = request.form['nmCorreoLogin']
        password  = request.form['nmPasswordLogin']
        password_encode = password.encode("utf-8")
        cur = mysql.connection.cursor()
        sQuery = 'SELECT correo, password, nombre, id, tipo FROM login WHERE correo = %s'
        cur.execute(sQuery,[correo])
        usuario = cur.fetchone()
        
        mysql.connection.commit()

        #Verifica si obtuvo datos
        if (usuario !=None ):
            password_encriptado_encode = usuario[1].encode()
            print("password_encode:", password_encode)
            print("password_encriptado_encode:", password_encriptado_encode)
            if (bcrypt.checkpw(password_encode, password_encriptado_encode)):

                #registra la sesion
                session['nombre'] = usuario[2]
                session['correo'] = correo
                session['id'] = usuario[3]
                session['tipo']= usuario[4]
                return redirect(url_for('inicio'))
            else:
                #mensaje flash
                flash("El password no es correcto", "alert-info")

                #redirige a Ingresar
                return render_template('ingresar.html')
        else:
            flash("El correo no existe", "alert-info")
            return render_template('ingresar.html')

# Revisa si el usuario logueado tiene equipo creado o no------------------------------------
@app.route("/fantasy")
def fantasy():
    global torneo
    
    if 'nombre' in session:
        
        app.config['MYSQL_DB'] = torneo
        cur = mysql.connection.cursor()
        sQuery = 'SELECT * FROM registrados WHERE login_id = %s'
        
        cur.execute(sQuery %(session['id']) )
        user_team = cur.fetchone()
        mysql.connection.commit()
        if user_team == None:
            
            return redirect(url_for('creaequipo'))
        else:
            
            
            return redirect(url_for('equipo'))    
    else:
        return render_template('ingresar.html')

# Bloque cración de equipo------------------------------------------------------------------
@app.route("/creaquipo", methods=["GET", "POST"])
def creaequipo():
    if 'nombre' in session:
        #return render_template('creaequipo.html')
        global P1,P2,D1,D2,D3,D4,D5,M1,M2,M3,M4,M5,A1,A2,A3,frecuencia,precio_equipo
        P1=P2=D1=D2=D3=D4=D5=M1=M2=M3=M4=M5=A1=A2=A3=precio_equipo=0
        frecuencia={}
        print('Variables reiniciadas')
        app.config['MYSQL_DB'] = torneo
        cur = mysql.connection.cursor()
        pQuery="SELECT players_id,img,dname,pos,pts,precio,teams.name,teams.teams_id,teams.logo FROM players JOIN teams ON players.team=teams.teams_id"
        tQuery="SELECT * FROM teams"

        cur.execute(pQuery)
        jugadores=cur.fetchall()
        listjug=list()
        for jugad in jugadores:
            jugador = list(jugad)
            jugador[3]= abr_posi(jugador[3])
            
            listjug.append(jugador)
        cur.execute(tQuery)
        equipos=cur.fetchall()

        return render_template('creaequipo.html', jugadores=listjug, equipos=equipos)

        
        
    else:
        return render_template('ingresar.html')


@app.route("/ajaxfile",methods=["POST","GET"])
def ajaxfile():
    
    if request.method == 'POST':
        userid = request.form['userid']

        app.config['MYSQL_DB'] = torneo
        curs = mysql.connection.cursor()
        mQuery="""SELECT img,fullname,pos,teams.name,teams.teams_id,nacion,birthdate,height,weight,birthplace FROM 
                players JOIN teams ON players.team=teams.teams_id WHERE players_id=%s"""
        curs.execute(mQuery %userid)
        employeelist=curs.fetchall()

        
        dQuery="SELECT players_id,min,imb,gol,asi,ta,tr,pts,precio FROM players WHERE players_id=%s"
        curs.execute(dQuery %userid)
        totales=curs.fetchone()

        
        aQuery="SELECT monks_id,min,imbat,gol,asis,ta,tr,pts,precio FROM pts_bol2021 WHERE monks_id=%s"
        curs.execute(aQuery %userid)
        total=curs.fetchone()
        
        mysql.connection.commit()        
        
    return jsonify({'htmlresponse': render_template('response.html',employeelist=employeelist, totales =totales, total=total )})

@app.route("/ajaxadd",methods=["POST","GET"])
def ajaxadd():
    global P1,P2,D1,D2,D3,D4,D5,M1,M2,M3,M4,M5,A1,A2,A3,frecuencia,precio_equipo,dicequipo,torneo
    
    if request.method == 'POST':
        userid = request.form['userid']
        
        print(userid)

        if userid=='crear':
            fav= request.form['favorito']
            print(fav)
            if P1==0 or P2==0 or D1==0 or D2==0 or D3==0 or D4==0 or D5==0 or M1==0 or M2==0 or M3==0 or M4==0 or M5==0 or A1==0 or A2==0 or A3==0:
                return jsonify(msg ="Debes elejir a los 15 jugadores de la plantilla")
                
            else:
                if precio_equipo > 90:
                    msgp = 'Te pasaste! tu planilla es de '+str(precio_equipo)+'UFB, tu presupuesto total es de 80UFB.'
                    return jsonify(msg=msgp)
                    
                else:
                    app.config['MYSQL_DB'] = torneo
                    name = request.form['nameteam']
                    print(name)
                    sQuery = """INSERT into registrados (name,login_id,team,fav) 
                    VALUES (%s,%s,%s,%s)"""
                    fQuery = """INSERT into ultimo (name,login_id,team,fav) 
                    VALUES (%s,%s,%s,%s)"""
                    rQuery="INSERT INTO registrado_liga (registrado_id, liga_id) VALUES (%s,%s)"
                    ses=session['id']
                    #crea cursor
                    cur = mysql.connection.cursor()
                    dicequipo['suplentes']=P2,D5,M5,A3
                    equipo=json.dumps(dicequipo)
                    #Ejecuta
                    cur.execute(sQuery, (name,session['id'],equipo,fav))
                    cur.execute(fQuery, (name,session['id'],equipo,fav))
                    cur.execute(rQuery ,(ses,'2'))
                    cur.execute(rQuery ,(ses,'3'))

                    mysql.connection.commit()
                    creado=True
                    return jsonify(creado=creado)

        app.config['MYSQL_DB'] = torneo
        cur = mysql.connection.cursor()
        tQuery="""SELECT pos,teams.teams_id,teams.name,precio 
        FROM players JOIN teams ON players.team=teams.teams_id WHERE players_id=%s"""
        cur.execute(tQuery %userid)
        listajugador = cur.fetchone()
        teamid = listajugador[1]

        if teamid in frecuencia: 
            if frecuencia[teamid] == 3:
                print('ya tienes 3 jugadores de ', listajugador[2])
                mens = 'Ya tienes 3 jugadores de '+listajugador[2]+', reemplaza alguno'
                print(mens)
                return jsonify(msg=mens)
            else: frecuencia[teamid] += 1
        else: frecuencia[teamid] = 1



        if listajugador[0] == '1':
            
            if P1 == 0:
                P1 = userid
                POS="P1"
                dicequipo['P1']=userid
                
            else:
                if P2 == 0: 
                    P2 = userid
                    POS="P2"
                    dicequipo['P2']=userid
                else: 
                    return jsonify (msg = "Ya elegiste tus dos porteros, reemplaza alguno")
        elif listajugador[0] == '2':
            
            if D1 == 0:
                D1 = userid
                POS="D1"
                dicequipo['D1']=userid
            elif D2 == 0:
                D2 = userid
                POS="D2"  
                dicequipo['D2']=userid
            elif D3 == 0:
                D3 = userid
                POS="D3"
                dicequipo['D3']=userid
            elif D4 == 0: 
                D4 = userid
                POS="D4"
                dicequipo['D4']=userid
            elif D5 == 0:
                D5 = userid
                POS="D5"
                dicequipo['D5']=userid
            else: 
                return jsonify (msg = "Ya elegiste tus cinco defensores, reemplaza alguno")
        elif listajugador[0] == '3':
            
            if M1 == 0:
                M1 = userid
                POS="M1"
                dicequipo['M1']=userid
            elif M2 == 0:
                M2 = userid
                POS="M2"  
                dicequipo['M2']=userid
            elif M3 == 0:
                M3 = userid
                POS="M3"
                dicequipo['M3']=userid
            elif M4 == 0: 
                M4 = userid
                POS="M4"
                dicequipo['M4']=userid
            elif M5 == 0:
                M5 = userid
                POS="M5"
                dicequipo['M5']=userid
            else: 
                return jsonify (msg = "Ya elegiste tus cinco mediocampistas, reemplaza alguno")
        elif listajugador[0] == '4':
            
            if A1 == 0:
                A1 = userid
                POS="A1"
                dicequipo['A1']=userid
            elif A2 == 0:
                A2 = userid
                POS="A2"
                dicequipo['A2']=userid  
            elif A3 == 0:
                A3 = userid
                POS="A3"
                dicequipo['A3']=userid           
            else: 
                return jsonify (msg = "Ya elegiste tus tres delanteros, reemplaza alguno")
        
    else: return render_template("inicio.html")
    
    
    
    
    print(dicequipo)

    precio_equipo = precio_equipo + float(listajugador[3])
    return jsonify (POS=POS,price=precio_equipo)

@app.route("/ajaxrem",methods=["POST","GET"])
def ajaxrem():
    global P1,P2,D1,D2,D3,D4,D5,M1,M2,M3,M4,M5,A1,A2,A3,frecuencia,precio_equipo
    if request.method == 'POST':
        userpos = request.form['userpos']
        preciorem = request.form['price']
        teamrem = int(request.form['team'])
        frecuencia[teamrem] -= 1
        print(preciorem)
        precio_equipo = precio_equipo - float(preciorem)
        print(userpos, precio_equipo)
        if 'P1' == userpos: P1= 0
        elif 'P2' == userpos: P2= 0
        elif 'D1' == userpos: D1= 0
        elif 'D2' == userpos: D2= 0
        elif 'D3' == userpos: D3= 0
        elif 'D4' == userpos: D4= 0
        elif 'D5' == userpos: D5= 0
        elif 'M1' == userpos: M1= 0
        elif 'M2' == userpos: M2= 0
        elif 'M3' == userpos: M3= 0
        elif 'M4' == userpos: M4= 0
        elif 'M5' == userpos: M5= 0
        elif 'A1' == userpos: A1= 0
        elif 'A2' == userpos: A2= 0
        elif 'A3' == userpos: A3= 0
    return jsonify(msg='variable reiniciada')

# Bloque revision Puntos y cambios en equipo------------------------------------------------
@app.route("/puntos",methods=["POST","GET"])
def puntos():
    jugado=list()
    if 'nombre' in session:
        app.config['MYSQL_DB'] = torneo
        cur = mysql.connection.cursor()
        sQuery = 'SELECT * FROM registrados WHERE login_id = %s'
        
        cur.execute(sQuery %(session['id']) )
        user_team = cur.fetchone()
        mysql.connection.commit()
        if user_team == None:
            
            return redirect(url_for('creaequipo'))
        else:
            app.config['MYSQL_DB'] = torneo
            cur = mysql.connection.cursor()
            sQuery = 'SELECT * FROM registrados WHERE login_id = %s'
            
            
            cur.execute(sQuery %(session['id']) )
            user_team = cur.fetchone()
            print ('equipo favorito:',user_team[3])
            fQuery="SELECT logo,name,teams_id FROM teams WHERE teams_id=%s"
            cur.execute(fQuery %user_team[3])
            fav=cur.fetchone()
            mysql.connection.commit()
            ses=session['id']
            ligas=info_liga(ses)
            pts=0
            if user_team == None:
                
                return redirect(url_for('creaequipo'))
            else:
                ant=-1
                jugado=carga_equipo(ant)
                escuadra=dict(jugado[16])
                supl=list(escuadra['suplentes'])
                for jug in jugado:
                    juga=list(jug)
                    print (juga[2])
                    if str(juga[2]) in supl:
                        print('esta')
                        continue
                    else:
                        try:
                            pts+=int(jug[5])
                        except:continue
                print(pts)
                return render_template('puntos.html',jP1=jugado[0],jP2=jugado[1],jD1=jugado[2],
                jD2=jugado[3],jD3=jugado[4],jD4=jugado[5],jD5=jugado[6],jM1=jugado[7],
                jM2=jugado[8],jM3=jugado[9],jM4=jugado[10],jM5=jugado[11],jA1=jugado[12],
                jA2=jugado[13],jA3=jugado[14],name_team=jugado[15],pts=pts,favorito=fav,ligas=ligas, supl=supl)
            
    else:
        return render_template('ingresar.html')

@app.route("/p/<string:login_id>/")
def puntos_equipo(login_id):
    jugado=list()
    if 'nombre' in session:
        app.config['MYSQL_DB'] = torneo
        cur = mysql.connection.cursor()
        sQuery = 'SELECT * FROM registrados WHERE login_id = %s'
        elegido=login_id
        
        cur.execute(sQuery %elegido)
        user_team = cur.fetchone()
        print ('equipo favorito:',user_team[3])
        fQuery="SELECT logo,name,teams_id FROM teams WHERE teams_id=%s"
        cur.execute(fQuery %user_team[3])
        fav=cur.fetchone()
        mysql.connection.commit()
        ses=session['id']
        ligas=info_liga(elegido)
        pts=0
        if user_team == None:
            
            return redirect(url_for('creaequipo'))
        else:
            ant=-1
            jugado=carga_equipos(ant,elegido)
            escuadra=dict(jugado[16])
            supl=list(escuadra['suplentes'])
            for jug in jugado:
                juga=list(jug)
                print (juga[2])
                if str(juga[2]) in supl:
                    print('esta')
                    continue
                else:
                    try:
                        pts+=int(jug[5])
                    except:continue
            print(pts)
            return render_template('puntos.html',jP1=jugado[0],jP2=jugado[1],jD1=jugado[2],
            jD2=jugado[3],jD3=jugado[4],jD4=jugado[5],jD5=jugado[6],jM1=jugado[7],
            jM2=jugado[8],jM3=jugado[9],jM4=jugado[10],jM5=jugado[11],jA1=jugado[12],
            jA2=jugado[13],jA3=jugado[14],name_team=jugado[15],pts=pts,favorito=fav,ligas=ligas,supl=supl)
            
    else:
        return render_template('ingresar.html')


# Bloque revision Puntos y cambios en equipo------------------------------------------------
@app.route("/equipo",methods=["POST","GET"])
def equipo():
    jugado=list()
    if 'nombre' in session:
        app.config['MYSQL_DB'] = torneo
        cur = mysql.connection.cursor()
        sQuery = 'SELECT * FROM registrados WHERE login_id = %s'
        
        cur.execute(sQuery %(session['id']) )
        user_team = cur.fetchone()
        mysql.connection.commit()
        if user_team == None:
            
            return redirect(url_for('creaequipo'))
        else:
            ant=-1
            jugado=carga_equipo(ant)

            return render_template('equipo.html',jP1=jugado[0],jP2=jugado[1],jD1=jugado[2],jD2=jugado[3],jD3=jugado[4],jD4=jugado[5], 
            jD5=jugado[6],jM1=jugado[7],jM2=jugado[8],jM3=jugado[9],jM4=jugado[10],jM5=jugado[11],jA1=jugado[12],jA2=jugado[13],jA3=jugado[14],name_team=jugado[15])
            
    else:
        return render_template('ingresar.html')


    jugado=list()
    if 'nombre' in session:
        app.config['MYSQL_DB'] = torneo
        cur = mysql.connection.cursor()
        sQuery = 'SELECT * FROM registrados WHERE login_id = %s'
        
        cur.execute(sQuery %(format(login_id)) )
        user_team = cur.fetchone()
        mysql.connection.commit()
        if user_team == None:
            
            return redirect(url_for('creaequipo'))
        else:
            ant=-1
            jugado=carga_equipos(ant,login_id)

            return render_template('equipo.html',jP1=jugado[0],jP2=jugado[1],jD1=jugado[2],jD2=jugado[3],jD3=jugado[4],jD4=jugado[5], 
            jD5=jugado[6],jM1=jugado[7],jM2=jugado[8],jM3=jugado[9],jM4=jugado[10],jM5=jugado[11],jA1=jugado[12],jA2=jugado[13],jA3=jugado[14],name_team=jugado[15])
            
    else:
        return render_template('ingresar.html')

#Ruta para ver los equipos
@app.route("/t/<string:login_id>/")
def show_post(login_id):
    jugado=list()
    if 'nombre' in session:
        app.config['MYSQL_DB'] = torneo
        cur = mysql.connection.cursor()
        sQuery = 'SELECT * FROM registrados WHERE login_id = %s'
        
        cur.execute(sQuery %(login_id) )
        user_team = cur.fetchone()
        mysql.connection.commit()
        if user_team == None:
            
            return redirect(url_for('creaequipo'))
        else:
            ant=-1
            jugado=carga_equipos(ant,login_id)

            return render_template('equipo.html',jP1=jugado[0],jP2=jugado[1],jD1=jugado[2],jD2=jugado[3],jD3=jugado[4],jD4=jugado[5], 
            jD5=jugado[6],jM1=jugado[7],jM2=jugado[8],jM3=jugado[9],jM4=jugado[10],jM5=jugado[11],jA1=jugado[12],jA2=jugado[13],jA3=jugado[14],name_team=jugado[15])
            
    else:
        return render_template('ingresar.html')

    

@app.route("/ajaxequipo",methods=["POST","GET"])
def ajaxequipo():
    global dicequipo,torneo
    app.config['MYSQL_DB'] = torneo
    sQuery = "SELECT name FROM registrados WHERE login_id = %s"
    #crea cursor
    cur = mysql.connection.cursor()
    #Ejecuta
    ses=session['id']
    
    cur.execute(sQuery %(ses))
    name=cur.fetchone()
    equipo=list()
    for k,v in dicequipo.items():
        if k!='suplentes':
            equipo.append(v)
    print('el equipo es: ',equipo)
    aQuery="SELECT precio FROM players WHERE players_id=%s"
    precio_equipo=0
    for jugador in equipo:
        cur.execute(aQuery %jugador)
        precio_jugador=cur.fetchone()[0]
        precio_equipo+=precio_jugador
        precio_equipo=round(precio_equipo,1)
        print(precio_jugador,precio_equipo)
        
    return jsonify(name_team = name, supl=dicequipo['suplentes'],precio_eq=precio_equipo)

@app.route("/ajaxsubs",methods=["POST","GET"])
def ajaxsubs():
    global dicequipo
    return jsonify(form=dicequipo['form'])

#Bloque de transferencias------------------------------------------------------------------
@app.route("/transfer",methods=["POST","GET"])
def transfer():
    if 'nombre' in session:
        cero=0
        jugado=carga_equipo(cero)
        app.config['MYSQL_DB'] = torneo
        cur = mysql.connection.cursor()
        pQuery="SELECT players_id,img,dname,pos,pts,precio,teams.name,teams.teams_id,teams.logo FROM players JOIN teams ON players.team=teams.teams_id"
        
        cur.execute(pQuery)
        jugadores=cur.fetchall()
        listjug=list()
        for jugad in jugadores:
            jugador = list(jugad)
            jugador[3]= abr_posi(jugador[3])
            
            listjug.append(jugador)

        return render_template('transfer.html',jP1=jugado[0],jP2=jugado[1],
        jD1=jugado[2],jD2=jugado[3],jD3=jugado[4],jD4=jugado[5],jD5=jugado[6],
        jM1=jugado[7],jM2=jugado[8],jM3=jugado[9],jM4=jugado[10],jM5=jugado[11],
        jA1=jugado[12],jA2=jugado[13],jA3=jugado[14],name_team=jugado[15], jugadores=listjug)
        
        
    else:
        return render_template('ingresar.html')

@app.route("/ajaxtransfer",methods=["POST","GET"])
def ajaxtransfer():
    global dicequipo,torneo,ronda
    equipo=list()
    app.config['MYSQL_DB'] = torneo
    sQuery = "SELECT team,name FROM ultimo WHERE login_id = %s"
    fQuery = "SELECT %s FROM registrados WHERE login_id = %s"
    cur = mysql.connection.cursor()
    ses=session['id']
    rond='team_fecha_'+ronda
    cur.execute(fQuery %(rond,ses))
    plantilla=cur.fetchone()
    if plantilla == None:
        cur.execute(sQuery %(ses))
        plantilla=cur.fetchone()
   
    #dicequipo=json.loads(plantilla[0])
    cQuery = "SELECT name, fav, ligas FROM registrados WHERE login_id = %s"
    
    cur.execute(cQuery %(ses))
    datos=cur.fetchone()
    mysql.connection.commit()
    name=datos[0]

    posicion = request.form['POS']
    dicequipo[posicion]=0
    
    

    equipo=list()
    for k,v in dicequipo.items():
        if k!='suplentes':
            equipo.append(v)
    aQuery="SELECT precio FROM players WHERE players_id=%s"
    precio_equipo=0
    for jugador in equipo:
        if jugador == 0:
            print('jug eliminado')
        else:
            cur.execute(aQuery %jugador)
            precio_jugador=cur.fetchone()[0]
            precio_equipo+=precio_jugador
            precio_equipo=round(precio_equipo,1)

    operacion = request.form['operacion']
    if operacion=='carga':
        return jsonify(equipo=equipo, precio_eq=precio_equipo)
    
    
    
    P1=dicequipo['P1']; P2=dicequipo['P2']
    D1=dicequipo['D1'];D2=dicequipo['D2'];D3=dicequipo['D3'];D4=dicequipo['D4'];D5=dicequipo['D5']
    M1=dicequipo['M1'];M2=dicequipo['M2'];M3=dicequipo['M3'];M4=dicequipo['M4'];M5=dicequipo['M5']
    A1=dicequipo['A1'];A2=dicequipo['A2'];A3=dicequipo['A3']

@app.route("/ajaxrecupera",methods=["POST","GET"])
def ajaxrecupera():
    global dicequipo,torneo,ronda
    equipo=list()
    app.config['MYSQL_DB'] = torneo
    sQuery = "SELECT team,name FROM ultimo WHERE login_id = %s"
    fQuery = "SELECT %s FROM registrados WHERE login_id = %s"
    cur = mysql.connection.cursor()
    ses=session['id']
    rond='team_fecha_'+ronda
    cur.execute(fQuery %(rond,ses))
    plantilla=cur.fetchone()
    if plantilla == None:
        cur.execute(sQuery %(ses))
        plantilla=cur.fetchone()
   
    #dicequipo=json.loads(plantilla[0])
    cQuery = "SELECT name, fav, ligas FROM registrados WHERE login_id = %s"
    
    cur.execute(cQuery %(ses))
    datos=cur.fetchone()
    mysql.connection.commit()
    name=datos[0]

    posicion = request.form['POS']
    usr_recu = request.form['usr']
    dicequipo[posicion]=usr_recu
    
    

    equipo=list()
    for k,v in dicequipo.items():
        if k!='suplentes':
            equipo.append(v)
    aQuery="SELECT precio FROM players WHERE players_id=%s"
    precio_equipo=0
    for jugador in equipo:
        if jugador == 0:
            print('jug eliminado')
        else:
            cur.execute(aQuery %jugador)
            precio_jugador=cur.fetchone()[0]
            precio_equipo+=precio_jugador
            precio_equipo=round(precio_equipo,1)

    operacion = request.form['operacion']
    if operacion=='carga':
        return jsonify(equipo=equipo, precio_eq=precio_equipo)
    
    
    
    P1=dicequipo['P1']; P2=dicequipo['P2']
    D1=dicequipo['D1'];D2=dicequipo['D2'];D3=dicequipo['D3'];D4=dicequipo['D4'];D5=dicequipo['D5']
    M1=dicequipo['M1'];M2=dicequipo['M2'];M3=dicequipo['M3'];M4=dicequipo['M4'];M5=dicequipo['M5']
    A1=dicequipo['A1'];A2=dicequipo['A2'];A3=dicequipo['A3']


@app.route("/ajaxchange",methods=["POST","GET"])
def ajaxchange():
    global dicequipo,torneo,ronda
    
    play_in = request.form['user_a']
    
    if play_in=='guardar':
        app.config['MYSQL_DB'] = torneo
        rond=str('team_fecha_'+ronda)
        sQuery= """UPDATE ultimo SET team = %s WHERE login_id = %s"""
        
        fQuery= """UPDATE registrados SET %s = '%s' WHERE login_id = %s"""
        print('ronda ajaxChange:',ronda)
        #crea cursor
        cur = mysql.connection.cursor()
        equipo=json.dumps(dicequipo)
        #Ejecuta
        cur.execute(sQuery, (equipo,session['id']))
        cur.execute(fQuery %(rond,equipo,session['id']))
        mysql.connection.commit()
        return jsonify(msg="Equipo guardado!")

    play_out = request.form['user_b']    
    suplentes= list(dicequipo['suplentes'])
    for suplente in suplentes:
        if suplente==play_out:
            suplentes.remove(suplente) 
    suplentes.append(play_in)
    dicequipo['suplentes']=suplentes
    #print(list(dicequipo.keys())[list(dicequipo.values()).index(play_in)])
    
    return jsonify(sub=dicequipo['suplentes'])


@app.route("/ajaxcompra",methods=["POST","GET"])
def ajaxcompra():
    global dicequipo,torneo,ronda
    pos=str()
    userid = request.form['userid']
    
    cur = mysql.connection.cursor()
    if userid=='crear':
        if dicequipo['P1']==0 or dicequipo['P2']==0 or dicequipo['D1']==0 or dicequipo['D2']==0 or dicequipo['D3']==0 or dicequipo['D4']==0 or dicequipo['D5']==0 or dicequipo['M1']==0 or dicequipo['M2']==0 or dicequipo['M3']==0 or dicequipo['M4']==0 or dicequipo['M5']==0 or dicequipo['A1']==0 or dicequipo['A2']==0 or dicequipo['A3']==0:
            return jsonify(msg ="Debes elejir a los 15 jugadores de la plantilla")
            
        else:
            equipo=list()
            for k,v in dicequipo.items():
                if k!='suplentes':
                    equipo.append(v)
            print('el equipo es: ',equipo)
            if precio_equipo > 90:
                msgp = 'Te pasaste! tu planilla es de '+str(precio_equipo)+'UFB, tu presupuesto total es de 80UFB.'
                return jsonify(msg=msgp)
                
            else:
                app.config['MYSQL_DB'] = torneo
                sQuery= """UPDATE ultimo SET team = %s WHERE login_id = %s"""
                equipo=json.dumps(dicequipo)
                cur.execute(sQuery, (equipo,session['id']))
                creado= True
                return jsonify(creado= creado)
    
    equipo=list()
    for k,v in dicequipo.items():
        if k!='suplentes':
            equipo.append(v)
    print('el equipo es: ',equipo)
    for k,v in dicequipo.items():
        if v==0:
            dicequipo[k]=userid
            pos=k
    
    return jsonify(pos=pos)
#------------------------------------------------------------------------------------------
# Bloque Administracion de Fantasy---------------------------------------------------------
@app.route("/adminGMD",methods=["POST","GET"])
def adminGMD():
    global torneo
    if 'nombre' in session:
        torneo = 'bolivia2022'
        if session['tipo']=='administrador':
            if request.method=='POST':
                print('entra')    
                league_id = request.form['API_league_ID']
                current=API_currents(league_id)
                print('pasa current',current)
                API_season(current['season'])
                print('pasa season')
                teams=API_teams(current['season'])
                print ('pasa teams')
                #season_id = request.form['API_season_ID']
                API_fixtures(current['season'])
                print('pasa fixtures')
                API_squads(current['season'],teams)
                print('pasa squad')
                API_rounds()
                print('pasa rounds')
                API_events()
                print('pasa events')
                
                return render_template('adminGMD.html')
            else:
                
                return render_template('adminGMD.html')
        else:
            return render_template('inicio.html')
    else:
        return render_template('ingresar.html')

@app.route("/adminTarea",methods=["POST","GET"])
def adminTarea():
    img_change()
    precio()
    tpuntos()
    return render_template('adminGMD.html')

@app.route("/adminUPD",methods=["POST","GET"])
def adminUPD():
    rpuntos()
    return render_template('adminGMD.html')

@app.route("/adminLigas",methods=["POST","GET"])
def adminLigas():
    crea_ligas()
    return render_template('adminGMD.html')


@app.route("/adminTasks",methods=["POST","GET"])
def adminTasks():
    global torneo
    
    #Crea el objeto MySQL
    rondas=fecha_live()
    scheduler = BackgroundScheduler()
    ahora=datetime.datetime.now().isoformat()
    print(ahora)
    for ronda in rondas:
        inicio=str(ronda[0].isoformat()+'T11:00:00')
        fin=str(ronda[1].isoformat()+'T23:59:00')
        if ahora < fin:
            print('inicio:',inicio, 'fin',fin)
            scheduler.add_job(func=livescores, trigger="interval", seconds=120, start_date=inicio , end_date=fin)
        else:
            continue
            
    scheduler.print_jobs()
    scheduler.start()



    # Shut down the scheduler when exiting the app
    atexit.register(lambda: scheduler.shutdown())
    return render_template('adminGMD.html')

@app.route("/adminTPuntos",methods=["POST","GET"])
def adminTPuntos():
    crea_puntos_ronda()
    return render_template('adminGMD.html')



@app.route('/salir')
def salir():
    session.clear()
    return redirect(url_for('ingresar'))


if __name__ == '__main__':
    #ejecuta el servidor en debug
    app.run(host='0.0.0.0', debug=True )
    
    

