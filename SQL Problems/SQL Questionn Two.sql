SELECT
    CASE
        WHEN IsPromoted = TRUE THEN '[PROMOTED] ' || CompanyName
        ELSE CompanyName
    END AS Name,
    CASE
        WHEN IsPromoted = TRUE THEN 'NULL'
        ELSE
            CASE
                WHEN Rating >= 4.5 THEN '*****'
                WHEN Rating >= 3.5 THEN '****'
                WHEN Rating >= 2.5 THEN '***'
                WHEN Rating >= 1.5 THEN '**'
                ELSE '*'
            END || ' (' || CAST(Rating AS TEXT) || ', based on ' || CAST(ReviewCount AS TEXT) || ' reviews)'
    END AS Rating
FROM
    Companies
ORDER BY
    CASE WHEN IsPromoted = TRUE THEN 0 ELSE 1 END, -- Promoted companies first
    CompanyName ASC;