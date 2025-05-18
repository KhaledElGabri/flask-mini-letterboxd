# MINI LETTERBOXD

A web application that allows users to track movies they've watched and share reviews.

- What does it do?
  - This is a web project which tracks movies users have watched and allows them to write reviews for each movie.

- What is the "new feature" which you have implemented that we haven't seen before?
  - Movie tracking and a review system that allows users to create, edit, and delete their reviews.

## Prerequisites
- Flask web framework
- No additional modules needed beyond Python's standard library

## Project Checklist
- [x] It is available on GitHub.
- [x] It uses the Flask web framework.
- [x] It uses at least one module from the Python Standard Library other than the random module.
  - Module name: datetime, json
- [x] It contains at least one class written by you that has both properties and methods. It uses `__init__()` to let the class initialize the object's attributes (note that `__init__()` doesn't count as a method). This includes instantiating the class and using the methods in your app.
  - File name for the class definition: user.py
  - Line number(s) for the class definition: 3-11
  - Name of two properties: username, user_id
  - Name of two methods: marked_movies, unmarked_movies
  - File name and line numbers where the methods are used: routes/movie_routes.py, lines 79-81
- [x] It makes use of JavaScript in the front end and uses the localStorage of the web browser.
- [x] It uses modern JavaScript (for example, let and const rather than var).
- [x] It makes use of the reading and writing to the same file feature.
- [x] It contains conditional statements. Please provide below the file name and the line number(s) of at least one example of a conditional statement in your code.
  - File name: app.py
  - Line number(s): 35-41
- [x] It contains loops. Please provide below the file name and the line number(s) of at least one example of a loop in your code.
  - File name: user.py
  - Line number(s): 40-44
- [x] It lets the user enter a value in a text box at some point. This value is received and processed by your back end Python code.
- [x] It doesn't generate any error message even if the user enters a wrong input.
- [x] It is styled using your own CSS.
- [x] The code follows the code and style conventions as introduced in the course, is fully documented using comments and doesn't contain unused or experimental code. In particular, the code should not use `print()` or `console.log()` for any information the app user should see. Instead, all user feedback needs to be visible in the browser.
- [x] All exercises have been completed as per the requirements and pushed to the respective GitHub repository.