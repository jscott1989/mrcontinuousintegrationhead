class Device(object):
	def __init__(self, *args, **kwargs):
		self.map_gpio()
		super(Device, self).__init__(*args, **kwargs)