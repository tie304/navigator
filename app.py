"""

_______              .__              __
 \      \ _____ ___  _|__| _________ _/  |_  ___________
 /   |   \\__  \\  \/ /  |/ ___\__  \\   __\/  _ \_  __ \
/    |    \/ __ \\   /|  / /_/  > __ \|  | (  <_> )  | \/
\____|__  (____  /\_/ |__\___  (____  /__|  \____/|__|
        \/     \/       /_____/     \/


"""

from models.navigator import Navigator
from database.database import Database

Database().initialize()


Navigator()
