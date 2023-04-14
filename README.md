# AISystance
Mission Junior Entreprise : PEP x Systra

## What's next ? :grey_question:
- Even if the login page is finished, I still have to do the authentication system
- I haven't made the KNN algorithm but it's not a challenge yet
- I have to make a nav bar to clean the design of the pages

## Installation :construction_worker:

### Installation with pip

Make sure you have Python>=3.10.9.

```
pip install -r requirements.txt
```

### Installation with Anaconda

```
conda env create -f environment.yml
conda activate PEP
```

## Purposes :rocket:

There are several main usages you may be interested in:

1. Make predictions
2. Fetch the nearest neighbors 
3. Modify the database and fit the model

## How to use :man_technologist:

```
python -m app
open http://127.0.0.1/5000
```
### Homepage
![Login page](demo/home.png)

### Prediction page
![Prediction_page](demo/index.png)

### Database page
![Database_page](demo/database.png)

## Debug :bug:

1. If you see error :  
```
* Serving Flask app 'app'
* Debug mode: on
Address already in use
Port 5000 is in use by another program. Either identify and stop that program, or start the server with a different port.
```

You should launch the commands : 
```
lsof -i :5000
```
And kill the process.

For example for the message:
```
COMMAND     PID           USER   FD   TYPE             DEVICE SIZE/OFF NODE NAME
python3.1 76462 sullivancastro    4u  IPv4 0x5d2535ef8742ddc9      0t0  TCP localhost:commplex-main (LISTEN)
python3.1 76462 sullivancastro    6u  IPv4 0x5d2535ef8742ddc9      0t0  TCP localhost:commplex-main (LISTEN)
```

You should launch:
```
kill 76462
```
