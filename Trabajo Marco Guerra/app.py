from flask import Flask, request, render_template, redirect, flash; # type: ignore
from datetime import datetime;

app = Flask(__name__)
app.secret_key = 'd94231c751543589c4619656fb1781f28bc9452632e5977ef76660c352bc5da7'

recordatorios = []
idActial = 1

@app.route("/")
def index():
    ordered_reminder = sorted(
        recordatorios, key= lambda r:(not r["importante"], r["Fecha"]), reverse=True
    )
    ordered_reminder = ordered_reminder[::-1]
    return render_template("index.html",recordatorios = ordered_reminder)


@app.post("/crear-recordatorio")
def crear_recordatorio():
    global idActial
    datos = request.form
    texto = datos.get("texto")
    

    if not texto.strip() or len(texto.strip()) > 120: #strip devuelve los caracteres "  " y los convierte "" por lo que eso ya hace que entre el if
        flash("Ingrese algun recordatorio (la cantidad de letras maxima es de 120)","danger")
        return redirect("/")

    recordatorioNueva = recordatorioNueva = {"id": idActial, "texto": texto, "importante": False, "Fecha": datetime.now()}
    recordatorios.append(recordatorioNueva)

    idActial += 1

    flash("recordatorio agregado","success")
    return redirect("/")

@app.route("/api/taskList", methods=["GET"])
def api_recargar_lista():
    return recordatorios

@app.route("/api/taskList", methods=["POST"])
def api_crear_recordatorio():
    global idActial
    datos = request.get_json()
    nueva_recordatorio = {"id":idActial, "texto":datos["texto"],"importante":False, "Fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
    idActial += 1
    recordatorios.append(nueva_recordatorio)
    return nueva_recordatorio, 201

@app.route("/api/taskList/<int:id>", methods=["PATCH"])
def api_actualizar_recordatorio(id):
    for recordatorio in recordatorios:
       if recordatorio["id"] == id:
           recordatorio["importante"] = not recordatorio["importante"]
           return recordatorio
    return "recordatorio encontrado", 404

@app.route("/api/eliminar-recordatorio/<int:id>", methods=["POST"])
def api_eliminar_recordatorio(id):
    if request.form.get('_method') == 'DELETE':
        for index, recordatorio in enumerate(recordatorios):
            if recordatorio["id"] == id:
                del recordatorios[index]
                return redirect('/')
        return "recordatorio encontrado",404
    return "error metodo", 405

@app.route("/api/editar-recordatorio/<int:id>", methods=["GET", "POST"])#se que no es necesario pero prefiero dejarlo debido a que se que hace
def Edicion(id):
    for recordatorio in recordatorios:
        if recordatorio["id"] == id:
            if request.method == "POST":
                texto = request.form.get("texto")
                if not texto.strip() or len(texto.strip() > 120):
                    flash("El campo no puede estar vacio o con mas de 120 caracteres", "danger")
                    return render_template("index.html", recordatorios=recordatorios, recordatorio= recordatorio)
                importante = request.form.get("importante") == "True"
                recordatorio["texto"] = texto
                recordatorio["importante"] = importante

                flash("recordatorio actualizado correctamente", "success")
                return redirect("/")
            else:
                return render_template("index.html", recordatorios=recordatorios, recordatorio=recordatorio)
    return "recordatorio encontrado", 404

if __name__ == "__main__":
    app.run(debug=True)

