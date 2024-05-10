# OPEN_Controller
Open-Source controlling software for the OPEN Root Phenotyping System at the David Mendoza labs

## Description

This controlling software runs on a Raspberry Pi that is conencted to two Arduinos running independent drivers. The Raspberry Pi acts as the brain of the system for the user to interact with. It allows for setting up automated experiments and specific manual commands for operation of the OPEN root system. The software is written in Python using serial libraries and Tkinter. 

There are two Arduinos with the system. The first Arduino is the GRBL Arduino that operates the stepper motor system for moving the camera to specific locations. The second controls the lightning systems for the robot. The MCUs are designed to be independent of the controlling software and only communication via serial commands. Theoretically, each system is independent. 

## Requirements

The requirements for the project can be found in the `requirements.txt` file in the main directory. 

`pip install -r requirements.txt`

## Usage

To run the project, copy the repo into a directory of a Raspberry Pi (I recommend the user's desktop directory or system `opt/` directory).

Run the project using python : `python path\to\project\src\main.py` 

## License

This project is licensed under the GNU General Public License. More infomation can be found in `License.txt`.

## Authors
Principal Contributor: Landon Swartz

Contact at lgsm2n@umsystem for any questions.

## Proposed Improvements
There are a few improvements that I was never able to implement that I think would be very useful for future projects. Some tasks are simple and others complex, I will denote my intended difficulty with the task.
- Enable and disable the stepper motor through the enable/disable pin on the stepper driver to reduce stress on motors (EASY)
    - requires putting pin 8 on the GRBL arduino high or low 
- Remote communication with the robotics systems via a webpage or mobile app (HARD)
    - main obstacele would be university IT
- Unit testing and hardware-in-the-loop testing for controlling software and arduino drivers (EASY-ISH)