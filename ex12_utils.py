import os.path
import math

NOT_PATH_ERROR_MESSAGE = "File doesn't exist!"
OPTION_DICT = {
    "RIGHT": lambda x, y: (x, y + 1),
    "LEFT": lambda x, y: (x, y - 1),
    "UP": lambda x, y: (x - 1, y),
    "DOWN": lambda x, y: (x + 1, y),
    "DIAG-UP-RIGHT": lambda x, y: (x - 1, y + 1),
    "DIAG-DOWN-RIGHT": lambda x, y: (x + 1, y + 1),
    "DIAG-UP-LEFT": lambda x, y: (x - 1, y - 1),
    "DIAG-DOWN-LEFT": lambda x, y: (x + 1, y - 1)
}

def load_words_dict(file_path):
    """
    this function converts the words in a given txt file to a dictionary
    """
    if os.path.isfile(file_path):
        with open(file_path) as words:
            words_dict = {}
            for line in words:
                words_line = line.strip()
                words_dict[words_line] = True
            return words_dict
    else:
        raise ValueError(NOT_PATH_ERROR_MESSAGE)


def is_valid_coordinte(max_x_coordintae, max_y_coordiante, coordinate):
    """
    this function checks if the given coordinate is a valid one - which means
    it doesn't exceed from the board boundaries
    """
    x = coordinate[0]
    y = coordinate[1]
    if x < 0 or x > max_x_coordintae:
        return False
    if y < 0 or y > max_y_coordiante:
        return False
    return True


def are_neighbors(coordinate_1, coordinate_2):
    """
    this function checks is coordinate_1 and coordinate_2 next to each other
    """
    if coordinate_1 == coordinate_2:
        return False
    x_difference = coordinate_1[0] - coordinate_2[0]
    y_difference = coordinate_1[1] - coordinate_2[1]
    if math.fabs(x_difference) <= 1 and math.fabs(y_difference) <= 1:
        return True
    return False


def is_not_duplicate(coordinates_list, coordinate):
    """
    this function checks if the given coordinate exist in coordinates_list
    """
    if coordinate in coordinates_list:
        return False
    return True


def is_in_words(words, current_word):
    """
    this function checks if current_word exists in the dictionary words
    """
    if current_word in words.keys():
        return True
    return False


def is_valid_path(board, path, words):
    """
    this function checks if the given path is valid - which means it has
    valid coordinates, and the letters on each coordinate creates (in a
    specific order), an existing word
    """
    max_x_coordinate = len(board[0]) - 1
    max_y_coordinate = len(board) - 1
    if not len(path):
        return None
    if is_valid_coordinte(max_x_coordinate, max_y_coordinate, path[0]):
        coordinates_list = [path[0]]
        current_word = ""
        current_word += board[path[0][0]][path[0][1]]
        for i in range(1, len(path)):
            if is_valid_coordinte(max_x_coordinate, max_y_coordinate,
                                  path[i]) and is_not_duplicate(
                    coordinates_list, path[i]) and are_neighbors(path[i - 1],
                                                                 path[i]):
                current_word += board[path[i][0]][path[i][1]]
                coordinates_list.append(path[i])
            else:
                return None
    else:
        return None
    if is_in_words(words, current_word):
        return current_word
    else:
        return None


def find_length_n_words_aux(n, options_dict, max_x_coor, max_y_coor, board,
                            current_coordinate, current_path_coordinates,
                            all_coordinates_list):
    """
    this is a recursive function which used to find all possible valid paths on the board
    of length n
    :param n: the path length
    :param options_dict: a dictionary which holds all possible valid 'moves'
    in the game
    :param current_path_coordinates: a list which holds the path coordinates
    :param all_coordinates_list: a list which holds all the possible paths
    """
    if not is_valid_coordinte(max_x_coor, max_y_coor, current_coordinate):
        return
    if n == 1:
        current_path_coordinates.append(current_coordinate)
        all_coordinates_list.append(current_path_coordinates[:])
        current_path_coordinates.pop()
        return
    current_path_coordinates.append(current_coordinate)
    for func in options_dict.values():
        x = current_coordinate[0]
        y = current_coordinate[1]
        find_length_n_words_aux(n - 1, options_dict, max_x_coor, max_y_coor,
                                board, func(x, y), current_path_coordinates,
                                all_coordinates_list)
    current_path_coordinates.pop()


def find_length_n_words(n, board, words):
    """
    this function finds all possible valid path of length n which represents existing
    words in the board
    """
    if n > len(board) * len(board[0]) or n == 0:
        return []
    max_x_coordinate = len(board[0]) - 1
    max_y_coordinate = len(board) - 1
    all_coordinates_list = []
    for i in range(len(board[0])):
        for j in range(len(board)):
            find_length_n_words_aux(n, OPTION_DICT, max_x_coordinate,
                                    max_y_coordinate, board, (i, j), [],
                                    all_coordinates_list)
    all_valid_coordinates_lst = []
    for i in range(len(all_coordinates_list)):
        word = is_valid_path(board, all_coordinates_list[i], words)
        if word is not None:
            all_valid_coordinates_lst.append((word, all_coordinates_list[i]))
    return all_valid_coordinates_lst

    # all_valid_coordinates_dict = {}
    # for i in range(len(all_coordinates_list)):
    #     word = is_valid_path(board, all_coordinates_list[i], words)
    #     if word is not None:
    #         all_valid_coordinates_dict[word] = all_coordinates_list[i]
    # all_valid_coordinates_list = []
    # for key, value in all_valid_coordinates_dict.items():
    #     all_valid_coordinates_list.append((key, value))
    # return all_valid_coordinates_list


def is_guessed(list, word):
    return word in list


if __name__ == '__main__':
    board1 = [['a', 'b', 'c'], ['d', 'd', 'e'], ['t', 'p', 's']]
    words = load_words_dict("boggle_dict_tests.txt")
    print(find_length_n_words(3, board1, words))
