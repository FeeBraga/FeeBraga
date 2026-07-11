#!/usr/bin/env python3
"""
Generate custom footer SVG for GitHub Profile
Minimalist design matching header
"""

import os
from datetime import datetime

def generate_footer_svg():
    """Generate minimalist footer SVG with transparent background"""
    
    svg_content = '''<svg width="900" height="70" viewBox="0 0 900 70" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <!-- Gradient for horizontal line: gray -> blue -> gray -->
    <linearGradient id="lineGradient" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" style="stop-color:#30363D"/>
      <stop offset="20%" style="stop-color:#30363D"/>
      <stop offset="50%" style="stop-color:#58A6FF"/>
      <stop offset="80%" style="stop-color:#30363D"/>
      <stop offset="100%" style="stop-color:#30363D"/>
    </linearGradient>
  </defs>
  
  <!-- Horizontal line - 80% of width, centered -->
  <line x1="90" y1="15" x2="810" y2="15" stroke="url(#lineGradient)" stroke-width="1" stroke-linecap="round"/>
  
  <!-- Left technical detail - subtle circuit pattern -->
  <g stroke="#58A6FF" stroke-width="0.5" fill="none" opacity="0.3">
    <path d="M20 35 L50 35 L55 30 L70 30 L75 35"/>
    <circle cx="55" cy="30" r="1.5" fill="#58A6FF" opacity="0.5"/>
    <circle cx="75" cy="35" r="1" fill="#58A6FF" opacity="0.4"/>
  </g>
  
  <!-- Right technical detail - subtle circuit pattern -->
  <g stroke="#58A6FF" stroke-width="0.5" fill="none" opacity="0.3">
    <path d="M880 35 L850 35 L845 30 L830 30 L825 35"/>
    <circle cx="845" cy="30" r="1.5" fill="#58A6FF" opacity="0.5"/>
    <circle cx="825" cy="35" r="1" fill="#58A6FF" opacity="0.4"/>
  </g>
  
  <!-- Centered text -->
  <g font-family="system-ui, -apple-system, sans-serif" text-anchor="middle">
    
    <!-- Name -->
    <text x="450" y="40" fill="#C9D1D9" font-size="16" font-weight="600">Felipe Braga</text>
    
    <!-- Tagline -->
    <text x="450" y="58" fill="#8B949E" font-size="11">Building intelligent solutions with modern technologies.</text>
  </g>
</svg>'''
    
    # Ensure profile directory exists
    os.makedirs('profile', exist_ok=True)
    
    # Write SVG to file
    with open('profile/footer.svg', 'w') as f:
        f.write(svg_content)
    
    print("✓ Generated footer.svg")

if __name__ == "__main__":
    generate_footer_svg()
