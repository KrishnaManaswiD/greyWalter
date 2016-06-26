messagesDict = {
    "greetings": chr(27) + "[2J" + "\n" + "Tortoise alive! Press the pause/resume button to set me going.",
    "running": "[TORTOISE RUNNING]",
    "paused": "[TORTOISE PAUSED]",
    "resumed": "[TORTOISE RESUMED]",    
    "calibration_ambient": "Press enter to take a reading at normal light levels.",
    "calibration_light_source": "Now please place a light source in front of the light sensor and press enter.",
    "calibration_complete": "Calibration complete!",
    "bad_touch_sensor": "You've asked for a touch sensor that doesn't exist.\n\tHINT: check the position of the sensor you want to set.",
    "bad_light_sensor": "I only have one light sensor.\n\tHINT: check the position of the sensor you want to set.",
    "bad_proximity_sensor": "You've asked for a proximity sensor that doesn't exist.\n\tHINT: check the position of the sensor you want to set.",
    "bad_emergency_sensor": "You've asked for a emergency stop that doesn't exist.\n\tHINT: check the position of the sensor you want to set.",
    "bad_sensor": "You've asked for a sensor that doesn't exist.\n\tHINT: check the type of the sensor you want to read.",
    "no_calibration": "The light sensor hasn't been calibrated properly. Try calibrating again.",
    "bad_LED": "You've asked for an LED that doesn't exist.\n\tHINT: check the position of the LED you want to set.",
    "bad_LED_value": "In binary code, we only have 0s and 1s.\n\tHINT: check the value you want to set (0 = OFF, 1 = ON).",
    "blinks_negative": "I can't blink a negative number of times!\n\tHINT: check the number of blinks.",
    "blinks_zero": "Do you want me to blink or not?\n\tHINT: check the number of blinks.",
    "blinking_fast": "I can't blink that fast.\n\tHINT: check the delay.",
    "bad_direction": "I can only move backwards or forwards, and either left or right.\n\tHINT: check the direction.",
    "bad_direction_turn": "I can only turn backwards or forwards, and either left or right.\n\tHINT: check the direction.",
    "bad_shuffle": "I can only shuffle clockwise or counter clockwise.\n\tHINT: check the direction.",
    "bad_steps": "I can't move a negative number of steps!\n\tHINT: check the number of steps.",
    "bad_delay": "I can't move my motors faster than 2 ms.\n\tHINT: check the delay.",
    "bad_turn": "I won't turn the way you want.\n\tHINT: check the direction and number of steps."
}

def printMessage(code):
    print messagesDict[code]
