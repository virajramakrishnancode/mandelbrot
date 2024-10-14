# mandelbrot
## A viewer for exploring the mandelbrot set!

### Usage
First of all, install required packages (numpy and matplotlib) with this command:

`pip install -r requirements.txt`

Now, just run `mandelbrot.py`! You can left click to zoom in on any particular area, and right click to zoom out. The zoom factor is set to 2x. The program will take increasingly longer to load the new image as you zoom in further.

Feel free to adjust any of the following parameters! An explanation is below as to how they fit into creating the fractal.
- `iterations`: The number of iterations for which the program will calculate the set. Increase this to see more detail at higher zoom levels.
- `show_iterations`: Setting this to true will show how the algorithm arrives at the set. It shows 10 evenly spaced snapshots of intermediary iterations, before settling at the set after the last iteration. 
- `granularity`: The resolution of the image. I recommend 500x500 for quick loading.
- `iterate`: feel free to play with the iteration function itself! As a starter, try changing the power we raise each pixel in `grid` to! Maybe try cubing instead of squaring?

### Explanation

The Mandelbrot set is an interesting fractal that can be created with a relatively unassuming formula. Before we talk about the weird shape itself, let's talk about the canvas we're painting on. The Mandelbrot Set arises from applying a function to a set of values.

#### Domain
The _domain_ of this function (the set of values we apply our function to) is the _complex plane_: all numbers of the form `a + bi`. To show this very..._complex_...set of numbers in a way we can understand, we plot the real part on the `x` axis, and the imaginary part on the `y`. So the value `a + bi` would be at location `(a, b)`.

#### Range
The range of the function is also going to be complex. So, for a real-valued function in one dimension, `f(x)`, maybe the value of `f` at `5` is `3`. but with this kind of function, perhaps the value at `2 + 3i` is `-i`.

#### Ok, what's the formula?
 You can see formula in the code in the `iterate` function:

```
def iterate(self, grid, coord_grid, iteration_number):
		grid = grid**2 + coord_grid
		grid[np.abs(grid) > 2] = 2
		return grid
```

#### "Iterate"
The set is generated via an iterative formula. Every iteration, a pixel will recalculate its value according to a formula. Over more and more iterations, the set begins to approach a particular shape. In this particular implementation, I've set the number to be `iterations`. To see the iteration in action, turn on `show_iterations`.

#### The formula
`grid = grid**2 + coord_grid`
This is meat of the formula, let's write it a bit more simply:
 
`x_{t+1} = {x_t}^2 + c`.
The value of the function at the `t^th` iteration is `x_t`. We let `x_0 = 0`.
`c` is the location of the point, where we are on the complex plane.

So, for example, let's try with `-1`. `c = -1` in this case. 

`x_{1} = {x_0}^2 + c = 0 + c = -1`

`x_{2} = {x_1}^2 + c = 1 + c = 0`

`x_{3} = {x_2}^2 + c = 0 + c = -1`

Seems like a pattern is emerging... let's try with `1`:

`x_{1} = {x_0}^2 + c = 0 + c = 1`

`x_{2} = {x_1}^2 + c = 1 + c = 2`

`x_{3} = {x_2}^2 + c = 4 + c = 5`

`x_{4} = {x_3}^2 + c = 25 + c = 26`

Seems like this is going to blow up...

So, for some starting numbers, the sequence seems to blow up, and for some others it stays small. And that's exactly it - the Mandlebrot set is the set of points that do not blow up (or diverge).

#### Preventing stuff from blowing up too much
`grid[np.abs(grid) > 2] = 2`
It turns out, if the magnitude of `x_t` ever exceeds `2`, it will certainly diverge. So, to prevent having to plot extremely large values, I manually set back all values that exceed to magnitude `2` to `2` again. 

#### "Grid"
We can never plot the set it all its detail, but we can plot it for a set of pixel in a grid. To streamline computation, I apply the iteration to the whole grid at once. You can mess with the `granularity` to get a higher resolution grid.

#### Magnitudes
`self.im.set_data(np.abs(grid))` To actually show you the image, we can take the magnitude of the function output. If the maginitude is closer to `0`, it means that the function is not diverging at that particular coordinate. If it's at `2` (remember we capped magnitudes at `2`) then it means that the function is diverging.

