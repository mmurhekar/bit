import os
import click
import subprocess
import commands.merge_info

trunkReposUrl = 'http://ltc-repos.lcd.colo.seagate.com/sc/trunk/SC/src'
MERGED_FILE = 'merged.txt'
IGNORE_FILE = 'ignore.txt'

class Merge:
    def __init__(self, src_branch, dest_branch):
        self.src_branch = src_branch
        self.dest_branch = dest_branch
        self.src_url = self.get_repo_url(self.src_branch)
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

    def merge_revision(self, revision):
        filepath1 = self.dest_branch + '/' + MERGED_FILE
        merged_file = open(filepath1, 'a+')
        filepath2 = self.dest_branch + '/' + IGNORE_FILE
        ignore_file = open(filepath2, 'a+')

        # Attempt to merge the revision
        click.echo(click.style('Attempting to merge ' + revision + '...', fg='green'))
        os.chdir(self.dest_branch)
        cmd = 'svn merge -c ' + revision + ' ' + self.src_url
        print(cmd)
        process = subprocess.Popen(cmd, shell=True)
        results = process.communicate()

        merged_file.write(str(revision).strip() + '\n')
        ignore_file.write(str(revision).strip() + '\n')
        merged_file.close()
        ignore_file.close()
        click.echo(click.style('Merge Completed.', fg='green'))

    def merge_to_head(self):
        # get all eligible revision lists from source branch to merge
        merge = commands.merge_info.MergeInfo(self.src_branch, self.dest_branch)
        revisions = merge.get_merge_info(False)

        os.chdir(self.dest_branch)
        merged_file = open(MERGED_FILE, 'a')
        ignore_file = open(IGNORE_FILE, 'a')

        click.echo(click.style('Attempting to merge all revisions...', fg='green'))
        for revs in revisions:
            cmd = 'svn merge -c ' + revs + ' ' + self.src_url + ' . '
            print(cmd)
            process = subprocess.Popen(cmd, shell=True)
            results = process.communicate()

            merged_file.write(str(revs).strip() + '\n')
            ignore_file.write(str(revs).strip() + '\n')

        merged_file.close()
        ignore_file.close()
        click.echo(click.style('Merge Completed.', fg='green'))

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
@click.argument('src_branch')
@click.argument('dest_branch')
@click.option('--revision', type=str, help='svn revision to merge')
@click.option('--merge-all', is_flag=True, help='merge all revisions from src')
def cli(src_branch, dest_branch, revision, merge_all):
    """Merge revision from source to current working repo branch"""
    click.echo(click.style('Merge command', fg='green'))
    obj = Merge(src_branch, dest_branch)
    if revision != None:
        obj.merge_revision(revision)
    elif merge_all == True:
        obj.merge_to_head()
    else:
        click.echo('No input revision')
