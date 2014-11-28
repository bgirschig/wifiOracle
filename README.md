#Oracle Controller

###How to run:
This program should be run on a raspberry pi, connected to the oracle wheel (circuit decribed [here](https://upverter.com/bastien.girschig@gmail.com/46dc96200ea85d84/wifiCrakcer/), object images below), containing a stepper motor, an easyDriver, an LED, and a switch).
No Build required: simply push the "oracleController.py" file on the raspberry pi, then run it:
```
sudo python ~/oracleController.py
```

###Calibration
You will be asked to calibrate the wheel:
```
calibrate ('h' for help): 
```
Using the letters `q`,`Q`,`w`,`W`, rotate it so that it shows the 'PW' character.
Lowercase is for 1 step at a time,capital for 10.
`q` rotates anticlockwise, `w` is for clockwise
you can also type in the number of steps you want to rotate, or turn the wheel manually with the switch on the 'off' position.

When the wheel is in the right position, hit return with nothing written. this will send you to the next step

###Record sequence
You will then be asked if you want to record a new sequence (this is for the demo mode)
```
record new sequence? (y/n)
```
if you want to, type `y` then use the same commands as before. return key with nothing will save the current position and continue on the next one.
when you are done, type `e` to exit the record mode

The sequence will then be played in loops indefinitely

###Object
A wheel with all ASCII characters engraved on it, that rotates to show characters one by one:
![object](object.jpg)
![detail](detail.jpg)

###Credits
Project made by Martin Hertig and Bastien Girschig.
Made during the Botcave workshop at ECAL with Matthew plummer-fernandez. More info about the workshop [here](http://www.iiclouds.org/20141118/iic-workshop-at-ecal-the-birth-of-botcaves/).