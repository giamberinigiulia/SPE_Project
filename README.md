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
$ python app.py mu
```

#### Endpoints
- API for being served from the server with rate mu
```
url: http://127.0.0.1:5000/
```
- API for choosing which plot to show (with _mu_'s rate that were already used)
```
url: http://127.0.0.1:5000/plot
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

