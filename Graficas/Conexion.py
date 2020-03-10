import pymysql

def getBacterias():
    db = pymysql.connect("gautabases.ga","microuniverse_user","microuniverse_user_PASS_223","microuniverse")
    cursor = db.cursor()
    grafica = []
    sql = "SELECT * FROM cbacteria"
    cursor.execute(sql)
    grafica = cursor.fetchall()
    db.close()

    return grafica


def getGrafica(id):
    db = pymysql.connect("gautabases.ga","microuniverse_user","microuniverse_user_PASS_223","microuniverse")
    cursor = db.cursor()
    grafica = []
    sql = "SELECT * FROM mpoblaciones WHERE id_pob = {}".format(id)


    cursor.execute(sql)
    grafica = cursor.fetchall()
    db.close()

    return grafica

def getbac(id):
    db = pymysql.connect("gautabases.ga","microuniverse_user","microuniverse_user_PASS_223","microuniverse")
    cursor = db.cursor()
    sql = "SELECT * FROM mproyectos WHERE id_pry = {}".format(id)
    cursor.execute(sql)
    bac_id = cursor.fetchall()
    
    sql = "SELECT * FROM cbacteria WHERE id_bac = {}".format(bac_id[0][1])

    cursor.execute(sql)
    grafica = cursor.fetchall()
    db.close()

    return grafica


def getbacR(id):
    db = pymysql.connect("gautabases.ga","microuniverse_user","microuniverse_user_PASS_223","microuniverse")
    cursor = db.cursor()
    sql = "SELECT * FROM cbacteria WHERE id_bac = {}".format(id)

    cursor.execute(sql)
    grafica = cursor.fetchall()
    db.close()

    return grafica


import math

def TazaCrecimiento(tem, ph,aw,creOP,cof,tp,tm,tma,po,pm,pma,awma,awm,awp):
    t = float(tem)
    p = float(ph)
    awc = float(aw)
    top = float(tp)
    tmin = float(tm)
    tmx = float(tma)
    phmin = float(pm)
    phop = float(po)
    phmax = float(pma)
    awop = float(awp)
    awmin = float(awm)
    awmax = float(awma)
    M = float(creOP)
    #-0.3996050206110664
    #-0.399
    #-0.39999407705623075
    cofc = float(cof)
    if awc == 0:
        awc = 1
    faw = pow((((awc-awmin)*(1-(2.77*(cofc*(awc)))))/((awop-awmin)*(1-(2.77*(cofc*(awc)))))),2) 
    ft = pow((((t-tmin)*(1-(2.77*(cofc*(t-tmx)))))/((top-tmin)*(1-(2.77*(cofc*(t-tmx)))))),2)
    fp = (((p-phmax)*(p-phmin))/(((p-phmin)*(p-phmax))-(pow((p-phop),2))))
    Mm = M*ft* fp*faw

    return Mm

def PobF(b,Mm,pi,pm,ti):
    t = float(ti)
    pIt = float(pi)
    a = float(pm)-pIt
    pf =(a*(+(math.e**(b*(-math.e**(-Mm*t))))))+pIt
    return pf

def curva(tem, ph,aw,creOP,cof,tp,tm,tma,po,pm,pma,awma,awm,awp,pi,poma,tr):

    t = float(tr)
    horas = []
    poblacion = []
    c =0
    Mm =TazaCrecimiento(tem, ph,aw,creOP,cof,tp,tm,tma,po,pm,pma,awma,awm,awp)
    b = 1
    xm = PobF(b,Mm,float(pi),float(poma),0)
    print()
    while (xm>(float(pi)+0.01) or xm<(float(pi)-0.01)):
        
        b = b +0.01
        if b>20:
            break
        xm = PobF(b,Mm,float(pi),float(poma),0) 
    while t>= c:
        horas.append(c)
        pft =PobF(b,Mm,float(pi),float(poma),c)
        poblacion.append(pft)
        c = c +1
    conar = [horas,poblacion]
    return conar

def curvae(tem, ph,aw,creOP,cof,tp,tm,tma,po,pm,pma,awma,awm,awp,pi,poma,tr):

    t = float(tr)
    Mm =TazaCrecimiento(tem, ph,aw,creOP,cof,tp,tm,tma,po,pm,pma,awma,awm,awp)
    b = 1
    xm = PobF(b,Mm,float(pi),float(poma),0)
    while (xm>(float(pi)+0.01) or xm<(float(pi)-0.01)):
        
        b = b +0.01
        if b>20:
            break
        xm = PobF(b,Mm,float(pi),float(poma),0) 
    
    pft =PobF(b,Mm,float(pi),float(poma),t)
    
    return pft