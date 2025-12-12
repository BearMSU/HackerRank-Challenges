"""Given a string of lowercase English letters and an integer of the substring length, determine the substring of that length that contains the most vowels.
Vowels are in the set (a, e, i, o, u). If there is more than one substring with the maximum number of vowels, return the one that starts at the lowest index.
If there are no vowels in the input string, return the string "Not found!" without quotes.

Example 1
s = 'caberqiitefg'
k = 5
The substring of length k = 5 that contains the maximum number of vowels is 'erqii' with 3 vowels.
The final answer is 'erqii'.

Example 2
s = 'aeiouia'
k = 3

All of the characters are vowels, so any substring of length 3 will have 3 vowels. The lowest index substring is at index 0, 'aei'.

Function Description
Complete the function findSubstring in the editor below.

findSubstring has the following parameters:
    s: a string
    k: an integer

Returns:
    string: a string containing the final answer

Constraints

- 1 <= length(s) <= 2 * 10 ** 5
- 1 <= k <= length(s)

Input Format For Custom Testing:
The first line contains a string (s).
The second line contains an integer (k).

Sample Case 0:
    Sample Input:
        STDIN        Function
        -----        --------
        azerdii ->   s = 'azerdii'
        5       ->   k = 5
    Sample Output:
        erdii
    Explanation:
        s='azerdii'
        k = 5
        The possible 5 character substrings are:
            'azerd' which contains 2 vowels
            'zerdi' which contains 2 vowels
            'erdii' which contains 3 vowels

Sample Case 1:
    Sample Input:
        STDIN       Function
        -----       --------
        qwdftr  ->  s = 'qwdftr'
        2       ->  k = 2
    
    Sample Output:
        Not found!
    
    Explanation:
        The given string ddoes not contain any vowels, so 'Not found!' is returned.
"""

#!/bin/python3

import math
import os
import random
import re
import sys



#
# Complete the 'findSubstring' function below.
#
# The function is expected to return a STRING.
# The function accepts following parameters:
#  1. STRING s
#  2. INTEGER k
#

def findSubstring(s, k):
    # Write your code here
    vowels = set('aeiou')
    max_count = 0
    current_count = 0
    start_index = -1
    
    for i in range(k):
        if s[i] in vowels:
            current_count += 1
    if current_count > 0:
        max_count = current_count
        start_index = 0
    
    for i in range(k, len(s)):
        if s[i - k] in vowels:
            current_count -= 1
        if s[i] in vowels:
            current_count += 1
        if current_count > max_count:
            max_count = current_count
            start_index = i - k + 1
    
    if start_index == -1:
        return "Not found!"
    else:
        return s[start_index:start_index + k]

if __name__ == '__main__':
    fptr = open(os.environ['OUTPUT_PATH'], 'w')

    s = input()

    k = int(input().strip())

    result = findSubstring(s, k)

    fptr.write(result + '\n')

    fptr.close()
