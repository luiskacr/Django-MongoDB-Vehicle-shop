# Store Django-MongoDB

## About the project
***
This is a project created as a final project of the subject NOSQL Databases of the Fidelitas University given by Professor Marvin Solano Campos in the first quarter of 2023.

This project aims to learn about the use of Django Framework and Mongodb technologies with a practical approach. 

## Requirements for this project
***
A list of technologies used within the project:
* [Git](https://git-scm.com/): Version 2.39.0
* [Python](https://www.python.org/): Version 3.10 
* [PIP](https://pypi.org/project/pip/): Version 22.3.*
* [MongoDB](https://www.mongodb.com/): Version 6.0.5


> it is recommended to have installed visual studio code or the IDLE of your preference, if you have installed visual studio code it is recommended to have the Python extension.

## Used libraries
***
A list of libraries used within the project:
* pymongo
* djongo
* pytz


## Mongodb Configuration
***
Before installing the project you must configure the database, this requires the setup of the following: 


## Installation
***
To start, copy the repository, open a Git terminal in the folder where you want to install the project and run the following command:

```
$ git clone https://github.com/luiskacr/Store-Django-MongoDB-.git
$ cd <Store-Django-MongoDB>
```
To configure the database enter the following file tiendaMongo/settings.py search for the line with the # Database indication and configure your mongo database connection as shown in the following example

```python
DATABASES = {
    'default': {
        'ENGINE': 'djongo',
        'NAME': '<Database name>',
        'CLIENT': {
            'host': '<URL_from_database>',
            'port': <database_port>,
            'username': '<database_username>',
            'password': '<database_password>'',
        }
    }
}
```

Run the migrations: 
```
$ python manage.py makemigrations
$ python manage.py migrate
```

To create a super user or administrator user, you must run the following command and follow the instructions where you will be asked for the user name, email and password 

```
$ python  manage.py createsuperuser 
```

Finally run the project:
```
$ python manage.py runserver
```

## Collaboration
***
Give instructions on how to collaborate with your project.
> Maybe you want to write a quote in this part. 
> Should it encompass several lines?
> This is how you do it.



