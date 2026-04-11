#!/usr/bin/env python3
"""Fix mobile full-width issue by adding html, body overflow-x: hidden"""

import os
import re

PROJECT_DIR = "/Users/globalaffiliate/westchester-county-repair"

OLD_PATTERN = r'''( <style>
 :root \{
 --blue: #003087;
 --red: #e41e26;
 --gray: #f8f9fa;
 \}
 body \{
 font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;)
 margin: 0;
( color: #333;
 background: #fff;
 line-height: 1\.6;
 box-sizing: border-box;
 overscroll-behavior: none;
 \})'''

NEW_TEXT = ''' <style>
 :root {
 --blue: #003087;
 --red: #e41e26;
 --gray: #f8f9fa;
 }
 html, body {
 margin: 0;
 padding: 0;
 width: 100%;
 overflow-x: hidden;
 }
 body {
 font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
 color: #333;
 background: #fff;
 line-height: 1.6;
 box-sizing: border-box;
 overscroll-behavior: none;
 }'''

# Multiple patterns to handle different file variants
PATTERNS = [
    # Pattern 1: with leading space before <style>
    (''' <style>
 :root {
 --blue: #003087;
 --red: #e41e26;
 --gray: #f8f9fa;
 }
 body {
 font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
 margin: 0;
 color: #333;
 background: #fff;
 line-height: 1.6;
 box-sizing: border-box;
 overscroll-behavior: none;
 }''', ''' <style>
 :root {
 --blue: #003087;
 --red: #e41e26;
 --gray: #f8f9fa;
 }
 html, body {
 margin: 0;
 padding: 0;
 width: 100%;
 overflow-x: hidden;
 }
 body {
 font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
 color: #333;
 background: #fff;
 line-height: 1.6;
 box-sizing: border-box;
 overscroll-behavior: none;
 }'''),
    # Pattern 2: without leading space before <style>
    ('''<style>
 :root {
 --blue: #003087;
 --red: #e41e26;
 --gray: #f8f9fa;
 }
 body {
 font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
 margin: 0;
 color: #333;
 background: #fff;
 line-height: 1.6;
 box-sizing: border-box;
 overscroll-behavior: none;
 }''', '''<style>
 :root {
 --blue: #003087;
 --red: #e41e26;
 --gray: #f8f9fa;
 }
 html, body {
 margin: 0;
 padding: 0;
 width: 100%;
 overflow-x: hidden;
 }
 body {
 font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
 color: #333;
 background: #fff;
 line-height: 1.6;
 box-sizing: border-box;
 overscroll-behavior: none;
 }'''),
]

def fix_file(filepath):
    """Fix a single HTML file"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        # Check if already fixed
        if 'html, body {' in content and 'overflow-x: hidden;' in content:
            return 'SKIPPED (already fixed)'

        # Try each pattern
        new_content = content
        for old_str, new_str in PATTERNS:
            if old_str in new_content:
                new_content = new_content.replace(old_str, new_str)
                break

        if new_content == content:
            return 'SKIPPED (pattern not found)'

        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)

        return 'FIXED'
    except Exception as e:
        return f'ERROR: {e}'

def main():
    fixed = 0
    skipped = 0
    errors = 0

    for root, dirs, files in os.walk(PROJECT_DIR):
        # Skip hidden directories and node_modules
        dirs[:] = [d for d in dirs if not d.startswith('.')]

        for file in files:
            if file.endswith('.html'):
                filepath = os.path.join(root, file)
                result = fix_file(filepath)

                if result == 'FIXED':
                    fixed += 1
                    print(f"FIXED: {filepath}")
                elif 'ERROR' in result:
                    errors += 1
                    print(f"ERROR: {filepath} - {result}")
                else:
                    skipped += 1

    print(f"\n=== SUMMARY ===")
    print(f"Fixed: {fixed}")
    print(f"Skipped: {skipped}")
    print(f"Errors: {errors}")

if __name__ == "__main__":
    main()
