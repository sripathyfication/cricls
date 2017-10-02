from prettytable import PrettyTable
from cricli import *
import datetime
import sys, cmd, os


class CricShell(cmd.Cmd):
    intro = "\n Welcome to CricShell. (Command line tool for cricket scores. Type ? or help for commands) \n"
    prompt = 'cricShell >'
    main_header = " CricShell - Cricket on the command line, 2017"

    def create_cric_instance(self):
        self.cric_inst = Cricket()

    def do_list(self,arg):
        ''' Fetch the current ongoing international matches '''
        current_matches = self.cric_inst.get_ongoing_matches()

        print "\n\t " + self.main_header
        table = PrettyTable(["Match-Id","Date","Team-1","Team-2"])
        table.align = "l"
        for match in current_matches:
            date = datetime.datetime.strptime(match['date'],"%Y-%m-%dT%H:%M:%S.%fZ")
            date_new = date.strftime("%d-%m-%Y")
            table.add_row([match['unique_id'],date_new,match['team-1'],match['team-2']])
        print table

    def do_watch(self,arg):
        ''' Watch for updates on a match continuously unless interrupted
            Usage: watch <match-id>
            '''
        print "Not supported"

    def do_score(self,arg):
        '''Get scores for match id :
            Usage: score <match-id>
        '''
        score = self.cric_inst.get_score(int(arg))

        if score['matchStarted'] is True:
            print "\n\t\t " + self.main_header
            table = PrettyTable(["Match-Id","Score","Team-1","Team-2","State"])
            table.align = "l"
            table.add_row([int(arg),score['score'],score['team-1'],score['team-2'],score['stat']])
            print table
        elif score['matchStarted'] is False and score['score']:
            print "\n\t\t " + self.main_header
            table = PrettyTable(["Match-Id","Score","Team-1","Team-2","State"])
            table.align = "l"
            table.add_row([int(arg),score['score'],score['team-1'],score['team-2'],score['stat']])
            print table
        else:
            print "\n\t" + self.main_header
            table = PrettyTable(["Match-Id","Team-1","Team-2","State"])
            table.add_row([int(arg),score['team-1'],score['team-2'],'Match not started yet.'])
            print table


    def do_stop(self, arg):
        ''' Stop watching for updates to match-id '''
        print "Not supported"

    def do_help(self, arg):
        print "\n\t\t ==== CricShell Help Menu ==== "
        print "\tlist  --- List all ongoing international cricket matches"
        print "\tscore --- Fetch the score for match <match-id>"
        print "\twatch --- Watch for updates to match <match-id>"
        print "\tstop  --- Stop watching for updates to match <match-id>"
        print "\tclear --- Clear screen."
        print "\texit  --- Exit cricShell. Are you sure you want to go to espncricinfo? "

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
