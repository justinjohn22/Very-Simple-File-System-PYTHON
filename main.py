def execute():
    command = input(">").split()

    valid = False
    while not valid:
        if len(command) > 1 and (command[0].lower() == 'vsfs' or command[0].lower() == 'fs'):
            if command[1] == 'list':
                if len(command) > 2:
                    content = list_files(command, False)

                    if content != 'invalid':
                        print(content)
                    else:
                        valid = True
                else:
                    print('Invalid list command.')
                    valid = True

            elif command[1] == 'copyin':
                err_catch = copyin(command)
                if err_catch == 'invalid':
                    valid = True

            elif command[1] == 'copyout':
                err_catch = copyout(command)
                if err_catch == 'invalid':
                    valid = True

            elif command[1] == 'mkdir':
                err_catch = mkdir(command)
                if err_catch == 'invalid':
                    valid = True

            elif command[1] == 'rm':
                err_catch = rm(command)
                if err_catch == 'invalid':
                    valid = True

            elif command[1] == 'rmdir':
                err_catch = rmdir(command)
                if err_catch == 'invalid':
                    valid = True

            elif command[1] == 'defrag':
                err_catch = defrag(command)
                if err_catch == 'invalid':
                    valid = True

        elif len(command) > 0 and command[0] == 'exit':
            print("Exit Success.")
            valid = True

        else:
            print("Unknown command. Please try again.")
            command = input(">").split()
            if len(command) > 0 and command[0] == 'exit':
                print("Exit Success.")
                valid = True

        if not valid:
            command = input(">").split()
            if len(command) > 0 and command[0] == 'exit':
                print("Exit Success.")
                valid = True


def list_files(command: [], add_content: bool) -> str:
    file_names = ''
    content = ''
    return_string = ''
    file_opened = False
    try:
        fs = open('VSFS.notes', 'r')
        line = fs.readline().strip('\n')
        if line != 'NOTES V1.0':
            print("Invalid FS format - Must begin with > NOTES V1.0")
            return 'invalid'
        content += line + '\n'
        if line and (line[0] == '@' or line[0] == '='):
            file_names += line + '\n'
        while line != '':
            line = fs.readline().strip('\n')
            content += line + '\n'
            if line and (line[0] == '@' or line[0] == '='):
                file_names += line + '\n'
        file_opened = True
    except FileNotFoundError:
        print("Invalid VSFS")
    except IOError:
        print("Invalid VSFS")
    finally:
        if file_opened:
            fs.close()

    if not add_content:
        if file_names == '':
            return_string = 'empty'
        else:
            return_string = file_names
    else:
        return_string = content

    return return_string


def copyin(command) -> str:
    if len(command) != 5:
        print("Invalid VSFS")
        return 'invalid'
    elif command[2].lower() == 'fs':
        content = ''
        read_success = False
        filename = command[3] + '.txt'
        check_exist = list_files(command, False).strip('\n').split('@')
        if command[4] in check_exist or command[4] + '\n' in check_exist:
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
        except FileNotFoundError:
            print("Invalid VSFS")
            return 'invalid'
        except IOError:
            print("Invalid VSFS")
            return 'invalid'
        finally:
            if read_success:
                fs.close()

        if read_success:
            fs = open("VSFS.notes", "a")
            fs.write("@" + command[4] + '\n')
            fs.write(content + '\n')
            fs.close()
    elif command[2].lower() != 'fs':
        print('Invalid VSFS')
        return 'invalid'
    return 'command success'


def copyout(command) -> str:
    if len(command) != 5:
        print("Invalid VSFS")
        return 'invalid'

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
                if index_line == len(copy_items) - 1:
                    start_copy = False

                if start_copy:
                    transfer += copy_items[index_line] + '\n'
            transfer_files(transfer, command[4])
        else:
            print('Invalid VSFS')
            return 'invalid'

    return 'command success'


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

    if opened:
        new_file.close()


def mkdir(command) -> str:
    if len(command) != 4:
        print('Invalid VSFS')
        return 'invalid'
    elif command[2] == 'FS' and len(command) == 4:
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


def rm(command) -> str:
    if len(command) != 4:
        print("Invalid remove command.")
        return 'invalid'
    elif len(command) == 4 and command[2] == 'FS':
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


def rmdir(command) -> str:
    if len(command) != 4:
        print('invalid remove command.')
        return 'invalid'
    elif len(command) == 4 and command[2] == 'FS':
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


def defrag(command) -> str:
    if len(command) != 3:
        print('Invalid defrag command.')
        return 'invalid'
    elif len(command) == 3 and command[2] == 'FS':
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
