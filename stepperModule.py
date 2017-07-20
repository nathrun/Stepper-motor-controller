#---Documentation---------------------------------------------------------------
# This module was designed to run with a L298N h-bridge module. I created this
# in my spare time and did not test extensively so there might be bugs
# def __init__:
#   params  - motorPinsArray is an array that contains the GPIO pins that go to
#             these inputs -> [IN1,IN2,IN3,IN4]
#           - stepsPerRevolution is the amount of steps your stepper motor
#             requires to do a single revolution
#           - defaultRPM -> pretty obvious...
#
#   Will return False if any paramater is not correct
#
#
#
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
            return False
        else:
            return True
    #---end of def __init__-----------------------------------------------------

    #Function returns a bool, False if any arguments are not correct
    #and True once the stepper motor has completed spinning.
    def spinMotor(self, numRevolution, stepPhase="dual", stepType='full', rpm=0):    #<-- needs to be tested
        if(stepPhase != 'dual' and stepPhase != 'single'):
            return 'fail 1'
            #should change to throw exception as well for more detail
        if(stepType != 'half' and stepType != 'full'):
            return 'fail 2'
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

        print stepBreak

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
        self.d_RPM = defaultRPM
        return True
