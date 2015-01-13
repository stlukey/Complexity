##!/usr/bin/env coffee
# -*- coding: UTF-8 -*-
###
    Complexity: quizzes/the_modulus.coffee
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    :copyright: (c) 2014 Luke Southam <luke@devthe.com>.
    :license: New BSD, see LICENSE for more details.
###

# Where to store quiz content.
$content = $('#quiz-content')

# Where score is displayed.
$score = $('#quiz-score-value')


class Quiz
    constructor: (@ID) ->
        console.log "Quiz ID: #{@ID}"

        @question = null
        @answered = false

        @getQuestion =>
            alert @w

    # @score is a property so the displayed score also gets updated
    # when set.
    Object.defineProperties @prototype,
        score:
            get: -> @_score
            set: (value) ->
                @_score = value
                $score.text value

    # Load next question.
    getQuestion: (callback) ->
        if @question? and not @answered
            return callback()

        Quiz.get 'next', (json) =>
            {w:@w, z:@z} = json['data']
            @question = json['question']
            callback()

    # Get requests to quiz.
    @get: (name, callback) ->
        $.getJSON $SCRIPT_ROOT + $SCRIPT_QUIZ_URLS[name]
            .success callback
            .error @showError

    # For critical errors.
    @showError: (jqXHR, textStatus, errorThrown) ->
        console.log "[Error] #{textStatus} #{errorThrown}"
        $content.empty()
        
        $div = $ '<div>', class: "center vcenter error"
        $h1 = $ '<h1>'
        
        $h1.text "A critical error occured!"
        $div.append $h1
        $content.append $div

    # Runs when page is loaded.
    @main: ->
        Quiz.get 'new', (json) ->
            new Quiz json['ID']

$ Quiz.main

