from ssg.config import CSS_BUNDLE_FILE, CSS_DIR, CSS_STYLES_FILE


def collect_css_files():
  files = [f for f in CSS_DIR.glob("**/*.css") if f != CSS_BUNDLE_FILE]

  def sort_key(path):
    name = str(path)
    priorities = {
      "reset.css": 0,
      "base": 1,
      "animations.css": 2,
      "header.css": 3,
      "components": 4,
      "utilities.css": 1000,
    }

    for key, priority in priorities.items():
      if key in name:
        return (priority, name)
    return (5, name)

  return sorted(files, key=sort_key)


def extract_imports(path):
  if not path.exists():
    return []

  with path.open(encoding="utf-8") as f:
    return [line for line in f if "@import url(" in line]


def extract_root_css(files):
  for file in files:
    content = file.read_text(encoding="utf-8")
    if ":root" in content:
      start = content.find(":root")
      end = content.find("}", start) + 1
      return content[start:end]
  return ""


def write_css_bundle(files, imports, root_css):
  def remove_root_block(content):
    if ":root" not in content:
      return content
    start = content.find(":root")
    end = content.find("}", start) + 1
    return content[:start] + content[end:]

  with CSS_BUNDLE_FILE.open("w", encoding="utf-8") as bundle:
    bundle.write("/* Bundled CSS file - auto-generated */\n\n")

    if imports:
      bundle.write("/* Google Fonts */\n")
      bundle.writelines(line.strip() + "\n" for line in imports)
      bundle.write("\n")

    if root_css:
      bundle.write("/* CSS Variables */\n")
      bundle.write(root_css + "\n\n")

    for css_file in files:
      if css_file.name == "styles.css":
        continue

      rel_path = css_file.relative_to(CSS_DIR.parent)
      bundle.write(f"/* Source: {rel_path} */\n")

      content = css_file.read_text(encoding="utf-8")
      content = remove_root_block(content)
      lines = [line for line in content.splitlines() if "@import" not in line]
      bundle.write("\n".join(lines) + "\n\n")
      print(f"Added {rel_path} to bundle.")


def bundle_css():
    print("Starting to bundle CSS...")
    CSS_BUNDLE_FILE.parent.mkdir(parents=True, exist_ok=True)

    css_files = collect_css_files()
    print(f"Found {len(css_files)} CSS files to bundle.")

    imports = extract_imports(CSS_STYLES_FILE)
    root_css = extract_root_css(css_files)

    write_css_bundle(css_files, imports, root_css)

    print(f"CSS bundling completed. Bundled file saved to {CSS_BUNDLE_FILE}")
