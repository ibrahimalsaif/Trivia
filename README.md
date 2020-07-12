# Trivia API

This is a trivia app that student will be able to play with it, it has many features you can view all questions and view them from a certain category, and you can add a question, and finally, you can play with the quiz and challenge your colleague and see who is the most knowledgeable.

## Getting Started

### Pre-requisites and Local Development

Developers using this project should already have Python3, pip and node installed on their local machines.

### Backend

From the backend folder run pip install requirements.txt. All required packages are included in the requirements file.

To run the application run the following commands:

export FLASK_APP=flaskr
export FLASK_ENV=development
flask run

These commands put the application in development and directs our application to use the __init__.py file in our flaskr folder. Working in development mode shows an interactive debugger in the console and restarts the server whenever changes are made. 

The application is run on http://127.0.0.1:5000/ by default and is a proxy in the frontend configuration.

### Frontend

From the frontend folder, run the following commands to start the client:

npm install 
npm start 

By default, the frontend will run on localhost:3000.

### Tests

In order to run tests navigate to the backend folder and run the following commands:

dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py

The first time you run the tests, omit the dropdb command.

All tests are kept in that file and should be maintained as updates are made to app functionality.

## API Reference

### Getting Started

Base URL: At present this app can only be run locally and is not hosted as a base URL. The backend app is hosted at the default, http://127.0.0.1:5000/, which is set as a proxy in the frontend configuration.

### Error Handling

Errors are returned as JSON objects in the following format:

{
    "success": False, 
    "error": 400,
    "message": "bad request"
}

The API will return three error types when requests fail:

400: Bad Request
404: Resource Not Found
422: Not Processable

### GET /categories

#### General:

Returns a list of categories objects, success value.

#### Sample:

curl http://127.0.0.1:5000/categories

### GET /questions

#### General:

Returns a list of questions objects, and categories objects, success value, and total number of questions.
Results are paginated in groups of 10.

#### Sample:

curl http://127.0.0.1:5000/questions?page=1

### DELETE /questions/<int:question_id>

#### General:

Deletes the question of the given ID if it exists.
Returns the id of the deleted question, success value, total questions, and questions list based on current page number to update the frontend.

#### Sample:

curl http://127.0.0.1:5000/questions/10

### POST /questions

#### General:

Adds a new question using the submitted question, answer, difficulty and category.
Returns success value.

#### Sample:

curl http://127.0.0.1:5000/questions?page=3 -X POST -H "Content-Type: application/json" -d '{"question":"what is the capital of saudi arabia", "answer":"riyadh", "difficulty":"1",  "category":"2"}'

### POST /questions/serach

#### General:

Search for a question using the search term.
Returns success value, and a list of questions, and the total number of questions.

#### Sample:

curl http://127.0.0.1:5000/questions/serach -X POST -H "Content-Type: application/json" -d '{"searchTerm":"what is the capital of saudi arabia"}'

### GET /categories/<int:category_id>/questions

#### General:

Returns a list of questions objects by a certain category, and the current category, and total number of questions, and a success value.

#### Sample:

curl http://127.0.0.1:5000/categories/2/questions

### POST /quizzes

#### General:

Let you able to get random questions, and by a certain category if you want, and answer them and get a score.
Returns a list of questions, and a success value.

#### Sample:

curl http://127.0.0.1:5000/quizzes -X POST -H "Content-Type: application/json" -d '{"category":"3"}'

## Authors

Yours truly, Ibrahim
