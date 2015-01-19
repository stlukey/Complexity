##!/usr/bin/env coffee
# -*- coding: UTF-8 -*-
###
    Complexity: quizzes/the_modulus.coffee
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Client side script for 'the_modulus' quiz.

    :copyright: (c) 2015 Luke Southam <luke@devthe.com>.
    :license: New BSD, see LICENSE for more details.
###

class QuizPageData
    ###
    Manages page data.
    ###

    # Get elements on page.
    content: document.getElementById 'quiz-content'
    msg: document.getElementById 'quiz-msg'

    msg:  document.getElementById 'quiz-msg'
    msgWait: document.getElementById 'quiz-msg-wait'
    msgStart:  document.getElementById 'quiz-msg-start'

    _score = document.getElementById 'quiz-score-value'
    _score_value = 0

    _dataZ = document.getElementById 'quiz-data-z'
    _dataW = document.getElementById 'quiz-data-w'
    
    _answers = document.getElementById('quiz-answers')
                       .children

    _question = document.getElementById 'quiz-question-value'
    _possibleAnswers = document
                        .getElementById 'quiz-answer-selection'
                        .getElementsByClassName 'answer-box'

    # Properties to update page content as set.
    Object.defineProperties @prototype,
        score:
            get: -> _score_value
            set: (value) ->
                _score_value = value
                _score.innerHTML = value

        z:
            set: (value) ->
                katex.render "z = #{ value }", _dataZ

        w:
            set: (value) ->
                katex.render "w = #{ value }", _dataW

    setQuestionPart: (part, callback) ->
        ###
        Setup page for given question part.
        ###

        [question, answers, correctAnswer] = part
        katex.render "#{ question } = ", _question
        @setPossibleAnswers answers, callback

    setPossibleAnswers: (answers, callback) ->
        ###
        Setup possible answers on page.
        ###
        katex.render answers[0], _possibleAnswers[0]
        _possibleAnswers[0].onclick = -> callback(0)

        katex.render answers[1], _possibleAnswers[1]
        _possibleAnswers[1].onclick = -> callback(1)

        katex.render answers[2], _possibleAnswers[2]
        _possibleAnswers[2].onclick = -> callback(2)

    setAnswerPart: (part, question, answer) ->
        ###
        Add previous part's answer to page.
        ###
        katex.render "#{ question } = #{ answer } ", _answers[part]
    
    flashAnswer: (answer, color, callback) ->
        ###
        Flash answer a given color.
        ###
        el = $(_possibleAnswers[answer])
        el.animate { 'background-color': color }, 200
        el.animate { 'background-color': 'white' }, 200
        el.promise().done callback if callback?

    clearAnswers: ->
       ###
       Clear answers for previouse parts.
       ###
       for answer in _answers
           answer.innerHTML = ''

    removeAnswerHooks: ->
        ###
        Remove any click hooks from possible answers.
        ###
        for answer in _possibleAnswers
            answer.onclick = null

class Quiz
    constructor: (@ID) ->
        Quiz.log "ID: #{@ID}"

        @page = new QuizPageData
        @getQuestion @showStart

    getQuestion: (callback) =>
        ###
        Get question from server.
        ###
        Quiz.get 'next', (json) =>
            if json['finish']
                return @onFinish()

            @question = json['question']
            @data = json['data']

            # Save z and w
            @page.z = @data['z']
            @page.w = @data['w']

            # Clear page.
            @page.clearAnswers()
            @currentQuestionAnswers = []

            # Setup first part of question.
            @currentPart = @question.shift()
            @lastStartTime = +new Date
            @page.setQuestionPart @currentPart, @onAnswer
            callback() if callback?

    onAnswer: (answer) =>
        ###
        When a question is answered.
        ###
        @page.removeAnswerHooks()

        timeNow = +new Date
        timeDelta = timeNow - @lastStartTime
        answer = [answer, timeDelta]
        @currentQuestionAnswers.push(answer)
    
        correct = answer[0] == @currentPart[2]

        color = 'red'
        color = 'green' if correct
        if not correct
            @page.flashAnswer @currentPart[2], 'green'

        @page.flashAnswer answer[0], color, =>
            @page.score += 5 if correct
        
            if @question.length == 0
                return @sendAnswers @getQuestion
            
            @page.setAnswerPart(
                2 - @question.length,
                @currentPart[0],
                @currentPart[1][@currentPart[2]]
            )

            @currentPart = @question.shift()
            @lastStartTime = +new Date
            @page.setQuestionPart @currentPart, @onAnswer


    sendAnswers: (callback) =>
        ###
        Send answers to server.
        ###
        data = answer: @currentQuestionAnswers
        Quiz.post 'next', data, (json) =>
            if json['score'] != @page.score
                notEqual = "#{ @page.score } != #{ json['score'] }"
                Quiz.log "Warning",
                         "Client/Server score mismatch. #{ notEqual }"
                Quiz.log "Warning", "Using server's score."
                @page.score = json['score']
            
            if json['spotted']
                return @onSpotted callback

            callback() if callback?

    onSpotted: (callback) ->
        ###
        Called when server returns spotted=true.
        ###
        spotted = confirm("You answered it faster than last time." +
                          "\nCan you show the pattern?")
        
        Quiz.post 'next', spotted: spotted, (json) =>
            if not spotted
                 return callback() if callback?
                 return

            @currentQuestion = json['patterns']

            @page.z = ''
            @page.w = ''
            @page.clearAnswers()
            $('#quiz-question').hide()
            $('#quiz-data').hide()

            @page.setPossibleAnswers @currentQuestion, (i) =>
                @onSpottedAnswer i, callback

    onSpottedAnswer: (i, callback) ->
        ###
        When an answer is given for spotted question.
        ###
        Quiz.post 'next', answer: @currentQuestion[i], (json) =>
            @page.score = json['score']
            $('#quiz-question').show()
            $('#quiz-data').show()

            callback() if callback?

    onFinish: ->
        ###
        When the quiz has ended.
        ###
        name = prompt('Please enter your name:')
        path = $SCRIPT_ROOT + '/quiz/the_modulus/finish'

        form = $("<form>").attr "method", 'POST'
                          .attr "action", path

        nameInput = $("<input>").attr "type", "hidden"
                                .attr "name", "name"
                                .attr "value", name

        form.append nameInput

        form.appendTo $(document.body)
            .submit()

    # When the quiz object is ready, ask the user if they wish
    # to start.
    showStart: =>
        $(@page.msgWait).hide()
        @page.msgStart.onclick = @startQuiz
        $(@page.msgStart).fadeIn()
        Quiz.log "Ready!"

    startQuiz: =>
        ###
        When the start button is clicked.
        ###
        $(@page.msg).hide()
        $(@page.content).fadeIn()

    @post: (name, data, callback) ->
        $.ajax
            type: 'POST'
            url: $SCRIPT_ROOT + $SCRIPT_QUIZ_URLS[name]
            data: JSON.stringify(data)
            
            contentType: 'application/json'
            dataType: 'json'

            error: Quiz.showError
            success: callback


    # Get requests to quiz.
    @get: (name, callback) ->
        $.getJSON $SCRIPT_ROOT + $SCRIPT_QUIZ_URLS[name]
            .success callback
            .error @showError

    # Log data to console.
    @log: (options..., msg) ->
        options.unshift "Quiz"
        options.reverse()
        msg = "[" + option + "] " + msg for option in options
        console.log msg

    # For critical errors.
    @showError: (jqXHR, textStatus, errorThrown) ->
        json = jQuery.parseJSON jqXHR.responseText
        Quiz.log  "Error", json['error'], json['message']
        
        page = new QuizPageData
        page.content.style.display = 'none'
        page.msg.style.display  = 'none'
        page.msg.classList.add('hide', 'error')
        page.msg.innerHTML = ''

        errorText = document.createElement 'h1'
        errorText.innerHTML = "A critical error occurred!"
        
        page.msg.appendChild errorText
        page.msg.style.display = 'block'

    # Runs when page is loaded.
    @main: ->
        Quiz.get 'new', (json) ->
            window.quiz = new Quiz json['ID']

$ Quiz.main

