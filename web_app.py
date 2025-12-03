import sys
from pathlib import Path

# run using
# uv run web_app.py

# 1. Add cli/ to sys.path
ROOT = Path(__file__).resolve().parent
CLI_DIR = ROOT / "cli"
if str(CLI_DIR) not in sys.path:
    sys.path.insert(0, str(CLI_DIR))

from flask import Flask, request, render_template_string
from lib.keyword_search import keyword_search

app = Flask(__name__)

HTML_PAGE = """
<!doctype html>
<html>
<head>
  <meta charset="utf-8">
  <title>Movie Search</title>
  <style>
    body {
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
    }
    h1 {
      font-weight: 600;
    }
    form {
      margin-bottom: 1.5rem;
    }
    input[type="text"] {
      padding: 0.4rem 0.6rem;
      width: 60%;
      font-size: 1rem;
    }
    button {
      padding: 0.4rem 0.8rem;
      font-size: 1rem;
      cursor: pointer;
    }
    .movie {
      background: #fff;
      border-radius: 4px;
      padding: 0.75rem 1rem;
      margin-bottom: 0.75rem;
      box-shadow: 0 1px 2px rgba(0,0,0,0.08);
    }
    .movie-title {
      font-weight: 600;
      margin: 0 0 0.25rem;
    }
    .movie-id {
      color: #666;
      font-size: 0.85rem;
    }
    .movie-description {
      margin: 0.25rem 0 0;
    }
    .movie-header {
  display: flex;
  justify-content: space-between;
  align-items: baseline;
  cursor: pointer;
}

.movie-toggle {
  font-size: 0.85rem;
  color: #0070c9;
}

.movie-description {
  margin: 0.4rem 0 0;
}

.movie-description.collapsed {
  display: none;
}
  </style>
</head>
<script>
  function toggleDescription(headerEl) {
    const description = headerEl.nextElementSibling;
    const toggleText = headerEl.querySelector('.movie-toggle');
    const isCollapsed = description.classList.toggle('collapsed');
    toggleText.textContent = isCollapsed ? '[show]' : '[hide]';
  }
</script>
<body>
  <h1>Search Movies</h1>
  <form method="get">
    <input type="text" name="q" placeholder="Search..." value="{{ query or '' }}">
    <button type="submit">Search</button>
  </form>

  {% if results is not none %}
    <h2>Results ({{ results|length }})</h2>
    {% if results %}
      {% for movie in results %}
  <div class="movie">
    <div class="movie-header" onclick="toggleDescription(this)">
      <div class="movie-title">{{ movie.title }}</div>
      <div class="movie-id">ID: {{ movie.id }}</div>
      <div class="movie-toggle">[show]</div>
    </div>
    <div class="movie-description collapsed">
      {{ movie.description }}
    </div>
  </div>
{% endfor %}
    {% else %}
      <p>No results found.</p>
    {% endif %}
  {% endif %}
</body>
</html>
"""

@app.route("/", methods=["GET"])
def index():
    query = request.args.get("q")
    results = None
    if query:
        # call your existing search logic
        results = keyword_search(query, 10).movies
    return render_template_string(HTML_PAGE, query=query, results=results)

if __name__ == "__main__":
    app.run(debug=True)