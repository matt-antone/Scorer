#!/usr/bin/env python3

import cairosvg
import os

def convert_svg_to_png():
    # Input and output paths
    svg_path = 'pi_client/assets/gear-solid.svg'
    png_path = 'pi_client/assets/gear.png'
    
    # Ensure output directory exists
    os.makedirs(os.path.dirname(png_path), exist_ok=True)
    
    # Convert SVG to PNG
    # Using 48x48 size for good quality
    cairosvg.svg2png(url=svg_path, write_to=png_path, output_width=48, output_height=48)
    
    print(f"Converted {svg_path} to {png_path}")

if __name__ == '__main__':
    convert_svg_to_png() 