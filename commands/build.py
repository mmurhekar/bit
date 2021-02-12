import os
import sys
import click
import subprocess

# Build Commands
"""
build_cmd = {
    'B_INS100' : 'nant -D:project.current=indium -D:linear.build=true compile',
    'B_GS275'  : 'nant -D:project.current=galliumnx3 -D:linear.build=true compile',
    'B_SOS100' : 'nant -D:project.current=indiumec1 -D:linear.build=true compile',
    'B_GS265'  : 'nant -D:project.current=galliumlx3 -D:linear.build=true compile',
    'trunk'    : 'nant -D:project.current=indium -D:linear.build=true compile',
}
"""
build_cmd = {
    'B_INS100' : 'indium',
    'B_GS275'  : 'galliumnx3',
    'B_SOS100' : 'indiumec1',
    'B_GS265'  : 'galliumlx3',
    'trunk'    : 'indium',
}

class Build:
    def __init__(self, dir, clean):
        url = self.get_repo_url(dir)
        print(url)
        results = url.split('/')
        branch_name = ''
        for i in results:
            if i.find('B_') == 0:
                branch_name = i.strip()
                break
            elif i.strip() == 'trunk':
                branch_name = i.strip()
                break
        if self.check_key(build_cmd, branch_name):
            key = build_cmd[branch_name]
            if clean:
                cmd = 'nant -D:project.current=%s clean compile' % key
            else:
                cmd = 'nant -D:project.current=%s compile' % key
            click.echo(click.style('Build cmd: ' + cmd, fg='cyan'))
            process = subprocess.Popen(cmd, shell=True)
            results = process.communicate()
            click.echo(click.style('Build Completed', fg='green'))
        else:
            click.echo('Error: no build cmd defined')

    def check_key(self, dict, key):
        if key in dict:
            return True
        return False

    def get_repo_url(self, branch):
        os.chdir(branch)
        # get repository information from the local repository
        cmd = 'svn info .'
        process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        results = process.communicate()
        results1 = '\n'.join(str(x, "utf-8") for x in results)
        out = results1.split('\n')
        out = out[2].split(' ')
        ret = out.pop()
        return ret

@click.command()
@click.argument('dir')
@click.option('--clean', is_flag=True, help='do a clean build')
def cli(dir, clean):
    """
    Build Command
    """
    click.echo(click.style('Build command', fg='green'))
    os.chdir(dir)
    click.echo(os.getcwd())
    click.echo('Give some inputs')
    s = ''
    for line in sys.stdin:
        if 'quit' == line.rstrip():
            break
        s = s + line
    print(f'String : {s}')
    l = sys.stdin.readlines(2)
    print(f'lines read : {l}')
    Build(dir, clean)