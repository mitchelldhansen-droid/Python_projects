#String data type

#literal assignment
first = "Mitchell"
last = "Hansen"

# print (type(first))
# print (type(first) == str)
# print (isinstance(first,str))

#Constructor function
# pizza = str("pepperoni")

# print (type(pizza))
# print (type(pizza) == str)
# print (isinstance(pizza,str))

#Concatenation
# first = "Mitchell"
# last = "Hansen"
# fullname = first + " " + last
# print (fullname)

# fullname += "!"
# print (fullname)

# Casting a number to a string

# decade = str(1980)
# print(type(decade))
# print(decade)

# #or
# # decade = "1980"
# # decade = decade
# # print (decade)

# statement = "I like rock music from the " + decade + "s."
# print(statement)


# #Multiple lines

# multiline = """
# Hey, how are you?                                             

# I was just checking in.         
#                         All good?

# """
# print(multiline)

# # Escaping special characters with a \
# sentence = "I\'m back at work!\tHey!\n\nWhere\'s this at\\located?"
# print(sentence)

# # String Methods

# print(first)
# print(first.lower())
# print(first.upper())
# print(first)

# print(multiline.title())
# print(multiline.replace("good", "ok"))

# print(len(multiline))
# multiline += "                             "
# multiline = "                      " + multiline
# print (len(multiline))

# print(len(multiline.strip()))
# print(len(multiline.lstrip()))
# print(len(multiline.rstrip()))

#Build a menu

# title = "menu".upper()
# print(title.center(20, "="))
# print("Coffee".ljust(16, ".") + "$1".rjust(4))
# print("Muffin".ljust(16, ".") + "$3".rjust(4))
# print("Cake".ljust(16, ".") + "$4".rjust(4))


# Some methods return boolean data (True/False) (references name)

# print(first.startswith("M"))
# print(first.endswith("Z"))

# Boolean data type

myvalue = True 
x = bool(False)
print (type(x))
print(isinstance(myvalue, bool))

# Numeric data types include
# integers, solid numbers 17 or 99
# floats, numbers with decimals ex. 17.99
# complex type 
comp_value = 5+3j
print(comp_value.real)
print(comp_value.imag)

#Built-in functions for numbers

# print(abs()) #Print the absolute value of the second parentheses

# print(round()) #Rounds to nearest integer

# print(round(,1)) #closest to the value specified after ,

#Many modules include more functions with numbers or other things 