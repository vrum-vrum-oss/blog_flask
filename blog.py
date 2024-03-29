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

from flask_migrate import upgrade
from app.models import Role, User

# import tests as t


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
    # tests = unittest.TestLoader().loadTestsFromTestCase(t.test_selenium.SeleniumTestCase)
    # tests = unittest.TestLoader().loadTestsFromTestCase(t.test_client.FlaskClientTestCase)
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
        

@app.cli.command()
@click.option('--length', default=25,
              help='Number of functions to include in the profiler report.')
@click.option('--profile-dir', default=None,
              help='Directory where profiler data files are saved.')
def profile(length, profile_dir):
    """Start the application under the code profiler."""
    from werkzeug.middleware.profiler import ProfilerMiddleware
    app.wsgi_app = ProfilerMiddleware(app.wsgi_app, restrictions=[length],
                                      profile_dir=profile_dir)
    app.run(debug=False)
    
    

@app.cli.command()
def deploy():
    """Run deployment tasks"""
    # migrate database to latest revision
    upgrade()
    
    # create or update user roles
    Role.insert_roles()
    
    # ensure all users are following themselves
    User.add_self_follows()


if __name__ == '__main__':
    app.run()