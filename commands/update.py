import os
import click
import subprocess

class Update:
    def __init__(self, dest_branch):
        self.dest_branch = dest_branch
        self.dest_url = self.get_repo_url(self.dest_branch)
        os.chdir(self.dest_branch)
        click.echo(dest_branch)
        cmd = 'svn revert --recursive .'
        print(cmd)
        process = subprocess.Popen(cmd, shell=True)
        results = process.communicate()
        cmd = 'svn cleanup --remove-unversioned --remove-ignored .'
        print(cmd)
        process = subprocess.Popen(cmd, shell=True)
        results = process.communicate()
        cmd = 'svn update'
        print(cmd)
        process = subprocess.Popen(cmd, shell=True)
        results = process.communicate()
        pass

    def get_repo_url(self, branch):
        os.chdir(branch)
        # get repository information from the local repository
        cmd = 'svn info .'
        process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        results = process.communicate()
        results1 = '\n'.join(str(x, "utf-8") for x in results)
        out = results1.split('\n')
        out = out[2].split(' ')
        return out[1]

@click.command()
@click.argument('dest_branch')
def cli(dest_branch):
    """
    Update repository.
    """
    click.echo(click.style('Update command', fg='green'))
    Update(dest_branch)
