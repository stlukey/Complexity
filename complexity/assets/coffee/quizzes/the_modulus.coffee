##!/usr/bin/env coffee
# -*- coding: UTF-8 -*-
###
    Complexity: quizzes/the_modulus.coffee
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    :copyright: (c) 2015 Luke Southam <luke@devthe.com>.
    :license: New BSD, see LICENSE for more details.
###

class QuizPageData
    content: document.getElementById 'quiz-content'
    msg: document.getElementById 'quiz-msg'

    msgWait: document.getElementById 'quiz-msg-wait'
    msgStart:  document.getElementById 'quiz-msg-start'

    _score = document.getElementById 'quiz-score-value'

    _dataZ = document.getElementById 'quiz-data-z'
    _dataW = document.getElementById 'quiz-data-w'
    
    _answers = document.getElementById('quiz-answers')

    _question = document.getElementById 'quiz-question-value'
    _possibleAnswers = document
                        .getElementById 'quiz-answer-selection'
                        .getElementsByClassName 'answer-box'

    Object.defineProperties @prototype,
        score:
            set: (value) ->
                _score.innnerHTML = value

        z:
            set: (value) ->
                katex.render "z = #{ value }", _dataZ

        w:
            set: (value) ->
                katex.render "w = #{ value }", _dataW

    setQuestionPart: (part, callback) ->
        [question, answers, correctAnswer] = part
        katex.render "#{ question } = ", _question

        for i in [0..2]
            katex.render answers[i], _possibleAnswers[i]
            _possibleAnswers[i].onclick = -> callback(i)

    setAnswerPart: (part, question, answer) ->
        katex.render "#{ question } = #{ answer } ", _answers[part]


class Quiz
    constructor: (@ID) ->
        Quiz.log "ID: #{@ID}"

        @page = new QuizPageData
        @answered = false
        @getQuestion @showStart


    # When the quiz object is ready, ask the user if they wish
    # to start.
    showStart: =>
        @page.wait.style.display = 'none'
        @page.start.onclick = @startQuiz
        @page.start.classList.add 'show'
        @page.start.classList.remove 'hide'
        Quiz.log "Ready!"

    startQuiz: ->
        @page.msg.style.display = 'none'
        @page.content.classList.add 'show'
        @page.content.classList.remove 'hide'


    # Get requests to quiz.
    @get: (name, callback) ->
        $.getJSON $SCRIPT_ROOT + $SCRIPT_QUIZ_URLS[name]
            .success callback
            .error @showError

    # Log data to console.
    @log: (options..., msg) ->
        options.push "Quiz"
        msg = "[" + option + "] " + msg for option in options
        console.log msg

    # For critical errors.
    @showError: (jqXHR, textStatus, errorThrown) ->
        Quiz.log  "Error", "#{textStatus} #{errorThrown}"
        
        page = new QuizPageData
        page.content.style.display = 'none'
        page.msg.style.display  = 'none'
        page.msg.classList.add('hide', 'error')
        page.msg.innerHTML = ''

        errorText = document.createElement 'h1'
        errorText.innerHTML = "A critical error occurred!"
        
        page.msg.appendChild errorText

    # Runs when page is loaded.
    @main: ->
        Quiz.get 'new', (json) ->
            new Quiz json['ID']

$ Quiz.main

