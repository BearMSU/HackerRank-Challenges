from collections import Counter

def getSmallestPalindrome(s: str) -> str:
    n = len(s)
    char_counts = Counter()
    q_marks = 0
    for char in s:
        if char == '?':
            q_marks += 1
        else:
            char_counts[char] += 1

    # Identify characters with odd counts
    odd_chars = []
    for char_code in range(ord('a'), ord('z') + 1):
        char = chr(char_code)
        if char_counts[char] % 2 != 0:
            odd_chars.append(char)

    # Calculate how many '?' are needed to make existing odd counts even
    needed_q_for_balance = max(0, len(odd_chars) - 1)

    if q_marks < needed_q_for_balance:
        return "-1" # Not enough '?' to balance existing odd counts

    q_marks_remaining = q_marks - needed_q_for_balance

    # Adjust counts for characters that needed balancing
    # The first (len(odd_chars) - 1) odd characters will become even.
    # The last odd character (if any) will remain odd and become the potential middle.
    # If len(odd_chars) is 0 or 1, then needed_q_for_balance is 0.
    for i in range(len(odd_chars)):
        if i < len(odd_chars) - 1: # These characters will have their counts made even
            char_counts[odd_chars[i]] += 1 # We 'use' a '?' to make it even
        # If len(odd_chars) == 0, then we don't enter this loop.
        # If len(odd_chars) == 1, then odd_chars[0] is the potential middle.
        # We don't change its count here.

    # Now, q_marks_remaining can be used to add pairs or a single middle char.
    # If q_marks_remaining is odd, one '?' will be the middle char.

    first_half = []
    middle_char = ""

    # Build the first half of the palindrome
    for char_code in range(ord('a'), ord('z') + 1):
        char = chr(char_code)
        # Add half of the existing even count characters
        first_half.append(char * (char_counts[char] // 2))

    # Distribute remaining '?' marks for pairs in the first half (lexicographically smallest)
    # The remaining_q_marks can be distributed as 'a's, 'b's, etc.
    # We add q_marks_remaining // 2 'a's, then 'b's, etc., to the first half.
    q_pairs_to_add = q_marks_remaining // 2
    for char_code in range(ord('a'), ord('z') + 1):
        char = chr(char_code)
        if q_pairs_to_add > 0:
            count_to_add = min(q_pairs_to_add, (n // 2) - len("".join(first_half))) # Don't exceed half length
            if count_to_add < 0: count_to_add = 0 # Safety check
            first_half.append(char * count_to_add)
            q_pairs_to_add -= count_to_add
        else:
            break

    # Determine the middle character
    if n % 2 != 0: # Odd length string
        if q_marks_remaining % 2 != 0: # If remaining '?' are odd, use an 'a' as middle
            middle_char = 'a'
        elif len(odd_chars) == 1: # If there was a single odd char, it's the middle
            middle_char = odd_chars[0]
        else: # Should not happen if logic is correct, but for safety
            # If no odd chars and remaining_q_marks is even,
            # this means all chars are even or made even by '?'
            # and no '?' is left for middle. This case means middle_char should be empty if n is even.
            # But n is odd here. This implies a contradiction.
            # If n is odd, there must be a middle character.
            # If all character counts are even and q_marks_remaining is even, then it's impossible for an odd length string.
            return "-1" # This case means no way to make a middle character

    # If the combined length of first_half and middle_char doesn't match n // 2 or n // 2 + 1, it's an issue.
    # This suggests our construction logic for `first_half` is not filling it up to the required length (n // 2)
    # or the distribution of `q_pairs_to_add` is flawed.

    # Re-evaluating the construction of the first_half and middle_char:
    # A more robust way:
    # Construct the character counts for the final palindrome first.
    final_counts = Counter(char_counts) # Start with existing counts
    q_to_distribute = q_marks_remaining # Q marks left after balancing initial odds

    # Handle the middle character (if string length is odd)
    if n % 2 != 0:
        if len(odd_chars) == 1: # We already have a potential middle char
            middle_char = odd_chars[0]
            # It's count remains odd (e.g., 1, 3, 5...)
        elif len(odd_chars) == 0: # No existing odd chars
            if q_to_distribute > 0:
                middle_char = 'a' # Use an 'a' as the middle
                q_to_distribute -= 1
            else:
                return "-1" # Odd length string, but no middle char from existing or '?'
        else: # More than one odd char remaining after needed_q_for_balance, this should not happen
            return "-1" # This case should have been caught by q_marks < needed_q_for_balance if it was truly impossible.
            # If we reached here, it means we used q_marks to balance all but one odd_char.
            # The remaining single odd_char becomes the middle.

    # Distribute the remaining '?' marks for pairs
    for char_code in range(ord('a'), ord('z') + 1):
        char = chr(char_code)
        # Add as many pairs of 'char' as possible from remaining '?'
        pairs_from_q = q_to_distribute // 2
        final_counts[char] += pairs_from_q * 2
        q_to_distribute -= pairs_from_q * 2

    # Now, construct the palindrome based on final_counts
    final_left_half_chars = []
    for char_code in range(ord('a'), ord('z') + 1):
        char = chr(char_code)
        final_left_half_chars.append(char * (final_counts[char] // 2))

    final_left_half = "".join(final_left_half_chars)

    # The middle character needs to be determined carefully.
    # If n is odd, and we have one odd char count, that's the middle.
    # If n is odd, and all counts are even (or made even), and we have remaining '?', use 'a'.
    # If n is even, there is no middle character.

    # Re-re-evaluate: It's simpler to think about `final_counts` directly after
    # distributing `q_marks` and dealing with the potential middle character.

    # Step 1: Initialize final_counts
    final_counts = Counter(char_counts)
    q_left = q_marks

    # Step 2: Handle existing odd counts to make them even (using '?'s)
    # The idea is to make all counts even except for at most one.
    # If we have N odd counts, we need N-1 '?'s to make N-1 of them even.
    # The last one (if N is odd) remains odd and will be the middle.
    # If N is even, all N counts need to be made even, using N '?'s.
    # Let's collect which specific characters currently have odd counts.
    current_odd_chars = []
    for char_code in range(ord('a'), ord('z') + 1):
        char = chr(char_code)
        if final_counts[char] % 2 != 0:
            current_odd_chars.append(char)

    if len(current_odd_chars) > q_left + (1 if n % 2 != 0 else 0):
        # If we have too many odd characters that cannot be balanced
        # (even if we use a middle char for odd length strings)
        return "-1"

    # Distribute '?' to make existing odd counts even.
    # We prioritize making existing odd characters even.
    # If n is odd, one odd character can remain as the middle.
    # If n is even, all characters must have even counts.
    target_odd_count = 1 if n % 2 != 0 else 0
    num_to_make_even = len(current_odd_chars) - target_odd_count
    if num_to_make_even < 0: num_to_make_even = 0 # No need to make anything even if already 0 or 1 odd count

    if q_left < num_to_make_even:
        return "-1" # Not enough '?' to balance existing odd counts

    # Make the first `num_to_make_even` of `current_odd_chars` even using '?'s
    for i in range(num_to_make_even):
        char = current_odd_chars[i]
        final_counts[char] += 1 # We essentially 'used' a '?' to make it even
        q_left -= 1

    # At this point, `final_counts` might have at most one odd character (if n is odd).
    # `q_left` contains the remaining '?'s.

    # Now, add remaining `q_left` to `final_counts` in pairs, prioritizing 'a' then 'b', etc.
    # This ensures the lexicographically smallest result.
    for char_code in range(ord('a'), ord('z') + 1):
        char = chr(char_code)
        if q_left >= 2:
            final_counts[char] += 2
            q_left -= 2
        elif q_left == 1 and n % 2 != 0: # If odd '?' left and string length is odd, use as middle 'a'
            # We will handle the single middle 'a' in the final assembly.
            break # No more '?' for pairs

    # Final Check: if q_left is 1 but n is even, impossible to use.
    if q_left == 1 and n % 2 == 0:
        return "-1"

    # Construct the palindrome
    first_half_chars = []
    middle_char = ""

    # Determine the actual middle character
    current_odd_char_for_middle = None
    for char_code in range(ord('a'), ord('z') + 1):
        char = chr(char_code)
        if final_counts[char] % 2 != 0:
            current_odd_char_for_middle = char
            break # There should be at most one.

    if n % 2 != 0: # Odd length string
        if current_odd_char_for_middle:
            middle_char = current_odd_char_for_middle
        elif q_left == 1: # We have one '?' left, use it as 'a'
            middle_char = 'a'
        else: # Should not happen, implies no middle char for odd length
            return "-1"
    elif current_odd_char_for_middle: # Even length string with an odd count
        return "-1" # Impossible, all counts must be even

    # Build the first half using sorted characters (lexicographically smallest)
    for char_code in range(ord('a'), ord('z') + 1):
        char = chr(char_code)
        first_half_chars.append(char * (final_counts[char] // 2))

    first_half = "".join(first_half_chars)
    second_half = first_half[::-1]

    return first_half + middle_char + second_half      
