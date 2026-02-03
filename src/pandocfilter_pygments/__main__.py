#!/usr/bin/env python
"""
Pandoc filter to pass all code blocks through pygments highlighter.
"""
__app_name__ = "pandocfilter-pygments"

from pandocfilters import toJSONFilter, RawBlock
from pygments import highlight
from pygments.lexers import get_lexer_by_name, guess_lexer, TextLexer
from pygments.formatters import get_formatter_by_name

def pygmentize(key, value, format, meta):
    if key == 'CodeBlock':
        [[ident, classes, keyvals], code] = value

        lexer = None
        klass = 'shell'
        for klass in classes:
            if klass == "commonlisp":
                klass = "lisp"
            try:
                lexer = get_lexer_by_name(klass)
                break
            except:
                pass

        if lexer is None:
            try:
                lexer = guess_lexer(code)
            except:
                lexer = TextLexer()

        if format == "html5":
            format = "html"

        if format == "html":
            formatter = get_formatter_by_name(format) \
                            .__class__(cssclass="highlight " + klass)
        else:
            formatter = get_formatter_by_name(format)

        return RawBlock(format, highlight(code, lexer, formatter))


def cli():
    toJSONFilter(pygmentize)
