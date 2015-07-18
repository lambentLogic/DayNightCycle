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

    def func(self):
        if not self.command:
            self.caller.msg("Introducing: The rset command.")


#rset cycle <on/off>

#rset cycle length <dawn length> <day length> <dusk length> <night length>

#rset cycle echo <dawn/day/dusk/night> <string>

#rset cycle desc <dawn/day/dusk/night> <string>

#cadv

class CmdCadv(Command):
    """
    cadv

    Usage:
        cadv
    """