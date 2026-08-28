# #1. Using Square Brackets
# a = [1, 2, 3]
# a.append(12)
# print(a)

# #2. Using list() Constructor
# b = ["apple", "banana"]
# print(b)

# a = list((1, 2, 3, 'apple', 4.5))  
# print(a)

# b = list("GFG")
# print(b)

# #3. Creating List with Repeated Elements
# a = [2] * 5
# b = [0] * 7

# print(a)
# print(b)

# a = [1, 2, 2, "Python"]
# print(a[-1])   # index-based
# print(a)


# a = [2, 3, 4, 5]
# res = [val ** 2 for val in a]
# print(res)

# res = []
# for val in a:
#     val = val **2
#     res.append(val)

# a = [1, 2, 3, 4, 5]
# res = []
# for val in a:
#     if val%2==0:
#         res.append(val)
# print(res)

# b = [5, 12, 7, 18, 3, 20]
# res = []
# for val in b:
#     if val >10:
#         res.append(val)
# print(res)

# a = []
# for i in range(10):
#     a.append(i)
# print(a)

# c =[]
# for x in range(3):
#     for y in range(3):
#         c.append((x,y))
# print(c)


# mat = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
# res = []
# for row in mat:
#     for val in row:
#         res.append(val)
# print(res)

# a = [1, 2, 3, 4, 5]
# res = []
# for n in a:
#     if n % 2 == 0:
#         res.append('Even')
#     else:
#         res.append('Odd')
# print(res)


# a = [1, 2, 3, 4, 5]
# res = []
# for n in a :
#     if n % 2 == 0:
#         res.append(n)
# print(res)

# a = [1, 2, 3, 4, 5]
# a.extend([0,1])
# print(a.pop(4))
# print(max(a))
# print(min(a))
# print(sum(a))

# a.reverse()
# print(a)

# a.sort()
# print(a)

# a = ['awd', 'sas','Awe']
# print(max(a))
# print(min(a))
# a.sort()
# print(a)

# print(len(a))

# l = []
# for i in range(1,20):
#     l.append(i)
# print(l)

# a = [x for x in range(15) if x%2 == 0]
# b = [x for x in range(15) if x%2 != 0]
# print([a,b])

# x = 20
# a= [b for b in range (6,25) if b < x]
# if a < x:
#     c.append(a)
# print(a)

# def getevenorodd(l):
#     return ['Even' if a%2 == 0 else 'Odd' for a in l]

# l = [3,4,5,32,445,521,12,1]
# print(getevenorodd(l))

# def getEO(l):
#     Even = [x for x in l if x % 2 == 0]
#     Odd = [x for x in l if x%2 != 0]
#     return Even,Odd
# l = [221,1,312,312,4,324,34,3,52,5]
# Even,Odd = getEO(l)
# print(Even)
# print(Odd)

# s = "geekforgeeks"
# l1 = []
# for x in s:
#     if x in "aeiou":
#         l1.append(x)
# print(l1)



# l2 = ["geeks", "ide","courses", "gfg"]
# l3 = [x for x in l2 if x.startswith("g")]
# print(l3)

# l4= [x*2 for x in range(6)]
# print(l4)

# a = ['Python', 'Java', 'C++', 'Go']
# b = a
# c = a[:]
# b[0] = 'Code'
# c[1] = 'Quiz'
# count = 0

# for x in (a, b, c):
#     if x[0] == 'Code':
#         count += 1

#     if x[1] == 'Quiz':
#         count += 10

# print(count)

# def square_list(x, li=[]):
#     for i in range(x):
#         li.append(i * i)
#     print(li)

# square_list(3, [3, 2, 1])

# def sum(a,b):
#     s = a + b
#     s1 = a - b
#     s2 = a * b
#     s3 = a / b

#     print("Add  = ", s)
#     print("Sub = ", s1)
#     print("Mul = ",s2)
#     print("Divide = ", s3)

#     return s,s1,s2,s3
# sum(213323,4512)
# sum(3123323,452)
# sum(35564523,45)

# def avg(a,b,c):
#     average = (a+b+c)/3
#     print(average)
#     return a,b,c

# avg(150,321,543)
# avg(1512,321,543)
# avg(151212,321,543)

# def printlen(a):
#     b = len(a)
#     print(b)
#     return b
# a = [212,3,2,4,44]
# printlen(a)

# def printlist(list):
#     print(list)
#     return list
# list = [121,3,123,12,434,32,5]
# printlist(list)

# def factorial(n):
#     if n == 0 or n == 1:
#         return 1
#     return n * factorial(n-1) 

# n = int(input("Enter any inteer value to finf factorial = ") )
# print(factorial(n))


# def factorial(n):
#     fact = 1
#     for i in range(1, n +1):
#         fact *= i
#     return fact
# print(factorial(5))

# def evenodd(n):
#     if n % 2 == 0:
#         return "EVEN"
#     else:
#         return "ODD"
# n = int(input("Enter a number = "))
# print(evenodd(n))

# def show(n):
#     if (n== -2):
#         return
#     print(n)
#     show(n-1)
# show(6)


# def fact(n):
#     if n == 0 :
#         return 0
#     else:
#         for i in range(n):
#             return n + fact(n-1)
# print(fact(4))

# def fibonacci(n):
#     if n == 0:
#         return 0 
#     if n== 1:
#         return 1
#     return fibonacci(n-1) + fibonacci(n-2)

# num = 6
# for i in range(num):
#     print(fibonacci(i))

# def el(list, index=0):
#     if (index == len(list)):
#         return
#     print(list[index])
#     el(list, index +1)
# fruits = ["mango", "apple", "banana"]
# el(fruits)

# Write a function to check if a number is even or odd using recursion (Hint: keep subtracting 2).
# def check(n):
#     if n % 2 == 0:
#         return "Even"
#     if n % 2 != 0:
#         return "Odd"
#     return check(n-2)
    
    
# print(check(5))

# a = ["Python", "Java", "C++"]
# for i, v in enumerate(a):
#     print(i, v)

# a = [[1, 2], [3, 4], [5, 6]]
# b = [i for j in a for i in j]
# b.sort(reverse= True)
# print(b)
# c = []
# for j in a:
#     for i in j:
#         c.append(i)    
# print(c)

# tup = (1,2,5,5,3,4,5)
# print(tup.count(5))


#Q  wap to ask the user to enter names of three moves and store them in a list
# list = []
# i = 0
# while i < 3:
#     a = str(input("Enter name of three movies: "))
#     list.append(a)
#     i += 1
# print(list)

#Q wap to check if a list contains a plaindrom of element. (use copoy() method)
# a = [1,"abc", 1,2,"abc", 1]
# b = a.copy()
# a.reverse()
# if a == b:
#     print("palindrome! ",b)
# else:
#     print("Not palindrome")

# tup = ("c", "d", "a", "a","b", "d", "a")
# print(tup.count("a"))

# list = ["c", "d", "a", "a","b", "d", "a"]
# list.sort()
# print(tuple(list))

# a = 'akda'
# print(tuple((a)))

# str1 = "Muhammad"
# str2 = "Faizan"
# str3 = "Ali"

# str = str1  + " " + str2 + " " + str3

#print(str.endswith("Ali")) // True or False
#print(len(str))
#print(str.capitalize())
#print(str.replace("Ali", "ali"))
#print(str.find("Faizan"))
#print(str.count("a"))

# name = str(input("Enter your name"))
# print(len(name))

# a = ".$500"
# print(a.find("$"))


dict = {
    "name" : "Faizan",
    "age" : 19,
    "GPA_2" : 3.56  ,
    "is_adult" : True,
    "Subject" : ["CS", "FQ", "LA", "Oop", "DLD", "AP" , "Oop lab", "DLD lab", "Ap lab"],
    "Individual_GPA" : (3.50, 3.50, 3.50, 3.50, 3.70, 3.50, 4.00, 3.50, 3.70)
}
dict["name"] = "M Faizan"
# print(type(dict))
# print(len(dict))
#print(list(dict.values()))
#print(list(dict.items()))
#print(dict.get("key"))
#print(list(dict.values()))
# print(dict["name"])
# print(dict.get("name"))

# dict.update({"city" : "Karachi"})
# print(dict)


# set = {1,2,3,3,4,515,0}
# set.add("Faizan")
# print(set)