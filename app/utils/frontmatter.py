from dataclasses import dataclass
from datetime import datetime
from typing import Any, Dict


class FrontmatterException(Exception):
  """Base exception for frontmatter parsing errors."""


class InvalidDateFormatError(FrontmatterException):
  """Raised when a file is missing required frontmatter delimiters."""


class MissingFrontmatterError(FrontmatterException):
  """Raised when a file is missing required frontmatter delimiters."""


@dataclass
class ParsedMarkdown:
  """Represents a parsed markdown file with metadata and content."""
  metadata: Dict[str, Any]
  content: str


def frontmatter(content: str) -> ParsedMarkdown:
  """
  Parse a string containing frontmatter and markdown content.
  
  Format expected:
  ---
  key: value
  date: 2024-12-28
  ---
  Content ...

  Raises:
    MissingFrontmatterError: If the required frontmatter delimiters are missing
  """
  parts = content.split('---', 2)
  if len(parts) < 3:
      raise MissingFrontmatterError("File must contain frontmatter between '---' delimiters")

  metadata = {}
  for line in parts[1].strip().split('\n'):
    if ':' in line:
      key, value = line.split(':', 1)
      key = key.strip()
      value = value.strip()

      if key == 'date':
        try:
          value = datetime.strptime(value, '%Y-%m-%d')
        except ValueError as ex:
          raise InvalidDateFormatError(f'Invalid date format: {value}. Expected YYYY-MM-DD') from ex
      elif key == 'tags':
        value = [tag.strip() for tag in value.split(',') if tag.strip()]
      elif value.lower() in ('true', 'false'):
        value = value == 'true'
      elif value.isdigit():
        value = int(value)

      metadata[key] = value

  return ParsedMarkdown(
    metadata=metadata,
    content=parts[2].strip()
  )
