#---Documentation---------------------------------------------------------------
# This module was designed to run with a L298N h-bridge module. I created this
# in my spare time and did not test extensively so there might be bugs
# def __init__:
#   params  - motorPinsArray is an array that contains the GPIO pins that go to
#             these inputs -> [IN1,IN2,IN3,IN4]
#           - stepsPerRevolution is the amount of steps your stepper motor
#             requires to do a single revolution
#           - defaultRPM -> pretty obvious... can be either an integer or float
#
# def setDefaultRPM:
#   params  -defaultRPM -> new default rpm for object, can be either an
#            integer or float
#   will return True if operation happened successfully
#
# def spinMotor:
#   params  - numRevolution is a float that indicates exactly how many
#             revolution you would like the stepper motor to turn. If negative,
#             the motor will turn in the opposite direction.
#           - stepPhase (optional, default='dual'), refers to either 'single'
#             phase stepping or 'dual' phase stepping
#             (dual phase, both coils will always be engaged)
#           - stepType (optional, default='full'), can only be used of stepPhase
#             is equal to 'dual'.
#           - rpm (optional), if you want to set a temporary rpm,
#             either an integer or float
#-------------------------------------------------------------------------------

import time
import RPi.GPIO as GPIO

class stepperController(object):
    #array that rearanges the format of the pins to be used on an L298N h-bridge
    pinShuffle = [0,3,1,2]

    #dualPhaseStepping[0] for half stepping
    #dualPhaseStepping[1] for full stepping
    #can not do half stepping on singlePhaseStepping
    singlePhaseStepping = [
        [1,0,0,0],
        [0,1,0,0],
        [0,0,1,0],
        [0,0,0,1]
    ]
    dualPhaseStepping = [
        [
            [1,1,0,0],
            [0,1,1,0],
            [0,0,1,1],
            [1,0,0,1]
        ],
        [
            [1,0,0,0],
            [1,1,0,0],
            [0,1,0,0],
            [0,1,1,0],
            [0,0,1,0],
            [0,0,1,1],
            [0,0,0,1],
            [1,0,0,1]
        ]
    ]

    def __init__(self,motorPinsArray, stepsPerRevolution, defaultRPM):    #<-- needs to be tested
        self.pins = motorPinsArray
        self.stepsInRevolution = stepsPerRevolution
        self.d_RPM = defaultRPM

        #add some checks for the values entered
        if(type(self.pins) != list):
            #send exception
            print('please enter list')
        if (type(self.stepsInRevolution) != int):
            print('stepsPerRevolution must be an integer value')
        if (type(self.d_RPM) != int and type(self.d_RPM) != float):
            print('defaultRPM must be an integer value')
    #---end of def __init__-----------------------------------------------------

    #Function returns a bool, False if any arguments are not correct
    #and True once the stepper motor has completed spinning.
    def spinMotor(self, numRevolution, stepPhase="dual", stepType='full', rpm=0):    #<-- needs to be tested
        if(stepPhase != 'dual' and stepPhase != 'single'):
            return 'stepPhase must equal "single" or "dual"'
            #should change to throw exception as well for more detail
        if(stepType != 'half' and stepType != 'full'):
            return 'stepType must equal "half" or "full"'
            #should change to throw exception as well for more detail

        curSeq = []
        steps = self.stepsInRevolution
        if(stepPhase == 'single'):
            if(stepType == 'half'):
                print('can not do half steps on single phase stepping. defualted to full steps')
            curSeq = self.singlePhaseStepping
        elif(stepType == 'half'):
            curSeq = self.dualPhaseStepping[1]
            steps = steps*2
        else:
            curSeq = self.dualPhaseStepping[0]

        if (rpm==0):
            stepBreak = 1.0/(steps*self.d_RPM)
        else:
            stepBreak = 1.0/(steps*rpm)

        #if rpm < 0, reverse curSeq and change rpm to possitive
        if (rpm < 0):
            curSeq.reverse()
            rpm *= -1
            print 'DEBUG curSeq'
            print curSeq
            print 'DEBUG end'

        if (numRevolution ==0):
            return True #skip irrelavant setup and gpio.cleanup

        #assign GPIO pins here
        if(GPIO.getmode != GPIO.BCM):
            GPIO.setmode(GPIO.BCM)
        for pin in self.pins:
            GPIO.setup(pin, GPIO.OUT, initial=GPIO.LOW)

        #make for loop to run through curSeq to make motor spin the correct amount of times
        phase = 0
        for x in range(int(round(steps*numRevolution))):
            for pin in range(4):
                GPIO.output(self.pins[self.pinShuffle[pin]], curSeq[phase][pin])
            time.sleep(stepBreak)
            phase += 1
            if(phase >= len(curSeq)):
                phase = 0
        #end of turning phase
        #set pins to LOW
        for pin in self.pins:
            GPIO.output(pin,0)

        GPIO.cleanup()
        return True
    #---end of def spinMotor()------------------------------------------------------

    def setDefaultRPM(self, defaultRPM):
        result = True if(type(defaultRPM)==int or type(defaultRPM)== float) else 'defaultRPM must be an integer or a float'
        if result==True:
            self.d_RPM = defaultRPM
        return result
