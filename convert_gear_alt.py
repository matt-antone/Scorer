#!/usr/bin/env python3

from svglib.svglib import svg2rlg
from reportlab.graphics import renderPM
import os

def convert_svg_to_png():
    svg_path = 'pi_client/assets/gear-solid.svg'
    png_path = 'pi_client/assets/gear.png'
    
    # Load SVG and convert to ReportLab drawing
    drawing = svg2rlg(svg_path)
    # Save as PNG (48x48)
    renderPM.drawToFile(drawing, png_path, fmt='PNG')
    print(f"Converted {svg_path} to {png_path}")

if __name__ == '__main__':
    convert_svg_to_png() 