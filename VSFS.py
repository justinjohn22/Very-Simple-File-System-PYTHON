# main method that captures input from user
def execute():
    command = input(">").split()
    ELEMENT_ONE = 1
    ELEMENT_ZERO = 0
    VALID_LENGTH = 2
    valid = False
    while not valid:
        if len(command) > ELEMENT_ONE and (command[ELEMENT_ZERO].lower() == 'vsfs' or command[ELEMENT_ZERO].lower() == 'fs'):
            # list of commands and calling its respective methods
            if command[ELEMENT_ONE] == 'list':
                if len(command) > VALID_LENGTH:
                    content = list_files(command, False)

                    if content != 'invalid':
                        print(content)
                    else:
                        valid = True
                else:
                    print('Invalid list command.')
                    valid = True

            elif command[ELEMENT_ONE] == 'copyin':
                err_catch = copyin(command)
                if err_catch == 'invalid':
                    valid = True

            elif command[ELEMENT_ONE] == 'copyout':
                err_catch = copyout(command)
                if err_catch == 'invalid':
                    valid = True

            elif command[ELEMENT_ONE] == 'mkdir':
                err_catch = mkdir(command)
                if err_catch == 'invalid':
                    valid = True

            elif command[ELEMENT_ONE] == 'rm':
                err_catch = rm(command)
                if err_catch == 'invalid':
                    valid = True

            elif command[ELEMENT_ONE] == 'rmdir':
                err_catch = rmdir(command)
                if err_catch == 'invalid':
                    valid = True

            elif command[ELEMENT_ONE] == 'defrag':
                err_catch = defrag(command)
                if err_catch == 'invalid':
                    valid = True

        # successful execution
        elif len(command) > ELEMENT_ZERO and command[ELEMENT_ZERO] == 'exit':
            print("Exit Success.")
            valid = True

        # capturing errors with graceful output
        else:
            print("Unknown command. Please try again.")
            command = input(">").split()
            if len(command) > ELEMENT_ZERO and command[ELEMENT_ZERO] == 'exit':
                print("Exit Success.")
                valid = True

        if not valid:
            command = input(">").split()
            if len(command) > ELEMENT_ZERO and command[ELEMENT_ZERO] == 'exit':
                print("Exit Success.")
                valid = True

# command implementation of listing
def list_files(command: [], add_content: bool) -> str:
    ELEMENT_ZERO = 0
    file_names = ''
    content = ''
    return_string = ''
    file_opened = False
    # open file, check for errors, capture using exceptions
    try:
        fs = open('VSFS.notes', 'r')
        # getting only names of files and directories
        line = fs.readline().strip('\n')
        if line != 'NOTES V1.0':
            print("Invalid FS format - Must begin with > NOTES V1.0")
            return 'invalid'
        content += line + '\n'
        if line and (line[ELEMENT_ZERO] == '@' or line[ELEMENT_ZERO] == '='):
            file_names += line + '\n'
        while line != '':
            line = fs.readline().strip('\n')
            content += line + '\n'
            if line and (line[ELEMENT_ZERO] == '@' or line[ELEMENT_ZERO] == '='):
                file_names += line + '\n'
        file_opened = True
    # exception handling
    except FileNotFoundError:
        print("Invalid VSFS")
    except IOError:
        print("Invalid VSFS")
    finally:
        if file_opened:
            fs.close()

    # return either only names or names and its content
    if not add_content:
        if file_names == '':
            return_string = 'empty'
        else:
            return_string = file_names
    else:
        return_string = content

    return return_string

# copyin command execution
def copyin(command) -> str:
    TOTAL_LENGTH = 5
    ELEMENT_TWO = 2
    ELEMENT_THREE = 3
    ELEMENT_FOUR = 4
    # check input validity
    if len(command) != TOTAL_LENGTH:
        print("Invalid VSFS")
        return 'invalid'
    elif command[ELEMENT_TWO].lower() == 'fs':
        content = ''
        read_success = False
        filename = command[ELEMENT_THREE] + '.txt'
        # reading from file, and only adding required content
        check_exist = list_files(command, False).strip('\n').split('@')
        if command[ELEMENT_FOUR ] in check_exist or command[ELEMENT_FOUR ] + '\n' in check_exist:
            print("Invalid VSFS")
            return 'invalid'
        try:
            fs = open(filename, 'r')
            line = fs.readline()
            content += ' ' + line
            # print(line)

            while line != '':
                line = fs.readline()
                content += ' ' + line
                # print(line)
            read_success = True
        # exception handling
        except FileNotFoundError:
            print("Invalid VSFS")
            return 'invalid'
        except IOError:
            print("Invalid VSFS")
            return 'invalid'
        finally:
            if read_success:
                # close file after use
                fs.close()

        if read_success:
            # update VSFS if everything is fine
            fs = open("VSFS.notes", "a")
            fs.write("@" + command[ELEMENT_FOUR] + '\n')
            fs.write(content + '\n')
            fs.close()
    elif command[ELEMENT_TWO].lower() != 'fs':
        print('Invalid VSFS')
        return 'invalid'
    return 'command success'


# implementation for copyout
def copyout(command) -> str:
    VALID_LENGTH = 5
    ARR_LENGTH = 1
    if len(command) != VALID_LENGTH:
        print("Invalid VSFS")
        return 'invalid'

    # open file and retrieve what is needed
    elif command[2].lower() == 'fs':
        files = list_files(command, True)
        check_exist = list_files(command, False).strip('\n').split('@')
        if command[3] in check_exist or command[3] + '\n' in check_exist:
            print('file found')
            copy_items = files.split('\n')
            print(copy_items)
            start_copy = False
            transfer = ''
            for index_line in range(len(copy_items)):
                if copy_items[index_line] == '@' + command[3]:
                    print(copy_items[index_line])
                    start_copy = True
                if (copy_items[index_line]) != '':
                    if (copy_items[index_line])[0] == '@' and copy_items[index_line] != '@' + command[3]:
                        start_copy = False
                else:
                    start_copy = False
                if index_line == len(copy_items) - ARR_LENGTH:
                    start_copy = False

                if start_copy:
                    transfer += copy_items[index_line] + '\n'
            transfer_files(transfer, command[4])
        else:
            print('Invalid VSFS')
            return 'invalid'

    # return successful operation
    return 'command success'


# helper method for creating a new external file
def transfer_files(content: str, file_name: str):
    opened = False
    new_file = ''
    try:
        new_file = open(file_name + ".txt", "w")
        opened = True
        new_file.write(content)
        print("new file created")
    except IOError:
        print("Invalid VSFS")

    # only close if successfully opened
    if opened:
        new_file.close()

# command implementation for mkdir
def mkdir(command) -> str:
    VALID_LENGTH = 4
    # error handling
    if len(command) != VALID_LENGTH:
        print('Invalid VSFS')
        return 'invalid'
    elif command[2] == 'FS' and len(command) == VALID_LENGTH:
        file_opened = False
        check_exist = list_files(command, False).split('\n')
        try:
            if '=' + command[3] + '/' not in check_exist:
                fs = open('VSFS.notes', 'a')
                fs.write('=' + command[3] + '/' + '\n')
                file_opened = True
            else:
                print('Invalid VSFS')
                return 'invalid'
        except FileNotFoundError:
            print("Invalid VSFS")
        except IOError:
            print("Invalid VSFS")
        finally:
            if file_opened:
                fs.close()
    elif command[2] != 'FS':
        return 'invalid'

# command implementation for rm
def rm(command) -> str:
    VALID_LENGTH = 4
    if len(command) != VALID_LENGTH:
        print("Invalid remove command.")
        return 'invalid'
    elif len(command) == VALID_LENGTH and command[2] == 'FS':
        new_content = ''
        continue_copy = True
        initial = True
        content = list_files(command, True).split('\n')
        files = list_files(command, False)
        if command[3] not in files:
            print("File not found.")
            return 'invalid'
        for index in range(len(content)):
            if content[index] == '@' + command[3]:
                continue_copy = False

            if not initial and not continue_copy:
                if (content[index]).startswith('@'):
                    continue_copy = True
            elif initial and not continue_copy:
                initial = False

            if continue_copy:
                new_content += content[index] + '\n'
            if not continue_copy:
                if content[index].startswith('@'):
                    temp = content[index]
                    temp = temp.strip('@')
                    new_content += '#' + temp + '\n'
                else:
                    new_content += '#' + content[index] + '\n'

        fs = open("VSFS.notes", "w")
        fs.write(new_content + '\n')
        fs.close()

        return 'command success'
    else:
        print("Invalid remove command.")
        return 'invalid'

# command implementation for rmdir
def rmdir(command) -> str:
    VALID_LENGTH = 4
    if len(command) != VALID_LENGTH:
        print('invalid remove command.')
        return 'invalid'
    elif len(command) == VALID_LENGTH and command[2] == 'FS':
        new_content = ''
        continue_copy = True
        initial = True
        content = list_files(command, True).split('\n')
        files = list_files(command, False)
        if command[3] not in files:
            print("File not found.")
            return 'invalid'
        for index in range(len(content)):
            if content[index] == '@' + command[3] \
                    or content[index].startswith('=' + command[3] + '/'):
                continue_copy = False

            if not initial and not continue_copy:
                if (content[index]).startswith('@') and not (content[index]).startswith('@' + command[3]):
                    continue_copy = True
            elif initial and not continue_copy:
                initial = False

            if continue_copy:
                new_content += content[index] + '\n'
            if not continue_copy:
                if content[index].startswith('@') or content[index].startswith('='):
                    temp = content[index]
                    temp = temp.strip('@')
                    temp = temp.strip('=')
                    new_content += '#' + temp + '\n'
                else:
                    new_content += '#' + content[index] + '\n'

        fs = open("VSFS.notes", "w")
        fs.write(new_content + '\n')
        fs.close()

# command implementation for defrag
def defrag(command) -> str:
    VALID_LENGTH = 3
    if len(command) != VALID_LENGTH:
        print('Invalid defrag command.')
        return 'invalid'
    elif len(command) == VALID_LENGTH and command[2] == 'FS':
        content = list_files(command, True).split('\n')
        new_content = ''
        for index in range(len(content)):
            if not content[index].startswith('#'):
                new_content += content[index] + '\n'

        fs = open("VSFS.notes", "w")
        fs.write(new_content + '\n')
        fs.close()

    else:
        print("Error - wrong format.")
        return 'invalid'


execute()
