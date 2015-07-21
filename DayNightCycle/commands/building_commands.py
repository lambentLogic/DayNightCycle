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
        """
        Parsing method for the rset command.
        """
        self.command = self.args.strip() #everything after rset
        self.arguments = self.args.split() #list of arguments

    def func(self):
        """
        Functionality of the rset command. Currently either returns a default
        value, or uses the 'rset cycle' tool.
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
                """
                Usage: rset cycle on

                Turn light cycle on for the room
                """
                self.caller.location.db.light_cycle_active = True
                self.caller.msg("Light cycle activated.")

            elif self.arguments[1] == "off":
                """
                Usage: rset cycle off

                Turn light cycle off for the room
                """
                self.caller.location.db.light_cycle_active = False
                self.caller.msg("Light cycle deactivated.")

            elif self.arguments[1] == "length":
                """
                Usage:
                rset cycle length
                <dawn length> <day length> <dusk length> <night length>

                Sets what the lengths of the phases of the light cycle are
                """
                self.length_sum = 0 #variable to check cycle length adds up

                try:
                    length_map = map(int, self.arguments[2:])
                except (ValueError, IndexError):
                    #User failed to input arguments or input nonintegers
                    #no need to do anything in particular, else will cover
                    pass
                else:
                    #sum the arguments that should be numbers
                    self.length_sum = sum(length_map)

                if len(self.arguments) == 6 and self.length_sum == 24:
                    #replace 24 with zone-specific cycle length
                    #Good input; user input 4 numbers that add to 24
                    self.caller.location.db.light_phase_lengths = {
                    'dawn':int(self.arguments[2]),
                    'day':int(self.arguments[3]),
                    'dusk':int(self.arguments[4]),
                    'night':int(self.arguments[5])
                    }
                    self.caller.msg("Light phase lengths set.")
                    #go through and set room back to when it was in loop
                    dawn_length = int(self.arguments[2])
                    day_length = int(self.arguments[3])
                    dusk_length = int(self.arguments[4])
                    night_length = int(self.arguments[5])

                    dawn_end = dawn_length
                    day_end = day_length + dawn_end
                    dusk_end = dusk_length + day_end
                    night_end = night_length + dusk_end

                    #hours in range(dawn_end) is dawn
                    #hours in range(dawn_end,day_end) is day
                    #hours in range(day_end, dusk_end) is dusk
                    #hours in range(dusk_end, night_end) is night

                    for i in range(dawn_end):
                        if self.caller.location.db.light_phase_hour == i:
                            self.caller.location.db.light_phase = 'dawn'
                            self.caller.location.db.light_phase_time = \
                            dawn_length - i
                            self.caller.msg("It is dawn.")

                    for i in range(dawn_end, day_end):
                        if self.caller.location.db.light_phase_hour == i:
                            self.caller.location.db.light_phase = 'day'
                            self.caller.location.db.light_phase_time = \
                            day_length - (i - dawn_end)
                            self.caller.msg("It is day.")

                    for i in range(day_end, dusk_end):
                        if self.caller.location.db.light_phase_hour == i:
                            self.caller.location.db.light_phase = 'dusk'
                            self.caller.location.db.light_phase_time = \
                            dusk_length - (i - day_end)
                            self.caller.msg("It is dusk.")

                    for i in range(dusk_end, night_end):
                        if self.caller.location.db.light_phase_hour == i:
                            self.caller.location.db.light_phase = 'night'
                            self.caller.location.db.light_phase_time = \
                            night_length - (i - dusk_end)
                            self.caller.msg("It is night.")

                else:
                    self.caller.msg("Please enter four numbers that add to "
                        +str(24)+".")
                    #replace 24 with zone cycle length

            elif self.arguments[1] == "echo":
                """
                Usage:
                rset cycle echo <dawn/day/dusk/night> <string>

                Sets the echoes for the phases of the light cycle
                """

                #test if there are at least 2 arguments
                if len(self.arguments) == 2:
                    self.caller.msg(
                    "Usage: rset cycle echo <dawn/dusk/day/night> <string>"
                    )
                elif self.arguments[2] == 'dawn' or\
                self.arguments[2] == "day" or\
                self.arguments[2] == "dusk" or\
                self.arguments[2] == "night":
                    #formatted right, now we need to get <string>
                    echo = str(
                    self.command.partition(self.arguments[2])[2].strip()
                    )

                    #add echo to phase echoes
                    self.caller.location.db.light_phase_echoes[
                    self.arguments[2]
                    ] = echo

                    self.caller.msg("Echo written for "+self.arguments[2] +
                    ": " + echo)
                else:
                    self.caller.msg(
                    "Usage: rset cycle echo <dawn/dusk/day/night> <string>"
                    )

            elif self.arguments[1] == "desc":
                """
                Usage:
                rset cycle desc <dawn/day/dusk/night> <string>

                Writes additional room description based on phase in light cycle
                """

                #test if there are at least 2 arguments
                if len(self.arguments) == 2:
                    self.caller.msg(
                    "Usage: rset cycle desc <dawn/dusk/day/night> <string>"
                    )
                elif self.arguments[2] == 'dawn' or\
                self.arguments[2] == "day" or\
                self.arguments[2] == "dusk" or\
                self.arguments[2] == "night":
                    #formatted right, now we need to get <string>

                    desc = str(
                    self.command.partition(self.arguments[2])[2].strip()
                    )

                    if self.arguments[2] == 'dawn':
                        rdesc = "\n{Y" + desc #dark yellow
                    elif self.arguments[2] == 'day':
                        rdesc =  "\n{w" + desc #bright white
                    elif self.arguments[2] == 'dusk':
                        rdesc = "\n{R" + desc #dark red
                    elif self.arguments[2] == 'night':
                        rdesc = "\n{c" + desc #bright cyan
                    else:
                        print "Something has gone wrong" #shouldn't reach here

                    if desc == "": rdesc = desc

                    #add desc to phase descriptions
                    self.caller.location.db.light_phase_descs[
                    self.arguments[2]
                    ] = rdesc

                    #show builder what they wrote and for where
                    self.caller.msg(
                    "Light phase room description written for " +
                    self.arguments[2] + ": " + rdesc
                    )

                else:
                    #didn't use right in some fashion
                    self.caller.msg(
                    "Usage: rset cycle desc <dawn/dusk/day/night> <string>"
                    )

            else:
                #if not an implemented rset command
                self.caller.msg("Command not recognized.")
