#!/usr/bin/env python3
"""
Generate Activity SVG showing recent GitHub activity
Minimalist design with contribution summary
"""

import os
import requests
from datetime import datetime, timedelta

def fetch_activity_stats():
    """Fetch recent activity from GitHub API"""
    username = "felipebraga"
    token = os.environ.get('GITHUB_TOKEN')
    
    headers = {
        'Authorization': f'token {token}' if token else None,
        'Accept': 'application/vnd.github.v3+json'
    }
    
    # Remove None from headers
    headers = {k: v for k, v in headers.items() if v is not None}
    
    try:
        # Fetch user events
        events_response = requests.get(f'https://api.github.com/users/{username}/events/public?per_page=30', headers=headers)
        events_data = events_response.json()
        
        # Count activity types in last 30 days
        thirty_days_ago = datetime.now() - timedelta(days=30)
        
        activity = {
            'commits': 0,
            'pull_requests': 0,
            'issues': 0,
            'reviews': 0
        }
        
        for event in events_data:
            if isinstance(event, dict):
                event_date = datetime.strptime(event['created_at'], '%Y-%m-%dT%H:%M:%SZ')
                if event_date > thirty_days_ago:
                    event_type = event.get('type', '')
                    if 'PushEvent' in event_type:
                        activity['commits'] += 1
                    elif 'PullRequest' in event_type:
                        activity['pull_requests'] += 1
                    elif 'Issues' in event_type:
                        activity['issues'] += 1
                    elif 'PullRequestReview' in event_type:
                        activity['reviews'] += 1
        
        return activity
    except Exception as e:
        print(f"Error fetching activity stats: {e}")
        # Return default values if API fails
        return {
            'commits': 0,
            'pull_requests': 0,
            'issues': 0,
            'reviews': 0
        }

def generate_activity_svg(activity):
    """Generate activity SVG with custom design"""
    
    svg_content = f'''<svg width="400" height="160" viewBox="0 0 400 160" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="activityBg" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:#161B22"/>
      <stop offset="100%" style="stop-color:#0D1117"/>
    </linearGradient>
  </defs>
  
  <!-- Background -->
  <rect width="400" height="160" fill="url(#activityBg)" rx="8"/>
  
  <!-- Title -->
  <text x="20" y="30" fill="#58A6FF" font-family="system-ui, sans-serif" font-size="14" font-weight="600">Activity (30 days)</text>
  
  <!-- Activity Grid -->
  <g font-family="system-ui, sans-serif" font-size="12">
    <!-- Commits -->
    <text x="20" y="70" fill="#8B949E">Commits</text>
    <text x="380" y="70" fill="#C9D1D9" text-anchor="end" font-weight="600">{activity['commits']}</text>
    
    <!-- Pull Requests -->
    <text x="20" y="100" fill="#8B949E">Pull Requests</text>
    <text x="380" y="100" fill="#C9D1D9" text-anchor="end" font-weight="600">{activity['pull_requests']}</text>
    
    <!-- Issues -->
    <text x="20" y="130" fill="#8B949E">Issues</text>
    <text x="380" y="130" fill="#C9D1D9" text-anchor="end" font-weight="600">{activity['issues']}</text>
  </g>
  
  <!-- Border -->
  <rect width="400" height="160" fill="none" stroke="#30363D" stroke-width="1" rx="8"/>
</svg>'''
    
    # Ensure profile directory exists
    os.makedirs('profile', exist_ok=True)
    
    # Write SVG to file
    with open('profile/activity.svg', 'w') as f:
        f.write(svg_content)
    
    print("✓ Generated activity.svg")

if __name__ == "__main__":
    activity = fetch_activity_stats()
    generate_activity_svg(activity)
