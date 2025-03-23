from app.consts import CSS_DIR, CSS_BUNDLE_FILE, CSS_STYLES_FILE


def bundle_css():
  print("Starting to bundle CSS...")
  CSS_BUNDLE_FILE.parent.mkdir(parents=True, exist_ok=True)

  css_files = [f for f in CSS_DIR.glob('**/*.css') if f != CSS_BUNDLE_FILE]
  print(f"Found {len(css_files)} CSS files to bundle.")

  def sort_key(path):
    if 'reset.css' in str(path):
      return (0, str(path))
    if 'base' in str(path):
      return (1, str(path))
    if 'animations.css' in str(path):
      return (2, str(path))
    if 'header.css' in str(path):
      return (3, str(path))
    if 'components' in str(path):
      return (4, str(path))
    return (5, str(path))

  css_files.sort(key=sort_key)

  imports = []

  if CSS_STYLES_FILE.exists():
    with CSS_STYLES_FILE.open('r', encoding='utf-8') as file:
      content = file.read()
      import_lines = [line for line in content.split('\n') if '@import url(' in line]
      imports.extend(import_lines)


  with CSS_BUNDLE_FILE.open('w', encoding='utf-8') as bundle:
    bundle.write("/* Bundled CSS file - auto-generated */\n\n")
    if imports:
      bundle.write("/* Google Fonts */\n")
      for import_line in imports:
        bundle.write(import_line + "\n")
      bundle.write("\n")

    root_css = ""
    for css_file in css_files:
      with css_file.open('r', encoding='utf-8') as file:
        content = file.read()
        if ':root' in content:
          root_start = content.find(':root')
          root_end = content.find("}", root_start) + 1
          if root_start > -1:
            root_css = content[root_start:root_end]

    if root_css:
      bundle.write("/* CSS Variables */\n")
      bundle.write(root_css)
      bundle.write("\n\n")

    for css_file in css_files:
      if css_file.name == 'styles.css':
        # We've already handled styles.css
        continue

      rel_path = css_file.relative_to(CSS_DIR.parent)
      bundle.write(f"/* Source: {rel_path} */\n")
      with css_file.open('r', encoding='utf-8') as file:
        content = file.read()
        lines = content.split('\n')
        filtered_lines = []

        for line in lines:
          if '@import' in line:
            continue
          filtered_lines.append(line)

        if ":root" in content and root_css:
          root_start = content.find(":root")
          if root_start > -1:
            root_end = content.find("}", root_start) + 1
            content = content[:root_start] + content[root_end:]

        filtered_content = '\n'.join(filtered_lines)
        bundle.write(filtered_content)

      bundle.write("\n\n")
      print(f"Added {rel_path} to bundle.")

  print(f"CSS bundling completed. Bundled file saved to {CSS_BUNDLE_FILE}")


if __name__ == '__main__':
  bundle_css()
