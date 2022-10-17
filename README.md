# cinema_riak
Python console aplication using Riak distributed database system.

## Prerequisites

* [Docker](https://www.docker.com/)
* [Python + pip](https://pypi.org/project/pip/)

Application was created and tested on Linux (Ubuntu 20.04), commands below are meant to be run in Linux terminal.

# Set up
Start by cloning and entering this repository.

```
git clone https://github.com/WojtekProgramista/cinema_riak
```
```
cd cinema_riak
```

Next run cluster of Riak nodes using blueprint in ```docker-compose.yaml``` file.
(might require sudo privileges)

```
docker-compose up -d coordinator
```
```
docker-compose scale member=4
```

To run Python script, we need to get required Python libraries. We will use Python virtual environment.
```
python -m pip install virtualenv
```
```
virtualenv --python=python2.7 venv
```
```
source venv/bin/activate
```
```
pip install -r requirements.txt
```

Finally, to run basic version of the application, use command below.
```
python main.py
```
