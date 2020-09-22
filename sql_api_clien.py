from flask import Flask, request,make_response
from pysnmp.hlapi import *
import sqlite3

app = Flask(__name__)

@app.route('/login', methods=['POST'])
def get_user():
    content = request.json
    id = content["id"]
    ip = content["ip"]
    oid = content["oid"]
    comm = content["community"]

    respond_divided = 'Noo'

    if request.authorization.username == "galata" and request.authorization.password == "parola11":
        try:
            objectpart = ObjectType(ObjectIdentity(oid))
            errorIndication, errorStatus, errorIndex, varBinds = next(
                getCmd(SnmpEngine(),
                       CommunityData(comm),
                       UdpTransportTarget((ip, 161)),
                       ContextData(),
                       objectpart
                       )
            )
            for varBind in varBinds:
                respond_divided = str(varBind).split(" = ")[1]

            if respond_divided == 'No Such Object currently exists at this OID':
                    return make_response("Unrecognized OID ! ", 404)

        except Exception as e:
            return make_response(f"Fail ! {e}",400)

        conn = sqlite3.connect("snmp.db")
        c = conn.cursor()

        num = c.execute("SELECT NUM FROM RESPONDS ORDER BY NUM DESC LIMIT 1").fetchall()[0][0] + 1

        db = (num, id, oid, ip, respond_divided)

        c.execute("INSERT INTO RESPONDS VALUES (?,?,?,?,?)", db)
        conn.commit()
        conn.close()
        return "Connected Succesfully ! "
    else:
        return make_response("Fail ! ",401)



@app.route('/fetch', methods=['POST'])
def get_data():

    content = request.json
    id = content["id"]

    if request.authorization.username == "root" and request.authorization.password == "123":
            conn = sqlite3.connect("snmp.db", timeout=30)
            c = conn.cursor()

            for answer in c.execute("SELECT RESPOND FROM RESPONDS WHERE ID = ?",(id,)):
                return str(answer[0])

            return 'Not Ready Yet || Wrong ID'
    else:
        return "Not Authorized !"

@app.route('/delete',methods=['POST'])
def delete_it():
    content = request.json
    my_id = content["id"]

    try:
        if request.authorization.username == "galata" and request.authorization.password == "parola11":
            conn = sqlite3.connect("snmp.db", timeout=30)
            c = conn.cursor()
            c.execute("SELECT * FROM RESPONDS WHERE ID = ?",(my_id))
            sql = 'DELETE FROM RESPONDS WHERE ID=?'
            c.execute(sql, (my_id,))
            conn.commit()
            conn.close()
            return 'Successfully Deleted ! '
        else:
            return "Not Authorized"
    except:
        return 'Wrong ID Given\nCould not Delete It ! '

@app.route("/update",methods = ["POST"])
def update_it():
    content = request.json
    id = content["id"]
    new_id = content["new_id"]

    try:
        if request.authorization.username == "galata" and request.authorization.password == "parola11":
            conn = sqlite3.connect("snmp.db")
            c = conn.cursor()
            c.execute("SELECT * FROM RESPONDS WHERE ID = ?",(id))
            c.execute("UPDATE RESPONDS SET ID = ? WHERE ID = ?",(new_id,id))
            conn.commit()
            conn.close()
            return "Succesfully Updated"
        else:
            return "Not Authorized"
    except:
        return "Wrong ID Given !!"

if __name__ == '__main__':
    app.secret_key = "oh_its_so_secret"
    app.run(host='0.0.0.0',debug=True)





