from thot.plugins import ThotPlugin
from thot.plugins.project.core import Project
import os

class ThotProject(ThotPlugin):
	
	def name(self):
		return 'ThotProject'
	
	def description(self):
		return 'This is a project parser.'
	
	def on_before_parse_args(self, optparser):
		optparser.add_option('-n', '--project-name', action="store", type="string",
			help="Sets the name of the project. Default project's name is the project main folder's name.", dest="project_name")
		optparser.add_option('-p', '--project-path', action="store", default=os.getcwd(),  type="string",
			help="Sets the path for the project.", dest="project_path")
		optparser.add_option('-o', '--output', action="store", default=os.getcwd(), type="string",
			help="Sets the output path for the project.", dest="output")
		optparser.add_option('-f', '--format', action="append", choices=('html', 'pdf'),
			help="Sets the output format", dest="format")
	
	def on_after_parse_args(self, optparser, options):
		opt = OptionsValidator(options)
		if opt.is_valid():
			return True
		else:
			optparser.error(opt.get_error())
	
	def run(self, options):
		project = Project(options.project_path)
		project.parse(options.format, options.output)

class OptionsValidator(object):

	_options = None
	_error = None
	
	def __init__(self, options):
		self._options = options
	
	def is_valid(self):
		try:
			self.validate_project_path()
			self.validate_output()
			return True
		except ValueError as e:
			self._error = str(e)
			return False
	
	def get_error(self):
		return self._error

	def validate_project_path(self):
		if not os.path.isdir(self._options.project_path):
			raise ValueError('%s is not a valid path for the project.' % self._options.project_path)
		if not self.has_project_metadata(self._options.project_path):
			raise ValueError('%s seems to be an invalid project path.' % self._options.project_path)
	
	def has_project_metadata(self, path):
		return os.path.isdir(os.path.join(path, '.thot'))
		
	
	def validate_output(self):
		if os.path.isdir(self._options.output):
			raise ValueError('Output path %s already exists. Cannot output to this folder.' 
				% self._options.output)
		parent_dir = os.relpath(os.path.join(self._options.output, '..'))
		if not os.access(parent_dir, os.W_OK):
			raise ValueError('%s is not writable, so %s cannot be created.' % 
				(parent_dir, os.path.basename(self._options.outpu)))
	