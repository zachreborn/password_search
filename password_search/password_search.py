#! python3

import re
from sys import argv
import os

# Regular Expression Patterns
########################################################################################################################
username_regex = r'''((?!.*[!#$%^*()+,\'"])[a-zA-Z0-9_\.\-@]{4,40})'''
password_regex = r'''((?=.+[#?!@$%^&*.,()])(?=.+[0-9])[\w#?!@$%^&*.,()]{6,})'''
ip_addresses_regex = r'''\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}'''
mac_address_regex = r'''(\w{4,4}\.\w{4,4}\.\w{4,4})|(\w{2,2}:\w{2,2}:\w{2,2}:\w{2,2}:\w{2,2}:\w{2,2})'''
hex_regex = r'''\w+-\w+-\w+-\w+-\w+'''
date_regex = r'''\d{1,4}[\._\-]\d{1,4}[\._\-]\d{1,4}'''
vlan_regex = r'''(\d{1,4},)+'''


def argv_validation():
    """
    Function which checks that the user has input arguments via argv, if not it asks the user for input.
    :return: Root directory, file extension, and file to write log output to.
    """
    if len(argv) < 4:
        print('\nPlease provide an absolute directory to scan, filetype extension, and output file for results in order to begin.'
              '\nExample:\n', r'> python password_search.py C:\Users\username .txt C:\output_results.txt'
              '\n')

        scan_directory = get_user_input('Directory to scan?\n'
                                        r'Example: C:\Users\username'
                                        '\n> ')
        file_extension = get_user_input('File extension to scan for?\n'
                                        'Example: .txt'
                                        '\n> ')
        output_write_file = get_user_input('File to write output to?\n'
                                           r'Example: C:\Users\password_search_output_Users_txt_v1.txt'
                                           '\n> ')

    else:
        scan_directory = argv[1]
        file_extension = argv[2]
        output_write_file = argv[3]

    return scan_directory, file_extension, output_write_file


def get_user_input(prompt):
    """
    Grabs and sanitizes user input either from argv or direct input.
    :param prompt:
    :return:
    """
    result = None
    while result is None:
        val = input(prompt)
        result = val
    return result


def find_files(directory, file_type):
    """
    Function takes an input directory, and file type as strings then searches that directory and all subdirectories
    for a list of files. This list of files can then be acted upon.
    :param directory:
    :param file_type:
    :return:
    """
    found_files = []
    for dirpath, dirnames, filenames in os.walk(directory):
        for filename in [f for f in filenames if f.endswith(file_type)]:
            found_files.append(os.path.join(dirpath, filename))
    return found_files


def file_scanning(list_of_files, output_write_file):
    """

    :param list_of_files:
    :param output_write_file:
    :return:
    """
    for input_filename in list_of_files:
        write_file(output_write_file, 'Checking file: {0}\n'.format(input_filename))
        print('Checking file: {0}'.format(input_filename))

        try:
            with open(input_filename) as read_f:
                for line in read_f:
                    line_search(line, output_write_file)

        except PermissionError:
            write_file(output_write_file, '    Permission denied error')
            pass


def line_search(line, output_file):
    """
    Takes a string and passes it through some regular expressions. First check validates that the item is not devoid of
    a match. The following checks validate that the string does not match commonly used formats, such as dates, mac
    addresses, IP addresses, etc. Finally anything matching that is left over is written to a file.
    :param line:
    :param output_file:
    :return:
    """
    broken_up_line = line.split()
    for item in broken_up_line:
        if password_match(item, password_regex) is None:
            pass
        elif password_findall(item, ip_addresses_regex):
            pass
        elif password_findall(item, hex_regex):
            pass
        elif password_findall(item, mac_address_regex):
            pass
        elif password_findall(item, vlan_regex):
            pass
        elif password_findall(item, date_regex):
            pass
        else:
            write_file(output_file, '    {0}\n'.format(password_findall(item, password_regex)))


def password_match(line, regex):
    """
    Regex function searches an input string for match with at least one special character, at least one number,
     and is at least six characters long. This merely verifies that a match exists, it does not return the matched line.
    :param line: string
    :param regex: Regular expression
    :return: re.match
    """
    pattern = re.compile(regex)
    return pattern.match(line)


def password_findall(line, regex):
    """
    Regex function searches an input string for all matches with at least one special character,
     at least one number, and is at least six characters long.
    :param line:
    :param regex:
    :return:
    """
    pattern = re.compile(regex)
    return pattern.findall(line)


def username_findall(line):
    """
    Unused
    :param line:
    :return:
    """
    pattern = re.compile(username_regex)
    return pattern.findall(line)


def write_file(filename, line_to_write):
    """
    Simple file writing function. Additions will be appended, no possibility of wiping or truncating the file.
    :param filename:
    :param line_to_write:
    :return:
    """
    with open(filename, 'a') as out_f:
        out_f.write(line_to_write)


def main():
    r"""This script can be run via CLI with password_search.py <DIRECTORY> <FILETYPE> > <OUTPUT_FILE>.
    Example:
      >  python password_search.py C:\Users\zhill .txt > C:\Users\zhill\search_output.log
    """
    program_boilerplate = '----------------------------' \
                          '\nPassword Search Utility' \
                          '\n----------------------------\n'

    scan_directory, file_extension, output_write_file = argv_validation()

    status_text = (
                '\nScanning: {0}'
                '\nfor file extension: {1}'
                '\nLog output will write to: {2}\n'
                '======================================================================================================'
                '\n'.format(scan_directory, file_extension, output_write_file)
            )

    write_file(output_write_file, program_boilerplate)
    print(program_boilerplate)
    write_file(output_write_file, status_text)
    print(status_text)

    list_of_files = find_files(scan_directory, file_extension)
    file_scanning(list_of_files, output_write_file)


if __name__ == '__main__':
    main()
