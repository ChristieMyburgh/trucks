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

		year1 = sol[0] * self._capacity[0] + sol[1] * self._capacity[1]
		year2 = sol[2] * self._capacity[2] + sol[3] * self._capacity[3]
		year3 = sol[4] * self._capacity[4] + sol[5] * self._capacity[5]
		year4 = sol[6] * self._capacity[6] + sol[7] * self._capacity[7]

		if year1 < 0 or year2 < 0 or year3 < 0 or year4 < 0:
			raise Exception ("Invalid constraint detected...")

		violation = 0.0
		if year1 < self._tontarget[0]:
			violation += (self._tontarget[0] - year1) / self._tontarget[0]
		if year2 < self._tontarget[1]:
			violation += (self._tontarget[1] - year2) / self._tontarget[1]
		if year3 < self._tontarget[2]:
			violation += (self._tontarget[2] - year3)
		if year4 < self._tontarget[3]:
			violation += (self._tontarget[3] - year4) / self._tontarget[3]

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
