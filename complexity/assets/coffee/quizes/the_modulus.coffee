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
        @getId()

    getId: ->
        $.get '/quiz/the_modulus/new'
            .success (data) ->
                console.log "Quiz ID: #{data}"

            .error @showError

    showError: (jqXHR, textStatus, errorThrown) ->
        console.log "[Error] #{textStatus}"
        $("#quiz-content").empty()
        $("#quiz-content").append(
            $('<div class="center vcenter error"></div>').append(
                $('<h1></h1>').text("A critical error occured!")
            )
        )


    @main: -> new Quiz

$ Quiz.main

