import logging

from settings import MARKDOWN_PATH


logger = logging.getLogger(__name__)


def get_markdown_file(filename: str) -> str:
    """Read the contents from the markdown directory and return

    Args:
        filename (str): filename starting after MARKDOWN_PATH

    Returns:
        str: contents of markdown file
    """
    pathname = f'{MARKDOWN_PATH}{filename}.md'
    try:
        with open(pathname, 'r') as fh:
            content = fh.read()
        return content
    except FileNotFoundError as e:
        msg = f'FileNotFoundError: Could not find markdown file @ {pathname}'
        logger.warning(msg)
        return msg
