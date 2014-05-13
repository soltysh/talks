#!/usr/bin/python

from __future__ import print_function

import os
import os.path
import subprocess
import sys

def main(args):
    """Build the presentation given as parameter."""
    markdown_name, presentation_name = parse_args(args)
    return subprocess.call(["pandoc", "-t", "revealjs", "-s", markdown_name,
        "-o", presentation_name, "-V", "theme=solarized", "-V"
        "revealjs-url=http://cdnjs.cloudflare.com/ajax/libs/reveal.js/2.6.2",
        "-H", "header.css"])

def parse_args(args):
    """Parse arguments, there should be exactly one argument - the name of the
    directory containing *.md file with the same name as dir or exact path to
    the markdown file."""
    if len(args) < 2:
        sys.exit("""{script_name} should be called with the name of the presentation directory or path to *.md file"""\
            .format(script_name=args[0]))
    markdown_name = args[1]
    if os.sep not in markdown_name:
        markdown_name = os.path.join(markdown_name, markdown_name + ".md")
    presentation_name = os.path.splitext(markdown_name)[0] + ".html"
    return markdown_name, presentation_name

if __name__ == "__main__":
    sys.exit(main(sys.argv))

