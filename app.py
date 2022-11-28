from flask import Flask, request, render_template, jsonify
from datetime import datetime, timedelta
import mysql.connector

try:
    connection = mysql.connector.connect(
        host='localhost',
        port=3306,
        user='root',
        password='root',
        db='medidorco2'
    )

    if connection.is_connected():
        info_server = connection.get_server_info()
        print("Conexion exitosa a {}".format(info_server))
        cursor = connection.cursor()
        cursor.execute("SELECT DATABASE()")
        row = cursor.fetchone()
        print("Base de datos: {}".format(row))
        cursor.close()

except Exception as ex:
    print(ex)

app = Flask(__name__)
medida = 0.0
fecha = "12/12/22"
hora = "00:00"
auxCompararF = datetime.now() - timedelta(minutes=3)


@app.route('/')
def index():  # put application's code here
    comp = datetime.now() - auxCompararF
    nm = comp.minute
    return render_template('index.html', med=medida, fecha=fecha, hora=hora, nm=nm)


@app.route('/historial')
def historial():  # put application's code here

    dic1 = {"item": "hola", "a": "si"}

    return render_template('historial.html', dic1=dic1)


@app.route('/guardardatosar', methods=['GET'])
def guardardatosar():
    global medida, fecha, hora, auxCompararF
    if request.args.get('m') is not None:
        medida = request.args.get('m')
        fecha = datetime.now().date()
        hora = datetime.now().time().isoformat('minutes')
        if (auxCompararF + timedelta(minutes=3)) < datetime.now():
            registrar()
            auxCompararF = datetime.now()
        return "Datos guardados correctamente"
    return "Ocurrio un problema D:"


def registrar():
    try:
        if connection.is_connected():
            cursor = connection.cursor()
            sql = "INSERT INTO `mediciones`(`idMed`, `valorMed`, `fechaMed`,`horaMed`) VALUES(null, {},'{}'," \
                  "'{}');".format(medida, fecha, hora)
            cursor.execute(sql)
            connection.commit()
        else:
            print("Error al insertar registro")
    except Exception as ex:
        print(ex)


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
