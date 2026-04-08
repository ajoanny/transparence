# Transparence

## Overview

Transparence is an open-source project designed to improve access to public data related to political transparency. It
leverages data provided by  [Poligraph API](https://www.data.gouv.fr/dataservices/poligraph-api-transparence-politique-affaires-judiciaires-et-fact-checks-rest-json)([data.gouv.fr](https://www.data.gouv.fr/)) 
to expose structured information about political figures and their associated legal cases.

This API provides data for the transparence-app. In the long term, the project aims to aggregate data from multiple
sources and deliver it to the frontend, offering a more comprehensive and unified view of political transparency data.

## Tech Stack
- **Language:** Python
- **Framework:** Django
- **Database:** PostgreSQL

The application is composed of an API and a worker that fetch data from the [Poligraph API](https://www.data.gouv.fr/dataservices/poligraph-api-transparence-politique-affaires-judiciaires-et-fact-checks-rest-json).


## Installation

```bash
pip install -r dev-requirements.txt
```

### Migrations

```bash
python manage.py migrate
```

### Import data

```bash
python manage.py import_data 
```

### Server
#### Run with Docker Compose (recommended)

```bash
docker compose up -d
```

#### Alternative setup

```bash
docker compose up postgres -d
python manage.py runserver
```
### Worker

```bash
python manage.py qcluster
```

## Configuration

Create a .env file or set environment variables:

```bash
DB_NAME=
DB_USER=
DB_PASSWORD=
DB_HOST=
DB_PORT=
JWT_SECRET=
SECRET_KEY=
POLIGRAPH_API_URL=https://poligraph.fr
```

## Testing

```bash
pytest
```

Or with watch mode:
```bash
ptw
```

## API-KEY

To generate an API key, use the /admin interface.
Before accessing the admin, you must create a superuser.

````bash
python manage.py createsuperuser
````

## Contributing

Contributions are welcome.
Feel free to open an issue or submit a pull request for improvements or fixes.

This project is built on a commitment to transparency. Gamification features, such as ratings, are intentionally avoided
to allow individuals to form their own opinions.

## License

This project is licensed under the MIT License.