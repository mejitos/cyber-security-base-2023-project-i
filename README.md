# Cyber Security Base - Project I

- Included "stock images" are generated with [AI](https://www.craiyon.com/)

## Requirements

- Linux operating system
    - The demonstrated command injection uses shell commands, which does
    not work on Windows. Mac is so and so. I have no experience on Mac,
    so cannot tell. Basically all web applications run on Linux anyway,
    so now or never start learning it.
    - WSL on Windows should be fine.
- Python 3.9 or newer
- Python `venv`


## Installation

### Clone the repo

```bash
git clone git@github.com:mejitos/cyber-security-base-2023-project-i.git
cd cyber-security-base-2023-project-i
```

### Create a virtual environment

```bash
python -m venv env
source env/bin/activate
```

### Install library dependecies

```bash
pip install -r requirements.txt
```


## Run the application

Activate the virtual environment if you already haven't.

Start the server:

```bash
python run.py
```

and in browser, go to url [127.0.0.1:5000](127.0.0.1:5000)



## Usage

The application is called VISP, or Vulnerable Image Sharing Platform which
is exactly that: a vulnerable web application where you can upload and share
images with other users.

Has two users:

| username | password |
| -------- | -------- |
| alice    | alice    |
| bob      | bob      |
