# Making my first calculator by python
def add(a,b):
    return a +b
def substract(a,b):
    return a - b
def multiply(a,b):
    return a * b
def divide(a,b):
    if b == 0:
        return "Error: Division by zero is not allowed."
    return a/b

# now lets create a loop so the calculator doesnt stop
while True:
    print("\n--- taibah's smart calculator...")
    print("1. add(+)")
    print("2. substract(-)")
    print("3. multiply(*)")
    print("4. divide(/)")
    print("5. exit")

    choice = input("Enter your choice number (1/2/3/4/5):")
    if choice == "5":
        print("Exiting the calculator. Goodbye!")
        break
    if choice in ('1','2','3','4'):
        num1 = float(input("Enter your first number:"))
        num2 = float(input("Enter your second number:"))
        if choice == '1':
            print("result:", add(num1,num2))
        elif choice == '2':
            print("result:",substract(num1,num2))
        elif choice == '3':
            print("result:",multiply(num1,num2))
        elif choice == '4':
            print("result:",divide(num1,num2))
        else:
            print("Error, please  try again.")
            

