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
            if not self.arguments[1]:
                 print "rset cycle no arguments"
            elif self.arguments[1] == "on":
                #turn light cycle on for the room
                self.caller.location.db.light_cycle_active = True
                self.caller.msg("Light cycle activated.")
                pass
            elif self.arguments[1] == "off":
                #turn light cycle off for the room
                self.caller.location.db.light_cycle_active = False
                self.caller.msg("Light cycle deactivated.")
                pass
            elif self.arguments[1] == "length":
                #rset cycle length <dawn length> <day length> <dusk length> <night length>
                pass
            elif self.arguments[1] == "echo":
                #rset cycle echo <dawn/day/dusk/night> <string>
                pass
            elif self.arguments[1] == "desc":
                #rset cycle desc <dawn/day/dusk/night> <string>
                pass
        else:
            print "other"
