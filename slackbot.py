from slackclient import SlackClient
import random
import weather
import rail
import ccy
import mytoken


def run_function(inputstring):
    inputargs = str(inputstring).split(' ')

    if inputargs[0] == 'weather':
        output = weather.getData()
    elif inputargs[0] == 'rail' or inputargs[0] == 'train':
        output = rail.getJourney(inputargs[1], inputargs[2], inputargs[3])
    elif inputargs[0] == 'ccy':
        ccypair = inputargs[1].split('/')
        if len(inputargs) > 2:
            output = ccy.convertAmount(ccypair[0], ccypair[1], int(inputargs[2]))
        else:
            output = ccy.convertAmount(ccypair[0], ccypair[1])
    else:
        output = 'There was an error with' + inputstring
    return output


def get_last_user_message(varSlackClient, varChannel):
    # Returns a string of last human message to this channel.
    resMessage = varSlackClient.api_call('im.history', channel=varChannel)
    print(resMessage)
    resMess = resMessage['messages'][0]
    print(resMess)
    if resMess.get('bot_id') is None:
        # User is not a bot
        print(resMess['text'])
        return resMess['text']


def parse_text(varMessage):
    # Returns a string that should be sent to channel
    greetings = ['hello', 'hey', 'hi', 'hiya', 'bonjourno', 'howdy', 'howdy partner', 'yo']
    print(varMessage)
    if varMessage is None:
        # do nothing!
        print('do nothing here')
        return None
    elif varMessage[0] == '?':
        # do stuff!
        retString = run_function(varMessage.replace('?', ''))
        return retString

    elif varMessage.lower() in greetings:
        greetings.remove(varMessage.lower())
        print('responding nicely')
        return greetings[random.randrange(0, len(greetings))]

    else:
        # do nothing!
        print('Would do nothing here')
        return "Sorry I don't understand. Use ? to command me to do something."


def send_message(varSlackClient, varChannel, varMessage):
    if varMessage is None:
        print('sending null msg')
        # do nothing
    else:
        print(varSlackClient.api_call('chat.postMessage', as_user='true', channel=varChannel, text=varMessage))


if __name__ == "__main__":

    slacktoken = mytoken.getToken('slack')

    johnid = mytoken.getSlack('userid')
    johnchan = mytoken.getSlack('userchan')
    message = 'Yo, this is a test message'

    sc = SlackClient(slacktoken)
    # print(sc.api_call('api.test'))
    # print(sc.api_call('im.open', user=johnid))
    # print(sc.api_call('chat.postMessage', as_user='true', channel=johnchan, text=message))
    # print(sc.api_call('im.history', channel=johnchan))

    response = parse_text(get_last_user_message(sc, johnchan))
    send_message(sc, johnchan, response)

