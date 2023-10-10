# DeyUp-Backend
A simple login and subscription app
### Setup
Update the System
```bash
sudo apt-get update
```
To get this repository, run the following command inside your git enabled terminal
```bash
git clone https://github.com/saprahits/deyup_python.git
```

 
Install environment first
``` bash
sudo  pip3 install virtualenv
```
Create Environment
```bash 
virtualenv env
```

Activate the environment 
```bash 
source env/bin/activate
```

Install the all requiements using requirements.txt file in active environment
```bash
pip install -r requirements.txt
```

```bash
python3 manage.py makemigrations
```

This will create all the migrations file (database migrations) required to run this App.

Now, to apply this migrations run the following command
```bash
python3 manage.py migrate
```

One last step and then our todo App will be live. We need to create an admin user to run this App. On the terminal, type the following command and provide username, password and email for the admin user
```bash
python3 manage.py createsuperuser
```

That was pretty simple, right? Now let's make the App live. We just need to start the server now and then we can start using our simple todo App. Start the server by following command

```bash
python3 manage.py runserver
```

Once the server is hosted, head over to http://127.0.0.1:8000/todos for the App.





### API DOCUMENTATION 
I will provide postman collection


