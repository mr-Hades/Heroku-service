from flask import Flask, redirect, render_template, request
import os

from forms import HousesForm
from model import Model

Model().load('model.jlib')


project_root = os.path.dirname(__file__)
template_path = os.path.join(project_root, 'templates')
app = Flask(__name__, template_folder=template_path) 
app.secret_key = "asd576ADSADa_*';Basd"
 

@app.route("/", methods=['GET','POST'])
def index():
    form = HousesForm(request.form)
    model = Model()
    sub_areas = model.get_sub_area_list()
    form.sub_area.choices = [(str(i), name) for i, name in enumerate(sub_areas)]
    if request.method == 'POST' and form.validate():
        price = model.predict(form)
        return render_template('input_form.html', **{'form':form, 'price':price})
    return render_template('input_form.html', **{'form':form})


if __name__ == "__main__":
    Model().get_sub_area_list()
    app.run(host='0.0.0.0', port=80)