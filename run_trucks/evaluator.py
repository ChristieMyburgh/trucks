import numpy as np


class Evaluator:
	"""
	Evaluator for truck optimisation
	"""

	def __init__(self, path):
		self._num_obj = 1
		self._num_constraints = 1
		self._price = np.array(
			[
				9000000, 4000000,
				9000000, 4000000,
				9000000, 4000000,
				9000000, 4000000], dtype=np.int64
		)
		self._tontarget = np.array([140000000, 100000000, 0, 60000000], dtype=np.int64)
		self._capacity = np.array(
			[
				9000000, 3800000,
				10000000, 4000000,
				10000000, 4000000,
				8000000, 3700000], dtype=np.int64
		)
		self._path = path

	def __repr__(self):
		return(
			f'{self.__class__.__name__!r} ('
			f'{self._num_obj!r},\n'
			f'{self._num_constraints!r},\n'
		)

	def get_performance(self, individual, is_hifidelity):
		"""
		Evaluate performance of individual.
		:param individual: Incoming solution.
		:param is_hifidelity: Flag indicating if hifidelity eval is needed.
		:return: Returns objective vector and violation scaler.
		"""

		#  Calculate objective
		obj = self.get_objective(individual)

		violation = self.get_violation(individual)

		return obj, violation

	def get_objective(self, sol):
		obj = np.zeros(self._num_obj)

		obj[0] = -1.0 * np.sum(sol * self._price)

		return obj

	def get_violation(self, sol):

		years = np.zeros(self._tontarget.shape[0])
		violation = 0.0
		for i in range(self._tontarget.shape[0], 2):
			year[i] = (
					sol[i * 2] * self._capacity[i * 2] +
					sol[i * 2 + 1] * self._capacity[i * 2 + 1]
			)

			if year[i] < self._tontarget[i]:
				if self._tontarget[i] > 0:
					violation += (self._tontarget[i] - year[i]) / self._tontarget[i]
				else:
					violation += (self._tontarget[i] - year[i])

		if np.any(years < 0):
			raise Exception("Invalid constraint detected...")

		return violation

	def get_number_objectives(self):
		"""
		Return the number of objectives
		:return:  int
		"""
		return self._num_obj

	def get_number_constraints(self):
		"""
		Return number of constraints
		:return: int
		"""
		return self._num_constraints

	def get_composite_function(self):
		"""
		Return a composite function that combines all objectives and
		constraints.
		:return: Evaluator
		"""
		return NotImplementedError

	def train(self, hidef_sols, obj, constraints):
		"""
		Train the surrogate model.
		:param hidef_sols:  Hi-fidelity solutions.
		:param obj:         Objective values.
		:param constraints: Constraint values.
		:return:            None.
		"""
		return NotImplementedError

	def log_final(self, sol):
		obj, viol = self.get_performance(sol, False)

		with open(f"{self._path}/result.csv",'w') as file:
			file.write(f"Cost,{obj[0]}\n")
			file.write(f"Violation, {viol}\n")
			file.write("Solution\n")
			file.write(f"{sol[0]}, {sol[1]}, {sol[2]}, {sol[3]}, {sol[4]},"
						f"{sol[5]},{sol[6]},{sol[7]}"
			)
