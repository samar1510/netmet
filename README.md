# NETMET: Internet measurements codes and courses

This repository is dedicated to NETMET TD at Sorbonne University. It is meant for under-graduated master students with a background in computer networking.
It contains:
- subjects for practical courses
- small recaps on notions
- code for interacting with RIPE Atlas API

# Clone the repository

You first need a github account to clone the repository

```bash
git clone https://github.com/hrimlinger/netmet.git
cd netmet
```

Note: you might also need to create a token for cloning (check on how to create a token [here](#https://docs.github.com/en/enterprise-server@3.6/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens))


```bash
git clone https://<your_token_here>@github.com/hrimlinger/netmet.git
cd netmet
```

# Install dependencies

This project use poetry as package manager, you can install poetry using:
```bash
pip install poetry
```

The use the following commands:
```bash
poetry shell
poetry lock
poetry install
```

# Run some code

You are normally setup, you can now use the code and follow the exercises. Each TP/TD is composed of a main, where you will execute your code, good luck!
Run the following script to test your installation:
```bash
python TP1/main.py
``` 

# usefull

go check [RIPE Atlas API](#https://atlas.ripe.net/docs/apis/rest-api-manual/) it is your best friend for TP1.

# setup ripe credentials 

The professor will communicate you your credentials for RIPE Atlas API. an example of .env file required is given at [.env.example](./.env.example)

```bash
RIPE_USERNAME=
RIPE_SECRET_KEY=

``` 

Note: alternatively you can also simply export the two environment variables

