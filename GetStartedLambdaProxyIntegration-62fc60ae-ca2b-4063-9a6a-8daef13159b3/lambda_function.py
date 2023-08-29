import json
import logging
import os
import pandas
from helpers import get_users
from groupme_bot_functions import return_contestant, send_message, get_standings_message, get_standings, get_schedule
from configs import Config
from app_helper_functions import get_teams, get_current_week



def lambda_handler(request, context):
    # data = request.get_json()
    # data = json.loads(request['body'])
    data = request
    current_user = data['user_id']
    groupme_users = get_users()
    
    current_message = data['text'].lower().strip()
    split_current_message = current_message.split()
    
    if current_user == os.getenv('GROUPME_BOT_ID'):
        return

    # current message to be parsed
    current_message = data['text'].lower().strip()
    split_current_message = current_message.split()
    
    if current_user == '17900487':
        if "bama" in current_message or "alabama" in current_message:
            if "cfp" in current_message or "playoff" in current_message:
                message = 'My Grandfather smoked his whole life. I was about 10 years old when my mother said to him, If you ever want to see your grandchildren graduate, you have to stop immediately. Tears welled up in his eyes when he realized what exactly was at stake. He gave it up immediately. Three years later he died of lung cancer. It was really sad and destroyed me. My mother said to me- Dont ever smoke. Please dont put your family through what your Grandfather put us through." I agreed. At 28, I have never touched a cigarette. I must say, I feel a very slight sense of regret for never having done it, because your take that Alabama should have made the CFP gave me cancer anyway.'
                return send_message(message)
        if ("miller" in current_message or "brandon" in current_message) and "gun" in current_message:
            message = "This is ChatGPT from the future just letting you know that Nate's take on Brandon Miller has not aged well and is very problematic."
            return send_message(message)

    if current_message in Config['Responses']:
        standings = get_standings()

        # If message is 'standings', print Jack, Jordan, Nathan, Patrick records
        if current_message == 'standings':
            logging.info(f"Forming standings message with standings: {standings}")
            message = get_standings_message(standings)
            return send_message(message)

        elif current_message == 'standings right now':
            message = get_standings_message(standings)
            return send_message(message.upper())

        # Message options - either all teams, a player's teams, or print help

        elif len(split_current_message) == 2 and split_current_message[-1] == 'teams':
            name = current_message.split()[0].capitalize()
            if name in ['Jack', 'Jordan', 'Patrick', 'Nathan', 'All']:
                return_contestant(name, standings)
            elif name == 'My':
                user = next(item for item in groupme_users if item["user_id"] == current_user)['name'].split()[0]
                return_contestant(user, standings)
        elif current_message == 'nfl bot help':
            options = Config['Responses']
            header = "Input options for the NFL Wins Tracker bot:\n"
            message = header + "\n".join(options)
            return send_message(message)

    elif current_message[:4].lower() == '!who':
        # I think this can be teams_list = [get_teams()] but will test later
        teams = get_teams()
        teams_list = [teams["Jack"], teams["Jordan"], teams["Nathan"], teams["Patrick"]]
        names = ['Jack', 'Jordan', 'Nathan', 'Patrick']
        team_id = current_message[6:]
        for owner in range(4):
            if team_id in teams_list[owner]:
                return send_message(names[owner])
            else:
                for team in teams_list[owner]:
                    if team_id in team:
                        return send_message(names[owner])
    # elif current_message == 'weblink':
    #     host = Config["test_url"] if Config["ENVIRONMENT"] == "TEST" else Config["prod_url"]
    #     return send_message(host)

    elif split_current_message[0] == 'schedule':
        if len(split_current_message) == 1:
            return ''
        else:
            team_id = split_current_message[1].capitalize()
            starting_week = get_current_week()
            try:
                if split_current_message[0] == 'schedule' and split_current_message[2] == 'next' and \
                        split_current_message[3].isdigit():
                    finishing_week = starting_week + int(split_current_message[3])
            except IndexError:
                finishing_week = 19
            get_schedule(team_id, starting_week, finishing_week=finishing_week)
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
    

