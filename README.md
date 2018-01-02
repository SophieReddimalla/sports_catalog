# **Catalog Project**
 This application provides a list of items within a variety of categories as well as provide a user registration and authentication system. Registered users will have the ability to post, edit and delete their own items.

***

## Prerequisites
A linux Virtual Machine with following software 
    - postgres RDMS database
    - python 2.7 
A Google+ account 

***

## Initial setup
  1. Use git to clone the project
  ```shell
      git clone  https://github.com/SophieReddimalla/sports_catalog.git catalog
  ```
  2. Install the packages from requirements.txt
  ```shell
     pip install -r requirements.txt
  ```
  3. Create PostgreSQL Database catalog
  ```shell
     createdb catalog
  ```
  4. Create Tables
  ```shell
     python catalog_setup.py
  ```  
  5. Run the Project
  ```shell
     python catalog.py
  ```  
  6. Access Project
  ```shell
     http://localhost:8000
     You can view the catalog but to add new items you got to login with your Google+ id.
     Ensure that your google profile contains username and email..
  ```   

***

## Author 
Sophie Reddimalla.

## Acknowledgments
Samson Reddimalla


