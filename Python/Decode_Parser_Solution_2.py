import requests
from bs4 import BeautifulSoup

def print_unicode_grid(google_doc_url: str):
    """Fetches a published Google Doc table of (x, char, y), builds and prints the grid."""

    # Fetch and parse the HTML
    soup = BeautifulSoup(requests.get(google_doc_url).text, "html.parser")
    rows = soup.find_all("tr")

    points = []
    # Skip header row automatically
    for tr in rows[1:]:
        cols = [c.get_text(strip=True) for c in tr.find_all("td")]
        if len(cols) < 3:
            continue
        try:
            x, char, y = int(cols[0]), cols[1] or ' ', int(cols[2])
            points.append((char, x, y))
        except ValueError:
            continue

    if not points:
        print("No character data found.")
        return

    # Compute bounds
    max_x = max(x for _, x, _ in points)
    max_y = max(y for _, _, y in points)

    # Build grid efficiently
    grid = [[' ' for _ in range(max_x + 1)] for _ in range(max_y + 1)]
    for char, x, y in points:
        grid[y][x] = char

    # Auto-orientation detection (based on filled character distribution)
    left_fill = sum(row[0] != ' ' for row in grid)
    right_fill = sum(row[-1] != ' ' for row in grid)
    top_fill = sum(ch != ' ' for ch in grid[0])
    bottom_fill = sum(ch != ' ' for ch in grid[-1])

    if right_fill > left_fill:
        grid = [list(reversed(row)) for row in grid]
    if bottom_fill > top_fill:
        grid.reverse()

    # Print grid
    for row in grid:
        print(''.join(row))

  