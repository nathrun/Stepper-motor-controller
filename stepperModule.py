#add line to run on raspberry pi

#Documentation
#
#
#
#
#
#
#--------------------------------------------------------

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

    def __init__(self,motorPinsArray, stepsPerRevolution):
        self.pins = motorPinsArray
        self.stepsInRevolution = stepsPerRevolution


        #add some checks for the values entered
        if(type(self.pins) != list):
            #send exception

    #Function returns a bool, False if any arguments are not correct
    #and True once the stepper motor has completed spinning.
    def spinMotor(numRevolution, stepPhase="dual", stepType='full'):
        if(stepPhase != 'dual' or stepPhase != 'single'):
            return False
            #should change to throw exception as well for more detail
        if(stepType != 'half' or stepType != 'full'):
            return False
            #should change to throw exception as well for more detail


        curSeq = []
        if(stepPhase == 'single'):
            if(stepType == 'half'):
                print('can not do half steps on single phase stepping. defualted to full steps')
                #possibly change color to red to make more visible
            curSeq = singlePhaseStepping
        elif(stepType == 'half'):
            curSeq = dualPhaseStepping[0]
        else:
            curSeq = dualPhaseStepping[1]

        #assign GPIO pins here

        #make for loop to run through curSeq to make motor spin the correct amount of times
        #do not forget to add sleep

        #GPIO.cleanup() <-- check if there is a way to just cleanup pins that were used for this script.
        #cleanup pins after each use of the stepperController to make sure that GPIO pins are never
        #left assigned. check if python has an OnDestroy, then this could be moved into there
