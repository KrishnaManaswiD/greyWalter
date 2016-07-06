import RPi.GPIO as GPIO
import time
import enums

GPIO.setmode(GPIO.BCM)


class Sensors:
    """Class Sensors. Explanation:"""

    def __init__(self):
        """returns (arg1 / arg2) + arg3

        This is a longer explanation, which may include math with latex syntax
        :math:`\\alpha`.
        Then, you need to provide optional subsection in this order (just to be
        consistent and have a uniform documentation. Nothing prevent you to
        switch the order):

          - parameters using ``:param <name>: <description>``
          - type of the parameters ``:type <name>: <description>``
          - returns using ``:returns: <description>``
          - examples (doctest)
          - seealso using ``.. seealso:: text``
          - notes using ``.. note:: text``
          - warning using ``.. warning:: text``
          - todo ``.. todo:: text``

        **Advantages**:
         - Uses sphinx markups, which will certainly be improved in future
           version
         - Nice HTML output with the See Also, Note, Warnings directives


        **Drawbacks**:
         - Just looking at the docstring, the parameter, type and  return
           sections do not appear nicely

        :param arg1: the first value
        :param arg2: the first value
        :param arg3: the first value
        :type arg1: int, float,...
        :type arg2: int, float,...
        :type arg3: int, float,...
        :returns: arg1/arg2 +arg3
        :rtype: int, float

        :Example:

        >>> import template
        >>> a = template.MainClass1()
        >>> a.function1(1,1,1)
        2

        .. note:: can be useful to emphasize
            important feature
        .. seealso:: :class:`MainClass2`
        .. warning:: arg2 must be non-zero.
        """

        self.dictionaryPinsToPositions = {}

        self.lightSensor_pin = [-1,-1]
        self.touchSensor_pin = [-1,-1,-1,-1] # e-stop also here
        self.proximitySensor_pin = [-1,-1,-1,-1]

        self.light_value = [-1,-1]
        self.touch_timesPressed = [0,0,0,0]
        self.proximity_state = [-1,-1,-1,-1]



    #if everything OK, return 0. If sensor type unknown or position > limit, return -1
    def setSensor(self, sensor_type, pos, pin):
        """returns (arg1 / arg2) + arg3

        This is a longer explanation, which may include math with latex syntax
        :math:`\\alpha`.
        Then, you need to provide optional subsection in this order (just to be
        consistent and have a uniform documentation. Nothing prevent you to
        switch the order):

          - parameters using ``:param <name>: <description>``
          - type of the parameters ``:type <name>: <description>``
          - returns using ``:returns: <description>``
          - examples (doctest)
          - seealso using ``.. seealso:: text``
          - notes using ``.. note:: text``
          - warning using ``.. warning:: text``
          - todo ``.. todo:: text``

        **Advantages**:
         - Uses sphinx markups, which will certainly be improved in future
           version
         - Nice HTML output with the See Also, Note, Warnings directives


        **Drawbacks**:
         - Just looking at the docstring, the parameter, type and  return
           sections do not appear nicely

        :param arg1: the first value
        :param arg2: the first value
        :param arg3: the first value
        :type arg1: int, float,...
        :type arg2: int, float,...
        :type arg3: int, float,...
        :returns: arg1/arg2 +arg3
        :rtype: int, float

        :Example:

        >>> import template
        >>> a = template.MainClass1()
        >>> a.function1(1,1,1)
        2

        .. note:: can be useful to emphasize
            important feature
        .. seealso:: :class:`MainClass2`
        .. warning:: arg2 must be non-zero.
        """

        idx = pos - 1

        if sensor_type == enums.SensorType.touch or sensor_type == enums.SensorType.emergencyStop:

            if pos <= len(self.touchSensor_pin) and pos > 0:

                self.touchSensor_pin[idx] = pin
                self.dictionaryPinsToPositions[str(pin)] = pos
                GPIO.setup(pin, GPIO.IN, pull_up_down = GPIO.PUD_UP)
                GPIO.add_event_detect(pin, GPIO.FALLING, callback = self.callback_touch, bouncetime = 300)
                return 0

            else:
                raise RuntimeError('Touch sensor can only be assigned to position 1-' + str(len(self.touchSensor_pin)))
                return -1


        elif sensor_type == enums.SensorType.light:

            if pos <= len(self.lightSensor_pin) and pos > 0:

                self.lightSensor_pin[idx] = pin
                self.dictionaryPinsToPositions[str(pin)] = pos
                GPIO.setup(pin, GPIO.OUT)
                return 0

            else:
                raise RuntimeError('Light sensor can only be assigned to position 1-' + str(len(self.lightSensor_pin)))
                return -1


        elif sensor_type == enums.SensorType.proximity:

            if pos <= len(self.proximitySensor_pin) and pos > 0:

                self.proximitySensor_pin[idx] = pin
                self.dictionaryPinsToPositions[str(pin)] = pos

                GPIO.setup(pin, GPIO.IN, pull_up_down = GPIO.PUD_UP)

                if GPIO.input(pin) == GPIO.HIGH:
                    self.proximity_state[idx] = 0
                else:
                    self.proximity_state[idx] = 1

                GPIO.add_event_detect(pin, GPIO.BOTH, callback = self.callback_proximity, bouncetime = 100)
                return 0

            else:
                raise RuntimeError('Proximity sensor can only be assigned to position 1-' + str(len(self.proximitySensor_pin)))
                return -1


        else:
            raise RuntimeError('Unknown sensor type!')
            return -1



    def callback_touch(self, channel):

        try:
    
            idx = self.dictionaryPinsToPositions[str(channel)] - 1
            self.touch_timesPressed[idx] = self.touch_timesPressed[idx] + 1

        except KeyError:
            raise RuntimeError('Bad channel in callback_touch: ' + str(channel))
            return -1



    def callback_proximity(self,channel):

        time.sleep(0.1)

        try:
    
            idx = self.dictionaryPinsToPositions[str(channel)] - 1


            if GPIO.input(channel) == GPIO.HIGH:
                self.proximity_state[idx] = 0
            else:
                self.proximity_state[idx] = 1

        except KeyError:
            raise RuntimeError('Bad channel in callback_proximity: ' + str(channel))
            return -1



    #if everything OK, return sensor value. If sensor type unknown or position > limit, return -1
    def readSensor(self,sensor_type,pos):

        idx = pos - 1

        if sensor_type == enums.SensorType.touch or sensor_type == enums.SensorType.emergencyStop:

            if pos <= len(self.touchSensor_pin) and pos > 0:

                if(self.touchSensor_pin[idx] == -1) :
                    raise RuntimeError('Pin for touch sensor in position ' + str(pos) + ' is not assigned')
                    return -1

                else:

                    return self.touch_timesPressed[idx]

            else:
                raise RuntimeError('Touch sensor can only be assigned to position 1-' + str(len(self.touchSensor_pin)))
                return -1


        elif sensor_type == enums.SensorType.light:

            if pos <= len(self.lightSensor_pin) and pos > 0:

                if(self.lightSensor_pin[idx] == -1):
                    raise RuntimeError('Pin for light sensor in position ' + str(pos) + ' is not assigned')
                    return -1

                else:

                    return self.read_light(self.lightSensor_pin[idx])

            else:
                raise RuntimeError('Light sensor can only be assigned to position 1-' + str(len(self.lightSensor_pin)))
                return -1

        elif sensor_type == enums. SensorType.proximity:

            if pos <= len(self.proximitySensor_pin) and pos > 0:

                if(self.proximitySensor_pin[idx] == -1):
                    raise RuntimeError('Pin for proximity sensor in position ' + str(pos) + ' is not assigned')
                    return -1

                else:

                    return self.proximity_state[idx]

            else:
                raise RuntimeError('Proximity sensor can only be assigned to position 1-' + str(len(self.proximitySensor_pin)))
                return -1

        else:
            raise RuntimeError('Unknown sensor type!')
            return -1



    def read_light(self,lspin):

        reading = 0

        GPIO.setup(lspin, GPIO.OUT)
        GPIO.output(lspin, GPIO.LOW)

        time.sleep(0.1)

        GPIO.setup(lspin, GPIO.IN)

        # This takes about 1 millisecond per loop cycle
        while (GPIO.input(lspin) == GPIO.LOW):
            reading += 1

        return reading

