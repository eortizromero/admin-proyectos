# -*- coding: utf-8 -*-

from flask import Flask, render_template, redirect, url_for
from github import Github
import bd
from modelos import Sesion


app = Flask(__name__)

sesion = Sesion()

@app.route('/')
@app.route('/index')
def pagina(data=None):
    # total_repos = len([repo for repo in g.get_user().get_repos()])
    usuario = sesion.inicio_sesion('eortiz', 'admin00')
    if usuario:
        nombre = sesion.nombre
    data = {
            # 'usuario': g.get_user().name,
            # 'repos': g.get_user().get_repos(),
            # 'total_repos': total_repos,
            'user': nombre,
            }
    # base._buscar([('name', '=', 'Jorge'), ('edad', '=', '10'), ('activo', '=', True), ('es_admin', '=', True)])
    return render_template('pagina.html', data=data)


@app.route('/entrar')
def entrar():
    return render_template('entrar.html')


@app.route('/registrar')
def registrar():
    return render_template('registrar.html')


@app.route('/proyectos')
def proyectos():
    return render_template('proyectos.html')


@app.route('/repo/')
def repo():
    return redirect(url_for('pagina'))


@app.route('/repo/<name>')
def repository(name=None):
    return "Repository name %s" % name

if __name__ == '__main__':
    app.run(debug=True)
