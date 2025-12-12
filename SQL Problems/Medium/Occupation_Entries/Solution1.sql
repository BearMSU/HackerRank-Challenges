-- Solution 1: My Solution (It's dirty but it works)

/*
    Enter your query here and follow these instructions:
    1. Please append a semicolon ";" at the end of the query and enter your query in a single line to avoid error.
    2. The AS keyword causes errors, so follow this convention: "Select t.Field From table1 t" instead of "select t.Field From table1 AS t"
    3. Type your code immediately after comment. Don't leave any blank line.
*/




SELECT
    -- 1. Combine Name and Abbreviation (First Column is Fine)
    Name || '(' || 
        CASE Occupation 
            WHEN 'Doctor' THEN 'D'
            WHEN 'Actor' THEN 'A'
            WHEN 'Singer' THEN 'S'
            WHEN 'Professor' THEN 'P'
            ELSE '?'
        END 
    || ')' AS new_occ
FROM
    OCCUPATIONS

UNION

SELECT
    -- 2. Use a Window Function to Count Per Occupation
    'There are a total of ' ||
    (
        COUNT(Occupation) OVER (PARTITION BY Occupation) 
    ) 
    || ' ' 
    || 
    -- Use a clean CASE to select the appropriate pluralized occupation name
    CASE Occupation
        WHEN 'Doctor' THEN 'doctors.'
        WHEN 'Actor' THEN 'actors.'
        WHEN 'Singer' THEN 'singers.'
        WHEN 'Professor' THEN 'professors.'
        ELSE 'unknowns.'
    END AS new_occ
FROM 
    OCCUPATIONS;