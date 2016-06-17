messagesDict = {
    "greetings": chr(27) + "[2J" + "\n" + "TORTOISE alive! Press the pause/resume button to set me going.",
    "running": "[TORTOISE RUNNING]",
    "calibration_ambient": "Press enter to take a reading at normal light levels.",
    "calibration_light_source": "Now please place a light source in front of the light sensor and press enter.",
    "calibration_complete": "Calibration complete!",
    "bad_touch_sensor": "You've asked for a touch sensor that doesn't exist.\tHINT: check the position of the sensor you want to set."
}

def printMessage(code):
    print messagesDict[code]
