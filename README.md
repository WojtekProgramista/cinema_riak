# cinema_riak
Python console aplication using Riak distributed database system.

## Prerequisites

* [Docker](https://www.docker.com/)
* [Virtualenv](https://virtualenv.pypa.io/en/latest/)

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

```
docker-compose up -d coordinator
```
```
docker-compose scale member=4
```

To run Python script, we need to activate this application's Python virtual environment.

```
virtualenv venv --distribute
```
```
source venv/bin/activate
```

Finally, to run basic version of the application, use command below.
```
python main.py
```
