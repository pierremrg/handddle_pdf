import re
from flask_weasyprint import HTML, CSS, render_pdf

class TemplateManager:

	def __init__(self, root_directory, html_filepath):
		self.root_directory = root_directory
		self.html = TemplateManager._read_file(self.root_directory + '/' + html_filepath)
		self.css_list = []
		self.fill_fields_called = False

	@staticmethod
	def _read_file(filepath):
		with open(filepath, 'r') as f:
			return f.read()

	@staticmethod
	def _get_fields_in_html(html):
		return re.findall('\{\{([A-Za-z0-9_.]+)\}\}', html)

	@staticmethod
	def _fill_fields_in_html(html, data):
		fields = TemplateManager._get_fields_in_html(html)

		for field in fields:
			if field in data:
				html = html.replace('{{' + field + '}}', str(data[field]))
			else:
				html = html.replace('{{' + field + '}}', '-')

		return html


	def fill_template_fields(self, data):
		self.fill_fields_called = True
		self.html = TemplateManager._fill_fields_in_html(self.html, data)

	def fill_template_repeated_parts(self, part_name, data):
		if self.fill_fields_called:
			raise Exception('fill_template_repeated_parts() must be called before fill_template_fields().')

		filled_part_content = ''

		pattern = r'\{\{repeated_part\[' + part_name + '\]\[([^[]+)\]\}\}'
		part_html = re.findall(pattern, self.html, flags=re.DOTALL)[0]

		for d in data:
			filled_part_content += TemplateManager._fill_fields_in_html(part_html, d)

		self.html = re.sub(pattern, filled_part_content, self.html, flags=re.DOTALL)


	def add_css(self, css_filepath):
		self.css_list.append(
			CSS(string=TemplateManager._read_file(self.root_directory + '/' + css_filepath))
		)

	def generate_pdf(self):
		pdf_html = HTML(string=self.html, base_url='')
		return render_pdf(pdf_html, stylesheets=self.css_list)