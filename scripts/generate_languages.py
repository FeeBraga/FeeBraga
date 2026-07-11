#!/usr/bin/env python3
"""
Generate Top Languages SVG using GitHub API
Fetches language statistics and creates custom SVG
"""

import os
import requests
from collections import Counter

def fetch_language_stats():
    """Fetch language statistics from GitHub API"""
    username = "FeeBraga"
    token = os.environ.get('GITHUB_TOKEN')
    
    headers = {
        'Authorization': f'token {token}' if token else None,
        'Accept': 'application/vnd.github.v3+json'
    }
    
    # Remove None from headers
    headers = {k: v for k, v in headers.items() if v is not None}
    
    try:
        # Fetch user repositories
        repos_response = requests.get(f'https://api.github.com/users/{username}/repos?per_page=100', headers=headers)
        repos_data = repos_response.json()
        
        # Count languages
        language_counter = Counter()
        
        for repo in repos_data:
            if isinstance(repo, dict) and repo.get('language'):
                language_counter[repo['language']] += 1
        
        # Get top 5 languages
        top_languages = language_counter.most_common(5)
        
        return top_languages
    except Exception as e:
        print(f"Error fetching language stats: {e}")
        # Return default values if API fails
        return [('Python', 1), ('TypeScript', 1), ('C#', 1), ('JavaScript', 1), ('Other', 1)]

def generate_languages_svg(languages):
    """Generate languages SVG with custom design"""
    
    # Calculate total for percentages
    total = sum(count for _, count in languages)
    
    # Generate language bars
    bars_html = ""
    y_position = 70
    
    for lang, count in languages:
        percentage = (count / total) * 100
        bar_width = (percentage / 100) * 200
        
        bars_html += f'''
    <text x="20" y="{y_position}" fill="#8B949E" font-family="system-ui, sans-serif" font-size="11">{lang}</text>
    <rect x="120" y="{y_position - 8}" width="{bar_width}" height="12" fill="#58A6FF" rx="2" opacity="0.8"/>
    <text x="380" y="{y_position}" fill="#C9D1D9" font-family="system-ui, sans-serif" font-size="11" text-anchor="end">{percentage:.1f}%</text>
'''
        y_position += 25
    
    svg_content = f'''<svg width="400" height="200" viewBox="0 0 400 200" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="langBg" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:#161B22"/>
      <stop offset="100%" style="stop-color:#0D1117"/>
    </linearGradient>
  </defs>
  
  <!-- Background -->
  <rect width="400" height="200" fill="url(#langBg)" rx="8"/>
  
  <!-- Title -->
  <text x="20" y="30" fill="#58A6FF" font-family="system-ui, sans-serif" font-size="14" font-weight="600">Top Languages</text>
  
  <!-- Language Bars -->
{bars_html}
  
  <!-- Border -->
  <rect width="400" height="200" fill="none" stroke="#30363D" stroke-width="1" rx="8"/>
</svg>'''
    
    # Ensure profile directory exists
    os.makedirs('profile', exist_ok=True)
    
    # Write SVG to file
    with open('profile/languages.svg', 'w') as f:
        f.write(svg_content)
    
    print("✓ Generated languages.svg")

if __name__ == "__main__":
    languages = fetch_language_stats()
    generate_languages_svg(languages)
