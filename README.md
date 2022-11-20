# Vaccine Distribution Project with PostgreSQL database
Authors:  Bin Choi, Karina Mina, Phuong Hoang, Tommaso Praturlon
## How to work with git

Here's a list of recommended next steps to make it easy for you to get started with the project. However, understanding the concept of git workflow and git fork is necessary and essential. 

-   [Create a fork of this official repository](https://docs.gitlab.com/ee/user/project/repository/forking_workflow.html#creating-a-fork)
-   [Add a SSH key to your gitlab account](https://docs.gitlab.com/ee/user/ssh.html#add-an-ssh-key-to-your-gitlab-account)
-   Clone the fork to your local repository
```
git clone git@version.aalto.fi<your-teammate-name>/<project-repo-name>.git
```
-   [Add a remote to keep your fork synced with the official repository](https://docs.gitlab.com/ee/user/project/repository/forking_workflow.html#repository-mirroring)
```
git remote add upstream git@version.aalto.fi:cs-a1153_databases_projects/project-vaccine-distribution.git
git pull upstream main                                  # if the official repository is updated you must pull the upstream
git push origin main                                    # Update your public repository
```

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

## File structure
This section explains the recommended file structure for the project

    .project-vaccine-distribution
    ├── code                              # code base (python & sql files)
    │   ├── requirements.txt              # IMPORTANT: see NOTES below
    │   ├── test_postgresql_conn.py       # Example code to test connection with postgres server
    │   ├── ....py                        # python file for part III
    ├── data                              # contain the sample data for Vaccine Distribution projects
    │   ├── sampleData.xls                # sample data as an excel file
    ├── database                          # IMPORTANT: see NOTES below
    │   ├── database.db                   # final version of the project database
    ├── venv                              # path to venv should be added to .gitignore
    │   ├── bin
    │   │   ├── activate
    │   │   ├── ....
    │   ├── ....
    ├── .gitignore
    └── README.md

1. **requirements.txt**

    In order to keep track of Python modules and packages required by your project, we provided a ```requirements.txt``` file with some starter packages required for data preprocessing. After activating the virtual environment, you can install these packages by running ```pip install -r ./code/requirements.txt```. Please add additional packages that you install for the project to this file. 

2. PostgreSQL
    
### Connecting to the database server

In order to connect to the course PostgreSQL server, you must be inside the Aalto's network. You can choose either one of these options:

1. Establishing a remote connection (VPN) to an Aalto network. Instruction for installing the client software and establishing a connection is be found [here](https://www.aalto.fi/en/services/establishing-a-remote-connection-vpn-to-an-aalto-network?check_logged_in=1#6-remote-connection-to-students--and-employees--own-devices). This option allows you to use your own device. 

2. Connect to an Aalto Virtual Desktop Infrastructure (vdi.aalto.fi). Instruction for using vdi can be found [here](https://www.aalto.fi/en/services/vdiaaltofi-how-to-use-aalto-virtual-desktop-infrastructure). You can choose your prefer operating system. Please note that you don't have the ```sudo``` right for these machines (e.g. you can't install a software). Therefore, this option is less preferred. 

Once you are inside an Aalto's network (either though VPN or vdi) and have cloned the project to (either to your machine or an Aalto virtual machine), you will need to ```activate``` the virtual environment [see here](#how-to-work-with-virtual-environment), and install the required library (e.g. from the project root folder, run ```pip install -r ./code/requirements.txt```)

Finally, you can test the connection with the test_db by running ```python ./code/test_postgresql_conn.py``` from the project root folder. For your group database, we will share the "database" name, "user" and "password" information when Project Part 2 opens. 

