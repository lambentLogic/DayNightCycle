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
        self.db.lightCycleActive = False #whether phase is active

        self.db.lightPhaseLengths = {'dawn':2, 'day':10, 'dusk':2, 'night':10} #phase duration

        self.db.lightPhaseEchoes = {
        'dawn':'The sun rises.', 'day':'The day brightens.', 'dusk':'The sun descends.', 'night':'The light fades.'
        } #phase change echoes

        self.db.lightPhaseDescs = {
        'dawn':'\n{YRosy-fingered dawn caresses the land.', 'day':'\n{wThe sun shines brightly.',
         'dusk':'\n{RThe sky shines in the hues of twilight.', 'night':'\n{cStars sprinkle the dark sky.'
        } #phase room descriptions

        self.db.lightPhase = 'dawn' #current phase
        self.db.lightPhaseTime = 2 #time left


    def at_hour(self, *args, **kwargs):
        "Ticked at regular (hourly) intervals." #Set to minute for testing purposes
        print 'Tick, tock' #debug line
        if self.db.lightCycleActive == True:
            print 'cycle tick, tock' #debug line
            self.db.lightPhaseTime -= 1
            if self.db.lightPhaseTime <= 0: self.advance_light_cycle()


    def advance_light_cycle(self):
        "Called on to advance the room's light cycle by one phase."
        print "Cycle advanced" #debug line
        if self.db.lightPhase == 'dawn':
            print 'It was dawn.' #debug line
            self.db.lightPhase = 'day'
        elif self.db.lightPhase == 'day':
            print 'It was day.' #debug line
            self.db.lightPhase = 'dusk'
        elif self.db.lightPhase == 'dusk':
            print 'It was dusk.' #debug line
            self.db.lightPhase = 'night'
        elif self.db.lightPhase == 'night':
            print 'It was night.' #debug line
            self.db.lightPhase = 'dawn'
        else:
            print 'light phase is not a phase' #shouldn't reach


        self.msg_contents(self.db.lightPhaseEchoes[self.db.lightPhase])
        self.db.lightPhaseTime = self.db.lightPhaseLengths[self.db.lightPhase]
        print self.db.lightPhaseTime #debug line

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
        lightdesc = self.db.lightPhaseDescs[self.db.lightPhase]

        if desc:
            string += "%s" % desc
        if self.db.lightCycleActive == True:
            string += "%s" % lightdesc #Light phase associated description
        if exits:
            string += "\n{wExits:{n " + ", ".join(exits)
        if users or things:
            string += "\n{wYou see:{n " + ", ".join(users + things)
        return string
