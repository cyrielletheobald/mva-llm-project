# Define a function that takes no arguments
def greet():
    # Print "Hello, World!" to the console
    print("Hello, World!")

# Call the greeting function
greet()

# If you want to define a class instead of using a function,
class Greeter:
    # Initialize an instance variable with your name
    def __init__(self, name):
        self.name = name

    # Define another method called 'greet'
    def greet(self):
        print(f"Hello, {self.name}!")

# Create an instance of the class and call the greet method
greeter = Greeter("John")
greeter.greet()