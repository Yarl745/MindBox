class EmptyObject:
	def __str__(self) -> str:
		return "Вы ещё не вводили данные в этот фалй!"


	def __bool__(self) -> bool:
		return False
