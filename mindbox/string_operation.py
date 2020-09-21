from mindbox.not_none import EmptyObject


def get_keywords_from_string(string: str) -> list:
	return string.upper().split()


def get_dict_of_words_from_string(string: str) -> dict:
	list_of_words = get_dict_of_words_from_string(string)
	dict_of_words = {key: EmptyObject() for key in list_of_words}
	return dict_of_words


def get_list_of_words_from_string(string: str) -> list:
	return string.upper().split()


def join_string(*strings) -> str:
	joined_string = ' '.join(strings)
	return joined_string


def get_words_in_upper(words: list) -> list:
	return [word.upper() for word in words]
