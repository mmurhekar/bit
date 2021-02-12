import os
import click
import subprocess

HTTP_URL = 'http://ltc-repos.lcd.colo.seagate.com/sc/branches/'

class Clone:
    def __init__(self, url, dir_path):
        self.repo_url = url
        self.dir = dir_path
        os.chdir(dir_path)
        print(os.getcwd())
        cmd = 'svn co ' + url + ' .'
        print(cmd)
        process = subprocess.Popen(cmd, shell=True)
        process.communicate()
        click.echo(click.style('\nCompleted.', fg='green'))

@click.command()
@click.argument('repo_url')
@click.argument('dir_path')
def cli(repo_url, dir_path):
    """Clone Repository"""
    click.echo(click.style('Clone command', fg='green'))
    print("source repo", repo_url)
    Clone(repo_url, dir_path)
