#
# Commands and cmdset expanding building tools
#

from evennia import CmdSet, utils
from evennia import Command

import lightcycle

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
        """
        Parsing method for the rset command.
        """
        self.command = self.args.strip() #everything after rset
        self.arguments = self.args.split() #list of arguments


    def func(self):
        """
        Functionality of the rset command.

        Currently either returns a default value, or uses the 'rset cycle' tool.
        """

        if not self.command:
            rset_default_msg = \
              "List of RSET Commands (help <command> for more information)\n\n"
            list_rset_commands = "cycle"
            rset_default_msg += list_rset_commands
            self.caller.msg(rset_default_msg)

        elif self.arguments[0] == "cycle":
            if len(self.arguments) == 1:
                #no arguments, suggest how to use
                self.caller.msg("Usage: rset cycle <command> <arguments>")

            elif self.arguments[1] == "on":
                lightcycle.rset_cycle_on(self)

            elif self.arguments[1] == "off":
                lightcycle.rset_cycle_off(self)

            elif self.arguments[1] == "length":
                lightcycle.rset_cycle_length(self)

            elif self.arguments[1] == "echo":
                lightcycle.rset_cycle_echo(self)

            elif self.arguments[1] == "desc":
                lightcycle.rset_cycle_desc(self)

            else:
                #non-valid argument, suggest how to use
                self.caller.msg("Usage: rset cycle <command> <arguments>")

        else:
            #if not an implemented rset command
            self.caller.msg("Command not recognized.")
