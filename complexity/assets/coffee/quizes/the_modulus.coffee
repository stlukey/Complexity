##!/usr/bin/env coffee
# -*- coding: UTF-8 -*-
###
    Complexity: quiz.coffee
    ~~~~~~~~~~~~~~~~~~~~~~~
    Copyright: (c) 2014 Luke Southam <luke@devthe.com>.
    License: New BSD, see LICENSE for more details.
###

class Quiz
    constructor: ->
        @getID()

    getID: ->
        $.getJSON $SCRIPT_ROOT + $SCRIPT_QUIZ_URLS['new']
            .success @storeID

            .error @showError

    storeID: (data) ->
        @ID = data['ID']
        console.log "Quiz ID: #{@ID}"

    showError: (jqXHR, textStatus, errorThrown) ->
        console.log "[Error] #{textStatus} #{errorThrown}"
        $("#quiz-content").empty()
        $("#quiz-content").append(
            $('<div class="center vcenter error"></div>').append(
                $('<h1></h1>').text("A critical error occured!")
            )
        )

    @main: -> new Quiz

$ Quiz.main

