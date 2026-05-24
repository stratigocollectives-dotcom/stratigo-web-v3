import os
import re

def extract_styles(html_path):
    with open(html_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Extract font styles
    font_css_match = re.search(r'<style data-framer-font-css>(.*?)</style>', content, re.DOTALL)
    font_css = font_css_match.group(1) if font_css_match else ''

    # Extract other styles
    other_css = ''
    breakpoint_css = re.search(r'<style data-framer-breakpoint-css>(.*?)</style>', content, re.DOTALL)
    if breakpoint_css:
        other_css += breakpoint_css.group(1) + '\n'
        
    ssr_css = re.search(r'<style data-framer-css-ssr-minified.*?>(.*?)</style>', content, re.DOTALL)
    if ssr_css:
        other_css += ssr_css.group(1) + '\n'

    return font_css, other_css

def extract_body_inner_html(html_path):
    with open(html_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    body_match = re.search(r'<body.*?>(.*?)</body>', content, re.DOTALL)
    if body_match:
        return body_match.group(1)
    return ''

def create_nextjs_page(route, body_html):
    page_dir = os.path.join('app', route) if route else 'app'
    os.makedirs(page_dir, exist_ok=True)
    
    page_path = os.path.join(page_dir, 'page.tsx')
    
    # Escape backticks and ${} to avoid template literal issues in JSX
    safe_body = body_html.replace('`', '\\`').replace('${', '\\${')
    
    tsx_content = f"""
export default function Page() {{
  return (
    <div suppressHydrationWarning dangerouslySetInnerHTML={{{{ __html: `{safe_body}` }}}} />
  );
}}
"""
    with open(page_path, 'w', encoding='utf-8') as f:
        f.write(tsx_content.strip())
    print(f"Created {page_path}")

def main():
    # 1. Extract and write global styles
    font_css, other_css = extract_styles('assets/index.html')
    
    with open('app/framer-fonts.css', 'w', encoding='utf-8') as f:
        f.write(font_css)
    print("Created app/framer-fonts.css")
        
    with open('app/framer-styles.css', 'w', encoding='utf-8') as f:
        f.write(other_css)
    print("Created app/framer-styles.css")
    
    # 2. Process all pages
    pages = [
        ('', 'assets/index.html'),
        ('about', 'assets/about/index.html'),
        ('contact', 'assets/contact/index.html'),
        ('privacy', 'assets/privacy/index.html'),
        ('terms', 'assets/terms/index.html')
    ]
    
    for route, path in pages:
        if os.path.exists(path):
            body_html = extract_body_inner_html(path)
            create_nextjs_page(route, body_html)
        else:
            print(f"Warning: {path} not found.")

if __name__ == "__main__":
    main()
