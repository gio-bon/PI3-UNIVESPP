import os
from flask import Flask, render_template, request, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func

app = Flask(__name__)

# BANCO DE DADOS --------------------------------------------------------
basedir = os.path.abspath(os.path.dirname(__file__))

app.config['SQLALCHEMY_DATABASE_URI'] =\
        'sqlite:///' + os.path.join(basedir, 'database.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    sobrenome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(80), unique=True, nullable=False)
    senha = db.Column(db.String(16), nullable=False)
    idade = db.Column(db.Integer)
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
    ativo = db.Column(db.Boolean, default=True)

    def __repr__(self):
        return f'<User {self.nome}>'

class Curso(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    descricao  = db.Column(db.String(100))
    tecnologia  = db.Column(db.String(100), nullable=False)
    criador = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
    ativo = db.Column(db.Boolean, default=True)

    def __repr__(self):
        return f'<Curso {self.nome}>'

class Video(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_curso = db.Column(db.Integer, db.ForeignKey(Curso.id), nullable=False)
    ordem = db.Column(db.Integer)
    link = db.Column(db.String(200), nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
    ativo = db.Column(db.Boolean, default=True)

    def __repr__(self):
        return f'<Video {self.link}>'

# BANCO DE DADOS --------------------------------------------------------

# ROTAS --------------------------------------------------------

@app.route('/')
def index():
    cursos = Curso.query.all()
    return render_template('index.html', cursos=cursos, titulo='Cursos Univesp')

# ROTAS_Usuários --------------------------------------------------------

@app.route('/users')
def users():
    usuarios = Usuario.query.all()
    return render_template('users.html', usuarios=usuarios, titulo='Usuários')

""" @app.route('/<int:user_id>/user/')
def user(user_id):
    user = Usuario.query.get_or_404(user_id)
    return render_template('user.html', user=user) """

@app.route('/create-user/', methods=('GET', 'POST'))
def create_user():
    if request.method == 'POST':
        nome = request.form['nome']
        sobrenome = request.form['sobrenome']
        email = request.form['email']
        senha = request.form['senha']
        idade = int(request.form['idade'])
        novo_user = Usuario(nome=nome,
                          sobrenome=sobrenome,
                          email=email,
                          senha=senha,
                          idade=idade)
        db.session.add(novo_user)
        db.session.commit()

        return redirect(url_for('users'))

    return render_template('create_user.html')

@app.route('/<int:user_id>/edit-user/', methods=('GET', 'POST'))
def editu(user_id):
    user_edit = Usuario.query.get_or_404(user_id)

    if request.method == 'POST':
        nome = request.form['nome']
        sobrenome = request.form['sobrenome']
        email = request.form['email']
        senha = request.form['senha']
        idade = int(request.form['idade'])

        user_edit.nome = nome
        user_edit.sobrenome = sobrenome
        user_edit.email = email
        user_edit.senha = senha
        user_edit.idade = idade

        db.session.add(user_edit)
        db.session.commit()

        return redirect(url_for('users'))

    return render_template('edit-user.html', user=user_edit)

@app.post('/<int:user_id>/delete-user/')
def deleteu(user_id):
    user_deletar = Usuario.query.get_or_404(user_id)
    delecao_bool = False
    user_deletar.ativo = delecao_bool
    db.session.add(user_deletar)
    db.session.commit()
    return redirect(url_for('users'))

# ROTAS_Cursos --------------------------------------------------------

@app.route('/courses')
def courses():
    cursos = Curso.query.all()
    return render_template('courses.html', cursos=cursos, titulo='Cursos')

@app.route('/create-curso/', methods=('GET', 'POST'))
def create_course():
    if request.method == 'POST':
        nome = request.form['nome']
        descricao = request.form['descricao']
        tecnologia = request.form['tecnologia']
        criador = request.form['criador']
        novo_curso = Curso(nome=nome,
                          descricao=descricao,
                          tecnologia=tecnologia,
                          criador=criador)
        db.session.add(novo_curso)
        db.session.commit()

        return redirect(url_for('courses'))

    return render_template('create_course.html')

@app.route('/<int:curso_id>/edit-curso/', methods=('GET', 'POST'))
def editc(curso_id):
    curso_edit = Curso.query.get_or_404(curso_id)

    if request.method == 'POST':
        nome = request.form['nome']
        descricao = request.form['descricao']
        tecnologia = request.form['tecnologia']
        criador = request.form['criador']

        curso_edit.nome = nome
        curso_edit.descricao = descricao
        curso_edit.tecnologia = tecnologia
        curso_edit.criador = criador

        db.session.add(curso_edit)
        db.session.commit()

        return redirect(url_for('courses'))

    return render_template('edit-course.html', curso=curso_edit)

@app.post('/<int:curso_id>/delete-curso/')
def deletec(curso_id):
    curso_deletar = Curso.query.get_or_404(curso_id)
    delecao_bool = False
    curso_deletar.ativo = delecao_bool
    db.session.add(curso_deletar)
    db.session.commit()
    return redirect(url_for('courses'))

# ROTAS_Video --------------------------------------------------------

@app.route('/<int:curso_id>/videos')
def videos(curso_id):
    videos = Video.query.all()
    curso = Curso.query.get_or_404(curso_id)
    return render_template('videos.html', curso=curso, videos=videos)

@app.route('/create-video/<int:curso_id>', methods=('GET', 'POST'))
def create_video(curso_id):
    if request.method == 'POST':
        id_curso = curso_id
        ordem = int(request.form['ordem'])
        link = request.form['link']
        novo_video = Video(id_curso=id_curso,
                          ordem=ordem,
                          link=link)
        db.session.add(novo_video)
        db.session.commit()

        return redirect(url_for('videos', curso_id=id_curso))

    return render_template('create-video.html')

@app.route('/<int:video_id>/edit-video/<int:id_curso>', methods=('GET', 'POST'))
def editv(video_id, id_curso):
    video_edit = Video.query.get_or_404(video_id)

    if request.method == 'POST':
        ordem = request.form['ordem']
        link = request.form['link']

        video_edit.ordem = ordem
        video_edit.link = link

        db.session.add(video_edit)
        db.session.commit()

        return redirect(url_for('videos', curso_id=id_curso))

    return render_template('edit-video.html', video=video_edit)

@app.post('/<int:video_id>/delete-video/')
def deletev(video_id):
    video_deletar = Video.query.get_or_404(video_id)
    delecao_bool = False
    video_deletar.ativo = delecao_bool
    db.session.add(video_deletar)
    db.session.commit()
    return redirect(url_for('videos', curso_id=video_deletar.id_curso))

if __name__ == '__main__':
    app.run()