emotions = ["happy", "sad", "fear", "surprise"]

# Write code that uses a conditional expression (do not use an if-statement or ternary expression) to print "true" if the last element is "happy" and there are more than 3 elements, or "false" if it is not. (Hint: You can use the len function to determine how many elements are in the tuple and then use that information in the expression). 
result = (emotions[-1] == "happy" and len(emotions) > 3)
print(result) # Should return false

if(result) == True:
    print("true")
else:
    print("false")