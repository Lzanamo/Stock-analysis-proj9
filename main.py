import csv

###########################################################
#  Computer Project #9
#
#  Analyizing the Stock Market with Dictionary and sets
#    prompt for an input from a given option
#    Use that imput to preform a set of instructions which call the nessesary fucntion.
#   The functions open the files needed, reads the files and makes a master dictionary, gets the highest price that a company has from asking the user, gets which company has the highest price in the dictionary, gets the average high price of a company and displays a list of strings.
###########################################################


MENU = '''\nSelect an option from below:
            (1) Display all companies in the New York Stock Exchange
            (2) Display companies' symbols
            (3) Find max price of a company
            (4) Find the company with the maximum stock price
            (5) Find the average price of a company's stock
            (6) quit
    '''
WELCOME = "Welcome to the New York Stock Exchange.\n"


def open_file():
    '''Prompts for bothe price file and securities file. Reprompts if file does not exist.'''
    price_filename = input("\nEnter the price's filename: ")
    while price_filename:
        try:  # tries to open the price file
            price_fp = open(price_filename, "r")
            break
        except FileNotFoundError:
            print("\nFile not found. Please try again.")
            price_filename = input("\nEnter the price's filename: ")

    security_filename = input("\nEnter the security's filename: ")
    while security_filename:
        try:  # tries to open the securities file
            security_fp = open(security_filename, "r")
            break
        except FileNotFoundError:
            print("\nFile not found. Please try again.")
            security_filename = input("\nEnter the security's filename: ")

    return price_fp, security_fp


def read_file(securities_fp):
    '''Reads the securities file and make a set of the names of the companies and the dictionary of the compaies with all the info.'''
    reader = csv.reader(securities_fp)  # reads the securities file
    next(reader)  # skips the header
    # defines the empty set and dictionary
    name_set = set()
    code_dict = {}
    # loops through the lists returned from reading the file
    for line in reader:
        # assigns the the variables to the info on the list
        code = line[0]
        name = line[1]
        sector = line[3]
        subsector = line[4]
        address = line[5]
        date_added = line[6]
        empty_list = []

        name_set.add(name)  # adds the name to the set
        code_dict[code] = [name, sector, subsector, address, date_added,
                           empty_list]  # creats a key in the dictionary with the company symbol and adds the values

    return name_set, code_dict


def add_prices(master_dictionary, prices_file_pointer):
    '''Reads the prices file and adds the price info to the empty list in the dictionary'''
    reader = csv.reader(prices_file_pointer)  # reads the price file and puts them into lists
    next(reader)

    for line in reader:
        # assign the infos to variables
        date = line[0]
        code = line[1]
        open_detail = float(line[2])
        close_detail = float(line[3])
        low_price = float(line[4])
        high_price = float(line[5])
        temp_lst = [date, open_detail, close_detail, low_price,
                    high_price]  # makes the infos above into a list to be added into the dictionary
        if code in master_dictionary:  # checks if the company is in the dictionary
            master_dictionary[code][5].append(
                temp_lst)  # adds the list to the dictionary in the empyt list of the company


def get_max_price_of_company(master_dictionary, company_symbol):
    '''Loops throught the dictionary looking for a specific company and finds the highest price in the company.'''
    list_ofprices = []
    if company_symbol in master_dictionary:  # checks if the company is in the dictionary
        price_info = master_dictionary[company_symbol][5]  # gets all the price info
        if price_info:  # checks if there is any info in the list
            for line in price_info:  # loops through the list if it has info
                date = line[0]
                high = line[4]
                temp_tuple = (high, date)  # makes a tuple of the high price info and the date of that price
                list_ofprices.append(
                    temp_tuple)  # adds the tuple into a list which will contain all the high price info and their date for that company
            max_price = max(
                list_ofprices)  # finds the max in that list which contains all the high price info and their date for that company
            return max_price
        else:
            temp_tuple = (None, None)  # returns this if there is no price info
            return temp_tuple
    else:
        temp_tuple = (None, None)  # returns this if the company does not exist in the dictionary.
        return temp_tuple


def find_max_company_price(master_dictionary):
    '''Loops through the dictionary and for every company it gets that companies highest price by calling the get_max_price_of_company function and compares it to other companies and finds who has the highest price.'''
    # Initialize the needed lists
    list_prices = []
    final_prices = []
    for line in master_dictionary:  # Loops through the master dictionary
        company_max = [get_max_price_of_company(master_dictionary, line),
                       line]  # finds the higest price for each company and makes is a list with the company symbol
        list_prices.append(
            company_max)  # adds the list above to a new list and which will contain all the companies lists

    for i, item in enumerate(
            list_prices):  # loops through the list to remove any companies that do not have any price info and makes a new list for the ones with the info
        if (None, None) == item[0]:
            continue
        else:
            final_prices.append(item)

    max_company = max(final_prices)  # find the max of the prices

    for line in max_company:  # loops through the max list and returns the name and the price info company
        ret_tuple = (max_company[1], line[0])
        break
    return ret_tuple


def get_avg_price_of_company(master_dictionary, company_symbol):
    '''Gets the average of the high price info of a certain company.'''
    # initializes the sum and count variables
    sum_num = 0
    count = 0
    try:  # Uses try statment to see if the company exists in the dictionary
        price_info = master_dictionary[company_symbol][5]
        if price_info:  # checks if the price has the info needed
            for line in price_info:  # loops through the price info of the company
                sum_num += line[4]  # adds the high prices to the sum
                count += 1  # updates the counter

            return round(sum_num / count, 2)  # returns the average
        else:
            return 0.0  # if the price info is empty return 0.0
    except:
        return 0.0  # if the company does not exists returns 0.0


def display_list(lst):  # "{:^35s}"
    '''Docstring'''
    counter = 0

    for line in lst:  # loops through the lst
        print("{:^35s}".format(line), end="")  # prints items in it
        counter += 1  # updates the counter

        if counter == 3:  # if the counter is 3 it goes tot the next line
            print()
            counter = 0

    print("\n")  # prints this at the end


def main():
    print(WELCOME)

    price_fp, securities_fp = open_file()  # opens the files
    name_set, master_dict = read_file(securities_fp)  # calls the read_fiel
    add_prices(master_dict, price_fp)  # calls the add_price

    print(MENU)

    menu_input = int(input("\nOption: "))  # prompts the user for one of the options and changes it to int
    while menu_input:
        if menu_input >= 1 and menu_input <= 6:
            if menu_input == 1:
                print(
                    "\n{:^105s}".format("Companies in the New York Stock Market from 2010 to 2016"))  # prints the title
                sorted_names = sorted(list(name_set))  # sorts the name_set from calling the read_line
                display_list(sorted_names)  # calls display list

                # lines below re-prompt for user choice
                print(MENU)
                menu_input = int(input("\nOption: "))
            elif menu_input == 2:
                print("\ncompanies' symbols:")  # prints titles
                symbol_lst = sorted(master_dict.keys())  # sorts the list of dictionary keys
                display_list(symbol_lst)

                # lines below re-prompt for user choice
                print(MENU)
                menu_input = int(input("\nOption: "))
            elif menu_input == 3:
                company_symbol = input(
                    "\nEnter company symbol for max price: ")  # prompts the user for a company's name
                while company_symbol:
                    if company_symbol in master_dict:  # checks if the company is in the dictionary
                        max_tuple = get_max_price_of_company(master_dict,
                                                             company_symbol)  # calls the get_max_price_of_company with the companies name

                        if max_tuple == (None, None):  # checks if the tuple gots is equal to (None, None)
                            print("\nThere were no prices.")
                            break
                        else:
                            max_price = max_tuple[0]  # gets the price from the tuple
                            date = max_tuple[1]  # gets the date that is returned
                            print("\nThe maximum stock price was ${:.2f} on the date {:s}/\n".format(max_price, date))
                            break
                    else:
                        print(
                            "\nError: not a company symbol. Please try again.")  # if the companies name is not in the dictionary it prints this
                        company_symbol = input("\nEnter company symbol for max price: ")  # re-prompts for the name

                # lines below re-prompt for user choice
                print(MENU)
                menu_input = int(input("\nOption: "))
            elif menu_input == 4:
                max_tuple = find_max_company_price(master_dict)  # calls the find_max_company_price function
                # assigns the company symbol and price to variables
                cmpy_sybl = max_tuple[0]
                price = max_tuple[1]
                print("\nThe company with the highest stock price is {:s} with a value of ${:.2f}\n".format(cmpy_sybl,
                                                                                                            price))

                # lines below re-prompt for user choice
                print(MENU)
                menu_input = int(input("\nOption: "))
            elif menu_input == 5:
                company_symbol = input("\nEnter company symbol for average price: ")  # prompts for a company symbol
                while company_symbol:
                    if company_symbol in master_dict:  # checks if that symbol is in the dictionary
                        avg_result = get_avg_price_of_company(master_dict,
                                                              company_symbol)  # calls the get_avg_price_of_company function with the input symbol and master dictionary
                        print("\nThe average stock price was ${:.2f}.\n".format(avg_result))
                        break
                    else:  # if the symbol is not in the dictionary they re-prompt
                        print("\nError: not a company symbol. Please try again.")
                        company_symbol = input("\nEnter company symbol for average price: ")

                print(MENU)
                menu_input = int(input("\nOption: "))
            elif menu_input == 6:  # ends the program
                break
        else:  # if the user input for the option isn't between 1 and 5 then this re-prompts it
            print("\nInvalid option. Please try again.")
            menu_input = int(input("\nOption: "))

    # closes the files
    price_fp.close()
    securities_fp.close()


if __name__ == "__main__":
    main()
