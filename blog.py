import os


COV = None
if os.environ.get('FLASK_COVERAGE'):
    import coverage
    COV = coverage.coverage(branch=True, include='app/*')
    COV.start()


import sys
import click
from app import create_app, db
from app.models import Post, Tag, User, Role, Follow, Comment


app = create_app(os.getenv('FLASK_CONFIG') or 'default')
    
    
@app.shell_context_processor
def make_shell_context():
    return dict(db=db, Post=Post, Tag=Tag, User=User, Role=Role, Follow=Follow, Comment=Comment)


@app.cli.command()
@click.option('--coverage/--no-coverage', default=False,
              help='Run tests under code coverage')
def test(coverage):
    """Run unit tests"""
    if coverage and not os.environ.get('FLASK_COVERAGE'):
        os.environ['FLASK_COVERAGE'] = '1'
        os.execvp(sys.executable, [sys.executable] + sys.argv)
    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)
    if COV:
        COV.stop()
        COV.save()
        print('Coverage Summary:')
        COV.report()
        basedir = os.path.abspath(os.path.dirname(__file__))
        covdir = os.path.join(basedir, 'tmp/coverage')
        COV.html_report(directory=covdir)
        print('HTML version: file://%s/index.html' % covdir)
        COV.erase()
        


if __name__ == '__main__':
    app.run()