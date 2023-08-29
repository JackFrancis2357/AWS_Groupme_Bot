import datetime
import numpy as np
from pytz import timezone
from configs import Config


def get_teams():
    # TODO: Refactor this to at least be a dict of lists so we aren't hard-coding so much
    teams = {
        "Jack": Config["Jack"],
        "Jordan": Config["Jordan"],
        "Nathan": Config["Nathan"],
        "Patrick": Config["Patrick"]
    }

    all_teams = []
    for lst in teams.values():
        all_teams += [val for val in lst]
    teams["all"] = all_teams

    return teams
    
def get_current_week():
    tz = timezone('EST')
    nfl_season_start = datetime.datetime.strptime(Config["nfl_season_start_date"], '%m/%d/%Y')
    cur_date = datetime.datetime.now(tz).replace(tzinfo=None)
    delta = cur_date - nfl_season_start
    return max(1, int(np.floor(delta.days / 7) + 1))