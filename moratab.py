
from __future__ import unicode_literals
import re, mistune

ltr = re.compile(r'[ <>*+\t\n\\\/\[\]\(\)0-9\._-]*[A-Za-z]')
refine = lambda html: refine(html[html.find('>')+1:]) if html.startswith('<') else html
direction = lambda html: ' dir="ltr"' if ltr.match(refine(html)) else ''


class Moratab(mistune.Renderer):
	def header(self, text, level, raw=None):
		return '<h%d%s>%s</h%d>\n' % (level, direction(text), text, level)

	def paragraph(self, text):
		return '<p%s>%s</p>\n' % (direction(text), text)

	def list_item(self, text):
		return '<li%s><p>%s</p></li>\n' % (direction(text), text)

	def block_quote(self, text):
		return '<blockquote%s>%s\n</blockquote>' % (direction(text), text)

	def table_cell(self, content, **flags):
		tag = 'th' if flags['header'] else 'td'
		align = flags['align']
		if not align:
			return '<%s>%s</%s>\n' % (tag, content, tag)
		return '<%s align="%s">%s</%s>\n' % (tag, align, content, tag)

	def footnote_item(self, key, text):
		return '<li%s id="fn-%s">%s</li>\n' % (direction(text), mistune.escape(key), text)


markdown = mistune.Markdown(renderer=Moratab(), hard_wrap=True)


def replace_expressions(text):
	expressions = {}

	def expkey(match):
		key = 'x1x1x%dx' % (len(expressions)-1)
		expressions[key] = match.group(1)
		return key

	return re.sub(r'(\$\$?[^\$\n]+\$?\$)', expkey, text), expressions


def append_simple_footnotes(text):
	for footnote in re.finditer(r'\[\^([^\]]+)\]', text):
		ref = footnote.group(1)

		if not '[^{0}]:'.format(ref) in text:
			text += '\n[^{0}]: {0}'.format(ref)

	return text


def render(text):

	text = append_simple_footnotes(text)

	# remove expressions
	text, expressions = replace_expressions(text)

	# render text without expressions
	rendered = markdown.render(text)

	# add expressions
	for key, value in expressions.items():
		rendered = rendered.replace(key, value)

	return rendered
