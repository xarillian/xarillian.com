from jinja2 import Environment, FileSystemLoader
from ssg.config import TEMPLATES_DIR

env = Environment(loader=FileSystemLoader(str(TEMPLATES_DIR)))

def render_template(template_name: str, **context) -> str:
    template = env.get_template(template_name)
    return template.render(**context)
