def set_default_cycle(room):
    """
    Sets a room's light cycle attributes to their default state.
    """
    #Method not currently in use

    #Room Attributes
    #whether light cycle phase is active
    room.db.light_cycle_active = False

    #light phase duration
    room.db.light_phase_lengths = {"dawn":2, "day":10, "dusk":2, "night":10}

    room.db.light_phase_echoes = {
        "dawn":"", "day":"", "dusk":"", "night":""
        } #phase change echoes

    room.db.light_phase_descs = {
        "dawn":"", "day":"", "dusk":"", "night":""
        } #phase room descriptions

    room.db.light_phase = "dawn" #current phase
    room.db.light_phase_time = 2 #time left

    room.db.light_phase_hour = 0 #time into cycle, starting at dawn

#
#
#

def advance_light_cycle(room):
        """
        Called on to advance the room's light cycle by one phase.
        """

        if room.db.light_phase == "dawn":
            room.db.light_phase = "day"
            room.db.light_phase_hour = room.db.light_phase_lengths["dawn"]
            #room.db.lumens = 50
            #Dawn to day

        elif room.db.light_phase == "day":
            room.db.light_phase = "dusk"
            room.db.light_phase_hour = room.db.light_phase_lengths["dawn"] + \
                room.db.light_phase_lengths["day"]
            #room.db.lumens = 25
            #Day to dusk

        elif room.db.light_phase == "dusk":
            room.db.light_phase = "night"
            room.db.light_phase_hour = room.db.light_phase_lengths["dawn"] + \
                room.db.light_phase_lengths["day"] + \
                room.db.light_phase_lengths["dusk"]
            #room.db.lumens = 10
            #Dusk to night

        elif room.db.light_phase == "night":
            room.db.light_phase = "dawn"
            room.db.light_phase_hour = 0
            #room.db.lumens = 30
            #Night to dawn. Also resets our cycle clock

        else:
            print "Light phase is not a phase" #shouldn't reach


        if room.db.light_phase_lengths[room.db.light_phase] > 0:
            room.msg_contents(room.db.light_phase_echoes[room.db.light_phase])

        room.db.light_phase_time = room.db.light_phase_lengths[
            room.db.light_phase]

        if room.db.light_phase_time <= 0: advance_light_cycle(room)

def at_cycle_hour(room):
    if room.db.light_cycle_active:

        room.db.light_phase_time -= 1
        room.db.light_phase_hour += 1

        while room.db.light_phase_time <= 0: advance_light_cycle(room)

#
# Methods below relate to the rset cycle command
#

def rset_cycle_on(self):
    """
    Usage: rset cycle on

    Turn light cycle on for the room
    """
    self.caller.location.db.light_cycle_active = True
    self.caller.msg("Light cycle activated.")

def rset_cycle_off(self):
    """
    Usage: rset cycle off

    Turn light cycle off for the room
    """
    self.caller.location.db.light_cycle_active = False
    self.caller.msg("Light cycle deactivated.")

def rset_cycle_length(self):
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
                #room.db.lumens = 30
				self.caller.msg("It is dawn.")

		for i in range(dawn_end, day_end):
			if self.caller.location.db.light_phase_hour == i:
				self.caller.location.db.light_phase = 'day'
				self.caller.location.db.light_phase_time = \
				day_length - (i - dawn_end)
                #room.db.lumens = 50
				self.caller.msg("It is day.")

		for i in range(day_end, dusk_end):
			if self.caller.location.db.light_phase_hour == i:
				self.caller.location.db.light_phase = 'dusk'
				self.caller.location.db.light_phase_time = \
				dusk_length - (i - day_end)
                #room.db.lumens = 25
				self.caller.msg("It is dusk.")

		for i in range(dusk_end, night_end):
			if self.caller.location.db.light_phase_hour == i:
				self.caller.location.db.light_phase = 'night'
				self.caller.location.db.light_phase_time = \
				night_length - (i - dusk_end)
                #room.db.lumens = 10
				self.caller.msg("It is night.")

    else:
		self.caller.msg("Please enter four numbers that add to "
			+str(24)+".")
		#replace 24 with zone cycle length


def rset_cycle_echo(self):
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
        echo = str(self.command.partition(self.arguments[2])[2].strip())

        #add echo to phase echoes
        self.caller.location.db.light_phase_echoes[self.arguments[2]] = echo

        self.caller.msg("Echo written for "+self.arguments[2] + ": " + echo)

    else:
        self.caller.msg(
            "Usage: rset cycle echo <dawn/dusk/day/night> <string>"
            )


def rset_cycle_desc(self):
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

        desc = str(self.command.partition(self.arguments[2])[2].strip())

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

        if desc == "": rdesc = desc #removes any newline+color if empty

        #add desc to phase descriptions
        self.caller.location.db.light_phase_descs[self.arguments[2]] = rdesc

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