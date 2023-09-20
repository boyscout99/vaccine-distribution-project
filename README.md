# Modelling Vaccine Distribution in Finland with PostgreSQL database
Authors:  Bin Choi, Karina Mina, Phuong Hoang, Tommaso Praturlon

In this group project, we modelled a vaccine distribution system in Finland with the use of a relational database implemented in PostgreSQL. We used Python to connect to the database with SQLAlchemy, manipulate dataframes with pandas and queried the database to obtain information.

## How to work with virtual environment
**MacOS/Linux - Method 1**
```
sudo apt-get install python3-venv           # Note: this cannot be used in Aalto VM due to the lack of sudo right. 
cd project-vaccine-distribution             # Move to the project root folder
python3 -m venv venv                        # Create a virtual environment 
source venv/bin/activate                    # Activate the virtual environment
(venv) $                                    # You see the name of the virtual environment in the parenthesis.
```

**MacOS/Linux - Method 2**
```
python3 -m pip install --user virtualenv    # You can use virtualenv instead, if you are using Aalto VM.
cd project-vaccine-distribution             # Move to the project root folder
virtualenv venv                             # Create a virtual environment 
source venv/bin/activate                    # Activate the virtual environment
(venv) $                                    # You see the name of the virtual environment in the parenthesis.

```
**Windows**

You can install and create a virtual environment similar to the above. However, it should be noted that you activate the environment differently, as shown below. 
```
venv\Scripts\Activate.ps1
```
**Deactivate**  

You can deactivate the virtual environment with this command.
```
deactivate
```
    
### Connecting to the database server

In order to connect to the course PostgreSQL server, you must be inside the Aalto's network. You can choose either one of these options:

1. Establishing a remote connection (VPN) to an Aalto network. Instruction for installing the client software and establishing a connection is be found [here](https://www.aalto.fi/en/services/establishing-a-remote-connection-vpn-to-an-aalto-network?check_logged_in=1#6-remote-connection-to-students--and-employees--own-devices). This option allows you to use your own device. 

2. Connect to an Aalto Virtual Desktop Infrastructure (vdi.aalto.fi). Instruction for using vdi can be found [here](https://www.aalto.fi/en/services/vdiaaltofi-how-to-use-aalto-virtual-desktop-infrastructure). You can choose your prefer operating system. Please note that you don't have the ```sudo``` right for these machines (e.g. you can't install a software). Therefore, this option is less preferred. 

Once you are inside an Aalto's network (either though VPN or vdi) and have cloned the project to (either to your machine or an Aalto virtual machine), you will need to ```activate``` the virtual environment [see here](#how-to-work-with-virtual-environment), and install the required library (e.g. from the project root folder, run ```pip install -r ./code/requirements.txt```)

Finally, you can test the connection with the test_db by running ```python ./code/test_postgresql_conn.py``` from the project root folder. For your group database, we will share the "database" name, "user" and "password" information when Project Part 2 opens. 

