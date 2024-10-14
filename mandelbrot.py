import numpy as np
import matplotlib.pyplot as plt

class MandelbrotViewer:
	def __init__(self, center, width, granularity, iterations, show_iterations=False):

		self.show_iterations = show_iterations
		self.granularity = granularity
		self.center = center
		self.width = width
		self.iterations = iterations
		self.reset_grids()
		self.fig, self.ax = plt.subplots()
		self.grid = self.n_iterations(self.grid, self.coord_grid, iterations, False)
		self.cid = self.fig.canvas.mpl_connect('button_press_event', self.onclick)
		self.im = self.ax.imshow(np.abs(self.grid), cmap='viridis')
		self.fig.colorbar(self.im)

	def reset_grids(self):
		# keep grid of coordinates (only need to calculate once)
		real_part = np.linspace(self.center[0] - self.width/2, self.center[0] + self.width/2, self.granularity)
		real_part = np.tile(real_part, (self.granularity, 1))
		imag_part = np.linspace(self.center[1] - self.width/2, self.center[1] + self.width/2, self.granularity)
		imag_part = np.tile(imag_part, (self.granularity, 1))
		imag_part = imag_part.T * 1j
		self.coord_grid = real_part + imag_part
		self.grid = np.copy(self.coord_grid)

	def iterate(self, grid, coord_grid, iteration_number):
		grid = grid**2 + coord_grid
		grid[np.abs(grid) > 2] = 2
		return grid

	def n_iterations(self, grid, coord_grid, num_iterations, animate=False):
		
		if animate:
			plt.ion()
		
		for i in range(num_iterations):
			# iterate
			grid = self.iterate(grid, coord_grid, i)
			if animate and i % (num_iterations//10) == 0:
				print("iteration: " + str(i))
				self.im.set_data(np.abs(grid))
				self.ax.figure.canvas.draw()
				plt.pause(0.001)  # Short pause to allow the plot to update
		if animate:
			plt.ioff()  # Turn off interactive mode

		return grid

	def onclick(self, event):
		if event.xdata is None or event.ydata is None:
			# Ignore clicks outside the image area
			return
		
		# Get the coordinates of the click
		x, y = int(event.xdata), int(event.ydata)

		self.center = (self.width*x/self.granularity + self.center[0] - self.width/2, self.center[1] - self.width/2 + self.width*y/self.granularity)
		# Zoom in with left click (button=1), zoom out with right click (button=3)
		if event.button == 1:  # Left click: Zoom in
			self.width = self.width/2
			print("left click")
		elif event.button == 3:  # Right click: Zoom out
			print("right click")
			self.width = self.width*2

		self.reset_grids()
		print("center:", self.center)
		print("width of window:", self.width)
		self.grid = self.n_iterations(self.grid, self.coord_grid, self.iterations, self.show_iterations)
		self.im = self.ax.imshow(np.abs(self.grid), cmap='viridis')

		# Redraw the heatmap with the updated zoom view
		self.ax.figure.canvas.draw()
	def show(self):
		plt.show()

viewer = MandelbrotViewer((0,0), 4, 500, 200, show_iterations=True)
viewer.show()
