# ico_quiztime

## How to install

1. git clone https://github.com/pavankumarvm/ico_quiztime.git
2. Change to ico_quiztime directory
   ```bash
   cd ico_quiztime
   ```
3. create virtual environment using virtualenv
   Commands are as follows:
   ```bash
   pip install virtualenv
   python -m venv .venv
   .venv\Scripts\activate
   ```
4. Check in command line if virtualenv is activated or not.
   If activated it will be as follows:
   ```bash
   (venv) A:ico_quiztime>
   ```
5. Now install required packages:
   ```bash
   pip install -r requirements.txt
   ```

## How to run project

1. Be sure you have completed above installation steps.
2. Now first migrate all models.
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```
3. Now collect a static files.
   ```bash
   python manage.py collectstatic
   ```
5. Now you can run project using command:
   ```bash
   python manage.py runserver
   ```

## Contribute to Repository

```
1. Fork this repository
2. create a branch for your changes
3. configure an upstream to this repository
4. create a pull request
```
