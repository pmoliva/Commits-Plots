import subprocess
import re
import abc
import datetime


class BaseBackend(object):
    __metaclass__=abc.ABCMeta


    @abc.abstractmethod
    def create_tmp_file(self):
        return


    @abc.abstractmethod
    def get_parsed_commit(self):
        return


class SVNBackend(BaseBackend):
    """
    svn log |grep [0-9] | trac
    """
    TEMP_FILENALE = 'svn_log_tmp.txt'
    DIR = '/tmp'


    def create_tmp_file(self):
        subprocess.\
            call("svn log | grep [0-9] | trac | awk '{print $3,$5}' > %s/%s'"\
                % (self.DIR, self. TEMP_FILENAME), shell=True)


    def get_parsed_commit(self):
        """
        file format: 'dev  %Y-%m-%d'
        """
        f = open('%s/%s' % (self.DIR, self.TEMP_FILE), 'r')
        for line in f:
            info = line.split(' ')
            yield (info[0], datetime.datetime.strptime(re.sub(r'\n',
                                                      '', info[2]), 
                                                      '%Y-%m-%d'))
        f.close()


class GitBackend(BaseBackend):
    """
    git log | egrep 'Author|Date' | sed '$!N;s/\n/ /
    """
    TEMP_FILENAME = 'git_log_tmp.txt'
    DIR = '/tmp'


    def create_tmp_file(self):

        "git log | egrep 'Author|Date' | sed '$!N;s/\n/ /' | awk '{print $2,$6,$7,$9}'"
        subprocess.\
            call("git log | egrep 'Author|Date'" 
                    "| sed '$!N;s/\\n/ /' | "
                    "tac |"
                    "awk '{print $2,$6,$7,$9}' > %s/%s"
                    % (self.DIR, self.TEMP_FILENAME), 
                    shell=True)


    def get_parsed_commit(self):
        f = open('%s/%s' % (self.DIR, self.TEMP_FILENAME), 'r')
        for line in f:
            info = line.split(' ')
            yield (info[0], datetime.datetime.strptime(
                re.sub('\n', '', ' '.join(info[1:])), '%b %d %Y'))
        f.close()


