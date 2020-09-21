def change_record(old_record_name: str, new_record_name: str, new_keywords_str: str) -> bool:
	if is_record_exist(new_record_name):
		send_record_exist_msg()
		return False

	# Name and keywords are separated by spaces and used as keywords of record(file/dir)
	full_keywords_str = new_record_name + ' ' + new_keywords_str
	new_keywords = get_keywords_from_string(full_keywords_str)

	old_keywords = find_keywords_by_record_name(old_record_name)

	if old_record_name == new_record_name:
		# Delete same keywords from old and new keywords(change in the state of old_keywords and new_keywords)
		del_same_keywords(old_keywords, new_keywords)

		del_record_name_from_keywords(record_name=old_record_name, keywords=old_keywords)
		add_record_name_to_keywords(record_name=new_record_name, keywords=new_keywords)

	elif old_record_name != new_record_name:
		linked_records = get_linked_records(record_name=old_record_name)

		# Relink linked records from old name to new name
		relink_linked_records(old_record_name=old_record_name, new_record_name=new_record_name, linked_records=linked_records)

		del_record_name_from_keywords(record_name=old_record_name, keywords=old_keywords)
		add_record_name_to_keywords(record_name=new_record_name, keywords=new_keywords)

	return True


def escape():
	open_main_window()
