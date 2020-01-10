import os
import re


def find_files(root, file_types, ignore_dirs):
    """
    Find all files that match the regex in the root directory and below.
    Ignore all directories in the ignore_dirs array.

    :param root: The directory to start the search.
    :param file_types: Array of file types including a dot, e.g. ['.java','.js']
    :param ignore_dirs: Array of directories to ignore.
    :return: An array of file paths.
    """

    # Build regex
    file_types_regex = '|'.join(str(file_type) for file_type in file_types)
    regex = r'.*(' + file_types_regex + ')$'
    reg_obj = re.compile(regex, re.IGNORECASE)

    res = []
    for dirName, subdirList, fileList in os.walk(root):
        for fname in fileList:
            file_path = os.path.join(dirName, fname)
            if reg_obj.match(file_path) and not ignore_path(file_path, ignore_dirs):
                res.append(file_path)
    return res


def ignore_path(path, ignore_paths):
    """
    Determine if a path should be ignored based on paths in the ignore_path array.

    :param path: The directory path to test.
    :param ignore_paths: An array of paths to ignore.
    :return: A boolean determining to ignore or not.
    """
    ignore = False
    for ignore_path in ignore_paths:
        if ignore_path in path:
            return True

    return ignore


def grep_file(filepath, search_texts, ignore_texts):
    """
    Grep a file for a regex.
    :param filepath: The file path to read.
    :param search_texts: Array of strings to search for.
    :param ignore_texts: Array of strings to ignore.
    :return: Matched file path, line number and line.
    """

    # Build search regex
    search_text_regex = '|'.join(str(search_text) for search_text in search_texts)
    search_regex = r'(' + search_text_regex + ')'
    search_reg_obj = re.compile(search_regex)

    # Build ignore regex
    ignore_text_regex = '|'.join(str(ignore_text) for ignore_text in ignore_texts)
    ignore_regex = r'(' + ignore_text_regex + ')'
    ignore_reg_obj = re.compile(ignore_regex)

    res = []
    f = open(filepath, mode="r", encoding="utf-8")
    for num, line in enumerate(f, 1):
        if search_reg_obj.search(line):
            if not ignore_texts or not ignore_reg_obj.search(line):
                res.append(filepath + ' ' + str(num) + ' ' + line.strip())

    return res


def grep_files(root_dir, file_types, ignore_dirs, search_texts, ignore_texts):
    """
    Grep directory for matching lines, considering ignore directories, text to search and
    :param root_dir: The directory to start searching from.
    :param file_types: File types to search for.
    :param ignore_dirs: Directories to ignore.
    :param search_texts: Array of search terms to search for.
    :param ignore_texts: Array of texts to ignore.
    :param ignore_files: Array of file paths to ignore.
    :return: An array of found lines.
    """
    found_files = find_files(root_dir, file_types, ignore_dirs)
    all_found_lines = []
    for file in found_files:
        all_found_lines = all_found_lines + grep_file(file, search_texts, ignore_texts)

    return all_found_lines
