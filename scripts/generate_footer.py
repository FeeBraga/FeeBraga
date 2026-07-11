#!/usr/bin/env python3
"""
Generate custom footer SVG for GitHub Profile
Minimalist design matching header
"""

import os
from datetime import datetime

def generate_footer_svg():
    """Generate minimalist footer SVG"""
    
    current_year = datetime.now().year
    
    svg_content = f'''<svg width="800" height="60" viewBox="0 0 800 60" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="footerGradient" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" style="stop-color:#0D1117"/>
      <stop offset="100%" style="stop-color:#161B22"/>
    </linearGradient>
  </defs>
  
  <!-- Background -->
  <rect width="800" height="60" fill="url(#footerGradient)"/>
  
  <!-- Divider line -->
  <line x1="0" y1="0" x2="800" y2="0" stroke="#30363D" stroke-width="1"/>
  
  <!-- Text -->
  <text x="400" y="35" text-anchor="middle" fill="#484F58" font-family="system-ui, -apple-system, sans-serif" font-size="11">© {current_year} Felipe Braga</text>
  
  <!-- Corner accents -->
  <rect x="0" y="58" width="60" height="2" fill="#58A6FF" opacity="0.2"/>
  <rect x="0" y="0" width="2" height="60" fill="#58A6FF" opacity="0.2"/>
  <rect x="740" y="58" width="60" height="2" fill="#58A6FF" opacity="0.2"/>
  <rect x="798" y="0" width="2" height="60" fill="#58A6FF" opacity="0.2"/>
</svg>'''
    
    # Ensure profile directory exists
    os.makedirs('profile', exist_ok=True)
    
    # Write SVG to file
    with open('profile/footer.svg', 'w') as f:
        f.write(svg_content)
    
    print("✓ Generated footer.svg")

if __name__ == "__main__":
    generate_footer_svg()
