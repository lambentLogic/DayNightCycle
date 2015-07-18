#
# Commands and cmdset expanding storyteller tools
#

from evennia import CmdSet, utils
from evennia import Command


class StoryCmdSet(CmdSet):
    key = "storyteller_cmdset"

    def at_cmdset_creation(self):
        "Populate Cmdset"
        self.add(CmdCadv)

class CmdCadv(Command):
    """
    cadv

    Usage:
        cadv
    """

    key = "cadv"
    locks = "cmd.all()"
    help_category = "Storytelling"
    def parse(self):
        pass

    def func(self):
        self.caller.location.advance_light_cycle()