import os
import sys
import click
import subprocess
import commands.merge_info

MERGED_FILE = 'merged.txt'
COMMIT_FILE = 'commit_message.txt'

class Commit:
    def __init__(self, src_branch, dest_branch, auto):
        self.src_branch = src_branch
        self.dest_branch = dest_branch
        obj = commands.merge_info.MergeInfo(src_branch, dest_branch)
        self.src_url = obj.get_repo_url(self.src_branch)
        self.dest_url = obj.get_repo_url(self.dest_branch)
        self.auto = auto

    def do_commit(self):
        os.chdir(self.dest_branch)
        click.echo(self.dest_branch)
        click.echo(click.style('Attempting to commit...', fg='green'))
        filepath1 = self.dest_branch + '\\' + COMMIT_FILE
        filepath2 = self.dest_branch + '\\' + MERGED_FILE
        if os.access(filepath1, os.R_OK):
            cmd = 'svn commit -F ' + filepath1
            click.echo(click.style(cmd))
            """ Add Here a subprocess to run the commit command """
			process = subprocess.Popen(cmd, shell=True)
            results = process.communicate()
            os.remove(filepath1)
            os.remove(filepath2)
        else:
            click.echo('cannot commit')

    def generate_commit_mesg(self):
        os.chdir(self.dest_branch)
        testdir = os.getcwd()
        merged_file_path = testdir + '\\' + MERGED_FILE
        click.echo(merged_file_path)
        merged_file = open(merged_file_path, 'r')
        commit_file_path = testdir + '\\' + COMMIT_FILE
        commit_file = open(commit_file_path, 'w')
        click.echo(commit_file_path)

        logs = []
        list_fmw = []
        fmw_string = 'JIRA Number:'
        os.chdir(self.src_branch)
        click.echo(os.getcwd())

        for line in merged_file:
            cmd = 'svn log -r ' + line.strip()
            print(cmd)
            process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            results = process.communicate()
            logs.append(results)
            results1 = "".join(str(x, "utf-8") for x in results)
            loglist = results1.split('\n')

            fmw = ''
            for f in loglist:
                if f.find('JIRA Number:') != -1:
                    fmw = f
                    fmw = fmw.split(':')
                    fmw = fmw[1].strip()
            list_fmw.append(fmw)
        
        for l in logs:
            results1 = "".join(str(x, "utf-8") for x in l)
            tmp_list = results1.split('\n')

        click.echo(list_fmw)

        commit_file.write('TT Number: None\n')
        commit_file.write('CID Number: None\n')
        commit_file.write('JIRA Number: None\n')
        commit_file.write('Include this comment in Build Notes (Y/N): Y\n')
        commit_file.write('Change Summary: Merge From ' + self.src_url.strip() + ' To ' + self.dest_url.strip() + '\n')
        commit_file.write('Bug Type: (e.g. Legacy Bug/Introduced Bug/Unknown/None): Unknown\n')
        commit_file.write('New Functionality (Y/N): N\n')
        commit_file.write('Engineering Change Summary:\n')
        commit_file.write('Reviewer/s:\n')
        commit_file.write('Branches:\n')
        commit_file.write('Files changed: See Merge details below\n')
        commit_file.write('Testing: Rackbert Regression Tests\n')
        commit_file.write('Rackbert Results: PASS\n')
        commit_file.write('\n')
        commit_file.write('\n')
        commit_file.write('---------------------Individual Revision Details ----------------------------- \n')
        commit_file.write('\n')

        for log in logs:
            log = "".join(str(x, "utf-8") for x in log)
            lines = log.split('\n')
            for line in lines:
                commit_file.write(line.strip() + '\n')
            commit_file.write('\n')
            commit_file.write('\n')
        commit_file.close()
        merged_file.close()

    def write_commit(self, dest):
        os.chdir(dest)
        filepath = os.getcwd() + '\commit_mesg.txt'
        fp = open(filepath, 'w+')
        tt_num = input('tt_num: ')
        jira = input('JIRA Number: ')
        cid = input('CID: ')
        summary = input('Change Summary: ')

        fp.seek(0)
        s = f'tt_num : {tt_num}\n\n'
        fp.writelines(s)
        s = f'JIRA Number : {jira}\n\n'
        fp.writelines(s)
        s = f'CID Number : {cid}\n\n'
        fp.writelines(s)
        s = f'Change Summary : {summary}\n\n'
        fp.writelines(s)

        s = fp.readlines()
        print(s)
        fp.close()



@click.command()
@click.argument('src_branch')
@click.argument('dest_branch')
@click.option('--commit', is_flag=True, help='Do commit')
@click.option('--auto', is_flag=True, help='auto commit from merged log file')
@click.option('--gen', is_flag=True, help='generate commit message')
@click.option('--write', is_flag=True, help='write commit message')
def cli(src_branch, dest_branch, commit, auto, gen, write):
    """Commit the change"""
    click.echo(click.style('Commit command', fg='green'))
    obj = Commit(src_branch, dest_branch, auto)

    if gen:
        obj.generate_commit_mesg()
    elif write:
        obj.write_commit(dest_branch)
    elif commit:
        obj.do_commit()
    else:
        print('no options given')
