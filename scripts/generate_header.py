#!/usr/bin/env python3
"""
Generate custom header SVG for GitHub Profile
Inspired by Vercel, Microsoft, Linear design patterns
"""

import os

def generate_header_svg():
    """Generate minimalist header SVG with circuit patterns"""
    
    svg_content = '''<svg width="800" height="200" viewBox="0 0 800 200" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="bgGradient" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:#0D1117"/>
      <stop offset="100%" style="stop-color:#161B22"/>
    </linearGradient>
    <linearGradient id="lineGradient" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" style="stop-color:#58A6FF;stop-opacity:0"/>
      <stop offset="50%" style="stop-color:#58A6FF;stop-opacity:0.3"/>
      <stop offset="100%" style="stop-color:#58A6FF;stop-opacity:0"/>
    </linearGradient>
  </defs>
  
  <!-- Background -->
  <rect width="800" height="200" fill="url(#bgGradient)"/>
  
  <!-- Abstract circuit lines -->
  <g stroke="url(#lineGradient)" stroke-width="1" fill="none">
    <path d="M0 100 L200 100 L220 80 L300 80 L320 100 L500 100 L520 120 L600 120 L620 100 L800 100"/>
    <path d="M0 120 L150 120 L170 140 L250 140 L270 120 L450 120 L470 100 L550 100 L570 120 L800 120"/>
    <circle cx="220" cy="80" r="2" fill="#58A6FF" opacity="0.5"/>
    <circle cx="320" cy="100" r="2" fill="#58A6FF" opacity="0.5"/>
    <circle cx="520" cy="120" r="2" fill="#58A6FF" opacity="0.5"/>
    <circle cx="170" cy="140" r="2" fill="#58A6FF" opacity="0.5"/>
    <circle cx="270" cy="120" r="2" fill="#58A6FF" opacity="0.5"/>
    <circle cx="470" cy="100" r="2" fill="#58A6FF" opacity="0.5"/>
  </g>
  
  <!-- Text -->
  <text x="400" y="85" text-anchor="middle" fill="#C9D1D9" font-family="system-ui, -apple-system, sans-serif" font-size="32" font-weight="300">Felipe Braga</text>
  <text x="400" y="115" text-anchor="middle" fill="#58A6FF" font-family="system-ui, -apple-system, sans-serif" font-size="16" font-weight="400">Full Stack Developer</text>
  <text x="400" y="140" text-anchor="middle" fill="#8B949E" font-family="system-ui, -apple-system, sans-serif" font-size="12">Computer Engineering Student</text>
  <text x="400" y="165" text-anchor="middle" fill="#484F58" font-family="system-ui, -apple-system, sans-serif" font-size="11" font-style="italic">Building intelligent solutions with modern technologies</text>
  
  <!-- Corner accents -->
  <rect x="0" y="0" width="60" height="2" fill="#58A6FF" opacity="0.3"/>
  <rect x="0" y="0" width="2" height="60" fill="#58A6FF" opacity="0.3"/>
  <rect x="740" y="0" width="60" height="2" fill="#58A6FF" opacity="0.3"/>
  <rect x="798" y="0" width="2" height="60" fill="#58A6FF" opacity="0.3"/>
</svg>'''
    
    # Ensure profile directory exists
    os.makedirs('profile', exist_ok=True)
    
    # Write SVG to file
    with open('profile/header.svg', 'w') as f:
        f.write(svg_content)
    
    print("✓ Generated header.svg")

if __name__ == "__main__":
    generate_header_svg()
