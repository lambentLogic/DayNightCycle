"""
Room

Rooms are simple containers that has no location of their own.

"""

from evennia import DefaultRoom, TICKER_HANDLER

class Room(DefaultRoom):
    """
    Rooms are like any Object, except their location is None
    (which is default). They also use basetype_setup() to
    add locks so they cannot be puppeted or picked up.
    (to change that, use at_object_creation instead)

    See examples/object.py for a list of
    properties and methods available on all Objects.
    """




    #ticks a light cycle
    def at_object_creation(self):
        "Called when the object is first created." #Set to minute for testing purposes
        print 'Room created' #debug line
        TICKER_HANDLER.add(self, 60, hook_key="at_hour")

        #Room Attributes
        self.db.light_cycle_active = False #whether phase is active

        self.db.light_phase_lengths = {'dawn':2, 'day':10, 'dusk':2, 'night':10} #phase duration

        self.db.light_phase_echoes = {
        'dawn':'The sun rises.', 'day':'The day brightens.', 'dusk':'The sun descends.', 'night':'The light fades.'
        } #phase change echoes

        self.db.light_phase_descs = {
        'dawn':'\n{YRosy-fingered dawn caresses the land.', 'day':'\n{wThe sun shines brightly.',
         'dusk':'\n{RThe sky shines in the hues of twilight.', 'night':'\n{cStars sprinkle the dark sky.'
        } #phase room descriptions

        self.db.light_phase = 'dawn' #current phase
        self.db.light_phase_time = 2 #time left

        self.db.light_phase_hour = 0 #time into cycle


    def at_hour(self, *args, **kwargs):
        "Ticked at regular (hourly) intervals." #Set to minute for testing purposes
        print 'Tick, tock' #debug line
        if self.db.light_cycle_active == True:
            print 'cycle tick, tock' #debug line

            self.db.light_phase_time -= 1
            self.db.light_phase_hour += 1

            while self.db.light_phase_time <= 0: self.advance_light_cycle()

    def advance_light_cycle(self):
        "Called on to advance the room's light cycle by one phase."
        print "Cycle advanced" #debug line
        if self.db.light_phase == 'dawn':
            print 'It was dawn.' #debug line
            self.db.light_phase = 'day'
            self.db.light_phase_hour = self.db.light_phase_lengths['dawn']
        elif self.db.light_phase == 'day':
            print 'It was day.' #debug line
            self.db.light_phase = 'dusk'
            self.db.light_phase_hour = self.db.light_phase_lengths['dawn'] + \
                self.db.light_phase_lengths['day']
        elif self.db.light_phase == 'dusk':
            print 'It was dusk.' #debug line
            self.db.light_phase = 'night'
            self.db.light_phase_hour = self.db.light_phase_lengths['dawn'] + \
                self.db.light_phase_lengths['day'] + self.db.light_phase_lengths['dusk']
        elif self.db.light_phase == 'night':
            print 'It was night.' #debug line
            self.db.light_phase = 'dawn'
            self.db.light_phase_hour = 0
        else:
            print 'light phase is not a phase' #shouldn't reach


        if self.db.light_phase_lengths[self.db.light_phase] > 0: self.msg_contents(self.db.light_phase_echoes[self.db.light_phase])
        self.db.light_phase_time = self.db.light_phase_lengths[self.db.light_phase]
        print self.db.light_phase_time #debug line

        if self.db.light_phase_lengths == 0: advance_light_cycle(self)

    #Generate a description that includes the light cycle phase (if active)
    def return_appearance(self, looker):
        """
        This formats a description. It is the hook a 'look' command
        should call.

        Args:
            looker (Object): Object doing the looking.
        """
        if not looker:
            return
        # get and identify all objects
        visible = (con for con in self.contents if con != looker and
                                                    con.access(looker, "view"))
        exits, users, things = [], [], []
        for con in visible:
            key = con.key
            if con.destination:
                exits.append(key)
            elif con.has_player:
                users.append("{c%s{n" % key)
            else:
                things.append(key)
        # get description, build string
        string = "{c%s{n\n" % self.key
        desc = self.db.desc
        lightdesc = self.db.light_phase_descs[self.db.light_phase]

        if desc:
            string += "%s" % desc
        if self.db.light_cycle_active == True:
            string += "%s" % lightdesc #Light phase associated description
        if exits:
            string += "\n{wExits:{n " + ", ".join(exits)
        if users or things:
            string += "\n{wYou see:{n " + ", ".join(users + things)
        return string
