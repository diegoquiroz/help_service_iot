## How to run?

You need an .env file, you can copy the one from the example.
```
cp .env.example .env
```
Edit .env to set ENV variables.


### Install dependencies with poetry
```
poetry install
```

### Run virtual env and run code
```
# For Unix systems
source $(poetry env info --path)/bin/activate
python sos.py
```


## LICENCE
MIT
