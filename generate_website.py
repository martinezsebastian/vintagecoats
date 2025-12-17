#!/usr/bin/env python3
"""
Generate static HTML website from database
"""
import sqlite3
from datetime import datetime
import json

def generate_website():
    """Generate index.html from database"""

    # Connect to database
    conn = sqlite3.connect('seen_items.db')
    cursor = conn.cursor()

    # Get all items, sorted by date (newest first)
    cursor.execute('''
        SELECT id, title, url, price, source, found_date, image_url
        FROM seen_items
        ORDER BY found_date DESC
    ''')

    items = cursor.fetchall()
    conn.close()

    # Count by source
    source_counts = {}
    for item in items:
        source = item[4]
        source_counts[source] = source_counts.get(source, 0) + 1

    # Generate HTML
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Vintage Coat Finder - {len(items)} Items</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }}

        .container {{
            max-width: 1200px;
            margin: 0 auto;
        }}

        header {{
            background: white;
            padding: 30px;
            border-radius: 15px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
            margin-bottom: 30px;
        }}

        h1 {{
            font-size: 2.5em;
            color: #333;
            margin-bottom: 10px;
        }}

        .stats {{
            display: flex;
            gap: 20px;
            flex-wrap: wrap;
            margin-top: 20px;
        }}

        .stat {{
            background: #f0f0f0;
            padding: 10px 20px;
            border-radius: 8px;
            font-size: 0.9em;
        }}

        .stat strong {{
            color: #667eea;
        }}

        .controls {{
            background: white;
            padding: 20px;
            border-radius: 15px;
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
            margin-bottom: 20px;
            display: flex;
            gap: 15px;
            flex-wrap: wrap;
            align-items: center;
        }}

        .search-box {{
            flex: 1;
            min-width: 250px;
        }}

        input, select {{
            padding: 12px 15px;
            border: 2px solid #e0e0e0;
            border-radius: 8px;
            font-size: 1em;
            width: 100%;
            transition: border-color 0.3s;
        }}

        input:focus, select:focus {{
            outline: none;
            border-color: #667eea;
        }}

        .items-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
            gap: 20px;
        }}

        .item-card {{
            background: white;
            border-radius: 12px;
            overflow: hidden;
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
            transition: transform 0.3s, box-shadow 0.3s;
            display: flex;
            flex-direction: column;
        }}

        .item-card:hover {{
            transform: translateY(-5px);
            box-shadow: 0 10px 25px rgba(0,0,0,0.2);
        }}

        .item-image {{
            width: 100%;
            height: 280px;
            object-fit: cover;
            background: linear-gradient(135deg, #f5f5f5 0%, #e0e0e0 100%);
        }}

        .item-image-placeholder {{
            width: 100%;
            height: 280px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            font-size: 4em;
        }}

        .item-content {{
            padding: 15px;
            flex: 1;
            display: flex;
            flex-direction: column;
        }}

        .item-title {{
            font-size: 1.1em;
            font-weight: 600;
            color: #333;
            margin-bottom: 12px;
            line-height: 1.4;
        }}

        .item-info {{
            display: flex;
            flex-direction: column;
            gap: 8px;
            margin-bottom: 15px;
        }}

        .item-info div {{
            display: flex;
            align-items: center;
            gap: 8px;
            font-size: 0.9em;
            color: #666;
        }}

        .price {{
            font-weight: 700;
            color: #2ecc71;
            font-size: 1.2em;
        }}

        .source {{
            background: #667eea;
            color: white;
            padding: 4px 10px;
            border-radius: 15px;
            font-size: 0.8em;
            display: inline-block;
        }}

        .date {{
            color: #999;
            font-size: 0.85em;
        }}

        .view-btn {{
            display: inline-block;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 12px 24px;
            text-decoration: none;
            border-radius: 8px;
            font-weight: 600;
            transition: opacity 0.3s;
        }}

        .view-btn:hover {{
            opacity: 0.9;
        }}

        .no-results {{
            text-align: center;
            padding: 60px 20px;
            background: white;
            border-radius: 12px;
            color: #999;
        }}

        .footer {{
            text-align: center;
            color: white;
            margin-top: 40px;
            padding: 20px;
            font-size: 0.9em;
        }}

        @media (max-width: 768px) {{
            .items-grid {{
                grid-template-columns: 1fr;
            }}

            h1 {{
                font-size: 1.8em;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>🧥 Vintage Coat Finder</h1>
            <p style="color: #666; margin-top: 10px;">Your personal vintage coat catalog</p>
            <div class="stats">
                <div class="stat"><strong>{len(items)}</strong> Total Items</div>
"""

    # Add source counts
    for source, count in sorted(source_counts.items(), key=lambda x: x[1], reverse=True):
        html += f'                <div class="stat"><strong>{count}</strong> {source}</div>\n'

    html += f"""                <div class="stat">Updated: <strong>{datetime.now().strftime('%Y-%m-%d %H:%M UTC')}</strong></div>
            </div>
        </header>

        <div class="controls">
            <div class="search-box">
                <input type="text" id="searchInput" placeholder="🔍 Search by title..." onkeyup="filterItems()">
            </div>
            <select id="sourceFilter" onchange="filterItems()">
                <option value="all">All Sources</option>
"""

    # Add source filter options
    for source in sorted(source_counts.keys()):
        html += f'                <option value="{source}">{source}</option>\n'

    html += """            </select>
            <select id="sortOrder" onchange="sortItems()">
                <option value="newest">Newest First</option>
                <option value="oldest">Oldest First</option>
                <option value="price-low">Price: Low to High</option>
                <option value="price-high">Price: High to Low</option>
            </select>
        </div>

        <div class="items-grid" id="itemsContainer">
"""

    # Add items
    for item in items:
        item_id, title, url, price, source, found_date, image_url = item

        # Parse date
        try:
            date_obj = datetime.fromisoformat(found_date)
            date_str = date_obj.strftime('%b %d, %Y')
        except:
            date_str = found_date[:10] if found_date else 'Unknown'

        # Escape HTML
        title_escaped = title.replace('"', '&quot;').replace('<', '&lt;').replace('>', '&gt;')
        url_escaped = url.replace('"', '&quot;')
        image_url_escaped = image_url.replace('"', '&quot;') if image_url else ''

        # Generate image HTML
        if image_url:
            image_html = f'<img src="{image_url_escaped}" alt="{title_escaped}" class="item-image" loading="lazy">'
        else:
            image_html = '<div class="item-image-placeholder">🧥</div>'

        html += f"""            <div class="item-card" data-source="{source}" data-price="{price}" data-date="{found_date}" data-title="{title.lower()}">
                {image_html}
                <div class="item-content">
                    <div class="item-title">{title_escaped}</div>
                    <div class="item-info">
                        <div>
                            <span class="price">{price}</span>
                        </div>
                        <div>
                            <span class="source">{source}</span>
                        </div>
                        <div class="date">Found: {date_str}</div>
                    </div>
                    <a href="{url_escaped}" target="_blank" class="view-btn">View Item →</a>
                </div>
            </div>
"""

    html += """        </div>

        <div class="no-results" id="noResults" style="display: none;">
            <h2>No items found</h2>
            <p>Try adjusting your search or filters</p>
        </div>

        <div class="footer">
            <p>🤖 Automatically updated daily at 9 AM UTC</p>
            <p style="margin-top: 10px; font-size: 0.85em; opacity: 0.8;">
                Built with Claude Code • <a href="https://github.com/martinezsebastian/vintagecoats" style="color: white;">View Source</a>
            </p>
        </div>
    </div>

    <script>
        function filterItems() {
            const searchTerm = document.getElementById('searchInput').value.toLowerCase();
            const sourceFilter = document.getElementById('sourceFilter').value;
            const items = document.querySelectorAll('.item-card');
            let visibleCount = 0;

            items.forEach(item => {
                const title = item.getAttribute('data-title');
                const source = item.getAttribute('data-source');

                const matchesSearch = title.includes(searchTerm);
                const matchesSource = sourceFilter === 'all' || source === sourceFilter;

                if (matchesSearch && matchesSource) {
                    item.style.display = 'block';
                    visibleCount++;
                } else {
                    item.style.display = 'none';
                }
            });

            document.getElementById('noResults').style.display = visibleCount === 0 ? 'block' : 'none';
        }

        function sortItems() {
            const container = document.getElementById('itemsContainer');
            const items = Array.from(container.querySelectorAll('.item-card'));
            const sortOrder = document.getElementById('sortOrder').value;

            items.sort((a, b) => {
                if (sortOrder === 'newest') {
                    return b.getAttribute('data-date').localeCompare(a.getAttribute('data-date'));
                } else if (sortOrder === 'oldest') {
                    return a.getAttribute('data-date').localeCompare(b.getAttribute('data-date'));
                } else if (sortOrder === 'price-low' || sortOrder === 'price-high') {
                    const priceA = parseFloat(a.getAttribute('data-price').replace(/[^0-9.]/g, '')) || 0;
                    const priceB = parseFloat(b.getAttribute('data-price').replace(/[^0-9.]/g, '')) || 0;
                    return sortOrder === 'price-low' ? priceA - priceB : priceB - priceA;
                }
            });

            items.forEach(item => container.appendChild(item));
        }
    </script>
</body>
</html>
"""

    # Write to file
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html)

    print(f"✓ Generated website with {len(items)} items")
    print(f"  Sources: {', '.join(f'{k} ({v})' for k, v in source_counts.items())}")


if __name__ == '__main__':
    generate_website()
