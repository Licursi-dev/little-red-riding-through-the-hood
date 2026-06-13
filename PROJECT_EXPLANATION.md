little_red_engine.py – Game Logic Engine

Purpose

The little_red_engine.py file controls the main gameplay logic for Little Red Riding Through the Hood.

It stores the player’s progress, manages scenes, handles choices, updates lives, tracks inventory items and controls the route through the story.

How It Works

The game starts by creating a new game state.

The game state stores:

• Current location

• Number of lives

• Inventory items

• Story flags

• Last message shown to the player

• Return location after temporary messages

Each scene is split into two parts:

• A render function

• An apply function

The render function displays the story text and available choices.

The apply function handles the player’s selected choice and updates the game state.

Scene System

The game uses location names to decide which scene should be shown.

Examples include:

• home

• kitchen

• neighborhood

• school_entrance

• locker_combo

• classroom

• break_hub

• after_school_hub

• brad_confrontation

The step function acts as the central controller. It checks the current location, applies the player’s choice, then renders the next scene.

Game State

The player state includes lives, inventory and flags.

Lives are reduced when the player makes risky or dangerous choices.

Inventory items can unlock later options, such as collecting slingshot parts and assembling the slingshot.

Flags are used to remember important story events, such as meeting Lisa, warning signs about Brad, or whether the player has collected certain items.

Inventory System

The engine includes helper functions to add, remove and check inventory items.

These helpers prevent duplicate items and keep the game state organised.

Examples of inventory items include:

• Red hoodie

• Lunch money

• Rubber band

• Y-shaped wood

• Leather scraps

• Firecrackers

• Slingshot

Lives System

The player starts with three lives.

Dangerous decisions call the life-loss helper function.

If the player still has lives remaining, they are shown a warning message and returned to the story.

If lives reach zero, the game moves to the game over screen.

Ending System

The engine contains multiple endings based on player choices.

Different outcomes depend on the player’s route, inventory, and previous decisions.

This makes the game replayable because different choices can lead to different endings.

Why This Is Useful

The little_red_engine.py file separates the game logic from the web interface.

This makes the project easier to understand because the story, choices, inventory, lives and endings are all controlled in one place.

The file demonstrates branching logic, state management, reusable helper functions and interactive story design.



little_red_web.py – FastAPI Web Interface

Purpose

The little_red_web.py file connects the game engine to the browser.

It creates the FastAPI web application, displays the game interface, handles player choices, serves static assets and renders the current story scene as an HTML page.

This file acts as the bridge between the Python game logic and the visual web interface.

How It Works

The file starts a FastAPI application and mounts the static folder so that images can be loaded by the browser.

It imports the game engine functions:

• new_game_state

• step

The game begins by creating a new in-memory game state.

When the player opens the website, the app calls the engine, receives the current story text and choices, then builds an HTML page to display them.

FastAPI Application

The app is created using FastAPI.

The static folder is mounted so the game can display image files such as the Little Red character sprites.

The web app includes routes for:

• The main game page

• Player choice submission

• Game reset

• Instructions page

Game State

The file stores a simple in-memory game state called STATE.

This means the game remembers the player’s current progress while the server is running.

The state is updated each time the player chooses an option.

For a prototype project, this is a simple and effective way to manage gameplay without needing a database.

Page Rendering

The page function generates the main HTML interface.

It receives:

• The current game state

• The story text

• The available choices

It then builds the browser page dynamically.

This includes:

• The game title

• The retro prototype information

• The instructions link

• The lives display

• Inventory count

• Current location

• Story text

• Choice buttons

• Reset button

• Keyboard shortcut hints

• Character sprite

Escaping User-Facing Text

The file uses escape from Python’s html module.

This helps safely display text inside the generated HTML.

Story text, locations and choices are escaped before being inserted into the page.

This is useful because it reduces the risk of unexpected HTML being rendered as part of the page.

Choice Buttons

Each available choice is converted into a form button.

When the player clicks a choice:

• The selected option number is submitted

• FastAPI receives the POST request

• The game engine processes the choice

• The player is redirected back to the main page

This creates a simple turn-based interaction loop.

Keyboard Controls

The page includes JavaScript keyboard controls.

Players can use:

• Number keys 1–9 to choose options

• R to reset the game

This improves testing speed and makes the prototype easier to play.

Visual Styling

The file includes the game’s CSS inside a large CSS string.

The styling creates a retro arcade look using:

• Pixel-style font

• Neon-inspired colours

• Dark gradient background

• Grid overlay

• CRT-style panel

• Scanline effect

• Arcade-style buttons

• Hover effects

• Fixed character sprite

The design helps the game feel like a complete retro web experience rather than plain text on a page.

HUD System

The page includes a simple heads-up display.

The HUD shows:

• Lives

• Inventory count

• Current location

This is useful for both players and testers because it makes the internal game state visible during play.

Static Assets

The file serves images from the static folder.

The character sprite uses:

• stand.png

• walk.png

A simple CSS animation swaps between these images to create movement.

Routes

GET /

Loads the current game scene and displays it in the browser.

POST /choose

Receives the player’s selected choice, sends it to the game engine, then redirects back to the main page.

POST /reset

Creates a fresh game state and restarts the game.

GET /instructions

Loads instructions.html and displays the instructions page.

Why This File Is Important

little_red_web.py turns the Python game engine into a playable web application.

Without this file, the story engine would exist only as backend logic.

This file gives the project its browser interface, visual design, controls, routing and playable experience.

It demonstrates how Python and FastAPI can be used to build an interactive web-based game prototype.


instructions.html – Player Guide and Testing Documentation

Purpose

The instructions.html file provides a dedicated instructions page for players, testers and recruiters.

It explains the game’s story premise, controls, gameplay systems and testing routes without requiring users to discover everything through trial and error.

This page acts as the project’s built-in user guide.

How It Works

The page is a standalone HTML document served by the FastAPI application.

When a user clicks the Instructions button on the main game screen, the browser loads the instructions page through the /instructions route.

The page uses the same visual style as the main game to create a consistent experience.

Page Structure

The instructions page contains:

• Title section

• Back to Game navigation button

• Story introduction

• Gameplay instructions

• Lives explanation

• Inventory explanation

• Testing guidance

• Optional spoiler walkthrough

• Project footer

Story Introduction

The opening section introduces the game world.

Players learn that:

• The story takes place in Los Angeles in 1993

• Rival gangs influence daily life

• The player controls Little Red

• The main objectives involve survival, school life and social interactions

This provides context before the player begins the game.

Gameplay Instructions

The page explains how the game is played.

Players can:

• Click on choices

• Use number keys 1–9 to select options

• Press R to reset the game

This helps players understand the available controls immediately.

Lives System Documentation

The instructions page explains the lives mechanic.

Players begin with:

• Three lives

Dangerous decisions can reduce lives.

When all lives are lost, the game ends.

This section helps users understand the consequences of risky choices.

Inventory System Documentation

The inventory section explains that items are automatically tracked by the game.

Examples include:

• Red hoodie

• Rubber band

• Y-shaped wood

• Leather scraps

• Firecrackers

• Slingshot

The HUD displays the current inventory count so players can confirm item collection.

Play Session Overview

The page outlines the typical game progression:

• Home

• Neighborhood

• School

• Classroom

• After School

This gives players an understanding of the overall game structure without revealing major story outcomes.

Spoiler Walkthrough

An expandable spoiler section contains a recommended testing route.

This allows testers to:

• Verify inventory collection

• Test locker interactions

• Confirm life-loss mechanics

• Validate scene progression

The spoiler section remains hidden unless the user chooses to open it.

Visual Design

The page uses the same design language as the main game.

Features include:

• Pixel-art inspired typography

• Arcade colour palette

• CRT-style display panel

• Grid background

• Neon highlights

• Responsive layout

Maintaining visual consistency helps the instructions page feel like part of the game rather than a separate document.

Navigation

The page includes navigation links that allow users to:

• Return to the game

• Visit licursi.dev

This improves usability and makes testing easier.

Why This File Is Important

The instructions.html file improves the user experience by providing clear guidance before gameplay begins.

It reduces confusion, supports testing and helps demonstrate the project professionally by showing that user onboarding was considered during development.



requirements.txt – Project Dependencies

Purpose

The requirements.txt file lists the Python packages required to run Little Red Riding Through the Hood.

It allows other developers to install the correct dependencies quickly and ensures the project can be recreated on another machine.

Dependencies

fastapi

FastAPI is the web framework used to build the application.

It handles:

• Web routes

• Form submissions

• HTTP responses

• Page rendering

• Static file serving

The game uses FastAPI to connect the browser interface with the game engine.

uvicorn

Uvicorn is the ASGI server used to run the FastAPI application.

It provides the local development server and handles incoming web requests.

The game is launched using Uvicorn, which serves the application through the browser.

Installation

The dependencies can be installed using:

pip install -r requirements.txt

Running the Project

After installation, the application can be started with:

uvicorn little_red_web:app –reload

The –reload option automatically reloads the application when files are changed during development.

Why This File Is Important

The requirements.txt file ensures that anyone cloning the repository can install the correct packages and run the project without manually searching for dependencies.

It improves portability, reproducibility and project setup.


static/ – Character Sprite Assets

Purpose

The static folder contains image assets used by the web application.

These images are served by FastAPI and displayed directly in the browser.

Files

stand.png

The default character sprite.

This image represents Little Red standing still and is shown when the animation cycle begins.

walk.png

The alternate character sprite.

This image is used to create the illusion of movement by alternating between frames.

Animation System

The game uses a simple CSS animation to switch between the two sprite images.

The browser alternates between stand.png and walk.png at regular intervals, creating a basic walking animation effect.

This approach provides a lightweight animation system without requiring JavaScript game engines or sprite sheets.

Why This Is Useful

The sprite animation gives the interface more personality and helps reinforce the retro game aesthetic.

Although the gameplay is primarily text-based, the animated character provides a visual focal point and makes the application feel more interactive and game-like.


