#
# Commands and cmdset expanding building tools
#

from evennia import CmdSet, utils
from evennia import Command

class BuildingCmdSet(CmdSet):
    key = "building_cmdset"

    def at_cmdset_creation(self):
        "Populate Cmdset"
        self.add(CmdRset)

class CmdRset(Command):
    """
    rset

    Usage:
        rset <command> <arguments>

    Building tool to set room attributes.
    """

    key = "rset"

    locks = "cmd.all()"
    help_category = "Building"

    def parse(self):
        self.command = self.args.strip()
        self.arguments = self.args.split()

    def func(self):

        if not self.command:
            rset_default_msg = "List of RSET Commands (help <command> for more information)\n\n"
            list_rset_commands = "cycle"
            rset_default_msg += list_rset_commands
            self.caller.msg(rset_default_msg)
        elif self.arguments[0] == "cycle":
            if len(self.arguments) == 1: #check the number of arguments
                 print "rset cycle no arguments" #debug line

            elif self.arguments[1] == "on":
                #Usage: rset cycle on
                #turn light cycle on for the room
                self.caller.location.db.light_cycle_active = True
                self.caller.msg("Light cycle activated.")

            elif self.arguments[1] == "off":
                #Usage: rset cycle off
                #turn light cycle off for the room
                self.caller.location.db.light_cycle_active = False
                self.caller.msg("Light cycle deactivated.")

            elif self.arguments[1] == "length":
                #rset cycle length <dawn length> <day length> <dusk length> <night length>
                self.length_sum = 0

                try:
                    self.length_sum = sum(map(int, self.arguments[2:]))
                except (ValueError, IndexError):
                    #User failed to input arguments or input nonintegers
                    pass

                if len(self.arguments) == 6 and self.length_sum == 24:
                    print "4 lengths that add to the cycle length"

                else:
                    self.caller.msg("Please enter four numbers that add to "+str(24)+".")
                    #replace 24 with zone cycle length when implemented

            elif self.arguments[1] == "echo":
                #rset cycle echo <dawn/day/dusk/night> <string>
                #test if there are at least 2 arguments
                #go back to self.command and strip rset cycle echo <>
                pass

            elif self.arguments[1] == "desc":
                #rset cycle desc <dawn/day/dusk/night> <string>
                #test if there are at least 2 arguments
                #go back to self.command and strip rset cycle desc <>
                pass
        else:
            print "other"
