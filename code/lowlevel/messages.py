messagesDict = {
    'greetings': chr(27) + '[2J' + '\n' + 'Tortoise alive! Press the pause/resume button to set me going.',
    'running': '[TORTOISE RUNNING]'
}

def printMessage(code):
    print messagesDict[code]
