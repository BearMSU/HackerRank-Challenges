#!/bin/python3

import math
import os
import random
import re
import sys



#
# Complete the 'getSmallestPalindrome' function below.
#
# The function is expected to return a STRING.
# The function accepts STRING s as parameter.
#

def getSmallestPalindrome(s):
    # Write your code here
    n = len(s)
    char_counts = [0] * 26
    q_count = 0
    
    for char in s:
        if char == '?':
            q_count += 1
        else:
            char_counts[ord(char) - ord('a')] += 1
    required_odd_count = 1 if n % 2 != 0 else 0
    
    odd_indices = []
    
    for i in range(26):
        if char_counts[i] % 2 != 0:
            odd_indices.append(i)
    
    num_odd_existing = len(odd_indices)
    
    temp_q_count = q_count
    
    if num_odd_existing > required_odd_count:
        to_balance = num_odd_existing - required_odd_count
        
        if temp_q_count < to_balance:
            return "-1"
        
        temp_q_count -= to_balance
        
        for idx in sorted(odd_indices):
            if to_balance == 0:
                break
            char_counts[idx] += 1
            to_balance -= 1
    elif num_odd_existing < required_odd_count:
        if temp_q_count == 0:
            return "-1"
        
        temp_q_count -= 1
        char_counts[0] += 1
    
    if temp_q_count % 2 != 0:
        return "-1"
    
    char_counts[0] += temp_q_count
    
    first_half_chars = []
    final_middle_char = ''
    
    for i in range(26):
        char = chr(ord('a') + i)
        first_half_chars.append(char * (char_counts[i] // 2))
        
        if char_counts[i] % 2 != 0:
            final_middle_char = char
    
    first_half_str = "".join(first_half_chars)
    first_half_reversed_str = first_half_str[::-1]
    
    result = first_half_str + final_middle_char + first_half_reversed_str
    
    return result
       