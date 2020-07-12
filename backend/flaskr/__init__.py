import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from backend.models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10


def paginate_questions(request, selection):
    page = request.args.get('page', 1, type=int)
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE

    questions = [question.format() for question in selection]
    current_questions = questions[start:end]

    return current_questions


def create_app(test_config=None):
    app = Flask(__name__)
    setup_db(app)
    CORS(app)

    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers',
                             'Content-Type,Authorization,true')
        response.headers.add('Access-Control-Allow-Methods',
                             'GET,PUT,POST,DELETE,OPTIONS')
        return response

    @app.route('/categories', Methods=['GET'])
    def get_categories():
        categories = Category.query.order_by(Category.id).all()

        categories_list = {}
        for category in categories:
            categories_list[category.id] = category.type

        if (len(categories_list)) == 0:
            abort(404)

        return jsonify({
            'success': True,
            'categories': categories_list
        })

    @app.route('/questions', Methods=['GET'])
    def get_questions():
        selection = Question.query.order_by(Question.id).all()
        current_questions = paginate_questions(request, selection)

        categories = Category.query.order_by(Category.id).all()
        categories_list = {}
        for category in categories:
            categories_list[category.id] = category.type

        if len(current_questions) == 0 or len(categories_list) == 0:
            abort(404)

        return jsonify({
            'success': True,
            'questions': current_questions,
            'total_questions': len(Question.query.all()),
            'categories': categories_list,
        })

    @app.route('/questions/<int:question_id>', Methods=['DELETE'])
    def delete_question(question_id):
        try:
            question = Question.query.filter(id=question_id).one_or_none()

            if (question is None):
                abort(404)

            question.delete()

            selection = Question.query.order_by(Question.id).all()
            current_questions = paginate_questions(request, selection)

            categories = Category.query.order_by(Category.id).all()
            categories_list = {}
            for category in categories:
                categories_list[category.id] = category.type

            return jsonify({
                'success': True,
                'deleted': question_id,
                'questions': current_questions,
                'total_questions': len(Question.query.all()),
                'categories': categories_list
            })

        except:
            abort(422)

    @app.route('/questions', Methods=['POST'])
    def add_question():
        data = request.get_json()

        question = data.get('question', None)
        answer = data.get('answer', None)
        difficulty = data.get('difficulty', None)
        category = data.get('category', None)

        try:
            question = Question(question=question, answer=answer,
                                difficulty=difficulty, category=category)
            question.insert()

            return jsonify({
                'success': True
            })
        except:
            abort(422)

    @app.route('/questions/serach', Methods=['POST'])
    def serach_questions():

        data = request.get_json()
        search_term = data.get('searchTerm', None)
        questions = Question.query.filter(
            Question.question.ilike('%' + search_term + '%')).all()

        if len(questions) == 0:
            abort(404)

        return jsonify({
            'success': True,
            'questions': questions,
            'total_questions': len(questions)
        })

    @app.route('/categories/<int:category_id>/questions', Methods=['GET'])
    def get_questions_by_category(category_id):

        category = Category.query.filter_by(id=category_id).one_or_none()

        if (category is None):
            abort(404)

        selection = Question.query.filter_by(category=Category.id).all()
        current_questions = paginate_questions(request, selection)

        return jsonify({
            'success': True,
            'questions': current_questions,
            'total_questions': len(Question.query.all()),
            'current_category': category.type
        })

    @app.route('/quizzes', Methods=['POST'])
    def quiz():

        data = request.get_json()
        previous_questions = data.get('previous_questions')
        quiz_category = data.get('quiz_category')

        if ((quiz_category is None) or (previous_questions is None)):
            abort(400)

        if (quiz_category['id'] == 0):
            questions = Question.query.all()
        else:
            questions = Question.query.filter_by(
                category=quiz_category['id']).all()

        def get_random_question():
            return questions[random.randrange(0, len(questions), 1)]

        next_question = get_random_question()
        used = True

        while used:
            if next_question.id in previous_questions:
                next_question = get_random_question()
            else:
                used = False

        return jsonify({
            'success': True,
            'question': next_question.format()
        })

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": "bad request"
        }), 400

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "resource not found"
        }), 404

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "unprocessable"
        }), 422
        
    return app