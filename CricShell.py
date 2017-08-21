import sys, cmd, os
from cricli import *
import datetime

class CricShell(cmd.Cmd):
    intro = "\n Welcome to CricShell. (Command line tool for cricket scores. Type ? or help for commands) \n"
    prompt = 'cricShell >'

    def create_cric_instance(self):
        self.cric_inst = Cricket()

    def do_list(self,arg):
        ''' Fetch the current ongoing international matches '''
        _matches = self.cric_inst.get_ongoing_matches()

        _head_string = "Match Id\t Date \t\t Team-1\t\t\t\tTeam-2"
        print "\t\t International Matches \n"
        print _head_string
        print "-  "*len(_head_string)

        for match in _matches:
            date = datetime.datetime.strptime(match['date'],"%Y-%m-%dT%H:%M:%S.%fZ")
            date_new = date.strftime("%d-%m-%Y")
            print str(match['unique_id'])+" \t"+str(date_new)+"  "+match['team-1']+"\t\t\t\t"+match['team-2']

    def do_watch(self,arg):
        ''' Watch for updates on a match continuously unless interrupted
            Usage: watch <match-id>
            '''
        print "Watching for updates to " +arg
    def do_score(self,arg):
        '''Get scores for match id :
            Usage: score <match-id>
        '''
        print " Fetching scores for match " +arg

    def do_stop(self, arg):
        ''' Stop watching for updates to match-id '''
        print "Stopped watching for updates to " +arg

    def do_help(self, arg):
        print "\n\t\t ==== CricShell Help Menu ==== "
        print "\tlist    --- List all ongoing international cricket matches"
        print "\tscore --- Fetch the score for match <match-id>"
        print "\twatch --- Watch for updates to match <match-id>"
        print "\tstop  --- Stop watching for updates to match <match-id>"
        print "\tclear --- Clear screen."
        print "\texit  --- Exit cricShell. Are you sure you want to go to espncricinfo? "

        print "\t\t**    End Help   ** "
    def do_clear(self,arg):
        os.system('clear')

    def do_exit(self,arg):
        ''' Quit CricShell '''
        print " Thanks for using CricShell"
        sys.exit(0)


if __name__ == '__main__':
    cri = CricShell()
    cri.create_cric_instance()
    cri.cmdloop()
