from thot.docs import ThotDocument

class SupplementarySpecification(ThotDocument):

	def __init__(self, objects):
		super(SupplementarySpecification, self).__init__("supplementary_specification.rst", \
			"Supplementary Specification")
		self.objects = self.filter_objects(objects)
	
	def filter_objects(self, objects):
		filtered_objs = {}
		for obj in objects:
			if obj.source() == 'requirements/project.yml':
				filtered_objs['_PROJECT_'] = obj
			else:
				obj_type = obj.get('Type')
				if obj_type is not None:
					if not filtered_objs.get(obj_type):
						filtered_objs[obj_type] = []
					filtered_objs[obj_type].append( obj )
		return filtered_objs
	
	def append_product_section(self, title, index=None):
		if index is None:
			index = title
		try:
			objects = self.objects[index]
		except KeyError:
			return
		self.start("section")
		self.append("title", title)
		for obj in objects:
			self.start("section")
			self.append("title", obj.get('Name'))
			self.append_raw(obj.get('Description'))
			self.end() # section
		self.end() # section
	
	def append_project_section(self, title, index):
		try:
			obj = self.objects['_PROJECT_']
			content = obj.get(index)
			if content:
				self.start("section")
				self.append("title", title)
				self.append_raw( content )
				self.end() # section
		except KeyError:
			pass

	def build(self):
		self.append_product_section("Functionalities", "Functional")
		self.append_product_section("Usability")
		self.append_product_section("Reliability")
		self.append_product_section("Performance")
		self.append_product_section("Supportability")
		self.append_product_section("Design Constraint")
		self.append_project_section("Online User Documentation and Help System Requirements", "Documentation")
		self.append_project_section("Purchased Components", "Components")
		self.append_project_section("Interfaces", "Interfaces")
		self.append_project_section("Licensing Requirements", "License")
		self.append_project_section("Legal, Copyright and Other Notices", "Copyrights")
		self.append_project_section("Applicable Standards", "Standards")

class SingleRequirementDocument(ThotDocument):

	def __init__(self, requirement):
		filepath = requirement.source().replace('.yml', '.rst')
		title = requirement.get('Name')
		super(SingleRequirementDocument, self).__init__(filepath, title)
		self.requirement = requirement

	def build(self):
		try:
			self.start("section")
			self.append("title", "Category")
			self.append("paragraph", self.requirement.get("Type"))
			self.end() # section

			self.start("section")
			self.append("title", "Description")
			self.append_raw( self.requirement.get('Description') )
			self.end() # section

			usecases = self.requirement.get('Implemented By')
			self.start("section")
			self.append("title", "Use Cases implementing this requirement")
			if usecases is not None:
				self.start("bullet_list", bullet="*")
				for uc in usecases:
					self.start("list_item")
					self.append("paragraph", ":doc:`%s`" % "/".join(uc))
					self.end() # list_item
				self.end() # bullet_list
			else:
				self.append("paragraph", "No use cases implements this feature.")
			self.end() #section
		except:
			pass
