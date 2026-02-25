import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import json
import os
import random
import time
import threading
import hashlib
from datetime import datetime, date
import math

# ─── Optional audio support ──────────────────────────────────────────────────
try:
    from gtts import gTTS
    import tempfile, subprocess, sys
    AUDIO_AVAILABLE = True
except ImportError:
    AUDIO_AVAILABLE = False

# ═══════════════════════════════════════════════════════════════════════════════
#  DATA: CURRICULUM  (Python + JavaScript, expandable)
# ═══════════════════════════════════════════════════════════════════════════════

CURRICULUM = {
    "Python": {
        "icon": "🐍",
        "color": "#3572A5",
        "topics": [
            {
                "id": "py_basics",
                "title": "Python Basics",
                "emoji": "📌",
                "lesson": """Welcome to Python — one of the world's most popular programming languages!

Python was created by Guido van Rossum and first released in 1991. It is known for its clean, readable syntax that feels almost like plain English.

WHY PYTHON?
• Simple and beginner-friendly
• Used in web development, data science, AI, automation, and more
• Huge community and tons of free resources

YOUR FIRST PYTHON PROGRAM:
Every programmer's journey begins with printing "Hello, World!" to the screen.

  print("Hello, World!")

The print() function displays text on the screen. The text inside quotes is called a *string*.

VARIABLES:
A variable stores a value so you can use it later.

  name = "Alice"
  age = 20
  height = 5.6

• name is a string (text)
• age is an integer (whole number)
• height is a float (decimal number)

COMMENTS:
Lines starting with # are ignored by Python — they are notes for the programmer.

  # This is a comment
  print("This runs")  # inline comment

BASIC INPUT:
You can ask the user to type something:

  name = input("What is your name? ")
  print("Hello, " + name)

Python is case-sensitive: 'Name' and 'name' are different variables.
""",
                "examples": [
                    ("Print your name", 'print("My name is Alice")'),
                    ("Store and print a number", 'x = 42\nprint(x)'),
                    ("Simple addition", 'a = 10\nb = 5\nprint(a + b)'),
                    ("Get user input", 'name = input("Enter name: ")\nprint("Hi,", name)'),
                ],
                "quiz": [
                    {
                        "q": "Which function is used to display output in Python?",
                        "options": ["display()", "print()", "show()", "output()"],
                        "answer": 1,
                        "explanation": "print() is the built-in Python function to display output on the screen."
                    },
                    {
                        "q": "What symbol is used to write a comment in Python?",
                        "options": ["//", "/*", "#", "--"],
                        "answer": 2,
                        "explanation": "The # symbol starts a single-line comment in Python."
                    },
                    {
                        "q": "What is stored in: age = 25",
                        "options": ["A string", "A float", "An integer", "A boolean"],
                        "answer": 2,
                        "explanation": "25 is a whole number, so age is an integer variable."
                    },
                    {
                        "q": "Which of these is a valid variable name?",
                        "options": ["2name", "my-name", "my_name", "my name"],
                        "answer": 2,
                        "explanation": "Variable names can use letters, digits, and underscores, but cannot start with a digit or contain spaces/hyphens."
                    },
                    {
                        "q": "What does input() do?",
                        "options": ["Prints to screen", "Reads user keyboard input", "Opens a file", "Imports a module"],
                        "answer": 1,
                        "explanation": "input() pauses the program and waits for the user to type something."
                    },
                ]
            },
            {
                "id": "py_conditions",
                "title": "Conditions & Logic",
                "emoji": "🔀",
                "lesson": """CONDITIONAL STATEMENTS let your program make decisions.

IF / ELIF / ELSE:
The program checks a condition; if it is True, it runs that block.

  score = 85

  if score >= 90:
      print("Grade: A")
  elif score >= 75:
      print("Grade: B")
  elif score >= 60:
      print("Grade: C")
  else:
      print("Grade: F")

INDENTATION IS MANDATORY in Python! 4 spaces (or 1 tab) define a code block.

COMPARISON OPERATORS:
  ==   equal to
  !=   not equal to
  >    greater than
  <    less than
  >=   greater than or equal to
  <=   less than or equal to

LOGICAL OPERATORS:
  and   — both conditions must be True
  or    — at least one must be True
  not   — reverses True/False

  age = 20
  has_id = True

  if age >= 18 and has_id:
      print("You may enter.")

NESTED IF:
You can put an if inside another if:

  x = 15
  if x > 10:
      if x > 20:
          print("Very large")
      else:
          print("Medium")

TERNARY (one-line if):
  result = "Pass" if score >= 50 else "Fail"
""",
                "examples": [
                    ("Check positive/negative", 'n = int(input("Number: "))\nif n > 0:\n    print("Positive")\nelif n < 0:\n    print("Negative")\nelse:\n    print("Zero")'),
                    ("Login check", 'password = "secret"\nguess = input("Password: ")\nif guess == password:\n    print("Access granted")\nelse:\n    print("Wrong password")'),
                    ("Even or odd", 'n = int(input("Enter number: "))\nif n % 2 == 0:\n    print("Even")\nelse:\n    print("Odd")'),
                ],
                "quiz": [
                    {
                        "q": "What does == check?",
                        "options": ["Assignment", "Equality", "Greater than", "Not equal"],
                        "answer": 1,
                        "explanation": "== checks if two values are equal. = is for assignment."
                    },
                    {
                        "q": "What is required to define code blocks in Python?",
                        "options": ["{ }", "BEGIN/END", "Indentation", "Semicolons"],
                        "answer": 2,
                        "explanation": "Python uses indentation (spaces/tabs) to define blocks — not braces."
                    },
                    {
                        "q": "Which operator means 'and'?",
                        "options": ["&&", "and", "&", "AND"],
                        "answer": 1,
                        "explanation": "Python uses the keyword 'and' for logical AND."
                    },
                    {
                        "q": "What prints if x=5: print('Yes') if x>3 else print('No')",
                        "options": ["No", "Yes", "Error", "Nothing"],
                        "answer": 1,
                        "explanation": "5 > 3 is True, so 'Yes' is printed."
                    },
                    {
                        "q": "What does elif mean?",
                        "options": ["else if", "end loop if", "else loop", "extra if"],
                        "answer": 0,
                        "explanation": "elif is short for 'else if' — it checks another condition when the previous one was False."
                    },
                ]
            },
            {
                "id": "py_loops",
                "title": "Loops",
                "emoji": "🔁",
                "lesson": """LOOPS let you repeat actions without rewriting the same code.

FOR LOOP — iterate over a sequence:

  for i in range(5):
      print(i)
  # prints 0, 1, 2, 3, 4

  range(start, stop, step):
  range(1, 10, 2)  → 1, 3, 5, 7, 9

Loop over a list:
  fruits = ["apple", "banana", "cherry"]
  for fruit in fruits:
      print(fruit)

WHILE LOOP — repeat while condition is True:

  count = 0
  while count < 5:
      print(count)
      count += 1   # same as count = count + 1

BREAK & CONTINUE:
  break    — exit the loop immediately
  continue — skip current iteration, go to next

  for n in range(10):
      if n == 5:
          break       # stops at 5
      if n % 2 == 0:
          continue    # skips even numbers
      print(n)        # prints 1, 3

NESTED LOOPS:
  for row in range(3):
      for col in range(3):
          print(row, col)

LOOP WITH ELSE:
The else block runs when the loop finishes normally (no break):

  for i in range(3):
      print(i)
  else:
      print("Loop done!")
""",
                "examples": [
                    ("Sum 1 to 100", 'total = 0\nfor i in range(1, 101):\n    total += i\nprint("Sum:", total)'),
                    ("Multiplication table", 'n = 5\nfor i in range(1, 11):\n    print(f"{n} x {i} = {n*i}")'),
                    ("Countdown", 'count = 10\nwhile count > 0:\n    print(count)\n    count -= 1\nprint("Blast off!")'),
                    ("Find first even", 'for n in range(1, 20):\n    if n % 2 == 0:\n        print("First even:", n)\n        break'),
                ],
                "quiz": [
                    {
                        "q": "What does range(3) produce?",
                        "options": ["1, 2, 3", "0, 1, 2", "0, 1, 2, 3", "1, 2"],
                        "answer": 1,
                        "explanation": "range(3) generates 0, 1, 2 — it starts at 0 and stops before 3."
                    },
                    {
                        "q": "Which keyword exits a loop immediately?",
                        "options": ["stop", "exit", "break", "end"],
                        "answer": 2,
                        "explanation": "break immediately terminates the loop."
                    },
                    {
                        "q": "What does continue do?",
                        "options": ["Ends the loop", "Skips to next iteration", "Restarts loop", "Breaks out"],
                        "answer": 1,
                        "explanation": "continue skips the rest of the current iteration and moves to the next one."
                    },
                    {
                        "q": "How many times does this loop run: for i in range(2, 8, 2)",
                        "options": ["3", "4", "6", "2"],
                        "answer": 0,
                        "explanation": "range(2, 8, 2) gives 2, 4, 6 — three values."
                    },
                    {
                        "q": "A while loop runs as long as its condition is:",
                        "options": ["False", "True", "Zero", "None"],
                        "answer": 1,
                        "explanation": "A while loop continues executing while its condition evaluates to True."
                    },
                ]
            },
            {
                "id": "py_functions",
                "title": "Functions",
                "emoji": "⚙️",
                "lesson": """FUNCTIONS are reusable blocks of code that perform a specific task.

DEFINING A FUNCTION:
  def greet(name):
      print("Hello,", name)

  greet("Alice")   # calling the function → Hello, Alice
  greet("Bob")     # reuse it → Hello, Bob

RETURN VALUE:
  def add(a, b):
      return a + b

  result = add(3, 4)
  print(result)   # 7

DEFAULT PARAMETERS:
  def greet(name, greeting="Hello"):
      print(greeting + ", " + name)

  greet("Alice")           # Hello, Alice
  greet("Bob", "Hi")       # Hi, Bob

KEYWORD ARGUMENTS:
  def power(base, exponent):
      return base ** exponent

  print(power(exponent=3, base=2))   # 8

*ARGS (variable number of arguments):
  def add_all(*numbers):
      return sum(numbers)

  print(add_all(1, 2, 3, 4))   # 10

**KWARGS (keyword variable arguments):
  def info(**details):
      for key, val in details.items():
          print(key, ":", val)

  info(name="Alice", age=20)

SCOPE:
Variables inside a function are LOCAL — they don't exist outside.
Use global keyword to access global variables (use sparingly!).

LAMBDA (anonymous function):
  square = lambda x: x * x
  print(square(5))   # 25
""",
                "examples": [
                    ("Calculate area", 'def area(length, width):\n    return length * width\n\nprint(area(5, 3))   # 15'),
                    ("Factorial", 'def factorial(n):\n    if n == 0:\n        return 1\n    return n * factorial(n - 1)\n\nprint(factorial(5))   # 120'),
                    ("Check prime", 'def is_prime(n):\n    if n < 2:\n        return False\n    for i in range(2, int(n**0.5)+1):\n        if n % i == 0:\n            return False\n    return True\n\nprint(is_prime(17))   # True'),
                ],
                "quiz": [
                    {
                        "q": "Which keyword defines a function in Python?",
                        "options": ["function", "def", "func", "define"],
                        "answer": 1,
                        "explanation": "def is the keyword used to define a function in Python."
                    },
                    {
                        "q": "What does return do?",
                        "options": ["Prints a value", "Sends a value back to the caller", "Stops the program", "Loops back"],
                        "answer": 1,
                        "explanation": "return sends a value back from a function to wherever it was called."
                    },
                    {
                        "q": "What is a lambda function?",
                        "options": ["A loop function", "A class method", "An anonymous one-line function", "A built-in function"],
                        "answer": 2,
                        "explanation": "lambda creates a small anonymous function in a single expression."
                    },
                    {
                        "q": "What does *args allow?",
                        "options": ["Named arguments", "Variable number of positional arguments", "Only 2 arguments", "Default values"],
                        "answer": 1,
                        "explanation": "*args lets you pass any number of positional arguments to a function."
                    },
                    {
                        "q": "What is a local variable?",
                        "options": ["Available everywhere", "Only inside the function", "Stored in a file", "A global constant"],
                        "answer": 1,
                        "explanation": "Local variables are created inside a function and only exist within that function's scope."
                    },
                ]
            },
            {
                "id": "py_lists",
                "title": "Lists & Collections",
                "emoji": "📋",
                "lesson": """LISTS store multiple values in a single variable.

CREATING LISTS:
  fruits = ["apple", "banana", "cherry"]
  numbers = [1, 2, 3, 4, 5]
  mixed = [1, "hello", 3.14, True]

ACCESSING ITEMS (index starts at 0):
  print(fruits[0])    # apple
  print(fruits[-1])   # cherry (last item)

SLICING:
  print(numbers[1:4])  # [2, 3, 4]
  print(numbers[:3])   # [1, 2, 3]
  print(numbers[::2])  # [1, 3, 5] (every 2nd)

MODIFYING LISTS:
  fruits.append("mango")      # add to end
  fruits.insert(1, "grape")   # insert at index 1
  fruits.remove("banana")     # remove by value
  fruits.pop(0)                # remove by index
  fruits.sort()                # sort alphabetically
  fruits.reverse()             # reverse order

LIST METHODS:
  len(fruits)           # number of items
  fruits.count("apple") # how many times it appears
  fruits.index("cherry")# index of item
  "apple" in fruits     # True/False check

TUPLES (immutable lists):
  point = (3, 5)        # cannot be changed
  x, y = point          # unpacking

DICTIONARIES (key-value pairs):
  student = {"name": "Alice", "age": 20, "grade": "A"}
  print(student["name"])      # Alice
  student["score"] = 95       # add new key
  print(student.keys())       # all keys
  print(student.values())     # all values

SETS (unique values, no order):
  unique = {1, 2, 3, 2, 1}   # {1, 2, 3}

LIST COMPREHENSION (elegant way to create lists):
  squares = [x**2 for x in range(10)]
  evens   = [x for x in range(20) if x % 2 == 0]
""",
                "examples": [
                    ("Find max/min", 'nums = [3, 1, 4, 1, 5, 9, 2, 6]\nprint("Max:", max(nums))\nprint("Min:", min(nums))\nprint("Sum:", sum(nums))'),
                    ("Count words", 'sentence = "the cat sat on the mat"\nwords = sentence.split()\nword_count = {}\nfor w in words:\n    word_count[w] = word_count.get(w, 0) + 1\nprint(word_count)'),
                    ("List comprehension squares", 'squares = [x**2 for x in range(1, 6)]\nprint(squares)  # [1, 4, 9, 16, 25]'),
                ],
                "quiz": [
                    {
                        "q": "What index does the first item in a list have?",
                        "options": ["1", "-1", "0", "None"],
                        "answer": 2,
                        "explanation": "Python lists are zero-indexed, so the first item is at index 0."
                    },
                    {
                        "q": "Which method adds an item to the END of a list?",
                        "options": ["insert()", "add()", "append()", "push()"],
                        "answer": 2,
                        "explanation": "append() adds an item to the end of the list."
                    },
                    {
                        "q": "What is a dictionary in Python?",
                        "options": ["Ordered numbers", "Key-value pairs", "Unique items set", "Immutable list"],
                        "answer": 1,
                        "explanation": "A dictionary stores data as key-value pairs, like a real dictionary mapping words to definitions."
                    },
                    {
                        "q": "What does fruits[-1] return?",
                        "options": ["Error", "First item", "Last item", "Nothing"],
                        "answer": 2,
                        "explanation": "Negative indexing in Python: -1 refers to the last item."
                    },
                    {
                        "q": "What does a set guarantee?",
                        "options": ["Sorted order", "No duplicates", "Mutable items", "String only"],
                        "answer": 1,
                        "explanation": "A set only stores unique values — duplicates are automatically removed."
                    },
                ]
            },
        ]
    },
    "JavaScript": {
        "icon": "🌐",
        "color": "#f7df1e",
        "topics": [
            {
                "id": "js_basics",
                "title": "JavaScript Basics",
                "emoji": "🟡",
                "lesson": """JavaScript is the language of the web! It runs in every browser and makes websites interactive.

HISTORY:
Created by Brendan Eich in just 10 days in 1995, JavaScript has grown to be the most used programming language in the world.

VARIABLES:
Three ways to declare variables:
  var   name = "Alice";   // old way (avoid)
  let   age  = 20;        // modern, can change
  const PI   = 3.14159;   // constant, cannot change

Always end statements with semicolons (;) — it's good practice.

DATA TYPES:
  let text    = "Hello";          // String
  let number  = 42;               // Number
  let decimal = 3.14;             // Number (no float/int split)
  let isTrue  = true;             // Boolean
  let nothing = null;             // Null (intentionally empty)
  let undef   = undefined;        // Undefined (not yet assigned)

OUTPUT:
  console.log("Hello, World!");   // browser console
  alert("Hello!");                 // popup box (browser)
  document.write("Hello");        // write to webpage

TEMPLATE LITERALS (backtick strings):
  let name = "Alice";
  let msg  = `Hello, ${name}! You are ${age} years old.`;
  console.log(msg);

STRING METHODS:
  let s = "Hello World";
  s.length           // 11
  s.toUpperCase()    // "HELLO WORLD"
  s.toLowerCase()    // "hello world"
  s.includes("World") // true
  s.replace("World", "JS")  // "Hello JS"
  s.split(" ")       // ["Hello", "World"]

TYPE CONVERSION:
  Number("42")      // 42
  String(42)        // "42"
  Boolean(0)        // false
  parseInt("42px")  // 42
""",
                "examples": [
                    ("Greeting", 'let name = "Alice";\nlet age = 20;\nconsole.log(`Hi ${name}, you are ${age} years old!`);'),
                    ("Math operations", 'let a = 10, b = 3;\nconsole.log(a + b);  // 13\nconsole.log(a - b);  // 7\nconsole.log(a * b);  // 30\nconsole.log(a / b);  // 3.33\nconsole.log(a % b);  // 1 (remainder)\nconsole.log(a ** b); // 1000 (power)'),
                    ("String template", 'let product = "Laptop";\nlet price = 999;\nconsole.log(`The ${product} costs $${price}.`);'),
                ],
                "quiz": [
                    {
                        "q": "Which keyword declares a constant in JavaScript?",
                        "options": ["var", "let", "const", "fixed"],
                        "answer": 2,
                        "explanation": "const declares a variable whose value cannot be reassigned."
                    },
                    {
                        "q": "How do you print to the browser console?",
                        "options": ["print()", "echo()", "console.log()", "System.out.println()"],
                        "answer": 2,
                        "explanation": "console.log() is the standard way to output messages to the browser's developer console."
                    },
                    {
                        "q": "What symbol starts a template literal?",
                        "options": ["'", '"', "`", "#"],
                        "answer": 2,
                        "explanation": "Template literals use backticks (`) and allow ${} expressions inside."
                    },
                    {
                        "q": "In JS, are integer and float different types?",
                        "options": ["Yes, always", "No, both are 'Number'", "Only in strict mode", "Depends on browser"],
                        "answer": 1,
                        "explanation": "JavaScript has only one numeric type: Number. It handles both integers and decimals."
                    },
                    {
                        "q": "What does let vs var differ in?",
                        "options": ["Speed", "Block scope vs function scope", "Syntax only", "Nothing"],
                        "answer": 1,
                        "explanation": "let is block-scoped (confined to the nearest {} block), while var is function-scoped."
                    },
                ]
            },
            {
                "id": "js_functions",
                "title": "Functions & Scope",
                "emoji": "⚡",
                "lesson": """FUNCTIONS in JavaScript — multiple ways to write them!

FUNCTION DECLARATION:
  function greet(name) {
      return "Hello, " + name + "!";
  }
  console.log(greet("Alice"));

FUNCTION EXPRESSION:
  const greet = function(name) {
      return "Hello, " + name;
  };

ARROW FUNCTIONS (modern, concise):
  const greet = (name) => "Hello, " + name;
  const add   = (a, b) => a + b;
  const square = x => x * x;    // single param: no ()

DEFAULT PARAMETERS:
  function greet(name = "stranger") {
      return `Hello, ${name}!`;
  }
  greet()         // Hello, stranger!
  greet("Alice")  // Hello, Alice!

REST PARAMETERS:
  function sum(...numbers) {
      return numbers.reduce((a, b) => a + b, 0);
  }
  sum(1, 2, 3, 4)  // 10

HIGHER-ORDER FUNCTIONS:
Functions that take or return other functions.

  const numbers = [1, 2, 3, 4, 5];

  numbers.map(x => x * 2)     // [2, 4, 6, 8, 10]
  numbers.filter(x => x > 2)  // [3, 4, 5]
  numbers.reduce((a, b) => a + b, 0)  // 15

CLOSURES:
A function that remembers its outer variables:

  function counter() {
      let count = 0;
      return () => ++count;
  }
  const next = counter();
  next()  // 1
  next()  // 2

SCOPE:
  let x = "global";
  function test() {
      let x = "local";   // different x
      console.log(x);    // local
  }
  test();
  console.log(x);        // global
""",
                "examples": [
                    ("Arrow functions", 'const multiply = (a, b) => a * b;\nconst square   = x => x ** 2;\n\nconsole.log(multiply(3, 4));  // 12\nconsole.log(square(5));       // 25'),
                    ("Map, filter, reduce", 'const nums = [1, 2, 3, 4, 5, 6];\n\nconst doubled  = nums.map(n => n * 2);\nconst evens    = nums.filter(n => n % 2 === 0);\nconst total    = nums.reduce((sum, n) => sum + n, 0);\n\nconsole.log(doubled);  // [2,4,6,8,10,12]\nconsole.log(evens);    // [2,4,6]\nconsole.log(total);    // 21'),
                ],
                "quiz": [
                    {
                        "q": "What is the arrow function syntax for: function add(a,b){ return a+b; }",
                        "options": ["add = a,b -> a+b", "const add = (a,b) => a+b;", "add => (a,b) { a+b }", "func add(a,b)=>a+b"],
                        "answer": 1,
                        "explanation": "Arrow function: const add = (a, b) => a + b; — concise, modern syntax."
                    },
                    {
                        "q": "What does .map() do to an array?",
                        "options": ["Filters items", "Sorts items", "Creates new array transforming each item", "Finds one item"],
                        "answer": 2,
                        "explanation": "map() applies a function to each element and returns a new array of results."
                    },
                    {
                        "q": "What is a closure?",
                        "options": ["Closing a browser tab", "A function remembering its outer scope", "A loop that ends", "A try-catch block"],
                        "answer": 1,
                        "explanation": "A closure is a function that retains access to variables from its outer (enclosing) scope."
                    },
                    {
                        "q": "What does .filter() return?",
                        "options": ["The first match", "A new array of items passing the test", "true/false", "The index"],
                        "answer": 1,
                        "explanation": "filter() returns a new array containing only the elements that pass the provided test function."
                    },
                    {
                        "q": "Which parameter syntax accepts any number of arguments?",
                        "options": ["function f(args)", "function f(..args)", "function f(...args)", "function f(*args)"],
                        "answer": 2,
                        "explanation": "The rest parameter ...args collects all extra arguments into an array."
                    },
                ]
            },
            {
                "id": "js_dom",
                "title": "DOM & Events",
                "emoji": "🌐",
                "lesson": """The DOM (Document Object Model) is how JavaScript interacts with HTML.

SELECTING ELEMENTS:
  document.getElementById("myId")
  document.querySelector(".myClass")    // first match
  document.querySelectorAll("p")        // all <p> elements

CHANGING CONTENT:
  const heading = document.getElementById("title");
  heading.textContent = "New Title";    // just text
  heading.innerHTML   = "<b>Bold!</b>"; // HTML allowed

CHANGING STYLES:
  const box = document.querySelector(".box");
  box.style.backgroundColor = "blue";
  box.style.fontSize = "24px";
  box.classList.add("active");
  box.classList.remove("hidden");
  box.classList.toggle("visible");

CREATING ELEMENTS:
  const newPara = document.createElement("p");
  newPara.textContent = "I was added by JS!";
  document.body.appendChild(newPara);

EVENTS:
React to user actions (clicks, typing, hovering, etc.)

  const btn = document.getElementById("myBtn");

  btn.addEventListener("click", function() {
      alert("Button clicked!");
  });

  // Arrow function shorthand:
  btn.addEventListener("click", () => {
      console.log("Clicked!");
  });

COMMON EVENTS:
  click         — mouse click
  dblclick      — double click
  mouseover     — hover
  keydown       — key pressed
  keyup         — key released
  change        — input value changed
  submit        — form submitted
  load          — page finished loading

EVENT OBJECT:
  document.addEventListener("keydown", (event) => {
      console.log(event.key);   // which key was pressed
  });

FORM HANDLING:
  const input = document.getElementById("nameInput");
  const value = input.value;    // get typed text
""",
                "examples": [
                    ("Color changer button", '// HTML: <button id="btn">Click Me</button>\nconst btn = document.getElementById("btn");\nconst colors = ["red","blue","green","purple"];\nlet i = 0;\nbtn.addEventListener("click", () => {\n    document.body.style.backgroundColor = colors[i % colors.length];\n    i++;\n});'),
                    ("Live character counter", '// HTML: <textarea id="txt"></textarea>\nconst txt = document.getElementById("txt");\ntxt.addEventListener("input", () => {\n    console.log("Characters:", txt.value.length);\n});'),
                ],
                "quiz": [
                    {
                        "q": "What does document.querySelector() do?",
                        "options": ["Creates HTML", "Selects first matching element", "Adds an event", "Changes style"],
                        "answer": 1,
                        "explanation": "querySelector() returns the first element that matches the given CSS selector."
                    },
                    {
                        "q": "How do you add a click listener?",
                        "options": ["element.onClick(fn)", "element.on('click', fn)", "element.addEventListener('click', fn)", "element.listen('click', fn)"],
                        "answer": 2,
                        "explanation": "addEventListener() is the modern standard for attaching event listeners."
                    },
                    {
                        "q": "What is the difference between textContent and innerHTML?",
                        "options": ["No difference", "textContent treats as plain text; innerHTML parses HTML", "innerHTML is faster", "textContent is deprecated"],
                        "answer": 1,
                        "explanation": "textContent sets/gets text only; innerHTML allows embedding HTML tags."
                    },
                    {
                        "q": "What does classList.toggle() do?",
                        "options": ["Always adds class", "Always removes class", "Adds if absent, removes if present", "Checks if class exists"],
                        "answer": 2,
                        "explanation": "toggle() adds the class if it doesn't exist, removes it if it does."
                    },
                    {
                        "q": "What event fires when a key is pressed down?",
                        "options": ["keypress", "keydown", "keyup", "keyhit"],
                        "answer": 1,
                        "explanation": "keydown fires when a key is first pressed down."
                    },
                ]
            },
        ]
    },
}

# Translations (minimal but functional)
TRANSLATIONS = {
    "en": {
        "app_title": "LearnSphere",
        "tagline": "AI-Powered Personalized Learning",
        "welcome": "Welcome back",
        "start": "Start Learning",
        "register": "Register",
        "login": "Login",
        "logout": "Logout",
        "choose_language": "Choose a Programming Language",
        "topics": "Topics",
        "lesson": "Lesson",
        "examples": "Examples",
        "quiz": "Quiz",
        "next": "Next →",
        "prev": "← Back",
        "submit": "Submit Answer",
        "correct": "✅ Correct!",
        "wrong": "❌ Wrong!",
        "score": "Score",
        "progress": "Progress",
        "settings": "Settings",
        "audio": "Read Aloud",
        "stop_audio": "Stop Audio",
        "dashboard": "Dashboard",
        "name_label": "Your Name",
        "username_label": "Username",
        "password_label": "Password",
        "confirm_pass": "Confirm Password",
        "already_acc": "Already have an account? Login",
        "no_acc": "No account? Register",
        "select_lang_ui": "Interface Language",
        "quiz_result": "Quiz Complete!",
        "weak": "Needs Practice",
        "average": "Average",
        "good": "Good Job!",
        "excellent": "Excellent!",
        "study_plan": "Study Plan",
        "continue": "Continue",
        "topic_complete": "Topic Complete! 🎉",
        "congratulations": "Congratulations",
        "all_done": "You've completed all topics!",
        "hint": "Hint",
        "explanation": "Explanation",
    },
    "ta": {
        "app_title": "லர்ன்ஸ்பியர்",
        "tagline": "AI சக்தி கொண்ட தனிப்பயன் கற்றல்",
        "welcome": "மீண்டும் வரவேற்கிறோம்",
        "start": "கற்றலை தொடங்கு",
        "register": "பதிவு செய்",
        "login": "உள்நுழை",
        "logout": "வெளியேறு",
        "choose_language": "நிரலாக்க மொழியை தேர்ந்தெடு",
        "topics": "தலைப்புகள்",
        "lesson": "பாடம்",
        "examples": "எடுத்துக்காட்டுகள்",
        "quiz": "வினாடி வினா",
        "next": "அடுத்து →",
        "prev": "← பின்",
        "submit": "பதில் சமர்ப்பி",
        "correct": "✅ சரி!",
        "wrong": "❌ தவறு!",
        "score": "மதிப்பெண்",
        "progress": "முன்னேற்றம்",
        "settings": "அமைப்புகள்",
        "audio": "சத்தமாக படி",
        "stop_audio": "ஆடியோ நிறுத்து",
        "dashboard": "டாஷ்போர்டு",
        "name_label": "உங்கள் பெயர்",
        "username_label": "பயனர்பெயர்",
        "password_label": "கடவுச்சொல்",
        "confirm_pass": "கடவுச்சொல் உறுதி",
        "already_acc": "கணக்கு உள்ளதா? உள்நுழை",
        "no_acc": "கணக்கு இல்லையா? பதிவு செய்",
        "select_lang_ui": "இடைமுக மொழி",
        "quiz_result": "வினாடி வினா முடிந்தது!",
        "weak": "மேலும் பயிற்சி தேவை",
        "average": "சராசரி",
        "good": "நல்லது!",
        "excellent": "அருமை!",
        "study_plan": "படிப்பு திட்டம்",
        "continue": "தொடர்",
        "topic_complete": "தலைப்பு முடிந்தது! 🎉",
        "congratulations": "வாழ்த்துக்கள்",
        "all_done": "அனைத்து தலைப்புகளும் முடிந்தன!",
        "hint": "குறிப்பு",
        "explanation": "விளக்கம்",
    },
    "hi": {
        "app_title": "लर्नस्फेयर",
        "tagline": "AI-संचालित व्यक्तिगत शिक्षा",
        "welcome": "वापस स्वागत है",
        "start": "सीखना शुरू करें",
        "register": "पंजीकरण करें",
        "login": "लॉगिन करें",
        "logout": "लॉगआउट",
        "choose_language": "प्रोग्रामिंग भाषा चुनें",
        "topics": "विषय",
        "lesson": "पाठ",
        "examples": "उदाहरण",
        "quiz": "प्रश्नोत्तरी",
        "next": "आगे →",
        "prev": "← पीछे",
        "submit": "उत्तर जमा करें",
        "correct": "✅ सही!",
        "wrong": "❌ गलत!",
        "score": "स्कोर",
        "progress": "प्रगति",
        "settings": "सेटिंग्स",
        "audio": "जोर से पढ़ें",
        "stop_audio": "ऑडियो रोकें",
        "dashboard": "डैशबोर्ड",
        "name_label": "आपका नाम",
        "username_label": "यूज़रनेम",
        "password_label": "पासवर्ड",
        "confirm_pass": "पासवर्ड पुष्टि",
        "already_acc": "खाता है? लॉगिन करें",
        "no_acc": "खाता नहीं? पंजीकरण करें",
        "select_lang_ui": "इंटरफेस भाषा",
        "quiz_result": "प्रश्नोत्तरी पूर्ण!",
        "weak": "अभ्यास करें",
        "average": "औसत",
        "good": "अच्छा!",
        "excellent": "उत्कृष्ट!",
        "study_plan": "अध्ययन योजना",
        "continue": "जारी रखें",
        "topic_complete": "विषय पूर्ण! 🎉",
        "congratulations": "बधाई",
        "all_done": "सभी विषय पूर्ण!",
        "hint": "संकेत",
        "explanation": "स्पष्टीकरण",
    },
    "ar": {
        "app_title": "ليرن سفير",
        "tagline": "تعلم شخصي مدعوم بالذكاء الاصطناعي",
        "welcome": "مرحباً بعودتك",
        "start": "ابدأ التعلم",
        "register": "سجّل",
        "login": "تسجيل الدخول",
        "logout": "تسجيل الخروج",
        "choose_language": "اختر لغة البرمجة",
        "topics": "المواضيع",
        "lesson": "الدرس",
        "examples": "أمثلة",
        "quiz": "اختبار",
        "next": "التالي →",
        "prev": "→ السابق",
        "submit": "أرسل الإجابة",
        "correct": "✅ صحيح!",
        "wrong": "❌ خطأ!",
        "score": "النتيجة",
        "progress": "التقدم",
        "settings": "الإعدادات",
        "audio": "اقرأ بصوت عالٍ",
        "stop_audio": "إيقاف الصوت",
        "dashboard": "لوحة التحكم",
        "name_label": "اسمك",
        "username_label": "اسم المستخدم",
        "password_label": "كلمة المرور",
        "confirm_pass": "تأكيد كلمة المرور",
        "already_acc": "لديك حساب؟ تسجيل الدخول",
        "no_acc": "ليس لديك حساب؟ سجّل",
        "select_lang_ui": "لغة الواجهة",
        "quiz_result": "اكتمل الاختبار!",
        "weak": "تحتاج تدريباً",
        "average": "متوسط",
        "good": "جيد!",
        "excellent": "ممتاز!",
        "study_plan": "خطة الدراسة",
        "continue": "تابع",
        "topic_complete": "اكتمل الموضوع! 🎉",
        "congratulations": "تهانينا",
        "all_done": "أتممت جميع المواضيع!",
        "hint": "تلميح",
        "explanation": "شرح",
    },
    "fr": {
        "app_title": "LearnSphere",
        "tagline": "Apprentissage personnalisé par IA",
        "welcome": "Bon retour",
        "start": "Commencer à apprendre",
        "register": "S'inscrire",
        "login": "Connexion",
        "logout": "Déconnexion",
        "choose_language": "Choisir un langage",
        "topics": "Sujets",
        "lesson": "Leçon",
        "examples": "Exemples",
        "quiz": "Quiz",
        "next": "Suivant →",
        "prev": "← Retour",
        "submit": "Soumettre la réponse",
        "correct": "✅ Correct!",
        "wrong": "❌ Faux!",
        "score": "Score",
        "progress": "Progrès",
        "settings": "Paramètres",
        "audio": "Lire à voix haute",
        "stop_audio": "Arrêter l'audio",
        "dashboard": "Tableau de bord",
        "name_label": "Votre nom",
        "username_label": "Nom d'utilisateur",
        "password_label": "Mot de passe",
        "confirm_pass": "Confirmer mot de passe",
        "already_acc": "Déjà un compte? Connexion",
        "no_acc": "Pas de compte? S'inscrire",
        "select_lang_ui": "Langue interface",
        "quiz_result": "Quiz terminé!",
        "weak": "Besoin de pratique",
        "average": "Moyen",
        "good": "Bien!",
        "excellent": "Excellent!",
        "study_plan": "Plan d'études",
        "continue": "Continuer",
        "topic_complete": "Sujet terminé! 🎉",
        "congratulations": "Félicitations",
        "all_done": "Tous les sujets complétés!",
        "hint": "Indice",
        "explanation": "Explication",
    },
}

# Background themes (topic-related colors)
THEMES = {
    "default":   {"bg": "#0f0f23", "bg2": "#1a1a3e", "fg": "#e8e8ff", "accent": "#7c6af7", "btn": "#4f46e5", "btn_hover": "#6366f1", "code": "#1e1e2e", "success": "#22c55e", "error": "#ef4444", "warning": "#f59e0b"},
    "Python":    {"bg": "#0d1117", "bg2": "#161b22", "fg": "#c9d1d9", "accent": "#3572A5", "btn": "#238636", "btn_hover": "#2ea043", "code": "#0d1117", "success": "#56d364", "error": "#f85149", "warning": "#e3b341"},
    "JavaScript":{"bg": "#1a1400", "bg2": "#2a2000", "fg": "#f0e6c0", "accent": "#f7df1e", "btn": "#b8860b", "btn_hover": "#d4a017", "code": "#1e1a00", "success": "#86efac", "error": "#fca5a5", "warning": "#fbbf24"},
    "quiz":      {"bg": "#0c0f1a", "bg2": "#131929", "fg": "#dde6ff", "accent": "#818cf8", "btn": "#4f46e5", "btn_hover": "#6366f1", "code": "#1e2235", "success": "#4ade80", "error": "#f87171", "warning": "#fbbf24"},
    "success":   {"bg": "#052e16", "bg2": "#064e3b", "fg": "#d1fae5", "accent": "#34d399", "btn": "#059669", "btn_hover": "#10b981", "code": "#022c22", "success": "#6ee7b7", "error": "#fca5a5", "warning": "#fde68a"},
}

DATA_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "learnsphere_data.json")

# ═══════════════════════════════════════════════════════════════════════════════
#  DATA PERSISTENCE
# ═══════════════════════════════════════════════════════════════════════════════

def load_data():
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r") as f:
                return json.load(f)
        except:
            pass
    return {"users": {}}

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)

def hash_password(pw):
    return hashlib.sha256(pw.encode()).hexdigest()

# ═══════════════════════════════════════════════════════════════════════════════
#  MAIN APPLICATION
# ═══════════════════════════════════════════════════════════════════════════════

class LearnSphere:
    def __init__(self, root):
        self.root = root
        self.root.title("LearnSphere — AI Personalized Learning")
        self.root.geometry("1100x720")
        self.root.minsize(900, 600)

        self.data = load_data()
        self.current_user = None
        self.ui_lang = "en"
        self.theme_name = "default"
        self.theme = THEMES["default"]
        self.audio_thread = None
        self.audio_stop = False

        # State
        self.selected_prog_lang = None
        self.current_topic_idx = 0
        self.current_view = "auth"       # auth | dashboard | lesson | quiz | results
        self.quiz_answers = []
        self.quiz_current_q = 0
        self.audio_lines = []
        self.audio_idx = 0

        self._build_root()
        self.show_auth()

    # ── Helpers ──────────────────────────────────────────────────────────────

    def T(self, key):
        lang = self.ui_lang
        return TRANSLATIONS.get(lang, TRANSLATIONS["en"]).get(key, TRANSLATIONS["en"].get(key, key))

    def apply_theme(self, theme_name="default"):
        self.theme_name = theme_name
        self.theme = THEMES.get(theme_name, THEMES["default"])
        self.root.configure(bg=self.theme["bg"])
        self._refresh_theme(self.root)

    def _refresh_theme(self, widget):
        t = self.theme
        try:
            cls = widget.winfo_class()
            if cls in ("Frame", "Toplevel"):
                widget.configure(bg=t["bg"])
            elif cls == "Label":
                widget.configure(bg=t["bg"], fg=t["fg"])
            elif cls == "Button":
                widget.configure(bg=t["btn"], fg="white", activebackground=t["btn_hover"])
            elif cls == "Text":
                widget.configure(bg=t["code"], fg=t["fg"])
            elif cls == "Entry":
                widget.configure(bg=t["bg2"], fg=t["fg"], insertbackground=t["fg"])
        except:
            pass
        for child in widget.winfo_children():
            self._refresh_theme(child)

    def _build_root(self):
        self.root.configure(bg=self.theme["bg"])
        self.main_frame = tk.Frame(self.root, bg=self.theme["bg"])
        self.main_frame.pack(fill="both", expand=True)

    def clear(self):
        for w in self.main_frame.winfo_children():
            w.destroy()

    def make_btn(self, parent, text, cmd, size=12, width=None, color=None):
        t = self.theme
        c = color or t["btn"]
        kw = {"text": text, "command": cmd, "bg": c, "fg": "white",
              "font": ("Courier", size, "bold"), "relief": "flat",
              "cursor": "hand2", "activebackground": t["btn_hover"],
              "activeforeground": "white", "padx": 14, "pady": 6,
              "bd": 0}
        if width:
            kw["width"] = width
        btn = tk.Button(parent, **kw)
        btn.bind("<Enter>", lambda e: btn.config(bg=t["btn_hover"]))
        btn.bind("<Leave>", lambda e: btn.config(bg=c))
        return btn

    def make_label(self, parent, text, size=12, bold=False, color=None, bg=None):
        t = self.theme
        style = "bold" if bold else "normal"
        fg = color or t["fg"]
        bg_ = bg or t["bg"]
        return tk.Label(parent, text=text, bg=bg_, fg=fg,
                        font=("Courier", size, style))

    def make_entry(self, parent, show=None, width=30):
        t = self.theme
        e = tk.Entry(parent, bg=t["bg2"], fg=t["fg"],
                     insertbackground=t["fg"], relief="flat",
                     font=("Courier", 12), bd=5, width=width)
        if show:
            e.config(show=show)
        return e

    def divider(self, parent, color=None):
        t = self.theme
        c = color or t["accent"]
        f = tk.Frame(parent, bg=c, height=2)
        f.pack(fill="x", pady=4)
        return f

    # ── USER PROGRESS HELPERS ────────────────────────────────────────────────

    def get_progress(self):
        u = self.data["users"].get(self.current_user, {})
        return u.get("progress", {})

    def set_topic_score(self, prog_lang, topic_id, score, total):
        u = self.data["users"].setdefault(self.current_user, {})
        p = u.setdefault("progress", {})
        p[f"{prog_lang}:{topic_id}"] = {"score": score, "total": total, "date": str(date.today())}
        save_data(self.data)

    def topic_done(self, prog_lang, topic_id):
        p = self.get_progress()
        return f"{prog_lang}:{topic_id}" in p

    def total_topics(self):
        return sum(len(v["topics"]) for v in CURRICULUM.values())

    def done_topics(self):
        return len(self.get_progress())

    # ══════════════════════════════════════════════════════════════════════════
    #  AUTH SCREEN
    # ══════════════════════════════════════════════════════════════════════════

    def show_auth(self, mode="login"):
        self.apply_theme("default")
        self.clear()
        t = self.theme

        # Canvas gradient-ish background
        canvas = tk.Canvas(self.main_frame, bg=t["bg"], highlightthickness=0)
        canvas.pack(fill="both", expand=True)

        # Language selector top-right
        lang_frame = tk.Frame(canvas, bg=t["bg"])
        lang_frame.place(relx=1.0, x=-10, y=10, anchor="ne")
        tk.Label(lang_frame, text="🌍", bg=t["bg"], fg=t["fg"], font=("Arial", 12)).pack(side="left")
        lang_var = tk.StringVar(value=self.ui_lang)
        lang_opts = ["en", "ta", "hi", "fr", "ar"]
        lang_cb = ttk.Combobox(lang_frame, textvariable=lang_var, values=lang_opts, width=5, state="readonly")
        lang_cb.pack(side="left", padx=4)
        def on_lang_change(e):
            self.ui_lang = lang_var.get()
            self.show_auth(mode)
        lang_cb.bind("<<ComboboxSelected>>", on_lang_change)

        # Center box
        center = tk.Frame(canvas, bg=t["bg2"], relief="flat", padx=40, pady=40)
        center.place(relx=0.5, rely=0.5, anchor="center")

        # Logo
        logo_frame = tk.Frame(center, bg=t["bg2"])
        logo_frame.pack(pady=(0, 10))
        tk.Label(logo_frame, text="🧠", bg=t["bg2"], font=("Arial", 48)).pack()
        tk.Label(logo_frame, text=self.T("app_title"),
                 bg=t["bg2"], fg=t["accent"],
                 font=("Courier", 28, "bold")).pack()
        tk.Label(logo_frame, text=self.T("tagline"),
                 bg=t["bg2"], fg=t["fg"],
                 font=("Courier", 11)).pack(pady=(4, 0))

        self.divider(center, t["accent"])

        # Form
        form = tk.Frame(center, bg=t["bg2"])
        form.pack(pady=10)

        entries = {}

        if mode == "register":
            for lbl, key, show in [
                (self.T("name_label"), "name", None),
                (self.T("username_label"), "user", None),
                (self.T("password_label"), "pass", "•"),
                (self.T("confirm_pass"), "pass2", "•"),
            ]:
                tk.Label(form, text=lbl, bg=t["bg2"], fg=t["fg"],
                         font=("Courier", 11)).pack(anchor="w")
                e = self.make_entry(form, show=show)
                e.pack(pady=4, fill="x")
                entries[key] = e
        else:
            for lbl, key, show in [
                (self.T("username_label"), "user", None),
                (self.T("password_label"), "pass", "•"),
            ]:
                tk.Label(form, text=lbl, bg=t["bg2"], fg=t["fg"],
                         font=("Courier", 11)).pack(anchor="w")
                e = self.make_entry(form, show=show)
                e.pack(pady=4, fill="x")
                entries[key] = e

        self.divider(center, t["accent"])

        msg_lbl = tk.Label(center, text="", bg=t["bg2"], fg=t["error"],
                           font=("Courier", 10))
        msg_lbl.pack()

        if mode == "login":
            def do_login():
                u = entries["user"].get().strip()
                p = entries["pass"].get()
                if not u or not p:
                    msg_lbl.config(text="Please fill all fields.")
                    return
                if u not in self.data["users"]:
                    msg_lbl.config(text="User not found.")
                    return
                if self.data["users"][u]["password"] != hash_password(p):
                    msg_lbl.config(text="Wrong password.")
                    return
                self.current_user = u
                self.ui_lang = self.data["users"][u].get("ui_lang", "en")
                self.show_dashboard()

            self.make_btn(center, self.T("login"), do_login, size=13, width=20).pack(pady=8)
            self.make_btn(center, self.T("no_acc"), lambda: self.show_auth("register"),
                          size=10, color=t["bg"]).pack()
        else:
            def do_register():
                name = entries["name"].get().strip()
                u = entries["user"].get().strip()
                p = entries["pass"].get()
                p2 = entries["pass2"].get()
                if not all([name, u, p, p2]):
                    msg_lbl.config(text="Fill all fields.")
                    return
                if p != p2:
                    msg_lbl.config(text="Passwords don't match.")
                    return
                if u in self.data["users"]:
                    msg_lbl.config(text="Username taken.")
                    return
                self.data["users"][u] = {
                    "name": name, "password": hash_password(p),
                    "progress": {}, "ui_lang": self.ui_lang,
                    "joined": str(date.today()),
                }
                save_data(self.data)
                self.current_user = u
                self.show_dashboard()

            self.make_btn(center, self.T("register"), do_register, size=13, width=20).pack(pady=8)
            self.make_btn(center, self.T("already_acc"), lambda: self.show_auth("login"),
                          size=10, color=t["bg"]).pack()

    # ══════════════════════════════════════════════════════════════════════════
    #  DASHBOARD
    # ══════════════════════════════════════════════════════════════════════════

    def show_dashboard(self):
        self.apply_theme("default")
        self.clear()
        t = self.theme
        user_info = self.data["users"][self.current_user]

        # Top bar
        topbar = tk.Frame(self.main_frame, bg=t["bg2"], height=60)
        topbar.pack(fill="x")
        topbar.pack_propagate(False)

        tk.Label(topbar, text="🧠 " + self.T("app_title"),
                 bg=t["bg2"], fg=t["accent"],
                 font=("Courier", 18, "bold")).pack(side="left", padx=20, pady=10)

        # Right side controls
        right = tk.Frame(topbar, bg=t["bg2"])
        right.pack(side="right", padx=15)

        # Language UI selector
        tk.Label(right, text="🌍", bg=t["bg2"], fg=t["fg"], font=("Arial", 12)).pack(side="left")
        lang_var = tk.StringVar(value=self.ui_lang)
        lang_cb = ttk.Combobox(right, textvariable=lang_var,
                                values=list(TRANSLATIONS.keys()), width=5, state="readonly")
        lang_cb.pack(side="left", padx=4)
        def change_lang(e):
            self.ui_lang = lang_var.get()
            self.data["users"][self.current_user]["ui_lang"] = self.ui_lang
            save_data(self.data)
            self.show_dashboard()
        lang_cb.bind("<<ComboboxSelected>>", change_lang)

        self.make_btn(right, self.T("logout"), lambda: self.show_auth(),
                      size=10, color="#dc2626").pack(side="left", padx=8)

        # Welcome banner
        banner = tk.Frame(self.main_frame, bg=t["accent"], pady=1)
        banner.pack(fill="x")
        inner_banner = tk.Frame(banner, bg=t["bg2"], padx=30, pady=20)
        inner_banner.pack(fill="x")

        name = user_info.get("name", self.current_user)
        done = self.done_topics()
        total = self.total_topics()
        pct = int(done / total * 100) if total else 0

        tk.Label(inner_banner,
                 text=f"👋 {self.T('welcome')}, {name}!",
                 bg=t["bg2"], fg=t["fg"],
                 font=("Courier", 16, "bold")).pack(anchor="w")
        tk.Label(inner_banner,
                 text=f"📊 {self.T('progress')}: {done}/{total} topics completed ({pct}%)",
                 bg=t["bg2"], fg=t["accent"],
                 font=("Courier", 11)).pack(anchor="w", pady=(4, 0))

        # Progress bar
        pb_frame = tk.Frame(inner_banner, bg=t["bg2"])
        pb_frame.pack(anchor="w", fill="x", pady=(6, 0))
        pb_bg = tk.Frame(pb_frame, bg=t["bg"], height=10, relief="flat")
        pb_bg.pack(fill="x")
        pb_bg.update_idletasks()
        w = pb_bg.winfo_width() or 500
        fill_w = int(w * pct / 100) if pct > 0 else 4
        tk.Frame(pb_bg, bg=t["accent"], height=10, width=fill_w).place(x=0, y=0)

        # Main content area
        content = tk.Frame(self.main_frame, bg=t["bg"])
        content.pack(fill="both", expand=True, padx=20, pady=20)

        tk.Label(content, text=self.T("choose_language"),
                 bg=t["bg"], fg=t["fg"],
                 font=("Courier", 15, "bold")).pack(pady=(0, 15))

        lang_cards = tk.Frame(content, bg=t["bg"])
        lang_cards.pack(pady=10)

        for lang_name, lang_data in CURRICULUM.items():
            topics = lang_data["topics"]
            done_topics = sum(1 for tp in topics if self.topic_done(lang_name, tp["id"]))

            card = tk.Frame(lang_cards, bg=t["bg2"], relief="flat",
                            padx=25, pady=25, cursor="hand2")
            card.pack(side="left", padx=15, ipadx=5, ipady=5)

            icon_lbl = tk.Label(card, text=lang_data["icon"],
                                bg=t["bg2"], font=("Arial", 40))
            icon_lbl.pack()

            tk.Label(card, text=lang_name,
                     bg=t["bg2"], fg=lang_data["color"],
                     font=("Courier", 16, "bold")).pack()

            tk.Label(card, text=f"{done_topics}/{len(topics)} {self.T('topics')}",
                     bg=t["bg2"], fg=t["fg"],
                     font=("Courier", 10)).pack(pady=(4, 8))

            # Mini progress
            for tp in topics:
                done_f = self.topic_done(lang_name, tp["id"])
                ck = "✅" if done_f else "⬜"
                score_str = ""
                if done_f:
                    pd = self.get_progress().get(f"{lang_name}:{tp['id']}", {})
                    sc = pd.get("score", 0)
                    tot = pd.get("total", 5)
                    score_str = f" ({sc}/{tot})"
                tk.Label(card, text=f"{ck} {tp['emoji']} {tp['title']}{score_str}",
                         bg=t["bg2"], fg=t["fg"],
                         font=("Courier", 9), anchor="w").pack(anchor="w")

            btn_text = self.T("continue") if done_topics > 0 else self.T("start")
            def start_lang(ln=lang_name):
                self.selected_prog_lang = ln
                self.apply_theme(ln)
                # find first incomplete topic
                for i, tp in enumerate(CURRICULUM[ln]["topics"]):
                    if not self.topic_done(ln, tp["id"]):
                        self.current_topic_idx = i
                        break
                else:
                    self.current_topic_idx = 0
                self.show_topic_list(ln)

            self.make_btn(card, f"{btn_text} →", start_lang,
                          size=10, color=lang_data["color"]).pack(pady=(10, 0))

        # Recent activity
        progress = self.get_progress()
        if progress:
            tk.Label(content, text=f"\n📈 Recent Activity",
                     bg=t["bg"], fg=t["fg"],
                     font=("Courier", 12, "bold")).pack(anchor="w")
            for key, val in list(progress.items())[-5:]:
                parts = key.split(":")
                if len(parts) == 2:
                    lname, tid = parts
                    for tp in CURRICULUM.get(lname, {}).get("topics", []):
                        if tp["id"] == tid:
                            sc = val.get("score", 0)
                            tot = val.get("total", 5)
                            pct_q = int(sc / tot * 100)
                            bar_fill = "█" * (pct_q // 10) + "░" * (10 - pct_q // 10)
                            dt = val.get("date", "")
                            tk.Label(content,
                                     text=f"  {lname} › {tp['emoji']} {tp['title']}  [{bar_fill}] {sc}/{tot}  {dt}",
                                     bg=t["bg"], fg=t["accent"],
                                     font=("Courier", 9)).pack(anchor="w")

    # ══════════════════════════════════════════════════════════════════════════
    #  TOPIC LIST
    # ══════════════════════════════════════════════════════════════════════════

    def show_topic_list(self, lang_name):
        self.apply_theme(lang_name)
        self.clear()
        t = self.theme
        lang_data = CURRICULUM[lang_name]

        topbar = tk.Frame(self.main_frame, bg=t["bg2"], height=55)
        topbar.pack(fill="x")
        topbar.pack_propagate(False)

        self.make_btn(topbar, "← " + self.T("dashboard"),
                      self.show_dashboard, size=10,
                      color=t["bg"]).pack(side="left", padx=15, pady=10)

        tk.Label(topbar, text=f"{lang_data['icon']} {lang_name}",
                 bg=t["bg2"], fg=lang_data["color"],
                 font=("Courier", 16, "bold")).pack(side="left", padx=10, pady=10)

        # Topics
        scroll_frame = tk.Frame(self.main_frame, bg=t["bg"])
        scroll_frame.pack(fill="both", expand=True, padx=30, pady=20)

        tk.Label(scroll_frame, text=f"📚 {self.T('topics')}",
                 bg=t["bg"], fg=t["fg"],
                 font=("Courier", 14, "bold")).pack(anchor="w", pady=(0, 10))

        for i, topic in enumerate(lang_data["topics"]):
            done = self.topic_done(lang_name, topic["id"])
            pd = self.get_progress().get(f"{lang_name}:{topic['id']}", {})

            row = tk.Frame(scroll_frame, bg=t["bg2"], relief="flat", padx=20, pady=12)
            row.pack(fill="x", pady=4)

            left = tk.Frame(row, bg=t["bg2"])
            left.pack(side="left", fill="both", expand=True)

            status_icon = "✅" if done else f"{'🔓' if i == 0 or self.topic_done(lang_name, lang_data['topics'][i-1]['id']) else '🔒'}"
            tk.Label(left, text=f"{status_icon} {topic['emoji']}  {topic['title']}",
                     bg=t["bg2"], fg=t["fg"],
                     font=("Courier", 13, "bold")).pack(anchor="w")

            if done:
                sc = pd.get("score", 0)
                tot = pd.get("total", 5)
                pct = int(sc / tot * 100)
                bar = "█" * (pct // 10) + "░" * (10 - pct // 10)
                clr = t["success"] if pct >= 80 else (t["warning"] if pct >= 50 else t["error"])
                tk.Label(left, text=f"  Score: {sc}/{tot} [{bar}] {pct}%",
                         bg=t["bg2"], fg=clr,
                         font=("Courier", 9)).pack(anchor="w")

            unlocked = (i == 0 or self.topic_done(lang_name, lang_data["topics"][i-1]["id"]))

            def open_topic(idx=i, ln=lang_name):
                self.current_topic_idx = idx
                self.show_lesson(ln, idx)

            btn_text = self.T("continue") if done else self.T("start")
            if unlocked:
                self.make_btn(row, f"{btn_text} →", open_topic,
                              size=10).pack(side="right", padx=5)
            else:
                tk.Label(row, text="🔒 Complete previous topic first",
                         bg=t["bg2"], fg=t["warning"],
                         font=("Courier", 9)).pack(side="right", padx=10)

    # ══════════════════════════════════════════════════════════════════════════
    #  LESSON VIEW
    # ══════════════════════════════════════════════════════════════════════════

    def show_lesson(self, lang_name, topic_idx):
        self.apply_theme(lang_name)
        self.clear()
        t = self.theme
        lang_data = CURRICULUM[lang_name]
        topic = lang_data["topics"][topic_idx]

        # Top bar
        topbar = tk.Frame(self.main_frame, bg=t["bg2"], height=55)
        topbar.pack(fill="x")
        topbar.pack_propagate(False)

        self.make_btn(topbar, "← Topics",
                      lambda: self.show_topic_list(lang_name),
                      size=10, color=t["bg"]).pack(side="left", padx=10, pady=10)

        tk.Label(topbar, text=f"{topic['emoji']} {topic['title']}",
                 bg=t["bg2"], fg=t["accent"],
                 font=("Courier", 14, "bold")).pack(side="left", padx=10)

        # Audio button
        if AUDIO_AVAILABLE:
            audio_btn = self.make_btn(topbar, "🔊 " + self.T("audio"),
                                       lambda: self.start_audio(topic["lesson"]),
                                       size=10, color="#7c3aed")
            audio_btn.pack(side="right", padx=10, pady=10)
            stop_btn = self.make_btn(topbar, "⏹ " + self.T("stop_audio"),
                                      self.stop_audio, size=10, color="#dc2626")
            stop_btn.pack(side="right", padx=5, pady=10)

        # Tabs: Lesson | Examples
        tab_bar = tk.Frame(self.main_frame, bg=t["bg2"])
        tab_bar.pack(fill="x")

        self.lesson_content_frame = tk.Frame(self.main_frame, bg=t["bg"])
        self.lesson_content_frame.pack(fill="both", expand=True)

        tabs = {}
        current_tab = tk.StringVar(value="lesson")

        def show_tab(tab_name):
            current_tab.set(tab_name)
            for n, btn in tabs.items():
                btn.config(bg=t["accent"] if n == tab_name else t["bg2"])
            for w in self.lesson_content_frame.winfo_children():
                w.destroy()
            if tab_name == "lesson":
                self._render_lesson_text(self.lesson_content_frame, topic["lesson"], t)
            elif tab_name == "examples":
                self._render_examples(self.lesson_content_frame, topic["examples"], lang_name, t)

        for tab_key, tab_label in [("lesson", "📖 " + self.T("lesson")),
                                    ("examples", "💡 " + self.T("examples"))]:
            btn = tk.Button(tab_bar, text=tab_label,
                            bg=t["accent"] if tab_key == "lesson" else t["bg2"],
                            fg="white", font=("Courier", 11, "bold"),
                            relief="flat", cursor="hand2", padx=20, pady=8,
                            command=lambda k=tab_key: show_tab(k))
            btn.pack(side="left")
            tabs[tab_key] = btn

        # Start Quiz button fixed at bottom
        bottom_bar = tk.Frame(self.main_frame, bg=t["bg2"], pady=12)
        bottom_bar.pack(fill="x", side="bottom")

        self.make_btn(bottom_bar, f"📝 {self.T('quiz')} →",
                      lambda: self.show_quiz(lang_name, topic_idx),
                      size=12).pack(pady=4)

        show_tab("lesson")

    def _render_lesson_text(self, parent, lesson_text, t):
        canvas = tk.Canvas(parent, bg=t["bg"], highlightthickness=0)
        scrollbar = tk.Scrollbar(parent, orient="vertical", command=canvas.yview)
        canvas.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)

        inner = tk.Frame(canvas, bg=t["bg"], padx=30, pady=20)
        canvas_window = canvas.create_window((0, 0), window=inner, anchor="nw")

        def on_resize(e):
            canvas.itemconfig(canvas_window, width=e.width)
        canvas.bind("<Configure>", on_resize)

        def update_scroll(e):
            canvas.configure(scrollregion=canvas.bbox("all"))
        inner.bind("<Configure>", update_scroll)

        # Render lesson lines with code detection
        in_code_block = False
        code_lines = []

        def flush_code():
            nonlocal code_lines
            if code_lines:
                code_text = "\n".join(code_lines)
                code_frame = tk.Frame(inner, bg=t["code"], relief="flat", padx=15, pady=10)
                code_frame.pack(fill="x", pady=4)

                # Copy button
                def copy_code(ct=code_text):
                    self.root.clipboard_clear()
                    self.root.clipboard_append(ct)
                copy_btn = tk.Button(code_frame, text="📋 Copy", command=copy_code,
                                     bg=t["btn"], fg="white", font=("Courier", 8),
                                     relief="flat", cursor="hand2", padx=6, pady=2)
                copy_btn.pack(anchor="ne")

                code_txt = tk.Text(code_frame, bg=t["code"], fg="#a8ff78",
                                   font=("Courier", 11), relief="flat",
                                   state="normal", wrap="none",
                                   height=len(code_lines) + 1)
                code_txt.insert("1.0", code_text)
                code_txt.config(state="disabled")
                code_txt.pack(fill="x")
                code_lines = []

        for line in lesson_text.split("\n"):
            stripped = line.strip()

            if stripped.startswith("  ") or (len(line) > 0 and line[0] == " "):
                # Treat indented lines as code
                flush_code() if not in_code_block else None
                in_code_block = True
                code_lines.append(line.rstrip())
            else:
                if in_code_block:
                    flush_code()
                    in_code_block = False

                if not stripped:
                    tk.Label(inner, text="", bg=t["bg"], height=1).pack()
                elif stripped.isupper() and len(stripped) > 3:
                    # Section heading
                    tk.Label(inner, text=stripped, bg=t["bg"],
                             fg=t["accent"],
                             font=("Courier", 12, "bold"),
                             anchor="w").pack(anchor="w", pady=(8, 2))
                elif stripped.startswith("•"):
                    tk.Label(inner, text=stripped, bg=t["bg"],
                             fg=t["fg"], font=("Courier", 11),
                             anchor="w", justify="left").pack(anchor="w")
                else:
                    lbl = tk.Label(inner, text=line, bg=t["bg"],
                                   fg=t["fg"], font=("Courier", 11),
                                   anchor="w", justify="left", wraplength=700)
                    lbl.pack(anchor="w")

        if in_code_block:
            flush_code()

        # Mouse wheel scrolling
        def on_mousewheel(e):
            canvas.yview_scroll(int(-1 * (e.delta / 120)), "units")
        canvas.bind_all("<MouseWheel>", on_mousewheel)

    def _render_examples(self, parent, examples, lang_name, t):
        canvas = tk.Canvas(parent, bg=t["bg"], highlightthickness=0)
        scrollbar = tk.Scrollbar(parent, orient="vertical", command=canvas.yview)
        canvas.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)

        inner = tk.Frame(canvas, bg=t["bg"], padx=30, pady=20)
        canvas_window = canvas.create_window((0, 0), window=inner, anchor="nw")

        def on_resize(e):
            canvas.itemconfig(canvas_window, width=e.width)
        canvas.bind("<Configure>", on_resize)

        def update_scroll(e):
            canvas.configure(scrollregion=canvas.bbox("all"))
        inner.bind("<Configure>", update_scroll)

        lang_icon = CURRICULUM[lang_name]["icon"]
        tk.Label(inner, text=f"💡 {self.T('examples')} — {lang_icon} {lang_name}",
                 bg=t["bg"], fg=t["fg"],
                 font=("Courier", 14, "bold")).pack(anchor="w", pady=(0, 15))

        for i, (title, code) in enumerate(examples):
            ex_frame = tk.Frame(inner, bg=t["bg2"], relief="flat", padx=20, pady=15)
            ex_frame.pack(fill="x", pady=8)

            tk.Label(ex_frame, text=f"Example {i+1}: {title}",
                     bg=t["bg2"], fg=t["accent"],
                     font=("Courier", 12, "bold")).pack(anchor="w", pady=(0, 8))

            code_frame = tk.Frame(ex_frame, bg=t["code"], relief="flat", padx=12, pady=8)
            code_frame.pack(fill="x")

            def copy_code(c=code):
                self.root.clipboard_clear()
                self.root.clipboard_append(c)
            copy_btn = tk.Button(code_frame, text="📋 Copy", command=copy_code,
                                 bg=t["btn"], fg="white", font=("Courier", 8),
                                 relief="flat", cursor="hand2", padx=6, pady=2)
            copy_btn.pack(anchor="ne")

            lines = code.split("\n")
            code_txt = tk.Text(code_frame, bg=t["code"], fg="#a8ff78",
                               font=("Courier", 11), relief="flat",
                               state="normal", wrap="none",
                               height=len(lines) + 1)
            code_txt.insert("1.0", code)
            code_txt.config(state="disabled")
            code_txt.pack(fill="x")

        def on_mousewheel(e):
            canvas.yview_scroll(int(-1 * (e.delta / 120)), "units")
        canvas.bind_all("<MouseWheel>", on_mousewheel)

    # ══════════════════════════════════════════════════════════════════════════
    #  QUIZ
    # ══════════════════════════════════════════════════════════════════════════

    def show_quiz(self, lang_name, topic_idx):
        self.apply_theme("quiz")
        self.clear()
        t = self.theme
        topic = CURRICULUM[lang_name]["topics"][topic_idx]
        questions = topic["quiz"]

        self.quiz_answers = [None] * len(questions)
        self.quiz_current_q = 0
        self.quiz_selected = tk.IntVar(value=-1)

        # Top bar
        topbar = tk.Frame(self.main_frame, bg=t["bg2"], height=55)
        topbar.pack(fill="x")
        topbar.pack_propagate(False)

        self.make_btn(topbar, f"← {self.T('lesson')}",
                      lambda: self.show_lesson(lang_name, topic_idx),
                      size=10, color=t["bg"]).pack(side="left", padx=10, pady=10)

        self.quiz_progress_lbl = tk.Label(topbar, text="",
                                           bg=t["bg2"], fg=t["accent"],
                                           font=("Courier", 12, "bold"))
        self.quiz_progress_lbl.pack(side="left", padx=20)

        # Main quiz area
        self.quiz_frame = tk.Frame(self.main_frame, bg=t["bg"])
        self.quiz_frame.pack(fill="both", expand=True, padx=40, pady=20)

        def render_question(q_idx):
            for w in self.quiz_frame.winfo_children():
                w.destroy()
            self.quiz_selected.set(-1)

            q = questions[q_idx]
            self.quiz_progress_lbl.config(
                text=f"Q {q_idx+1}/{len(questions)}")

            # Question header
            q_frame = tk.Frame(self.quiz_frame, bg=t["bg2"], padx=30, pady=20)
            q_frame.pack(fill="x", pady=(0, 15))

            tk.Label(q_frame, text=f"❓ Question {q_idx+1}",
                     bg=t["bg2"], fg=t["accent"],
                     font=("Courier", 11, "bold")).pack(anchor="w")
            tk.Label(q_frame, text=q["q"],
                     bg=t["bg2"], fg=t["fg"],
                     font=("Courier", 13), wraplength=700,
                     justify="left").pack(anchor="w", pady=(8, 0))

            # Options
            for i, opt in enumerate(q["options"]):
                # Already answered?
                prev = self.quiz_answers[q_idx]
                if prev is not None:
                    if i == q["answer"]:
                        bg_c = "#1a4d2e"
                        fg_c = t["success"]
                    elif i == prev and prev != q["answer"]:
                        bg_c = "#4d1a1a"
                        fg_c = t["error"]
                    else:
                        bg_c = t["bg2"]
                        fg_c = t["fg"]
                else:
                    bg_c = t["bg2"]
                    fg_c = t["fg"]

                opt_frame = tk.Frame(self.quiz_frame, bg=bg_c,
                                     relief="flat", padx=20, pady=12,
                                     cursor="hand2" if prev is None else "arrow")
                opt_frame.pack(fill="x", pady=3)

                prefix = ["A", "B", "C", "D"][i]
                tk.Label(opt_frame, text=f"{prefix}.  {opt}",
                         bg=bg_c, fg=fg_c,
                         font=("Courier", 12), anchor="w").pack(anchor="w")

                if prev is None:
                    def select(idx=i, frm=opt_frame):
                        self.quiz_selected.set(idx)
                        # Highlight selected
                        for j, ch in enumerate(self.quiz_frame.winfo_children()):
                            if j > 0:
                                ch.config(bg=t["bg2"] if j-1 != idx else t["btn"])
                                for lbl in ch.winfo_children():
                                    lbl.config(bg=t["bg2"] if j-1 != idx else t["btn"])
                    opt_frame.bind("<Button-1>", lambda e, idx=i: select(idx))
                    for child in opt_frame.winfo_children():
                        child.bind("<Button-1>", lambda e, idx=i: select(idx))

            # Feedback area
            feedback_frame = tk.Frame(self.quiz_frame, bg=t["bg"])
            feedback_frame.pack(fill="x", pady=10)

            if self.quiz_answers[q_idx] is not None:
                ans = self.quiz_answers[q_idx]
                correct = (ans == q["answer"])
                fb_text = self.T("correct") if correct else self.T("wrong")
                fb_color = t["success"] if correct else t["error"]
                tk.Label(feedback_frame, text=fb_text,
                         bg=t["bg"], fg=fb_color,
                         font=("Courier", 13, "bold")).pack()
                tk.Label(feedback_frame,
                         text=f"💡 {self.T('explanation')}: {q['explanation']}",
                         bg=t["bg"], fg=t["fg"],
                         font=("Courier", 10), wraplength=700,
                         justify="left").pack(pady=4)

            # Buttons
            btn_bar = tk.Frame(self.quiz_frame, bg=t["bg"])
            btn_bar.pack(pady=10)

            if self.quiz_answers[q_idx] is None:
                def submit_answer():
                    sel = self.quiz_selected.get()
                    if sel == -1:
                        messagebox.showwarning("LearnSphere", "Please select an answer first!")
                        return
                    self.quiz_answers[q_idx] = sel
                    render_question(q_idx)

                self.make_btn(btn_bar, f"✅ {self.T('submit')}",
                              submit_answer, size=12).pack(side="left", padx=8)
            else:
                if q_idx < len(questions) - 1:
                    self.make_btn(btn_bar, self.T("next"),
                                  lambda: render_question(q_idx + 1),
                                  size=12).pack(side="left", padx=8)
                else:
                    def finish_quiz():
                        correct_count = sum(
                            1 for i, a in enumerate(self.quiz_answers)
                            if a == questions[i]["answer"]
                        )
                        self.set_topic_score(lang_name, topic["id"],
                                             correct_count, len(questions))
                        self.show_quiz_results(lang_name, topic_idx,
                                               correct_count, len(questions),
                                               questions)
                    self.make_btn(btn_bar, f"🏁 {self.T('quiz_result')}",
                                  finish_quiz, size=12,
                                  color=t["success"]).pack(side="left", padx=8)

        render_question(0)

    # ══════════════════════════════════════════════════════════════════════════
    #  QUIZ RESULTS
    # ══════════════════════════════════════════════════════════════════════════

    def show_quiz_results(self, lang_name, topic_idx, correct, total, questions):
        pct = int(correct / total * 100)
        if pct >= 90:
            theme_key = "success"
        elif pct >= 70:
            theme_key = "quiz"
        else:
            theme_key = "default"
        self.apply_theme(theme_key)
        self.clear()
        t = self.theme
        topic = CURRICULUM[lang_name]["topics"][topic_idx]

        # Background canvas
        canvas = tk.Canvas(self.main_frame, bg=t["bg"], highlightthickness=0)
        canvas.pack(fill="both", expand=True)

        center = tk.Frame(canvas, bg=t["bg2"], padx=50, pady=40)
        center.place(relx=0.5, rely=0.5, anchor="center")

        # Badge
        if pct >= 90:
            badge = "🏆"; grade = self.T("excellent"); clr = t["success"]
        elif pct >= 70:
            badge = "🎯"; grade = self.T("good"); clr = t["accent"]
        elif pct >= 50:
            badge = "📈"; grade = self.T("average"); clr = t["warning"]
        else:
            badge = "📚"; grade = self.T("weak"); clr = t["error"]

        tk.Label(center, text=badge, bg=t["bg2"], font=("Arial", 60)).pack()
        tk.Label(center, text=self.T("quiz_result"),
                 bg=t["bg2"], fg=t["fg"],
                 font=("Courier", 18, "bold")).pack(pady=(8, 0))
        tk.Label(center, text=f"{topic['emoji']} {topic['title']}",
                 bg=t["bg2"], fg=t["accent"],
                 font=("Courier", 12)).pack()

        self.divider(center, t["accent"])

        tk.Label(center, text=f"{self.T('score')}: {correct}/{total}  ({pct}%)",
                 bg=t["bg2"], fg=clr,
                 font=("Courier", 20, "bold")).pack(pady=8)
        tk.Label(center, text=grade,
                 bg=t["bg2"], fg=clr,
                 font=("Courier", 14, "bold")).pack()

        # Score bar
        bar = "█" * (pct // 10) + "░" * (10 - pct // 10)
        tk.Label(center, text=f"[{bar}]",
                 bg=t["bg2"], fg=clr,
                 font=("Courier", 14)).pack(pady=6)

        # Answer review
        self.divider(center, t["accent"])
        tk.Label(center, text="Answer Review:",
                 bg=t["bg2"], fg=t["fg"],
                 font=("Courier", 11, "bold")).pack(anchor="w")

        for i, q in enumerate(questions):
            ans = self.quiz_answers[i] if i < len(self.quiz_answers) else None
            is_correct = (ans == q["answer"])
            icon = "✅" if is_correct else "❌"
            tk.Label(center,
                     text=f"{icon} Q{i+1}: {q['q'][:60]}{'...' if len(q['q'])>60 else ''}",
                     bg=t["bg2"],
                     fg=t["success"] if is_correct else t["error"],
                     font=("Courier", 9), anchor="w").pack(anchor="w")

        self.divider(center, t["accent"])

        # Navigation buttons
        btn_row = tk.Frame(center, bg=t["bg2"])
        btn_row.pack(pady=10)

        topics = CURRICULUM[lang_name]["topics"]
        if topic_idx + 1 < len(topics):
            next_topic = topics[topic_idx + 1]
            def go_next():
                self.current_topic_idx = topic_idx + 1
                self.show_lesson(lang_name, topic_idx + 1)
            self.make_btn(btn_row, f"Next: {next_topic['title']} →",
                          go_next, size=11,
                          color=t["success"]).pack(side="left", padx=8)
        else:
            tk.Label(center, text=self.T("all_done"),
                     bg=t["bg2"], fg=t["success"],
                     font=("Courier", 12, "bold")).pack(pady=4)

        self.make_btn(btn_row,
                      f"↩ {self.T('topics')}",
                      lambda: self.show_topic_list(lang_name),
                      size=11).pack(side="left", padx=8)
        self.make_btn(btn_row,
                      f"🏠 {self.T('dashboard')}",
                      self.show_dashboard,
                      size=11).pack(side="left", padx=8)

        # Retry if score < 60%
        if pct < 60:
            self.make_btn(center,
                          f"🔄 Retry Quiz",
                          lambda: self.show_quiz(lang_name, topic_idx),
                          size=11, color=t["warning"]).pack(pady=6)

    # ══════════════════════════════════════════════════════════════════════════
    #  AUDIO (optional)
    # ══════════════════════════════════════════════════════════════════════════

    def start_audio(self, text):
        if not AUDIO_AVAILABLE:
            messagebox.showinfo("LearnSphere",
                "Audio requires gTTS: pip install gtts\nAlso needs an audio player (mpg123 on Linux / afplay on Mac).")
            return
        self.audio_stop = False
        lines = [l.strip() for l in text.split("\n") if l.strip()]
        self.audio_thread = threading.Thread(target=self._play_lines,
                                              args=(lines,), daemon=True)
        self.audio_thread.start()

    def _play_lines(self, lines):
        lang_map = {"en": "en", "ta": "ta", "hi": "hi", "fr": "fr", "ar": "ar"}
        tts_lang = lang_map.get(self.ui_lang, "en")
        for line in lines:
            if self.audio_stop:
                break
            try:
                tts = gTTS(text=line, lang=tts_lang, slow=False)
                with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as f:
                    tts.save(f.name)
                    fname = f.name
                # Try common players
                if sys.platform == "darwin":
                    subprocess.run(["afplay", fname], capture_output=True)
                elif sys.platform == "win32":
                    import winsound
                    winsound.PlaySound(fname, winsound.SND_FILENAME)
                else:
                    subprocess.run(["mpg123", "-q", fname], capture_output=True)
                os.unlink(fname)
            except Exception:
                break

    def stop_audio(self):
        self.audio_stop = True


# ═══════════════════════════════════════════════════════════════════════════════
#  ENTRY POINT
# ═══════════════════════════════════════════════════════════════════════════════

def main():
    root = tk.Tk()
    root.title("LearnSphere")

    # Set window icon emoji substitute
    try:
        root.iconbitmap("")
    except:
        pass

    # Style ttk combobox
    style = ttk.Style()
    style.theme_use("clam")
    style.configure("TCombobox",
                     fieldbackground="#1a1a3e",
                     background="#1a1a3e",
                     foreground="#e8e8ff",
                     arrowcolor="#7c6af7")

    app = LearnSphere(root)
    root.mainloop()


if __name__ == "__main__":
    main()
