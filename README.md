# Tickets

Tickets is an Issue Tracking System developed with Django Rest Framework.

## Installation

If you don't have python installed, download and install python from here : https://www.python.org/downloads/

### Get the project files
```bash
git clone https://github.com/phi-lemon/tickets_api.git
```

### Create and activate the virtual environment:

```bash
python -m venv venv
venv\Scripts\activate  # on windows
source venv/bin/activate  # on linux
```
If you have any problems to activate the virtual environment on windows, 
you may need to authorize scripts execution : `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope process`

### Install the dependencies

```bash
pip install -r requirements.txt
```

## Usage

### Launch Server
```bash
venv\Scripts\activate  # on windows
source venv/bin/activate  # on linux
python manage.py runserver
```

### Interact with the API
Your may use your browser to request the browsable API provided by Django Rest Framework, or use a client like Postman. 
<br>Registration : http://127.0.0.1:8000/api/signup/

### Documentation
https://documenter.getpostman.com/view/24886844/2s8ZDeTyNq

## License
[MIT](https://github.com/phi-lemon/tickets_api/blob/main/LICENSE.md)
