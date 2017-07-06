#add line to run on raspberry pi

#---Documentation---------------------------------------------------------------
#
#
#
#
#
#
#-------------------------------------------------------------------------------

import time
import RPi.GPIO as GPIO

class stepperController(object):

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

    def __init__(self,motorPinsArray, stepsPerRevolution, timeBetweenStep):    #<-- needs to be tested
        self.pins = motorPinsArray
        self.stepsInRevolution = stepsPerRevolution
        self.stepBreak = timeBetweenStep


        #add some checks for the values entered
        if(type(self.pins) != list):
            #send exception
            print('please enter list')

    #---end of def __init__-----------------------------------------------------

    #Function returns a bool, False if any arguments are not correct
    #and True once the stepper motor has completed spinning.
    def spinMotor(self, numRevolution, stepPhase="dual", stepType='full'):    #<-- needs to be tested
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
                #possibly change color to red to make more visible
            curSeq = self.singlePhaseStepping
        elif(stepType == 'half'):
            curSeq = self.dualPhaseStepping[1]
            steps = steps*2
        else:
            curSeq = self.dualPhaseStepping[0]

        #assign GPIO pins here
        if(GPIO.getmode != GPIO.BCM):
            GPIO.setmode(GPIO.BCM)
        for pin in self.pins:
            GPIO.setup(pin, GPIO.OUT, initial=GPIO.LOW)

        #make for loop to run through curSeq to make motor spin the correct amount of times
        #do not forget to add sleep
        phase = 0
        for x in range(int(round(steps*numRevolution))):
            for pin in range(4):
                GPIO.output(self.pins[pin], curSeq[phase][pin])
            time.sleep(self.stepBreak)
            phase += 1
            if(phase >= len(curSeq)):
                phase = 0

        for pin in self.pins:
            GPIO.output(pin,0)

        #end of turning phase

        GPIO.cleanup()
        return True
#---end of def spinMotor()------------------------------------------------------
