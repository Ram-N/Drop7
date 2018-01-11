#Runtime Paramaters

_SIZE = 7
_FRACTION = (0.5, 0.7)
HORIZ, VERT = 0, 1
_printfreq = 30
_BALLS_TO_LEVELUP = 20
_outfile = "gamestats.txt"


# The canonical way to share information across modules within a single program 
# is to create a special module (often called config or cfg). Just import the 
# config module in all modules of your application; the module then becomes 
# available as a global name. Because there is only one instance of each module, 
# any changes made to the module object get reflected everywhere.