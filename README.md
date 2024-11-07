# College_ProjectEPB

This repository contains a Django project setup. Follow the instructions below to install Django, set up a virtual environment, create the project and app, and run the server locally.

## Table of Contents
- [Installation and Activating Virtual Environment](#installation)
- [Creating the Django Project and App](#creating-the-django-project-and-app)
- [Running the App](#running-the-app)

## Installation and Activating Virtual Environment

1. **Create a Virtual Environment**  
   To create a virtual environment named `venv`, run:
   ```
   python3 -m venv venv

2. **Activate the Virtual Environment**
   Activate the virtual environment based on your operating system:

   Windows:
   ```
   venv\Scripts\activate 
   ```
   macOS/Linux:
   ```
   source venv/bin/activate
   ```

3. **Install Django After activating the virtual environment, install Django using:**
     ```
     pip install django
     ```
     
4. **Verify the Django Installation To check if Django was installed correctly, run:**
   ```
   django-admin --version
   ```

## Creating the Django Project and App

1. **Create the Django Project**
   Start by creating a new Django project named file_upload_app:
   ```
   django-admin startproject file_upload_app
   ```

2. **Navigate to the Project Directory**
   Change into the project directory:
   ```
   cd file_upload_app
   ```

3. **Create the Django App**
   Inside the project, create a Django app named fileupload:
   ```
   python manage.py startapp fileupload
   ```

4.**Add the App to Project Settings**
   Open the file file_upload_app/settings.py and add 'fileupload' to the INSTALLED_APPS list:
   ```
   INSTALLED_APPS = [
    ...
    'fileupload',
   ]
   ```

## Running the App
If the virtual environment named venv has already been created, activate it as follows:

1. **Apply Migrations**
   Run the following command to set up the initial database tables:
   ```
   python manage.py makemigrations
   python manage.py migrate
   ```

2. **Run the Development Server**
   Start the Django development server using:
   ```
   python manage.py runserver
   ```

3. **Access the Application**
   Open your browser and go to http://127.0.0.1:8000/ to see the application in action.
   


   

   
   
