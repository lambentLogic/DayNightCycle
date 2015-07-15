#
# Commands and cmdset expanding building tools
#

from evennia import CmdSet, utils
from evennia import Command
from evennia import ObjManipCommand

class BuildingCmdSet(CmdSet):


class CmdRset(ObjManipCommand):
    """
    rset

    Usage:
        rset <command> <arguments>
    """

#rset cycle <on/off>

#rset cycle length <dawn length> <day length> <dusk length> <night length>

#rset cycle echo <dawn/day/dusk/night> <string>

#rset cycle desc <dawn/day/dusk/night> <string>

#cadv

class CmdCadv(ObjManipCommand):
    """
    cadv

    Usage:
        cadv
    """