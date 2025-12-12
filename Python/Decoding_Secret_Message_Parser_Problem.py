import requests
from bs4 import BeautifulSoup

def print_unicode_grid(google_doc_url: str):
    """
    Fetches a published Google Doc (table of x, char, y), builds the grid,
    auto-detects orientation, corrects it, and prints the grid so letters
    appear in the expected orientation.
    """
    # Fetch HTML
    resp = requests.get(google_doc_url)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "html.parser")

    # Collect rows from the first table we find (skip header if present)
    table = soup.find("table")
    if not table:
        print("No table found in document.")
        return

    rows = table.find_all("tr")
    points = []
    # If the first row looks like headers (non-numeric), skip it:
    start_idx = 0
    if rows:
        first_cols = [c.get_text(strip=True) for c in rows[0].find_all(["td","th"])]
        # Detect header: if coords are not numeric in first row, skip it
        if len(first_cols) >= 3:
            try:
                int(first_cols[0])
            except Exception:
                start_idx = 1

    for tr in rows[start_idx:]:
        cols = [c.get_text(strip=True) for c in tr.find_all("td")]
        if len(cols) >= 3:
            # first col -> x, second col -> char, third col -> y
            try:
                x = int(cols[0])
                ch = cols[1]
                y = int(cols[2])
                if ch == "":
                    ch = " "  # be safe
                points.append((ch, x, y))
            except ValueError:
                # skip bad rows
                continue

    if not points:
        print("No character data found.")
        return

    # Build grid
    max_x = max(x for (_, x, _) in points)
    max_y = max(y for (_, _, y) in points)
    width = max_x + 1
    height = max_y + 1

    grid = [[' ' for _ in range(width)] for _ in range(height)]
    for ch, x, y in points:
        # If same coordinate appears multiple times, last one wins
        if 0 <= y < height and 0 <= x < width:
            grid[y][x] = ch

    # Helper to compute density (non-space counts)
    def col_densities(g):
        w = len(g[0])
        h = len(g)
        return [sum(1 for r in range(h) if g[r][c] != ' ') for c in range(w)]

    def row_densities(g):
        w = len(g[0])
        return [sum(1 for c in range(w) if row[c] != ' ') for row in g]

    # Detect horizontal flip: if rightmost col is denser than leftmost => flip horizontally
    cols = col_densities(grid)
    flip_x = False
    if len(cols) >= 2 and cols[0] < cols[-1]:
        flip_x = True

    # Detect vertical flip: if bottom row is denser than top row => flip vertically
    rows_density = row_densities(grid)
    flip_y = False
    if len(rows_density) >= 2 and rows_density[0] < rows_density[-1]:
        flip_y = True

    # Apply flips if detected
    if flip_x:
        grid = [list(reversed(row)) for row in grid]
    if flip_y:
        grid = list(reversed(grid))

    # Print (y increasing downward, rows printed top -> bottom)
    for row in grid:
        print(''.join(row))

print_unicode_grid("https://docs.google.com/document/d/e/2PACX-1vRPzbNQcx5UriHSbZ-9vmsTow_R6RRe7eyAU60xIF9Dlz-vaHiHNO2TKgDi7jy4ZpTpNqM7EvEcfr_p/pub")
