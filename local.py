# -*- coding: utf-8 -*-

from flask import Flask, render_template, redirect, url_for
from github import Github
import bd


g = Github('edgardoficial.yo@gmail.com', 'admin1992')

app = Flask(__name__)


base = bd.BaseDatos()
conectar = base.conectar()
version = base.get_version()
print version

@app.route('/')
def pagina(data=None):
    total_repos = len([repo for repo in g.get_user().get_repos()])
    data = {
            'usuario': g.get_user().name,
            'repos': g.get_user().get_repos(),
            'total_repos': total_repos,
            }

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
