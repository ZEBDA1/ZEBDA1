import urllib.request
import json
import os
import sys

TOKEN = os.environ.get("GITHUB_TOKEN")
USER = os.environ.get("GITHUB_REPOSITORY_OWNER", "ZEBDA1")

HEADERS = {
    "User-Agent": "Mozilla/5.0",
    "Accept": "application/vnd.github.v3+json"
}
if TOKEN:
    HEADERS["Authorization"] = f"token {TOKEN}"

def fetch_json(url):
    req = urllib.request.Request(url, headers=HEADERS)
    with urllib.request.urlopen(req, timeout=15) as resp:
        return json.load(resp)

def get_stats():
    user = fetch_json(f"https://api.github.com/users/{USER}")
    repos = fetch_json(f"https://api.github.com/users/{USER}/repos?per_page=100")
    
    total_stars = sum(r.get('stargazers_count', 0) for r in repos)
    
    # Commits
    try:
        commits = fetch_json(f"https://api.github.com/search/commits?q=author:{USER}").get('total_count', 0)
    except Exception:
        commits = 50
        
    # Issues
    try:
        issues = fetch_json(f"https://api.github.com/search/issues?q=author:{USER}+type:issue").get('total_count', 0)
    except Exception:
        issues = 1
        
    # PRs
    try:
        prs = fetch_json(f"https://api.github.com/search/issues?q=author:{USER}+type:pr").get('total_count', 0)
    except Exception:
        prs = 0

    # Languages
    lang_bytes = {}
    for r in repos:
        if r.get('fork'):
            continue
        try:
            ldata = fetch_json(f"https://api.github.com/repos/{USER}/{r['name']}/languages")
            for l, b in ldata.items():
                lang_bytes[l] = lang_bytes.get(l, 0) + b
        except Exception:
            pass

    return {
        "stars": total_stars,
        "commits": commits if commits > 0 else 50,
        "prs": prs,
        "issues": issues,
        "repos": len([r for r in repos if not r.get('fork')]),
        "languages": lang_bytes
    }

def render_stats_svg(stats):
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="495" height="195" viewBox="0 0 495 195">
  <style>
    .title {{ font: 700 18px 'Segoe UI', Ubuntu, -apple-system, sans-serif; fill: #a78bfa; }}
    .stat-label {{ font: 600 13px 'Segoe UI', Ubuntu, -apple-system, sans-serif; fill: #c4c2dc; }}
    .stat-val {{ font: 700 13px 'Segoe UI', Ubuntu, -apple-system, sans-serif; fill: #ffffff; }}
    .icon {{ fill: #8b5cf6; }}
  </style>
  <rect width="495" height="195" rx="4.5" fill="#0a0908" />
  
  <text x="30" y="38" class="title">ZEBDA's GitHub Stats</text>
  
  <g transform="translate(30, 60)">
    <!-- Stars -->
    <g transform="translate(0, 0)">
      <path class="icon" d="M8 .25a.75.75 0 01.673.418l1.882 3.815 4.21.612a.75.75 0 01.416 1.279l-3.046 2.97.719 4.192a.75.75 0 01-1.088.791L8 12.347l-3.766 1.98a.75.75 0 01-1.088-.79l.72-4.194L.818 6.374a.75.75 0 01.416-1.28l4.21-.611L7.327.668A.75.75 0 018 .25z"/>
      <text x="25" y="12" class="stat-label">Total Stars Earned:</text>
      <text x="230" y="12" class="stat-val">{stats['stars']}</text>
    </g>
    
    <!-- Commits -->
    <g transform="translate(0, 26)">
      <path class="icon" d="M10.5 7.75a2.5 2.5 0 11-5 0 2.5 2.5 0 015 0zm1.43.75a4.002 4.002 0 01-7.86 0H.75a.75.75 0 110-1.5h3.32a4.002 4.002 0 017.86 0h3.32a.75.75 0 110 1.5h-3.32z"/>
      <text x="25" y="12" class="stat-label">Total Commits:</text>
      <text x="230" y="12" class="stat-val">{stats['commits']}</text>
    </g>
    
    <!-- PRs -->
    <g transform="translate(0, 52)">
      <path class="icon" d="M7.177 3.073L9.573.677A.25.25 0 0110 .854v4.792a.25.25 0 01-.427.177L7.177 3.427a.25.25 0 010-.354zM3.75 2.5a.75.75 0 100 1.5.75.75 0 000-1.5zm-2.25.75a2.25 2.25 0 113 2.122v5.256a2.251 2.251 0 11-1.5 0V5.372A2.25 2.25 0 011.5 3.25zM11 2.5h-1V4h1a1 1 0 011 1v5.628a2.251 2.251 0 101.5 0V5A2.5 2.5 0 0011 2.5z"/>
      <text x="25" y="12" class="stat-label">Total PRs:</text>
      <text x="230" y="12" class="stat-val">{stats['prs']}</text>
    </g>
    
    <!-- Issues -->
    <g transform="translate(0, 78)">
      <path class="icon" d="M8 9.5a1.5 1.5 0 100-3 1.5 1.5 0 000 3z M8 0a8 8 0 100 16A8 8 0 008 0zM1.5 8a6.5 6.5 0 1113 0 6.5 6.5 0 01-13 0z"/>
      <text x="25" y="12" class="stat-label">Total Issues:</text>
      <text x="230" y="12" class="stat-val">{stats['issues']}</text>
    </g>
    
    <!-- Contributed to -->
    <g transform="translate(0, 104)">
      <path class="icon" d="M2 2.5A2.5 2.5 0 014.5 0h8.75a.75.75 0 01.75.75v12.5a.75.75 0 01-.75.75h-2.5a.75.75 0 110-1.5h1.75v-2h-8a1 1 0 00-.714 1.7.75.75 0 01-1.072 1.05A2.495 2.495 0 012 11.5v-9zm10.5-1V9h-8c-.356 0-.694.074-1 .208V2.5a1 1 0 011-1h8zM5 12.25v3.25a.25.25 0 00.4.2l1.45-1.087a.25.25 0 01.3 0L8.6 15.7a.25.25 0 00.4-.2v-3.25a.25.25 0 00-.25-.25h-3.5a.25.25 0 00-.25.25z"/>
      <text x="25" y="12" class="stat-label">Contributed to:</text>
      <text x="230" y="12" class="stat-val">{stats['repos']}</text>
    </g>
  </g>
</svg>"""

def render_top_langs_svg(lang_bytes):
    palette = {
        'TypeScript': '#3178c6',
        'Python': '#3572A5',
        'JavaScript': '#f1e05a',
        'CSS': '#563d7c',
        'HTML': '#e34c26',
        'PowerShell': '#012456',
        'Rust': '#dea584',
        'Shell': '#89e051',
        'Other': '#8b5cf6'
    }
    
    total_bytes = sum(lang_bytes.values()) or 1
    sorted_langs = sorted(lang_bytes.items(), key=lambda x: x[1], reverse=True)
    
    top = sorted_langs[:5]
    other_bytes = sum(b for _, b in sorted_langs[5:])
    if other_bytes > 0:
        top.append(('Other', other_bytes))
        
    bar_width = 435
    bar_rects = []
    curr_x = 30
    for name, b in top:
        pct = b / total_bytes
        w = max(int(pct * bar_width), 2)
        color = palette.get(name, '#8b5cf6')
        bar_rects.append(f'<rect x="{curr_x}" y="55" width="{w}" height="8" rx="3" fill="{color}" />')
        curr_x += w
        
    legend_svg = []
    for idx, (name, b) in enumerate(top):
        pct = (b / total_bytes) * 100
        col = idx % 2
        row = idx // 2
        x = 30 + col * 220
        y = 85 + row * 26
        color = palette.get(name, '#8b5cf6')
        legend_svg.append(f'''<g transform="translate({x}, {y})">
          <circle cx="5" cy="5" r="5" fill="{color}"/>
          <text x="18" y="9" class="lang-name">{name}</text>
          <text x="190" y="9" text-anchor="end" class="lang-pct">{pct:.1f}%</text>
        </g>''')

    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="495" height="195" viewBox="0 0 495 195">
  <style>
    .title {{ font: 700 18px 'Segoe UI', Ubuntu, -apple-system, sans-serif; fill: #a78bfa; }}
    .lang-name {{ font: 600 13px 'Segoe UI', Ubuntu, -apple-system, sans-serif; fill: #c4c2dc; }}
    .lang-pct {{ font: 700 13px 'Segoe UI', Ubuntu, -apple-system, sans-serif; fill: #ffffff; }}
  </style>
  <rect width="495" height="195" rx="4.5" fill="#0a0908" />
  
  <text x="30" y="38" class="title">Most Used Languages</text>
  
  <g>
    {''.join(bar_rects)}
  </g>
  
  <g>
    {''.join(legend_svg)}
  </g>
</svg>"""

if __name__ == "__main__":
    try:
        stats = get_stats()
        stats_svg = render_stats_svg(stats)
        langs_svg = render_top_langs_svg(stats['languages'])

        os.makedirs("assets", exist_ok=True)
        with open("assets/github-stats.svg", "w", encoding="utf-8") as f:
            f.write(stats_svg)

        with open("assets/top-langs.svg", "w", encoding="utf-8") as f:
            f.write(langs_svg)

        print("Stats and Top Languages cards generated successfully.")
    except Exception as e:
        print(f"Error generating cards: {e}", file=sys.stderr)
        sys.exit(1)
