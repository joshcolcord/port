import os
import re
import datetime
import json
import markdown

SOURCES_DIR = 'article-sources'
OUT_DIR = 'articles'
JSON_REGISTRY = 'jwriting_articles.js'

TEMPLATE = """<!DOCTYPE html>
<html lang="en">

<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title} — Joshua Colcord</title>
  <meta name="description" content="{description}">
  <style>
    @import url("https://fonts.googleapis.com/css2?family=Sorts+Mill+Goudy:ital@0;1&display=swap");

    :root {
      --background: #f1f0ec;
      --text: #1d1f23;
      --accent: #3a3d42;
      --muted: #8b9095;
      --line: #c9cdd1;
    }

    * {
      box-sizing: border-box;
    }

    body {
      margin: 0;
      min-height: 100vh;
      display: flex;
      flex-direction: column;
      align-items: center;
      background: var(--background);
      color: var(--text);
      font-family: "Sorts Mill Goudy", Georgia, "Times New Roman", serif;
      font-size: 15px;
      font-weight: 400;
      line-height: 1.6;
      padding: 0 24px 80px;
    }

    .page {
      width: min(100%, 620px);
      margin-top: 9vh;
      display: flex;
      flex-direction: column;
    }

    .article-header {
      margin-bottom: 12px;
      display: flex;
      justify-content: flex-start;
      align-items: baseline;
    }

    .back-link {
      display: inline-block;
      font-size: 15px;
      color: var(--muted);
      text-decoration: none;
      transition: color 0.15s;
      padding-bottom: 4px;
    }

    .back-link:hover {
      color: var(--text);
    }

    .article-date-top {
      font-size: 15px;
      color: var(--muted);
    }

    .article-title {
      font-size: 23px;
      font-weight: normal;
      margin: 0 0 32px 0;
      color: var(--text);
      line-height: 1.2;
      display: block;
      padding-bottom: 16px;
      border-bottom: 1px solid var(--line);
    }

    .meta-sep {
      margin: 0 8px;
      color: var(--muted);
      font-size: 15px;
    }

    article p, article li {
      margin: 0 0 16px 0;
      font-size: 16.5px;
      line-height: 1.6;
      color: var(--text);
    }

    article h2 {
      font-size: 1.75em;
      font-weight: normal;
      margin: 32px 0 16px 0;
      padding-bottom: 0.3em;
      color: var(--text);
      line-height: 1.2;
    }

    article h3 {
      font-size: 1.5em;
      font-weight: normal;
      margin: 28px 0 16px 0;
      color: var(--text);
      line-height: 1.2;
    }

    code {
      font-family: Menlo, Monaco, Consolas, 'Courier New', monospace;
      background: rgba(0, 0, 0, 0.05);
      padding: 0.2em 0.4em;
      border-radius: 3px;
      font-size: 0.85em;
      color: #000;
    }

    pre {
      margin: 0 0 16px 0;
      padding: 1em;
      overflow: auto;
      background: rgba(0, 0, 0, 0.03);
      border-radius: 3px;
    }

    pre code {
      padding: 0;
      background: transparent;
      font-size: 0.85em;
    }

    .article-figure {
      margin: 24px 0;
      padding: 0;
    }

    .article-figure img {
      width: 100%;
      border-radius: 8px;
      border: 1px solid var(--line);
    }

    .image-placeholder {
      width: 100%;
      aspect-ratio: 16 / 9;
      background-color: #e5e2db;
      border-radius: 8px;
      border: 1px solid var(--line);
      display: flex;
      align-items: center;
      justify-content: center;
      color: var(--muted);
      font-size: 13px;
    }

    .image-caption {
      font-size: 13px;
      color: var(--muted);
      text-align: center;
      margin-top: 10px;
      line-height: 1.4;
      font-style: italic;
    }

    .site-footer {
      width: 100%;
      text-align: center;
      margin-top: 48px;
      border-top: 1px solid var(--line);
      padding-top: 24px;
    }

    .footer-icons {
      display: flex;
      justify-content: center;
      gap: 14px;
      margin-bottom: 12px;
    }

    .footer-text {
      font-size: 13px;
      color: var(--muted);
    }

    .footer-link {
      color: var(--muted);
      text-decoration: underline;
      text-underline-offset: 0.12em;
      text-decoration-thickness: 1px;
    }

    .footer-link:hover {
      color: var(--text);
    }

    .icon-link {
      display: inline-flex;
      align-items: center;
      justify-content: center;
      color: var(--text);
      opacity: 1;
      transition: opacity 0.15s;
    }

    .icon-link:hover,
    .icon-link:focus-visible {
      opacity: 0.65;
    }

    .icon-link svg {
      width: 16px;
      height: 16px;
      fill: currentColor;
    }
  </style>
</head>

<body>

  <div class="page">
    <header class="article-header">
      <a class="back-link" href="../index.html#writing">← writing</a>
      <span class="meta-sep">/</span>
      <span class="article-date-top">{formatted_date}</span>
    </header>

    <main>
      <article>
        <h1 class="article-title">{title}</h1>

        {content}
      </article>
    </main>

    <footer class="site-footer">
      <div class="footer-icons" aria-label="Social links">
        <a class="icon-link" href="https://github.com/joshcolcord" target="_blank" rel="noopener noreferrer"
          aria-label="GitHub">
          <svg viewBox="0 0 15 15" fill="none" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">
            <path
              d="M7.49933 0.25C3.49635 0.25 0.25 3.49593 0.25 7.50024C0.25 10.703 2.32715 13.4206 5.2081 14.3797C5.57084 14.446 5.70302 14.2222 5.70302 14.0299C5.70302 13.8576 5.69679 13.4019 5.69323 12.797C3.67661 13.235 3.25112 11.825 3.25112 11.825C2.92132 10.9874 2.44599 10.7644 2.44599 10.7644C1.78773 10.3149 2.49584 10.3238 2.49584 10.3238C3.22353 10.375 3.60629 11.0711 3.60629 11.0711C4.25298 12.1788 5.30335 11.8588 5.71638 11.6732C5.78225 11.205 5.96962 10.8854 6.17658 10.7043C4.56675 10.5209 2.87415 9.89918 2.87415 7.12104C2.87415 6.32925 3.15677 5.68257 3.62053 5.17563C3.54576 4.99226 3.29697 4.25521 3.69174 3.25691C3.69174 3.25691 4.30015 3.06196 5.68522 3.99973C6.26337 3.83906 6.8838 3.75895 7.50022 3.75583C8.1162 3.75895 8.73619 3.83906 9.31523 3.99973C10.6994 3.06196 11.3069 3.25691 11.3069 3.25691C11.7026 4.25521 11.4538 4.99226 11.3795 5.17563C11.8441 5.68257 12.1245 6.32925 12.1245 7.12104C12.1245 9.9063 10.4292 10.5192 8.81452 10.6985C9.07444 10.9224 9.30633 11.3648 9.30633 12.0413C9.30633 13.0102 9.29742 13.7922 9.29742 14.0299C9.29742 14.2239 9.42828 14.4496 9.79591 14.3788C12.6746 13.4179 14.75 10.7025 14.75 7.50024C14.75 3.49593 11.5036 0.25 7.49933 0.25Z"
              fill="currentColor" fill-rule="evenodd" clip-rule="evenodd"></path>
          </svg>
        </a>
        <a class="icon-link" href="https://linkedin.com/in/joshcolcord/" target="_blank" rel="noopener noreferrer"
          aria-label="LinkedIn">
          <svg viewBox="0 0 15 15" fill="none" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">
            <path
              d="M2 1C1.44772 1 1 1.44772 1 2V13C1 13.5523 1.44772 14 2 14H13C13.5523 14 14 13.5523 14 13V2C14 1.44772 13.5523 1 13 1H2ZM3.05 6H4.95V12H3.05V6ZM5.075 4.005C5.075 4.59871 4.59371 5.08 4 5.08C3.4063 5.08 2.925 4.59871 2.925 4.005C2.925 3.41129 3.4063 2.93 4 2.93C4.59371 2.93 5.075 3.41129 5.075 4.005ZM12 8.35713C12 6.55208 10.8334 5.85033 9.67449 5.85033C9.29502 5.83163 8.91721 5.91119 8.57874 6.08107C8.32172 6.21007 8.05265 6.50523 7.84516 7.01853H7.79179V6.00044H6V12.0047H7.90616V8.8112C7.8786 8.48413 7.98327 8.06142 8.19741 7.80987C8.41156 7.55832 8.71789 7.49825 8.95015 7.46774H9.02258C9.62874 7.46774 10.0786 7.84301 10.0786 8.78868V12.0047H11.9847L12 8.35713Z"
              fill="currentColor" fill-rule="evenodd" clip-rule="evenodd"></path>
          </svg>
        </a>
        <a class="icon-link" href="mailto:jcolcord@wisc.edu" target="_blank" rel="noopener noreferrer"
          aria-label="Email">
          <svg viewBox="0 0 15 15" fill="none" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">
            <path
              d="M1 2C0.447715 2 0 2.44772 0 3V12C0 12.5523 0.447715 13 1 13H14C14.5523 13 15 12.5523 15 12V3C15 2.44772 14.5523 2 14 2H1ZM1 3L14 3V3.92494C13.9174 3.92486 13.8338 3.94751 13.7589 3.99505L7.5 7.96703L1.24112 3.99505C1.16621 3.94751 1.0826 3.92486 1 3.92494V3ZM1 4.90797V12H14V4.90797L7.74112 8.87995C7.59394 8.97335 7.40606 8.97335 7.25888 8.87995L1 4.90797Z"
              fill="currentColor" fill-rule="evenodd" clip-rule="evenodd"></path>
          </svg>
        </a>
      </div>
      <div class="footer-text">
        Joshua Colcord {current_year} &middot; Hosted locally on <a class="footer-link" href="https://blog.jcol.cx/mithrandir"
          target="_blank" rel="noopener">Mithrandir</a>
      </div>
    </footer>
  </div>

</body>
</html>"""

def parse_frontmatter(content):
    match = re.match(r'^---\n(.*?)\n---\n(.*)', content, re.DOTALL)
    if not match:
        return {}, content
    yaml_text = match.group(1)
    body = match.group(2)
    meta = {}
    for line in yaml_text.split('\n'):
        if ':' in line:
            key, val = line.split(':', 1)
            meta[key.strip()] = val.strip().strip('"\'')
    return meta, body

def format_date(date_str):
    try:
        parts = date_str.split(' ')
        if len(parts) == 3:
            months = {
                "jan": "January", "feb": "February", "mar": "March", "apr": "April",
                "may": "May", "jun": "June", "jul": "July", "aug": "August",
                "sep": "September", "oct": "October", "nov": "November", "dec": "December"
            }
            month = months.get(parts[0].lower(), parts[0])
            day = int(parts[1])
            year = parts[2]
            return f"{month} {day}, {year}"
    except Exception:
        pass
    return date_str

def fix_images(html):
    # Wrap standard markdown images <img alt="caption" src="url" /> in the <figure> format
    def replacer(match):
        alt = match.group(1) or ""
        src = match.group(2)
        return f'''<figure class="article-figure">
          <img src="{src}" alt="{alt}">
          <figcaption class="image-caption">
            {alt}
          </figcaption>
        </figure>'''
    
    # Simple regex to catch <img alt="..." src="..." /> generated by markdown
    return re.sub(r'<img\s+alt="([^"]*)"\s+src="([^"]+)"\s*/?>', replacer, html)

def update_registry(meta, html_filename):
    articles = []
    if os.path.exists(JSON_REGISTRY):
        with open(JSON_REGISTRY, 'r') as f:
            content = f.read().strip()
            if content.startswith('const jwritingArticles = '):
                json_str = content[len('const jwritingArticles = '):].rstrip(';')
                try:
                    articles = json.loads(json_str)
                except json.JSONDecodeError:
                    articles = []
                
    link_str = f"articles/{html_filename}"
    
    # Check if article already exists
    for article in articles:
        if article.get('article_link') == link_str:
            article['article_name'] = meta.get('title', 'Untitled')
            article['description'] = meta.get('description', '')
            article['date'] = meta.get('date', '')
            article['github_link'] = meta.get('github_link', '')
            break
    else:
        # Add new
        new_entry = {
            "article_name": meta.get('title', 'Untitled'),
            "description": meta.get('description', ''),
            "date": meta.get('date', ''),
            "github_link": meta.get('github_link', ''),
            "article_link": link_str
        }
        articles.insert(0, new_entry)
        
    with open(JSON_REGISTRY, 'w') as f:
        f.write('const jwritingArticles = ')
        json.dump(articles, f, indent=2)
        f.write(';')
    print(f"Updated registry with {html_filename}")

def build_articles():
    if not os.path.exists(SOURCES_DIR):
        print(f"Source directory '{SOURCES_DIR}' not found.")
        return
        
    os.makedirs(OUT_DIR, exist_ok=True)
    
    current_year = datetime.datetime.now().year

    for filename in os.listdir(SOURCES_DIR):
        if not filename.endswith('.md'):
            continue
            
        filepath = os.path.join(SOURCES_DIR, filename)
        with open(filepath, 'r') as f:
            content = f.read()
            
        meta, md_body = parse_frontmatter(content)
        
        html_body = markdown.markdown(md_body)
        html_body = fix_images(html_body)
        
        formatted_date = format_date(meta.get('date', ''))
        
        final_html = TEMPLATE.replace('{title}', meta.get('title', 'Untitled'))\
                             .replace('{description}', meta.get('description', ''))\
                             .replace('{formatted_date}', formatted_date)\
                             .replace('{content}', html_body)\
                             .replace('{current_year}', str(current_year))
        
        slug = meta.get('slug')
        if slug:
            out_filename = f"{slug}.html"
        else:
            out_filename = filename.replace('.md', '.html')
            
        out_filepath = os.path.join(OUT_DIR, out_filename)
        
        with open(out_filepath, 'w') as f:
            f.write(final_html)
            
        print(f"Compiled {out_filename}")
        update_registry(meta, out_filename)

if __name__ == "__main__":
    build_articles()
