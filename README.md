# Motivation for the project And Project Description 
The Casting Agency models a company that is responsible for creating movies and managing and assigning actors to those movies. 
You are an Executive Producer within the company and are creating a system to simplify and streamline your process.

The app is using render cloud platform to deploy.
````
https://capstone-uwse.onrender.com
````
## Local Setup
````
pip install --upgrade setuptools wheel
pip install -r requirements.txt
python3 -m virtualenv env
source env/bin/activate
````

## DB setup
````
createuser -s udacity
createdb agency
````

## Server startup
````
export FLASK_APP=app
export FLASK_DEBUG=true
python app.py
````
## Unit Test
````
createdb testagency
python test_app.py
````

# API
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




