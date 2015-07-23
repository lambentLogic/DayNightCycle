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


def advance_light_cycle(room):
        """
        Called on to advance the room's light cycle by one phase.
        """

        if room.db.light_phase == "dawn":
            room.db.light_phase = "day"
            room.db.light_phase_hour = room.db.light_phase_lengths["dawn"]
            #Dawn to day

        elif room.db.light_phase == "day":
            room.db.light_phase = "dusk"
            room.db.light_phase_hour = room.db.light_phase_lengths["dawn"] + \
                room.db.light_phase_lengths["day"]
            #Day to dusk

        elif room.db.light_phase == "dusk":
            room.db.light_phase = "night"
            room.db.light_phase_hour = room.db.light_phase_lengths["dawn"] + \
                room.db.light_phase_lengths["day"] + \
                room.db.light_phase_lengths["dusk"]
            #Dusk to night

        elif room.db.light_phase == "night":
            room.db.light_phase = "dawn"
            room.db.light_phase_hour = 0
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