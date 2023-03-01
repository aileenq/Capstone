# The Casting Agency Project
***
#### Live at: <a href="https://capstone-uwse.onrender.com">https://capstone-uwse.onrender
***
# Motivation for the project And Project Description 
The Casting Agency models a company that is responsible for creating movies and managing and assigning actors to those movies. 
You are an Executive Producer within the company and are creating a system to simplify and streamline your process.

# Main Dependencies and tech stack
````
Python 3.7+ 
Flask 
SQLAlchemy
Flask-Migrate
````
For a full list of required dependencies and libraries, please refer to the ````requirements.txt```` file 

# Development Setup
To start and run the local development server

1. Setup Virtual Environment
````
python3 -m virtualenv env
source env/bin/activate
````

2. Install Dependencies
````
pip install --upgrade setuptools wheel
pip install -r requirements.txt
````

3. Run the development server
````
export FLASK_APP=app
export FLASK_DEBUG=true
python app.py
````

## DB setup
````
createuser -s udacity
createdb agency
````

## Unit Test
````
createdb testagency
python test_app.py
````

## Environment Variables and config setup including Auth0 and DB config
Export the credentials as environment variable

````commandline
chmod +x setup.sh
source setup.sh
````

# RBAC

### 1- Executive_producers can:
- view actors and movies in list and in details
- post new actors and movies
- patch actors and movies
- cast actors to movies and fire actors from movies
- delete actors and movies

### 2- Casting_directors can:
- view actors and movies in list and in details
- post new actors and movies
- patch actors and movies
- cast actors to movies and fire actors from movies

### 3- Casting_assistant can:
- view actors and movies in list and details

# API Endpoints

### Get actors

`GET '/api/v1.0/actors'`

- Fetches a dictionary of all actors 

- Request Arguments: page -- type int
- Requires permission: get:actors
- Returns: An object with following fields
  - `success`: A boolean representing the status of the result of the request.
  - `actors`: An object of actor with following fields
    - id: id
    - name: actor name
    - gender: actor gender
    - age: actor age

```json
{
  "actors": [
    {
      "age": 25,
      "gender": "Male",
      "id": 1,
      "name": "Matthew"
    }
  ],
  "success": true
}

```

### POST Actors

`POST '/api/v1.0/actors'`
- Add a new actor 
- Request Body: {name:string, age: int, gender: string}
- Requires permission: post:actors
- Returns: An object with the following properties:
  - `success`: A boolean representing the status of the result of the request.
  - `created`: A integer representing the ID of the added actor
```json
{
  "success": true,
  "created": 1
}
```

### PATCH Actors

`PATCH '/api/v1.0/actors/<int:id>'`
- update an actor 
- Request Arguments: id -- type: int
- Request Body: {name:string, age: int, gender: string}
- Requires permission: edit:actors
- Returns: An object with the following properties:
  - `success`: A boolean representing the status of the result of the request.
  - `updated`: A integer representing the ID of the updated actor
  - 'actor': actor object
```json
{
    "actor": [
        {
            "age": 30,
            "gender": "female",
            "id": 1,
            "name": "Test Actor"
        }
    ],
    "success": true,
    "updated": 1
}
```

### DELETE Actors

`DELETE '/api/v1.0/actors/<int:id>'`
- delete a new actor 
- Request Arguments: id --type:int
- Requires permission: delete:actors
- Returns: An object with the following properties:
  - `success`: A boolean representing the status of the result of the request.
  - `deleted`: A integer representing the ID of the deleted actor
```json
{
  "success": true,
  "deleted": 1
}
```

### Get movies

`GET '/api/v1.0/movies'`

- Fetches a dictionary of all movies 

- Request Arguments: page -- type int
- Requires permission: get:movies
- Returns: An object with following fields
  - `success`: A boolean representing the status of the result of the request.
  - `movies`: An object of actor with following fields
    - id: id
    - title: movie name
    - release_date: movie release date

```json
{
  "movies": [
    {
      "id": 1,
      "release_date": "Sun, 16 Feb 2023 00:00:00 GMT",
      "title": "Aileen first Movie"
    }
  ],
  "success": true
}

```

### POST Movies

`POST '/api/v1.0/movies'`
- Add a new actor 
- Request Body: {title:string, released_date: date}
- Requires permission: post:movies
- Returns: An object with the following properties:
  - `success`: A boolean representing the status of the result of the request.
  - `created`: A integer representing the ID of the added movie
```json
{
  "success": true,
  "created": 1
}
```

### PATCH Actors

`PATCH '/api/v1.0/actors/<int:id>'`
- update a movie 
- Request Arguments: id -- type: int
- Request Body: {title:string, released_date: date}
- Requires permission: edit:movies
- Returns: An object with the following properties:
  - `success`: A boolean representing the status of the result of the request.
  - `updated`: A integer representing the ID of the updated movie
  - 'movie': movie object
```json
{
    "updated": 1,
    "movie": [
        {
            "id": 1,
            "release_date": "Sun, 16 Feb 2022 00:00:00 GMT",
            "title": "Test Movie"
        }
    ],
    "success": true
}
```

### DELETE Movie

`DELETE '/api/v1.0/movies/<int:id>'`
- delete a movie 
- Request Arguments: id --type:int
- Requires permission: delete:movies
- Returns: An object with the following properties:
  - `success`: A boolean representing the status of the result of the request.
  - `deleted`: A integer representing the ID of the deleted movie
```json
{
  "success": true,
  "deleted": 1
}
```
***
# Deployment Instruction
This project is deployed with Render Cloud. The cli is still in developing mode, so all
the changes have to be made in its Web UI. The connected github repo is https://github.com/aileenq/Capstone

Here's how:
#### 1. Create an account at <a href="render.com">render.com</a> and log in.
#### 2. On the Render Dashboard, click the ````New Postgres```` button to set up a Postgres cloud database.
#### 3. Connect your app from GitHub or GitLab repo to the Web Service.
#### 4. Go back to Render Dashboard and create a new ````Web Service````.
   1. Provide a name for the new database service
   2. Select an instance type: ````Free```` 
   3. Enter the build command: ````pip install -r requirements.txt````
   4. Connect the Postgres service
      1. From the Postgres service (name: "postgres-deployment-example"), click the "Info" side navigation and copy the Internal Database URL from the Connections page.
      2. From the web service (name: "render-deployment-example"), create an environment variable with the key: DATABASE_URL and value: the <Database URL> copied from the Postgres service.
   5. Now you can hit the ````Create Web Service```` button.
#### 5. After the Web Service is ready, you can click the App URL to start the app.
