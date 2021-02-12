import os
import click
import subprocess

trunkReposUrl = 'http://ltc-repos.lcd.colo.seagate.com/sc/trunk/SC/src'
MERGED_REV_FILE = 'merged_revisions.txt'
IGNORE_REV_FILE = 'ignore_revisions.txt'

class MergeInfo:
    def __init__(self, src, dest):
        self.trunkRepoUrl = 'http://ltc-repos.lcd.colo.seagate.com/sc/trunk/SC/src'
        self.work_dir = os.getcwd()
        self.src_branch = src
        self.dest_branch = dest
        self.src_url = self.get_repo_url(self.src_branch)
        self.dest_url = self.get_repo_url(self.dest_branch)
        self.isexport = False
        print('Source URL: ' + self.src_url)
        print('Target URL: ' + self.dest_url)

    def get_repo_url(self, branch):
        os.chdir(branch)
        # get repository information from the local repository
        cmd = 'svn info .'
        process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        results = process.communicate()
        results1 = '\n'.join(str(x, "utf-8") for x in results)
        out = results1.split('\n')
        out = out[2].split(' ')
        os.chdir(self.work_dir)
        ret = out.pop()
        return ret

    def get_merged_revisions(self):
        """
        export merged revisions of trunk branch into a text file
        """
        if self.isexport and self.src_url == trunkReposUrl:
            self.merged_rev_file = os.getcwd() + '/' + MERGED_REV_FILE
            cmd = 'svn mergeinfo --show-revs merged ' + self.src_url + ' > ' + self.merged_rev_file
            os.chdir(self.dest_branch)
            subprocess.call(cmd, shell=True)
            os.chdir(self.work_dir)

        os.chdir(self.dest_branch)
        cmd = 'svn mergeinfo --show-revs merged ' + self.src_url
        process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        results = process.communicate()
        results1 = "\n".join(str(x, "utf-8") for x in results)
        revs_tmp = results1.split('\n')
        revs_tmp.pop()
        revs_tmp.pop()
        return revs_tmp

    def get_eligible_revisions(self):
        """
        get eligible revisions to merge in target branch from trunk
        """
        if self.src_url == trunkReposUrl:
            os.chdir(self.dest_branch)
            cmd = 'svn mergeinfo --show-revs eligible ' + self.src_url
            process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            results = process.communicate()
            results1 = "\n".join(str(x, "utf-8") for x in results)
            revs_tmp = results1.split('\n')
            revs_tmp.pop()
            revs_tmp.pop()
            return revs_tmp

    def get_merge_info(self, merged):
        """
        get the revisions ready to merge to the target branch
        """

        if merged == True:
            # show merged revisions
            click.echo(click.style('\nMerged Revisions:', fg='red'))
            local_revs = self.get_merged_revisions()
        else:
            # show eligible revisions to be merged
            click.echo(click.style('\nEligible Revisions:', fg='red'))
            local_revs = self.get_eligible_revisions()

        # find revisions eligible for a merge
        revs = []

        # filter out the revisions which needs to be ignored
        ignore_rev_file = self.dest_branch + '/' + IGNORE_REV_FILE
        if os.path.isfile(ignore_rev_file):
            ignore_file = open(ignore_rev_file, 'r+')
            for r in local_revs:
                ignore = 0
                ignore_file.seek(0)
                for line in ignore_file:
                    if r.strip() == line.strip():
                        ignore = 1
                        break
                if ignore == 0:
                    revs.append(r)
            ignore_file.close()
        else:
            for r in local_revs:
                revs.append(r)

        return revs

    def show_revision_details(self, rev_list):
        # revs now contains a list of trunk revisions not yet merged to destination branch
        # and are not in the ignore list
        os.chdir(self.src_branch)
        ret_values = []
        test_file = self.work_dir + '/merged_revs_details.txt'
        fp = open(test_file, 'w+')
        for revision in rev_list:
            cmd = 'svn log -r ' + revision
            proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            results = proc.communicate()
            results1 = "".join(str(x, "utf-8") for x in results)
            temp_list = results1.split('\n')
            ismerge = 0
            templist1 = temp_list[1].split('| ')
            user = templist1[1]

            # ignore any revisions caused by the build
            if user == 'cruisebuilder ':
                continue
            if user == 'tmasar ':
                continue

            if temp_list[1].startswith('Merge'):
                ismerge = 1

            commit_date = templist1[2]

            fmw = ''
            for f in temp_list:
                if f.find("JIRA Number:") != -1:
                    fmw = f
                    fmw = fmw.split(':')
                    fmw = fmw[1]

            rec_branch = ''
            print_next = 0
            found = 0
            for i in temp_list:
                if i.startswith('Allow Merge'):
                    found = 0
                    break

                if i.find('Recommended Branches:') != -1:
                    found = 1
                    if i.strip() == 'Recommended Branches:':
                        continue
                if found == 1:
                    rec_branch = rec_branch + ' ' + i.strip()

            change_sum = ''
            print_next = 0
            found = 0
            ignore = False
            for i in temp_list:
                if i.startswith('Change Summary:'):
                    found = found + 1
                    if i.strip() == 'Change Summary:':
                        print_next = 1
                        continue
                    change_sum = change_sum + ' ' + i
                    match_str = 'Change Summary:' + ' Merge From ' + self.dest_url
                    if i.startswith(match_str):
                        ignore = True
                        break
                if print_next == 1:
                    change_sum = change_sum + ' ' + i
                    print_next = 0

            if ignore == True:
                continue

            # show the revisions with details
            pstring = (revision + ' | ' + user + ' | ' + commit_date + ' | ' + fmw + ' | ' + rec_branch + ' | ' + change_sum )
            print(pstring)
            ret_values.append(revision)
            fp.write(pstring)
            fp.write('\n')
        fp.close()

@click.command()
@click.argument('src_branch')
@click.argument('dest_branch')
@click.option('--merged', is_flag=True, help='show merged revisions')
@click.option('--log', is_flag=True, help='show revision details')
def cli(src_branch, dest_branch, merged, log):
    """
    Merge Information: get the eligible revisions from source branch to merge in target branch.
    """
    click.echo(click.style('Merge info command', fg='green'))
    obj = MergeInfo(src=src_branch, dest=dest_branch)
    rev_list = obj.get_merge_info(merged)
    if log == True:
        obj.show_revision_details(rev_list)
    else:
        click.echo(rev_list)
