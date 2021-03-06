# Webshop

A simple webshop by using Django framework

## Instructions

### For Mac/Linux


1. `Install MySQL and create a database for the project:`
    `1.1. Create a new database.`
    `1.2. Create a new MySQL user with a password.`
    `1.3. Grant the new MySQL user permissions to manipulate the database.`
        `mysql> CREATE DATABASE Webshop CHARACTER SET utf8;`
        `Query OK, 1 row affected (0.00 sec)`
        `mysql> CREATE USER 'username'@'localhost' IDENTIFIED BY 'password';`
        `Query OK, 0 rows affected (0.00 sec)`
        `mysql> GRANT ALL ON Webshop.* TO 'username'@'localhost';`
        `Query OK, 0 rows affected (0.00 sec)`
2. `git clone https://github.com/sainioan/Webshop`
3. `pip install virtualenv`
4. `source venv/bin/activate`
5. `cd Webshop`
6. `create an .env file which contains the following:`

   `DATABASE_NAME = xxxx`
   `DATABASE_USER = username`
   `DATABASE_PASSWORD = password`

7. `pip install -r requirements.txt`
8. `python manage.py makemigrations`
9. `python manage.py migrate`
10. `python manage.py runserver`

## Feature to Add Products:
1. `python manage.py createsuperuser`
2. Log in to the admin panel 'http://127.0.0.1:8000/admin/' with the superuser username and password.

<img src="https://github.com/sainioan/Webshop/blob/main/images/django_administration.jpg"  width="300" height="150">

4. Select Products and choose 'add product'

<img src="https://github.com/sainioan/Webshop/blob/main/Webshop/static_templates/admin_panel_2.jpg"  width="300" height="150">

### Sample images 

<a href="https://github.com/sainioan/Webshop/tree/main/images/sample%20product%20images">sample images</a>

### For more images, see: 
<a href="https://github.com/sainioan/Webshop/blob/main/images/images.md">images</a>
