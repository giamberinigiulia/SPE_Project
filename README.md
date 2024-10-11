# SPE_Project

## Installation

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

### Launching application
```bash
$ python app.py
```

#### Endpoints
- API for being served from the server with rate _mu_
```
url: http://127.0.0.1:5000/mu
```
- API for choosing which plot to show (with _mu_'s rate that were already used)
```
url: http://127.0.0.1:5000/plot
```
- API for plotting a graph of the exponential distribution expected as mu_ and the one evaluated by the mean of time delays
```
url: http:127.0.0.1:5000/plot/mu
```
- API for showing all the time delays saved in the .csv file
```
url: http:127.0.0.1:5000/csv
```
- API for removing the .csv file
```
url: http:127.0.0.1:5000/reset
```
## State-Spaces

![alt text](/utils/State-Space.jpg)

