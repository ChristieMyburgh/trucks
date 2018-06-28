import numpy as np


class Spawn:
	"""
	Interface defining spawning operation.  Any object implementing this
	interface must have this function and return a ndarray.
	"""
	def spawn_population(self, pop_size):
		"""
		Create the initial population.
		:param pop_size: Number of solutions in the population.
		:return: ndarray
		"""
		a = np.random.randint(0, 40, size=(pop_size, 8))
		return a

	def number_of_variables(self):
		"""
		The number of variables in a solution.
		:return: int
		"""
		return 8


def do_test():
	spawner = Spawn()
	result = spawner.spawn_population(10)
	print(result)


if __name__ == "__main__":
	do_test()
