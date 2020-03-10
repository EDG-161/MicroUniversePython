
import io
import matplotlib.pyplot as plt
import csv
import json
import math
from django.http import HttpResponse
from django.shortcuts import render
from matplotlib.backends.backend_agg import FigureCanvasAgg
from random import sample
from Graficas import Conexion

def plot(request, id):
    data =[]
    
    dire = "Rg{}.csv".format(id)
    
    try:
        with open(dire) as File:  
            reader = csv.reader(File)
            
            for row in reader:
                try:
                    print(row[0])
                    row = [float(row[0]),float(row[1])]
                    data.append(row)
                except Exception:
                    print("r e")
    except Exception:
        print("no hay archivo")
    data.sort()
    graficax = []
    graficay = []
    for x in data:
        print(x)
        graficax.append(float(x[0]))
        graficay.append(float(x[1]))

    grafica = [graficax,graficay]

    # Creamos una figura y le dibujamos el gráfico
    f = plt.figure(figsize=(8,3.5))

    # Creamos los ejes
    axes = f.add_axes([0.15, 0.15, 0.75, 0.75]) # [left, bottom, width, height]
    axes.plot(grafica[0],grafica[1])
    axes.set_xlabel("Hora")
    axes.set_ylabel("Poblacion")
    axes.set_title("Poblacion {}".format(id))

    # Como enviaremos la imagen en bytes la guardaremos en un buffer
    buf = io.BytesIO()
    canvas = FigureCanvasAgg(f)
    canvas.print_png(buf)

    # Creamos la respuesta enviando los bytes en tipo imagen png
    response = HttpResponse(buf.getvalue(), content_type='image/png')

    # Limpiamos la figura para liberar memoria
    f.clear()

    # Añadimos la cabecera de longitud de fichero para más estabilidad
    response['Content-Length'] = str(len(response.content))

    # Devolvemos la response
    return response

def regGrown(request, h1, p1, h2, p2, h3, p3,id):
    data =[]
    
    dire = "Rg{}.csv".format(id)
    
    try:
        with open(dire) as File:  
            reader = csv.reader(File)
            for row in reader:
                try:
                    data.append(row)
                except Exception:
                    print("r e")
    except Exception:
        print("no hay archivo")


    data.append([h1,p1])
    data.append([h2,p2])
    data.append([h3,p3])

    fil = open(dire,'w')
    with fil:  
        writer = csv.writer(fil)
        for r in data:
            writer.writerow(r)
       

    response = HttpResponse("<html><body onload='document.location.href=\"http://localhost:8080/MicroUniverse/Poblacion.jsp?id={}\"'>".format(id))

    return response

def dataR(request,id):
    data =[]
    
    dire = "Rg{}.csv".format(id)
    
    try:
        with open(dire) as File:  
            reader = csv.reader(File)
            
            for row in reader:
                try:
                    print(row[0])
                    row = [float(row[0]),float(row[1])]
                    data.append(row)
                except Exception:
                    print("r e")
    except Exception:
        print("no hay archivo")
    data.sort()
    graficax = []
    graficay = []
    for x in data:
        print(x)
        graficax.append(float(x[0]))
        graficay.append(float(x[1]))

    grafica = [graficax,graficay]
    cod = " google.load('visualization','1.0',{'packages':['corechart', 'line']}); google.setOnLoadCallback(graf);function graf() {var data = new google.visualization.DataTable();data.addColumn('number','Hora');data.addColumn('number','Poblacion');data.addRows(["

    for x in range(len(grafica[0])):
        cod = cod + ("[{},{}],").format(grafica[0][x],grafica[1][x])
        
    cod = cod +"]);var opciones = {title: "+"'Poblacion {}".format(id)
    cod = cod +"',subtitle: 'UFC/ml',vAxes: {0: {title: 'Poblacion UFC/ml'}},hAxis: {title: 'Hora'},colors: ['#a52714'],'height':350, curveType:"
    
    cod = cod +" 'function',legend: { position: 'bottom' },};"
    cod = cod +"var grafica = new google.visualization.LineChart(document.getElementById('Graficar'));grafica.draw(data,opciones);}"

    response = HttpResponse(cod)

    return response

def data(request, id):

    pob = Conexion.getGrafica(id)
    bacteria = Conexion.getbac(pob[0][1])
    tem = pob[0][3]
    ph = pob[0][4]
    aw = pob[0][5]
    creOP = bacteria[0][2]
    cof = 0.95
    tp = bacteria[0][3]
    tm = bacteria[0][6]
    tma = bacteria[0][9]
    po = bacteria[0][4]
    pm = bacteria[0][7]
    pma = bacteria[0][10]
    awma = bacteria[0][11]
    awm = bacteria[0][8]
    awp = bacteria[0][5]
    pi = int(pob[0][6])
    poma = 8.7
    tr =60
    
    grafica = Conexion.curva(tem, ph,aw,creOP,cof,tp,tm,tma,po,pm,pma,awma,awm,awp,pi,poma,tr)
    cod = " google.load('visualization','1.0',{'packages':['corechart', 'line']}); google.setOnLoadCallback(graf);function graf() {var data = new google.visualization.DataTable();data.addColumn('number','Hora');data.addColumn('number','Poblacion');data.addRows(["

    for x in range(len(grafica[0])):
        cod = cod + ("[{},{}],").format(grafica[0][x],grafica[1][x])
        
    cod = cod +"]);var opciones = {title: "+"'Poblacion {}".format(id)
    cod = cod +"',subtitle: 'UFC/ml',vAxes: {0: {title: 'Poblacion UFC/ml'}},hAxis: {title: 'Hora'},colors: ['#097138'],'width':400,'height':350, curveType:"
    
    cod = cod +" 'function',legend: { position: 'bottom' },};"
    cod = cod +"var grafica = new google.visualization.LineChart(document.getElementById('Grafica'));grafica.draw(data,opciones);}"

    response = HttpResponse(cod)

    return response

def compararPoblaciones(request, id):

    arrt = []

    for x in id:
        try:
            numtem = int(x)
            arrt.append(numtem)
        except Exception as e:
            pass

    id = arrt

    cod = "google.charts.load('current', {'packages':['corechart']});\n"
    cod = cod + "google.charts.setOnLoadCallback(drawChart);\n"
    cod = cod + "function drawChart() {\n"
    cod = cod + "var data = new google.visualization.DataTable();\n"
    cod = cod + "data.addColumn('number','Hora');\n"

    for x in id:
         cod = cod +("data.addColumn('number','Poblacion {}');\n").format(x)

    cod = cod + "data.addRows([\n"
    tr = 60
    for x in range(1,60):
        cod = cod + ("[{},").format(x)
        for ite in range(0,(len(id)-1)):
            pob = Conexion.getGrafica(id[ite])
            bacteria = Conexion.getbac(pob[0][1])
            tem = pob[0][3]
            ph = pob[0][4]
            aw = pob[0][5]
            creOP = bacteria[0][2]
            cof = 0.95
            tp = bacteria[0][3]
            tm = bacteria[0][6]
            tma = bacteria[0][9]
            po = bacteria[0][4]
            pm = bacteria[0][7]
            pma = bacteria[0][10]
            awma = bacteria[0][11]
            awm = bacteria[0][8]
            awp = bacteria[0][5]
            pi = int(pob[0][6])
            poma = 8.7
            grafica = Conexion.curvae(tem, ph,aw,creOP,cof,tp,tm,tma,po,pm,pma,awma,awm,awp,pi,poma,x)

            cod = cod + ("{},").format(grafica)

        pob = Conexion.getGrafica(id[len(id)-1])
        bacteria = Conexion.getbac(pob[0][1])
        tem = pob[0][3]
        ph = pob[0][4]
        aw = pob[0][5]
        creOP = bacteria[0][2]
        cof = 0.95
        tp = bacteria[0][3]
        tm = bacteria[0][6]
        tma = bacteria[0][9]
        po = bacteria[0][4]
        pm = bacteria[0][7]
        pma = bacteria[0][10]
        awma = bacteria[0][11]
        awm = bacteria[0][8]
        awp = bacteria[0][5]
        pi = int(pob[0][6])
        poma = 8.7
        grafica = Conexion.curvae(tem, ph,aw,creOP,cof,tp,tm,tma,po,pm,pma,awma,awm,awp,pi,poma,x)

        cod = cod + ("{}],\n").format(grafica)

    cod = cod + ("[{},").format(x)
    for ite in range(0,(len(id)-1)):
        pob = Conexion.getGrafica(id[ite])
        bacteria = Conexion.getbac(pob[0][1])
        tem = pob[0][3]
        ph = pob[0][4]
        aw = pob[0][5]
        creOP = bacteria[0][2]
        cof = 0.95
        tp = bacteria[0][3]
        tm = bacteria[0][6]
        tma = bacteria[0][9]
        po = bacteria[0][4]
        pm = bacteria[0][7]
        pma = bacteria[0][10]
        awma = bacteria[0][11]
        awm = bacteria[0][8]
        awp = bacteria[0][5]
        pi = int(pob[0][6])
        poma = 8.7
        grafica = Conexion.curvae(tem, ph,aw,creOP,cof,tp,tm,tma,po,pm,pma,awma,awm,awp,pi,poma,x)

        cod = cod + ("{},").format(grafica)
    pob = Conexion.getGrafica(id[len(id)-1])
    bacteria = Conexion.getbac(pob[0][1])
    tem = pob[0][3]
    ph = pob[0][4]
    aw = pob[0][5]
    creOP = bacteria[0][2]
    cof = 0.95
    tp = bacteria[0][3]
    tm = bacteria[0][6]
    tma = bacteria[0][9]
    po = bacteria[0][4]
    pm = bacteria[0][7]
    pma = bacteria[0][10]
    awma = bacteria[0][11]
    awm = bacteria[0][8]
    awp = bacteria[0][5]
    pi = int(pob[0][6])
    poma = 8.7
    grafica = Conexion.curvae(tem, ph,aw,creOP,cof,tp,tm,tma,po,pm,pma,awma,awm,awp,pi,poma,x)

    cod = cod + ("{}]]);").format(grafica)
    cod = cod +"\nvar opciones = {title: "+"'Poblaciones {}".format(id)
    cod = cod +"',\nsubtitle: 'UFC/ml',vAxes: {0: {title: 'Poblacion UFC/ml'}},hAxis: {title: 'Hora'},'width':400,'height':300, curveType:"
    
    cod = cod +" 'function',legend: { position: 'bottom' },};"
    cod = cod +"\nvar grafica =new google.visualization.LineChart(document.getElementById('Grafica'));\ngrafica.draw(data,opciones);}"

    response = HttpResponse(cod)

    return response

def RG(request):
    tem = request.GET.get('temperaturanumero')
    aw = request.GET.get('awnumero')
    ph = request.GET.get('phnumero')
    pi = request.GET.get('ufcnumero')
    idb = request.GET.get('bacteria')
    pob = Conexion.getGrafica(idb)
    bacteria = Conexion.getbacR(idb)
    creOP = bacteria[0][2]
    cof = 0.95
    tp = bacteria[0][3]
    tm = bacteria[0][6]
    tma = bacteria[0][9]
    po = bacteria[0][4]
    pm = bacteria[0][7]
    pma = bacteria[0][10]
    awma = bacteria[0][11]
    awm = bacteria[0][8]
    awp = bacteria[0][5]
    poma = 8.7
    tr =60
    
    grafica = Conexion.curva(tem, ph,aw,creOP,cof,tp,tm,tma,po,pm,pma,awma,awm,awp,pi,poma,tr)
    
    data = [{'Horas':grafica[0],'Poblacion':grafica[1]}]

    response = HttpResponse(json.dumps(data), content_type='application/json')

    return response

def templateGraf(requset):
    bacterias = Conexion.getBacterias()
    vs = []
    for bacteria in bacterias:
        vt = {'id':bacteria[0],'nom':bacteria[1]}
        vs.append(vt)
        print(bacteria)
    contexto = {'bacterias':vs}
    print(contexto)
    return render(requset,'grafica.html',contexto)


def POEA(request, id,t):
    pob = Conexion.getGrafica(id)
    bacteria = Conexion.getbac(pob[0][1])
    tem = pob[0][3]
    ph = pob[0][4]
    aw = pob[0][5]
    creOP = bacteria[0][2]
    cof = 0.95
    tp = bacteria[0][3]
    tm = bacteria[0][6]
    tma = bacteria[0][9]
    po = bacteria[0][4]
    pm = bacteria[0][7]
    pma = bacteria[0][10]
    awma = bacteria[0][11]
    awm = bacteria[0][8]
    awp = bacteria[0][5]
    pi = int(pob[0][6])
    poma = 8.7
    tr = float(t)
    pea = Conexion.curvae(tem, ph,aw,creOP,cof,tp,tm,tma,po,pm,pma,awma,awm,awp,pi,poma,tr)

    cod = "var obj = document.getElementById('PEA'); obj.value = {};".format(pea)

    response = HttpResponse(cod)

    return response

def POF(request, id,t):
    pob = Conexion.getGrafica(id)
    bacteria = Conexion.getbac(pob[0][1])
    tem = pob[0][3]
    ph = pob[0][4]
    aw = pob[0][5]
    creOP = bacteria[0][2]
    cof = 0.95
    tp = bacteria[0][3]
    tm = bacteria[0][6]
    tma = bacteria[0][9]
    po = bacteria[0][4]
    pm = bacteria[0][7]
    pma = bacteria[0][10]
    awma = bacteria[0][11]
    awm = bacteria[0][8]
    awp = bacteria[0][5]
    pi = int(pob[0][6])
    poma = 8.7
    tr = float(t)
    pea = Conexion.curvae(tem, ph,aw,creOP,cof,tp,tm,tma,po,pm,pma,awma,awm,awp,pi,poma,tr)
    g = 1/(3.33*math.log10(Conexion.curvae(tem, ph,aw,creOP,cof,tp,tm,tma,po,pm,pma,awma,awm,awp,pi,poma,5)/Conexion.curvae(tem, ph,aw,creOP,cof,tp,tm,tma,po,pm,pma,awma,awm,awp,pi,poma,4)))
    cod = "var obj = document.getElementById('PEA'); obj.value = {};".format(pea)
    cod = cod + "var obj2 = document.getElementById('TG'); obj2.value = {};".format(g)
    cod = cod + "var obj3 = document.getElementById('EL'); obj3.value = {};".format(pea)
    cod = cod + "var obj4 = document.getElementById('ELO'); obj4.value = {};".format(pea)
    cod = cod + "var obj5 = document.getElementById('EE'); obj5.value = {};".format(pea)

    response = HttpResponse(cod)

    return response