# Vevent

## A web application that allows users to find/host volunteer events.

More description is available on the [DevPost](https://devpost.com/software/ruby-orets5).

### How To Run

#### Setting Up The Environment

When you are in the command prompt, run the following three commands:

```
py -m venv env
py -m pip install --user virtualenv
.\env\Scripts\activate
```

> More description available here: https://packaging.python.org/en/latest/guides/installing-using-pip-and-virtual-environments/.

#### Installing Dependancies

To install the dependencies, run the following command:

```
pip install -r requirements.txt
```

#### Setting Up Application

To set up the application, run the following three commands:

```
set FLASK_APP=AudioAssembly
set FLASK_ENV=development
set GOOGLEMAPS_KEY=<YOUR GOOGLEMAPS_KEY>
set TWILIO_ACCOUNT_SID=<YOUR TWILIO_ACCOUNT_SID>
set TWILIO_AUTH_TOKEN=<YOUR TWILIO_AUTH_TOKEN>
```

#### Running The Application

Finally, to run the application, run the following command:

```
flask run
```
