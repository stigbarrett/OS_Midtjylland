from app import create_app, db, cli
from app.models import User, Post, Klub, Konkurrence, Grunddata, Medlemmer, Deltager, deltager_strak, Baner, PostBaner

app = create_app()
cli.register(app)


@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Post': Post, 'Klub': Klub}

if __name__ == "__main__":
    app.run(debug=True)