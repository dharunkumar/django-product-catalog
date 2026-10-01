# Django Product Catalog

A Django product catalog with categories and tags. The product list view/frontend template supports searching product descriptions and filtering by multiple categories or tags.

## Requirements

- Python 3.12 or newer
- pip

## Setup

Open a terminal in the project directory (the directory containing `manage.py`). Create and activate a virtual environment:

Windows:
```
python3 -m venv .venv
.\.venv\Scripts\Activate.ps1
```
Mac or Linux:
```
python3 -m venv .venv
source .venv/bin/activate
```

Install Django:

```
python -m pip install --upgrade pip
python -m pip install "Django==6.1.1"
```

Apply migrations to create the database and load the sample categories, tags and products:

```
python manage.py migrate
```

## Run

Start the development server:

```
python manage.py runserver
```

Open <http://127.0.0.1:8000/products/> to view the site. The admin site is available at <http://127.0.0.1:8000/admin/>. To create an admin login, run `python manage.py createsuperuser` and follow the prompts.

## Notes and Assumptions

- The project uses SQLite by default. `python manage.py migrate` creates `db.sqlite3` locally.
- The project also has a data migration additionally to seed the tables with initial data, so that when running the app for the first time, it will be easier to test the functionality without adding more data through the admin interface.
- the committed migrations, including the sample-data migration, are the source of truth for recreating the database.
- This is a local development setup. The checked-in Django settings enable debug mode and use a development secret key.
- The filters on both tags and categories support multiple selection.
- `ecomsite` is the django project and `products` is an app within the project.

## AI usage:
- AI assistance was used to outline and format the project setup instructions and markdown structure in `README.md` and subsequently modified my me to match the project's functionality and assumptions. 
- AI assistance was utilized to generate the initial HTML boilerplate `product_list.html` and further changed by me to reflect the API structure, query string parameters and added additional functionality.
