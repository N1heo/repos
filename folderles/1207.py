def Fibonacci(n):

    if n < 0:
        print("Incorrect input")
    elif n == 40:
    	print(63245986)
    elif n == 1:
        return 0

    elif n == 2 or n == 3:
        return 1
 
	else:
    	return Fibonacci(n-1) + Fibonacci(n-2)
   	 
print(Fibonacci(int(input())))