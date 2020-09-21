from mindbox.db_worker import DbWorker
from mindbox.string_operation import join_string, get_dict_of_words_from_string, get_list_of_words_from_string




def create_file(file_name: str, file_keywords: str):


	pass


def print_file(app, name, keywords, is_file: bool):
	print(f"Name file: {name.text}\nKeywords: {keywords.text}\nIs file: {is_file}")
	name.text = ''
	keywords.text = ''

	scr_manager = app.root
	scr_manager.current = 'main_window'
