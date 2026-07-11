#!/usr/bin/env python3
"""
Generate GitHub Stats SVG using GitHub API
Fetches real-time stats and creates custom SVG
"""

import os
import requests
import json

def fetch_github_stats():
    """Fetch GitHub stats from API"""
    username = "felipebraga"
    token = os.environ.get('GITHUB_TOKEN')
    
    headers = {
        'Authorization': f'token {token}' if token else None,
        'Accept': 'application/vnd.github.v3+json'
    }
    
    # Remove None from headers
    headers = {k: v for k, v in headers.items() if v is not None}
    
    try:
        # Fetch user profile
        user_response = requests.get(f'https://api.github.com/users/{username}', headers=headers)
        user_data = user_response.json()
        
        # Fetch repositories for additional stats
        repos_response = requests.get(f'https://api.github.com/users/{username}/repos?per_page=100', headers=headers)
        repos_data = repos_response.json()
        
        stats = {
            'public_repos': user_data.get('public_repos', 0),
            'followers': user_data.get('followers', 0),
            'following': user_data.get('following', 0),
            'stars': sum(repo.get('stargazers_count', 0) for repo in repos_data if isinstance(repo, dict)),
            'forks': sum(repo.get('forks_count', 0) for repo in repos_data if isinstance(repo, dict))
        }
        
        return stats
    except Exception as e:
        print(f"Error fetching GitHub stats: {e}")
        # Return default values if API fails
        return {
            'public_repos': 0,
            'followers': 0,
            'following': 0,
            'stars': 0,
            'forks': 0
        }

def generate_stats_svg(stats):
    """Generate stats SVG with custom design"""
    
    svg_content = f'''<svg width="400" height="180" viewBox="0 0 400 180" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="statsBg" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:#161B22"/>
      <stop offset="100%" style="stop-color:#0D1117"/>
    </linearGradient>
  </defs>
  
  <!-- Background -->
  <rect width="400" height="180" fill="url(#statsBg)" rx="8"/>
  
  <!-- Title -->
  <text x="20" y="30" fill="#58A6FF" font-family="system-ui, sans-serif" font-size="14" font-weight="600">GitHub Stats</text>
  
  <!-- Stats Grid -->
  <g font-family="system-ui, sans-serif" font-size="12">
    <!-- Repos -->
    <text x="20" y="70" fill="#8B949E">Repositories</text>
    <text x="380" y="70" fill="#C9D1D9" text-anchor="end" font-weight="600">{stats['public_repos']}</text>
    
    <!-- Followers -->
    <text x="20" y="100" fill="#8B949E">Followers</text>
    <text x="380" y="100" fill="#C9D1D9" text-anchor="end" font-weight="600">{stats['followers']}</text>
    
    <!-- Following -->
    <text x="20" y="130" fill="#8B949E">Following</text>
    <text x="380" y="130" fill="#C9D1D9" text-anchor="end" font-weight="600">{stats['following']}</text>
    
    <!-- Stars -->
    <text x="20" y="160" fill="#8B949E">Stars</text>
    <text x="380" y="160" fill="#C9D1D9" text-anchor="end" font-weight="600">{stats['stars']}</text>
  </g>
  
  <!-- Border -->
  <rect width="400" height="180" fill="none" stroke="#30363D" stroke-width="1" rx="8"/>
</svg>'''
    
    # Ensure profile directory exists
    os.makedirs('profile', exist_ok=True)
    
    # Write SVG to file
    with open('profile/stats.svg', 'w') as f:
        f.write(svg_content)
    
    print("✓ Generated stats.svg")

if __name__ == "__main__":
    stats = fetch_github_stats()
    generate_stats_svg(stats)
