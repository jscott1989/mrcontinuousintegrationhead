class Outlet(object):
	def __init__(self, *args, **kwargs):
		self.map_gpio()
		super(Outlet, self).__init__(*args, **kwargs)