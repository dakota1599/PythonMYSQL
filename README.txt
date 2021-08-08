Dakota Shapiro
CS 4430
8/7/2021

This project was written in python using the mysql.connector pip package.
Python does not have a native driver for communication with SQL servers.
Mysql.connector was created by mysql.com as a driver for Python.

[INSTRUCTIONS] - Linux/Ubuntu
1. To get started, you first need to ensure that you have all your packages up to date.
Do that by running 'sudo apt update' in your console window.

2. Install pip if you do not already have it: 'sudo apt install python3-pip'.

3. Install mysql.connector with pip: 'sudo pip install mysql-connector-python'

4. Now you should be free to run the program.  You run the program by navigating
to its directory and running 'python3 ./main.py'.  The program will then begin and prompt
for connection credentials for your SQL server.

[INSTRUCTIONS] - Windows
1. To get started, ensure you have python installed on your device.  Python should come with pip, but
if you are not sure, you can run the following command: 'py -m ensurepip --upgrade' within your command window.

2. Install mysql.connector with pip: 'pip install mysql-connector-python'

3. Now you should be free to run the program.  You run the program by navigating
to its directory and running './main.py' or 'py ./main.py'.  The program will then begin and prompt
for connection credentials for your SQL server.