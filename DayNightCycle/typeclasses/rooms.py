"""
Room

Rooms are simple containers that has no location of their own.

"""

from evennia import DefaultRoom, TICKER_HANDLER


class LightCycle():

#artificial light cycle
    #on/off
    cycle_on = False

    #length (dawn/day/dusk/night)
    phase_lengths = {'dawn':2, 'day':10, 'dusk':2, 'night':10}

    #echo (dawn/day/dusk/night)
    echoes = {'dawn':'The sun rises.', 'day':'The day brightens.', 'dusk':'The sun descends.', 'night':'The light fades.'}

    #desc (dawn/day/dusk/night)
        #color this depending on phase
    phase_descs = {'dawn':None, 'day':None, 'dusk':None, 'night':None}

    #phase (dawn/day/dusk/night)
    current_phase = 'dawn'

    #time to next phase
    remaining_phase_time = 2

    #advance (for phase change or by cadv)
    def advance_cycle(self):
        #advance phase and adjust lumens
        if self.current_phase == 'dawn':
            self.current_phase = 'day'
            self.db.lumens = 50
        if self.current_phase == 'day':
            self.current_phase = 'dusk'
            self.db.lumens = 25
        if self.current_phase == 'dusk':
            self.current_phase = 'night'
            self.db.lumens = 10
        if self.current_phase == 'night':
            self.current_phase = 'dawn'
            self.db.lumens = 30

        #set new phase length
        self.remaining_phase_time = phase_lengths[self.current_phase]

    pass

class Room(DefaultRoom):
    """
    Rooms are like any Object, except their location is None
    (which is default). They also use basetype_setup() to
    add locks so they cannot be puppeted or picked up.
    (to change that, use at_object_creation instead)

    See examples/object.py for a list of
    properties and methods available on all Objects.
    """

    #has a light cycle
    roomLightCycle = LightCycle();

    #Generate a description that includes the light cycle phase (if active)
    def return_appearance(self, looker):
        """
        Called by the Look command.
        Here returns the light phase echo, if applicable.
        """
        ##overloaded method will go here. not doing anything unique yet
        string = super(Room, self).return_appearance(looker)
        return string

    pass


    #ticks a light cycle
    def at_object_creation(self):
        "Called when the object is first created." #Set to minute for testing purposes
        TICKER_HANDLER.add(self, 60, hook_key="at_hour")

    def at_hour(self, *args, **kwargs):
        "Ticked at regular (hourly) intervals." #Set to minute for testing purposes
        print 'Tick, tock'
        if self.roomLightCycle.cycle_on:
            #alter values properly
            self.roomLightCycle.remaining_phase_time -= 1
            #perform checks and phaseshift if appropriate
            if self.roomLightCycle.remaining_phase_time == 0:
                self.roomLightCycle.advance_cycle()
                #relevant echo
                self.msg_contents(self.roomLightCycle.echoes[self.roomLightCycle.current_phase])
            #generate description

