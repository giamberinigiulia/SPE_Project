# SPE_Project

## Introduction

This project simulates a closed M/M/1 and M/M/k queuing system. The simulation includes the following features:
- **Closed M/M/1 System**: A single-server queue with a fixed number of clients cycling between being served and generating new requests.
- **Closed M/M/k System**: A multi-server queue with a fixed number of clients and multiple servers, where clients cycle between being served and generating new requests.

The project uses Flask to create a web server that handles client requests and manage multiple worker processes. Locust is used as a load generator to simulate client requests and measure the system's performance.


## Installation

### Cloning repository

Clone this repository locally and enter the cloned folder:

```bash
git clone https://github.com/giamberinigiulia/SPE_Project.git && cd SPE_Project
```


### Environment setup

- Windows:

```bash
$ python -m venv spe_env
$ spe_env\Scripts\activate 
```
- Linux:

```bash
$ python -m venv spe_env
$ source spe_env/bin/activate
```

### Installing dependency

```bash
$ pip install -r requirements.txt
```

## Execution

### Local mode

After cloning the repository and installing all necessarty dependencies, simply use the following command:

```bash
$ python main.py run -s <service_rate> -a <arrival_rate> -u <user_range_start> <user_range_end> -t <max_time> -k <number_of_servers>
```

### Docker

```bash
$ docker run --rm -v $(pwd)/data:/app/data spe python main.py run -s 10 -a 5 -u 1 2 -t 10 -k 2
```


### Example

Here is an example of how to run the application with a service rate of 10, an arrival rate of 5, a user range of 1 to 10, a maximum time of 60 seconds, and 4 servers:

```bash
$ python main.py run -s 10 -a 5 -u 1 10 -t 60 -k 4
```
