"""A Convenient Command Line Interface for common tasks"""
import click
import sys
from subprocess import call


@click.group()
def cli():
    """Command Line Interface for the CurrencyConverter project"""
    pass


@click.command()
def runserver():
    """Run the project"""
    call(
        'docker-compose -f local.yml up'.split()
    )


@click.command()
def stop():
    """Stop the project"""
    call(
        'docker-compose -f local.yml stop'.split()
    )


@click.command()
def build():
    """Build the django service of the project"""
    call(
        'docker-compose -f local.yml up --build django celeryworker '
        'celerybeat flower'.split()
    )


@click.command()
def test():
    """Test the project"""
    call(
        'docker-compose -f local.yml exec django bash -c'.split()
        + [
            "source compose/production/django/entrypoint && py.test --create-db"
        ]
    )


@click.command()
def testpdb():
    """Test the project with debugging"""
    call(
        'docker-compose -f local.yml exec django bash -c'.split()
        + [
            "source compose/production/django/entrypoint && py.test --create-db --pdb"
        ]
    )


@click.command()
def mypy():
    """Test the project"""
    call(
        'docker-compose -f local.yml exec django bash -c'.split()
        + [
            "source compose/production/django/entrypoint && "
            "mypy currency_converter"
        ]
    )


@click.command()
def sh():
    """Open the project's sh"""
    call(
        'docker-compose -f local.yml exec django bash -c'.split()
        + [
            "source compose/production/django/entrypoint && "
            "sh"
        ]
    )


@click.command()
def shp():
    """Open the project's shell_plus"""
    call(
        'docker-compose -f local.yml exec django bash -c'.split()
        + [
            "source compose/production/django/entrypoint && "
            "python manage.py shell_plus"
        ]
    )


@click.command()
def makemigrations():
    """Perform makemigrations for the project"""
    call(
        'docker-compose -f local.yml exec django bash -c'.split()
        + [
            "source compose/production/django/entrypoint && "
            "python manage.py makemigrations"
        ]
    )


@click.command()
def migrate():
    """Perform migrate for the project"""
    call(
        'docker-compose -f local.yml exec django bash -c'.split()
        + [
            "source compose/production/django/entrypoint && "
            "python manage.py migrate"
        ]
    )


@click.command()
def cov():
    """Test the project with coverage and html report"""
    call(
        'docker-compose -f local.yml exec django bash -c'.split()
        + [
            "source compose/production/django/entrypoint && "
            "coverage run -m pytest && coverage html"
        ]
    )


@click.command()
def createsuperuser():
    """Create a superuser for the project"""
    call(
        'docker-compose -f local.yml exec django bash -c'.split()
        + [
            "source compose/production/django/entrypoint && "
            "python manage.py createsuperuser"
        ]
    )


@click.command()
@click.argument('model')
def dumpdata(model):
    """Dump data for application.model"""
    call(
        'docker-compose -f local.yml exec django bash -c'.split()
        + [
            "source compose/production/django/entrypoint && "
            "python manage.py dumpdata {0} > {0}.json".format(model)
        ]
    )


@click.command(context_settings=dict(
    allow_extra_args=True,
))
def rc():
    """Run an arbitrary command"""
    command = ' '.join(sys.argv[2:])
    call(
        'docker-compose -f local.yml exec django bash -c'.split()
        + [f"source compose/production/django/entrypoint && {command}"]
    )


cli.add_command(runserver)
cli.add_command(stop)
cli.add_command(test)
cli.add_command(build)
cli.add_command(sh)
cli.add_command(shp)
cli.add_command(cov)
cli.add_command(mypy)
cli.add_command(makemigrations)
cli.add_command(migrate)
cli.add_command(rc)
cli.add_command(createsuperuser)
cli.add_command(dumpdata)
cli.add_command(testpdb)


if __name__ == '__main__':
    cli()
