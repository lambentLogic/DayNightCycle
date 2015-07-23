"""
Room

Rooms are simple containers that has no location of their own.

"""

from evennia import DefaultRoom
import lightcycle

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
        """
        Called when the object is first created.
        """

        lightcycle.set_default_cycle(self)


    def at_hour(self, *args, **kwargs):
        """
        Ticked at regular (hourly) intervals.
        """

        lightcycle.at_cycle_hour(self)


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
