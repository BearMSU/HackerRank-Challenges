# Decorators 2 - Name Directory
"""
Let's use decorators to build a name directory! You oare given some information about N people. Each person has a first name, last name, age, and sex.
Print their names in a specific format sorted by their age in ascending order i.e. the youngest person's name should be printed first. For two people of the same age,
print them in the order of their input.

For Henry Davids, the output should be:

    Mr. Henry Davids
    

For Mary George, the output should be:

    Ms. Mary George


Input Format

The first line contains the integer N, the number of people.
N lines follow each containing the space separated valeus of the first name, last name, age, and sex, respectively.


Constraints

1 <= N <= 10


Output Format

Output N names on separate lines in the format describedd above in ascending order of age.


Sample Input

3
Mike Thomson 20 M
Robert Bustle 32 M
Andria Bustle 30 F


Sample Output

Mr. Mike Thomson
Ms. Andria Bustle
Mr. Robert Bustle


Concept

For sorting a nested list based on some parameter, you can use the itemgetter library.
"""

# My Code:
import operator

def person_lister(f):
    def inner(people):
        # 1. Convert age to integer for sorting
        # List comprehensino is used to achieve a similar result to using a map() function
        # map function could have worked well here, but list comprehension seemed suitable
        parsed_people = [p[:2] + [int(p[2])] + p[3:] for p in people]
        
        # 2. Sort the list by age (index 2), ascending
        # operator.itemgetter(2) is used to get hte age for sorting
        parsed_people.sort(key=operator.itemgetter(2))
        
        # 3. Call the decorated function 'f' for each perso in the sorted list
        # The original function 'f' will take care of formatting/printing each person
        return [f(p) for p in parsed_people]
    return inner

@person_lister
def name_format(person):
    return ("Mr. " if person[3] == "M" else "Ms. ") + person[0] + " " + person[1]

if __name__ == '__main__':
    people = [input().split() for i in range(int(input()))]
    print(*name_format(people), sep='\n')