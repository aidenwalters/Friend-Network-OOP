# NAME: <Aiden Walters>

# DESCRIPTION: <OOP that allows user to perform a number of operations on a friend network>


from GraphModule import *
from typing import IO, Tuple, List

# first some global variables will be defined used to define the different options for the user to use in this program
PROGRAMMER = "Aiden Walters"
MEMBER_INFO = "1"
NUM_OF_FRIENDS = "2"
LIST_OF_FRIENDS = "3"
RECOMMEND = "4"
SEARCH = "5"
ADD_FRIEND = "6"
REMOVE_FRIEND = "7"
SHOW_GRAPH = "8"
SAVE = "9"

LINE = "\n*-*_*-*_*-*_*-*_*-*_*-*_*-*_*-*_*-*_*-*_*-*_*-*_*-*_*-*_*-*\n"


# first a class will be defined that has all of a users info
class Member:
    # the definition statement will name all fields necessary for each member
    def __init__(self,
                 member_id: int,
                 first_name: str,
                 last_name: str,
                 email: str,
                 country: str):

        self.member_id = member_id
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.country = country
        self.friends_id_list = None

    # the first method defined will help the user add a friend to their friends list
    def add_friend(self, friend_id) -> None:
        if friend_id not in self.friends_id_list:
            # to add a member to the friends list .append() will be used on the friends list
            self.friends_id_list.append(friend_id)

    # the second method defined will help the user remove a friend from their friends list
    def remove_friend(self, friend_id) -> None:
        if friend_id in self.friends_id_list:
            # to remove a member to the friends list .remove() will be used on the friends list
            self.friends_id_list.remove(friend_id)

    # the next method is used to return the desired members friend list
    def friend_list(self) -> List[int]:
        return self.friends_id_list

    # this method will return the amount of friends of a member using the len() function
    def number_of_friends(self) -> int:
        return len(self.friends_id_list)

    # this last method is called when the class, Member, is printed
    def __str__(self) -> str:
        # this method will provide the user a message with all the info about a desired user
        user_info = self.first_name + ' ' + self.last_name + '\n' + self.email + '\nFrom' + self.country + \
                    '\nHas ' + str(self.number_of_friends()) + ' friends.'
        return user_info


# this function will open the files this script needs to run
def open_file(file_type: str) -> IO:
    # first the function must gather the file name from the user
    file_name = input("Enter the " + file_type + " filename:\n")


    file_pointer = None
    # this function will then use the try except method to make sure it gathers a valid filename
    while file_pointer is None:
        # try will be used to open the file name if the file exists
        try:
            file_pointer = open(file_name, "r")
        # if the file doesn't exist, except will prevent python from throwing an error and instead allow the user to try
        # a different file name
        except IOError:
            print(f"An error occurred while opening the file {file_name}.\n"
                  f"Make sure the file path and name are correct \nand that "
                  f"the file exist and is readable.")
            file_name = input("Enter the " + file_type + " filename:\n")

    return file_pointer


# this function creates a network of friends that will be used to recommend a friend if the user desires
def create_network(fp: IO) -> List[List[int]]:
    size = int(fp.readline())
    connection = []

    for i in range(size):
        connection.append([])

    line = fp.readline()
    # this function then reads in the connection file given by the user
    while line is not None and len(line) >= 3:
        # this while loop reads the connection list by taking the id of both users in each line and creating a
        # 'network' between them
        split_line = line.strip().split(" ")
        connection[int(split_line[0])].append(int(split_line[1]))
        connection[int(split_line[1])].append(int(split_line[0]))

        line = fp.readline()
    #
    return connection


# this function will be used later by the similarity matrix
def num_in_common_between_lists(list1: List, list2: List) -> int:
    degree = 0
    # this function gives two users similarity scores so that a friend can be recommended based on who is the most
    # similar
    for i in range(len(list1)):
        # the for loop checks how many friends in common the two users have and creates a similarity score
        if list1[i] in list2:
            degree += 1

    return degree


# this function initializes a matrix that will hold similarity scores and later be used to recommend friends
def init_matrix(size: int) -> List[List[int]]:
    matrix = []
    # the following nested for loops create a square matrix between each member so that similarity scores
    # can be added for everyone
    for row in range(size):
        matrix.append([])
        for column in range(size):
            matrix[row].append(0)

    return matrix


# this function will calc the similarity scores and add it to the matrix that will be used to recommend a friend
def calc_similarity_scores(profile_list: List[Member]) -> List[List[int]]:
    matrix = init_matrix(len(profile_list))

    # the nested loop below calculates the similarity score between each user so that a matrix of all the scores
    # can be stored and used to recommend a friend for anyone
    for i in range(len(profile_list)):
        for j in range(i, len(profile_list)):
            degree = num_in_common_between_lists(profile_list[i].friends_id_list,
                                                 profile_list[j].friends_id_list)
            matrix[i][j] = degree
            matrix[j][i] = degree

    return matrix


# this function will take a member id from the user and recommend a person that has the most friends in common
def recommend(member_id: int, friend_list: List[int], similarity_list: List[int]) -> int:
    max_similarity_val = -1
    max_similarity_pos = -1

    # the nested loops while check each similarity score and return the user with the highest similarity score
    for i in range(len(similarity_list)):
        if i not in friend_list and i != member_id:
            if max_similarity_val < similarity_list[i]:
                max_similarity_pos = i
                max_similarity_val = similarity_list[i]

    return max_similarity_pos


# this next function will take the list of profiles given as a file by the user and store each profile in a list of
# classes
def create_members_list(profile_fp: IO) -> List[Member]:
    # first an empty list is created that will store classes later
    profiles = []
    # the profiles will then be read using commas as delimiters
    profile_fp.readline()
    line = profile_fp.readline()
    profile_list = line.split(',')
    # the while loop will iterate through each profile in the given file and store the info in as Member classes
    while line is not None and len(profile_list) == 5:
        # since the first piece of info given is the id, the member id will be stored first
        member_id = int(profile_list[0].strip())
        # each of the following lines will add the next pieces of info as given in the profile.csv files
        first_name = profile_list[1].strip()
        last_name = profile_list[2].strip()
        email = profile_list[3].strip()
        country = profile_list[4].strip()
        # this next line will add a Member class for each user profile given in the profiles.csv file
        profiles.append(Member(member_id, first_name, last_name, email, country))

        line = profile_fp.readline()
        profile_list = line.split(',')
    return profiles


# the next function will display a list of options that the user can choose to perform
def display_menu():
    print("\nPlease select one of the following options.\n")
    # the list of action will be printed using the global variables defined at the beginning of this script
    print(MEMBER_INFO + ". Show a member's information \n" +
          NUM_OF_FRIENDS + ". Show a member's number of friends\n" +
          LIST_OF_FRIENDS + ". Show a member's list of friends\n" +
          RECOMMEND + ". Recommend a friend for a member\n" +
          SEARCH + ". Search members by country\n" +
          ADD_FRIEND + ". Add friend\n" +
          REMOVE_FRIEND + ". Remove friend\n" +
          SHOW_GRAPH + ". Show graph\n" +
          SAVE + ". Save changes\n")
    # then this function will gather what option the user wants to use, using input()
    return input("Press any other key to exit.\n")


# this function will verify the member id requested by the user id is a valid id
def receive_verify_member_id(size: int):
    valid = False
    while not valid:
        # first the function will collect a member id from the user
        member_id = input(f"Please enter a member id between 0 and {size}:\n")
        # the first check will make sure the user id is all digits
        if not member_id.isdigit():
            print("This is not a valid entry")
        # the second check will make sure the member id is within the range of member ids given in the profiles.csv file
        elif not 0 <= int(member_id) < size:
            print("This member id does not exist")
        # if both checks are passed the member id will be returned
        else:
            valid = True

    return int(member_id)


# the next function will be used to add a friend if the user requests
def add_friend(profile_list: List[Member],
               similarity_matrix: List[List[int]]) -> None:
    # first the user must input which members they would like to add as friends
    size = len(profile_list)
    print("For the first friend: ")
    member1 = receive_verify_member_id(size)
    print("For the second friend: ")
    member2 = receive_verify_member_id(size)
    # next the function will make sure the two members named by the user are not already friends and
    # that they are not the same person
    if member1 == member2:
        print("You need to enter two different ids. Please try again.")
    elif member1 in profile_list[member2].friends_id_list:
        print("These two members are already friends. Please try again.")
    else:
        # if the two members are valid, the members will be added to each individual friend list
        profile_list[member1].add_friend(member2)
        profile_list[member2].add_friend(member1)
        # if the two members are valid, the similarity matrix must also be modified to reflect the new friends
        for i in range(size):
            if member2 in profile_list[i].friends_id_list:
                similarity_matrix[member1][i] += 1
                if member1 != i:
                    similarity_matrix[i][member1] += 1
            if member1 in profile_list[i].friends_id_list:
                similarity_matrix[member2][i] += 1
                if member2 != i:
                    similarity_matrix[i][member2] += 1

        print("The connection is added. Please check the graph.")


# the next function will be used to remove a friend if the user requests
def remove_friend(profile_list: List[Member],
                  similarity_matrix: List[List[int]]) -> None:
    size = len(profile_list)
    # first the user must input which members they would like to remove as friends
    print("For the first friend: ")
    member1 = receive_verify_member_id(size)
    print(f"For the second friend, select from following list: {profile_list[member1].friends_id_list}")
    member2 = receive_verify_member_id(size)
    # next the function will make sure the two members named by the user are currently friends and that they are not the
    # same person
    if member1 == member2:
        print("You need to enter two different ids. Please try again.")
    elif member1 not in profile_list[member2].friends_id_list:
        print("These two members are not friends. Please try again.")
    else:
        # if the two members are valid, the members will be removed from each individual friend list
        profile_list[member1].remove_friend(member2)
        profile_list[member2].remove_friend(member1)
        # if the two members are valid, the similarity matrix must also be modified to reflect the two members who
        # are no longer friends
        for i in range(size):

            if member2 in profile_list[i].friends_id_list:
                similarity_matrix[member1][i] -= 1
                if member1 != i:
                    similarity_matrix[i][member1] -= 1
            if member1 in profile_list[i].friends_id_list:
                similarity_matrix[member2][i] -= 1
                if member2 != i:
                    similarity_matrix[i][member2] -= 1

        similarity_matrix[member1][member1] -= 1
        similarity_matrix[member2][member2] -= 1

        print("The connection is removed. Please check the graph.")


# This function asks for a country name and list all members from that country.
def search(profile_list: List[Member]) -> None:
    # first the user must be asked for which country they would like to search for
    country_search = input("Please enter a country name: ")
    # the following loop while then iterate through the profiles and print the name of each person from the country
    # the user decided to search for
    for i in range(len(profile_list)):
        if profile_list[i].country.lower() == country_search.lower():
            print(profile_list[i].first_name + ' ' + profile_list[i].last_name + '\n')



def add_friends_to_profiles(profile_list: List[Member],
                            network: List[List[int]]) -> None:
    for i in range(len(profile_list)):
        profile_list[i].friends_id_list = network[i]


# this function will perform the actions requested by the user
def select_action(profile_list: List[Member],
                  network: List[List[int]],
                  similarity_matrix: List[List[int]]) -> str:
    response = display_menu()

    print(LINE)
    size = len(profile_list)
    # if the action requires a user id, this part will verify the user id
    if response in [MEMBER_INFO, NUM_OF_FRIENDS, LIST_OF_FRIENDS, RECOMMEND]:
        member_id = receive_verify_member_id(size)
    # the first action prints the Member class to display all the info requested by the user
    if response == MEMBER_INFO:
        print(profile_list[member_id])
    # the second action displays the number of friends for the member named by the user
    elif response == NUM_OF_FRIENDS:
        name = profile_list[member_id].first_name
        print(name + ' has ' + str(profile_list[member_id].number_of_friends()) + ' friends.')
    # the third action prints the list of friends of a desired member using a function defined earlier
    elif response == LIST_OF_FRIENDS:
        for item in profile_list[member_id].friends_id_list:
            print(str(item) + ' ' + profile_list[item].first_name + ' ' + profile_list[item].last_name)
    # the fourth action recommends a friend using the function worked on in assignment 2
    elif response == RECOMMEND:
        list_of_friends = profile_list[member_id].friends_id_list
        recommended_id = recommend(member_id, list_of_friends, similarity_matrix[member_id])

        print(
            "The suggested friend for " + profile_list[member_id].first_name + ' ' + profile_list[member_id].last_name +
            " is " + profile_list[recommended_id].first_name + ' ' + profile_list[
                recommended_id].last_name + " with id " + str(recommended_id))
    # the fifth action will search for members from a desired country using the search function defined
    # earlier in this script
    elif response == SEARCH:
        search(profile_list)
    # the sixth action adds a friends using the add friend function defined earlier in this script
    elif response == ADD_FRIEND:
        add_friend(profile_list, similarity_matrix)
    # the seventh action removes a friends using the remove friend function defined earlier in this script
    elif response == REMOVE_FRIEND:
        remove_friend(profile_list, similarity_matrix)
    # this function displays a graph coded by the professor
    elif response == SHOW_GRAPH:
        tooltip_list = []
        for profile in profile_list:
            tooltip_list.append(profile)
        graph = Graph(PROGRAMMER,
                      [*range(len(profile_list))],
                      tooltip_list, network)
        graph.draw_graph()
        print("Graph is ready. Please check your browser.")
    # this final action, save, uses a new function to save a new list of connections that may have been
    # modified by the user who used the add and remove functions
    elif response == SAVE:
        save_changes(profile_list)
    else:
        return "Exit"

    print(LINE)

    return "Continue"


# this function saves a new connection file in case the user added or removed friends
def save_changes(profile_list: List[Member]) -> None:
    file_name = input("Please enter the filename: ")
    file_pointer = None
    while file_pointer is None:
        # try will be used to open the file name if the file exists
        try:
            file_pointer = open(file_name, "w")
            size = str(len(profile_list))
            # at the top of the file, the number of members in the connection file will be printed
            file_pointer.write(size + '\n')
            # an empty string will be defined so that each new connection can be added to check before duplicates are
            # added to the new file
            string = ''
            # the following nested loop will add each new connection
            for index in range(len(profile_list)):
                for item in profile_list[index].friends_id_list:
                    # first the new connection are added to the variable string
                    string += (str(index) + ' ' + str(item) + '\n')
                    # the if statement will then only add the connection to the file if it is not a duplicate by
                    # checking to see if the connection is already in the variable string
                    if str(item) + ' ' + str(index) not in string:
                        file_pointer.write(str(index) + ' ' + str(item) + '\n')
            file_pointer.close()
            print("All changes are saved in " + file_name)

        # if the file doesn't exist, except will prevent python from throwing an error and instead allow the user to try
        # a different file name
        except IOError:
            print(f"An error occurred while opening the file {file_name}.\n"
                  f"Make sure the file path and name are correct \nand that "
                  f"the file exist and is writeable.")
            file_name = input("Please enter the filename:\n")


# this section will initialize variables required to display the friend network
def initialization() -> Tuple[List[Member], List[List[int]], List[List[int]]]:
    profile_fp = open_file("profile")
    profile_list = create_members_list(profile_fp)

    connection_fp = open_file("connection")
    network = create_network(connection_fp)
    add_friends_to_profiles(profile_list, network)
    similarity_matrix = calc_similarity_scores(profile_list)

    profile_fp.close()
    connection_fp.close()

    return profile_list, network, similarity_matrix


def main():
    print("Welcome to the network program.")
    print("We need two data files.")
    profile_list, network, similarity_matrix = initialization()
    action = "Continue"
    while action != "Exit":
        action = select_action(profile_list, network, similarity_matrix)

    input("Thanks for using this program.")


if __name__ == "__main__":
    main()
