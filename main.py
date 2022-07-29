from typing import List, Tuple, Optional
from PIL import Image

# Kamenožrout available at https://is.muni.cz/auth/hry/01/

WIDTH: int = 20  # constant; width of a board
HEIGHT: int = 10  # constant; height of a board

Fill = int  # represents content of a tile; can be of following values:

EMPTY: Fill = 0
PURPLE: Fill = 1
MAGENTA: Fill = 2
NAVY: Fill = 3
TEAL: Fill = 4
SKY: Fill = 5

EMPTY_RGB: Tuple[int, int, int]
PURPLE_RGB: Tuple[int, int, int] = (219, 32, 255)
MAGENTA_RGB: Tuple[int, int, int] = (255, 19, 104)
NAVY_RGB: Tuple[int, int, int] = (0, 0, 128)
TEAL_RGB: Tuple[int, int, int] = (8, 201, 255)
SKY_RGB: Tuple[int, int, int] = (81, 81, 251)
# todo might want to add EMPTY_RGB

Matrix = List[List[Fill]]  # represents the grid of stones itself

Coord = Tuple[int, int]

COORD_SEP = ';'  # separates the two coordinates in a string representation of a move
MOVE_SEP = ' '  # separates two moves in a string representation of list of moves

SESSION_PROMPT: str = "playing session>>>"
PLAYER_PROMPT: str = "stoner>player>>>"
TASKMASTER_PROMPT: str = "stoner>taskmaster>>>"
CONFIRM_PROMPT: str = "resolved ^this board; proceed to save?\n" \
                      "input 'y' to confirm, anything else to cancel\n" \
                      ">>>"
ADMIN_PROMPT: str = "stoner>admin>>>"
MENU_PROMPT: str = "stoner>>>"
ENTER_ADMIN_PROMPT = ">>>"
ENTER_ADMIN_LOGIN_PROMPT: str = "login>>>"
ENTER_ADMIN_PASSWORD_PROMPT: str = "password"
ENTER_TASKMASTER_PROMPT: str = ">>>"

ADMIN_LOGIN_PROMPT: str = "stoner>admin login>>>"
ADMIN_PASSWORD_PROMPT: str = "stoner>admin password>>>"
TASKMASTER_LOGIN_PROMPT: str = "stoner>taskmaster login>>>"
TASKMASTER_PASSWORD_PROMPT: str = "stoner>taskmaster password>>>"
PLAYER_LOGIN_PROMPT: str = "stoner>player login>>>"
PLAYER_PASSWORD_PROMPT: str = "stoner>player password>>>"

USERDB: str = "userdb.txt"
USERDB_SEP: str = " "

AUTH_TRUE: str = "True"
AUTH_FALSE: str = "False"

BLACKLIST: List[str] = ["doskar"]

ADMIN_LOGIN: str = "admin"  # yeah
ADMIN_PASSWORD: str = "admin"

MENU_HELP: str = "commands:\n" \
                 "a : admin\n" \
                 "t : taskmaster\n" \
                 "p : player\ne : exit\n" \
                 "h : help"
ADMIN_HELP: str = "commands:\n" \
                  "a login password taskmaster_auth player_auth : add user to the database\n" \
                  "d login : delete user from the database\n" \
                  "u login password taskmaster_auth player_auth : update user\n" \
                  "v : view user database\n" \
                  "e : exit admin UI\n" \
                  "boolean values to be input as \"True\", \"False\""
TASKMASTER_HELP: str = "commands:\n" \
                       "l picture_path assignment_path : load assignment from picture\n" \
                       "v session_path : view player session (assignment, moves, final board)\n" \
                       "e : exit taskmaster interface"
PLAYER_HELP: str = "commands:\n" \
                   "c assignment_path output_path : create session from assignment_path in output_path\n" \
                   "p session_path : play session session_path\n" \
                   "e : exit player interface"
PLAY_SESSION_HELP: str = "commands:\n" \
                         "intCOORD_SEPint : click this tile\n" \
                         "z : undo\n" \
                         "y : redo\n" \
                         "a verbose : auto-solve; verbose: True | False\n" \
                         "s : save & exit\n" \
                         "h : help"


class Board:
    """
    Class Board represents current state of the board,
    namely its stones, their color and position

    Given the operations required from this class, the board matrix shall be represented
    as an array of columns, indexing then shall be matrix[col][row]. Although bit unorthodox,
    this representation maps neatly to the mental model, as it can be thought of as matrix[x][y],
    where x, y are coordinates of cartesian coordinate system.

    [0, 9]   [1, 9]    [2, 9]   ... [19, 9]
    ...      ...       ...      ... ...
    [0, 2]   [1, 2]    [2, 2]   ... [19, 2]
    [0, 1]   [1, 1]    [2, 1]   ... [19, 1]
    [0, 0]   [1, 0]    [2, 0]   ... [19, 0]
    ^mtrx[0] ^mtrx[1]  ^mtrx[2] ... ^mtrx[19]
    """

    __slots__ = "matrix", "flags"

    def __init__(self) -> None:
        self.matrix: Matrix = [[EMPTY for _ in range(HEIGHT)]
                                         for _ in range(WIDTH)]

        # flags invariant: after function using flags returns,
        # flags must be set to False
        self.flags: List[List[bool]] = [[False for _ in range(HEIGHT)]
                                        for _ in range(WIDTH)]

        return

    def load(self, content: str) -> int:
        """
        loads string representation of the content of the board
        :param content: string representation of the content
        :return: 0 if success else -1
        """

        if len(content) != WIDTH * HEIGHT:
            return -1

        for idx, string_fill in enumerate(content):
            if not 47 < ord(string_fill) < 54:  # only numbers 0-5 expected
                return -1

            fill: Fill = ord(string_fill) - ord('0')

            x: int = idx // 10
            y: int = idx % 10

            self.matrix[x][y] = fill

        return 0

    def get_fill(self, coord: Coord) -> Fill:
        """
        get fill of tile at given coord
        :param coord: coord
        :return: -1 if index error else fill of tile at given coord
        """

        x, y = coord

        if (not (0 <= x < WIDTH)) or (not (0 <= y < HEIGHT)):
            return -1  # announce error

        return self.matrix[x][y]

    def set_fill(self, coord: Coord, value: Fill) -> None:
        """
        sets fill associated with given tile to given value, expects valid coord
        :param coord: coord of the tile to set the associated fill of
        :param value: the value that the fill is to be set to
        :return: None
        """

        x: int
        y: int
        x, y = coord
        self.matrix[x][y] = value
        return

    def get_flag(self, coord: Coord) -> bool:
        """
        gets flag associated with given tile, expects valid coord
        :param coord: coord of the tile to get the associated flag of
        :return: flag associated with given tile
        """

        x, y = coord
        return self.flags[x][y]

    def set_flag(self, coord: Coord, value: bool) -> None:
        """
        sets flag associated with given tile to given value, expects valid coord
        :param coord: coord of the tile to set the associated flag of
        :param value: the value that the flag is to be set to
        :return: None
        """

        x: int
        y: int
        x, y = coord
        self.flags[x][y] = value
        return

    def get_patch_rec(self, coord: Coord, expected_fill: Fill, acc: List[Coord]) -> None:
        fill: Fill = self.get_fill(coord)

        if fill != expected_fill:  # catch idx error, tile not of same color
            return

        if self.get_flag(coord):  # check if been there
            return

        self.set_flag(coord, True)  # mark that been there

        acc.append(coord)

        x: int
        y: int
        x, y = coord
        for nxt_coord in [(x, y+1), (x+1, y), (x, y-1), (x-1, y)]:
            self.get_patch_rec(nxt_coord, expected_fill, acc)

    def get_patch(self, coord: Coord) -> List[Coord]:
        """
        get the patch that is affected by clicking on tile with given coord
        :param coord: the coord of the clicked tile
        :return: the affected patch (namely [] if clicked empty tile)
        """
        result: List[Coord] = []

        fill: Fill = self.get_fill(coord)

        if fill != EMPTY and fill != -1:  # patch might be EMPTY or coord invalid
            self.get_patch_rec(coord, fill, result)

        for coord in result:
            self.set_flag(coord, False)  # clean up

        return result

    def erase_patch(self, patch: List[Coord]) -> None:
        """
        sets all the tiles that correspond to coords in patch to EMPTY
        does not check anything, that is up to the caller
        :param patch: the list of tiles (their coords) to be set to EMPTY
        :return: None
        """

        for coord in patch:
            self.set_fill(coord, EMPTY)

    def gravity(self):
        """apply "gravity" to the stones ie in each column, the stones move down"""

        for col in self.matrix:
            col.sort(key=lambda fill: 1 if fill == EMPTY else 0)

    def wind(self):
        """apply "wind" to the columns ie non-empty columns get moved to the left"""
        self.matrix.sort(key=lambda col: 1 if col[0] == EMPTY else 0)

    def click(self, coord: Coord) -> int:
        """
        execute click ie
        if coord param a valid click then delete patch
        and move remaining tiles appropriately
        else announce coord invalid
        :param coord: coord of the clicked tile
        :return: 0 if click executed successfully else -1
        """
        patch: List[Coord] = self.get_patch(coord)

        if len(patch) < 2:  # idx error or is EMPTY or has no neighbors
            return -1

        self.erase_patch(patch)
        self.gravity()
        self.wind()

        return 0  # click executed successfully

    def to_string(self) -> str:
        """
        creates string representation of the board
        format compatible with load()
        :return: generated string representation of the board
        """

        return "".join(["".join([str(fill) for fill in col]) for col in self.matrix])

    def duplicate_matrix(self) -> Matrix:
        return [[fill for fill in col] for col in self.matrix]

    def get_moves(self) -> List[List[Coord]]:
        """
        get list of clickable patches (namely len of each move is > 1)
        :return: list of clickable patches
        """

        moves: List[List[Coord]] = []
        for x in range(WIDTH):
            for y in range(HEIGHT):
                if self.get_flag((x, y)):
                    continue  # already belongs to a move/patch

                this_move: List[Coord] = self.get_patch((x, y))
                for tile in this_move:
                    self.set_flag(tile, True)  # remember these tiles belong to a move

                if len(this_move) < 2:
                    continue

                moves.append(this_move)

        for move in moves:
            for tile in move:
                self.set_flag(tile, False)  # clean up

        return moves

    def is_solved(self) -> bool:
        for x in range(WIDTH):
            for y in range(HEIGHT):
                if self.get_fill((x, y)) != EMPTY:
                    return False

        return True

    def solve(self, verbose: bool, solution: List[Coord]) -> bool:
        if verbose:
            print_board(self)

        if self.is_solved():
            return True  # found a solution here

        aux_board: Board = Board()

        for move in self.get_moves():
            aux_board.matrix = self.duplicate_matrix()
            assert len(move) > 1
            solution.append(move[0])
            aux_board.click(move[0])

            if aux_board.solve(verbose, solution):
                return True  # found a solution in sub-board

            solution.pop()  # no solution using this move

        return False  # no solution of this board


def pic_processor(path: str) -> Optional[str]:
    """
    loads board from its picture located at path
    :param path: path to to-be-loaded-picture
    :return: string representation of the board at the picture
    """

    try:
        pic = Image.open(path, mode='r')
    except FileNotFoundError:
        return None

    pic_width: int
    pic_height: int
    pic_width, pic_height = pic.size

    tile_width: float = pic_width / WIDTH
    fst_tile_x: float = tile_width / 2
    x_coords: List[int] = [int(fst_tile_x + (offset * tile_width)) for offset in range(WIDTH)]

    tile_height: float = pic_height / HEIGHT
    fst_tile_y: float = tile_height / 2
    y_coords: List[int] = [int(fst_tile_y + (offset * tile_height)) for offset in range(HEIGHT)]
    y_coords.reverse()  # to list from bottom to top

    result: List[int] = []

    for x_coord in x_coords:
        for y_coord in y_coords:
            color = pic.getpixel((x_coord, y_coord))

            actual_fill: Fill

            if color == PURPLE_RGB:
                actual_fill = PURPLE
            elif color == MAGENTA_RGB:
                actual_fill = MAGENTA
            elif color == NAVY_RGB:
                actual_fill = NAVY
            elif color == TEAL_RGB:
                actual_fill = TEAL
            elif color == SKY_RGB:
                actual_fill = SKY
            else:
                actual_fill = EMPTY  # todo might be worth checking it matches empty tile

            result.append(actual_fill)

    return "".join([str(fill) for fill in result])


def print_board(board: Board) -> None:
    for weird_y in reversed(range(HEIGHT)):
        for weird_x in range(WIDTH):
            fill: Fill = board.matrix[weird_x][weird_y]
            print(fill if fill != 0 else ' ', end=" ")
        print()


def str_to_coord(str_coord: str) -> Optional[Coord]:
    """
    converts string representation of coord to coord
    :param str_coord: string representation of coord
    :return: coord if valid string representation of coord else None
    """

    x: int
    y: int

    str_x_y: List[str] = str_coord.split(sep=COORD_SEP)
    if len(str_x_y) != 2:
        return None  # expected coordinates separated by COORD_SEP

    try:
        x, y = int(str_x_y[0]), int(str_x_y[1])
    except ValueError:
        return None  # unable to convert

    return x, y


class Session:
    """
    Session class represents users interaction with a board
    """

    __slots__ = "current_board", "past_moves", "future_moves", "past_boards", "future_boards"

    def __init__(self, source: Board):
        self.current_board = source

        # past_moves and past_boards always edited together analogically -> same len()
        # clicking past_boards[i] at past_moves[i] ~> past_boards[i+1]
        # clicking past_boards[-1] at past_moves[-1] ~> current_board
        self.past_moves: List[Coord] = []
        self.past_boards: List[Matrix] = []

        # future_moves and future_boards always edited together analogically -> same len()
        self.future_moves: List[Coord] = []
        self.future_boards: List[Matrix] = []

    def request_click(self, click: Coord) -> int:
        """
        tries to click board at given coord
        if successful then edits the board and history appropriately else fails atomically
        :param click: coord of the requested click
        :return: 0 if success else -1
        """
        matrix_save: Matrix = self.current_board.duplicate_matrix()

        # attempt the click
        if self.current_board.click(click) == -1:
            return -1  # underlying function failed, so does this

        # click successful
        self.past_moves.append(click)
        self.past_boards.append(matrix_save)
        self.future_moves = []
        self.future_boards = []

        return 0  # ok

    def undo(self) -> int:
        """
        undoes the last move if theres a move do undo else fails
        :return: 0 if success else -1
        """

        if not self.past_boards:  # nothing to undo
            return -1

        # shift the boards
        self.future_boards.append(self.current_board.matrix)
        self.current_board.matrix = self.past_boards.pop()

        # shift the moves
        self.future_moves.append(self.past_moves.pop())

        return 0

    def redo(self) -> int:
        """
        redoes the last undo if theres a move to redo else fails
        :return: 0 if success else -1
        """

        if not self.future_moves:  # nothing to redo
            return -1

        # shift the boards
        self.past_boards.append(self.current_board.matrix)
        self.current_board.matrix = self.future_boards.pop()

        # shift the moves
        self.past_moves.append(self.future_moves.pop())

        return 0

    def load(self, string_repre: str) -> int:
        """
        load session from its string representation
        :param string_repre: strign representation of the session
        :return: 0 on success else -1
        """

        split: List[str] = string_repre.split(sep=MOVE_SEP, maxsplit=1)

        content: str = split[0]
        moves: str = split[1]

        matrix_save: Matrix = self.current_board.matrix

        parsed_moves: List[Coord] = []
        for str_coord in ([] if moves == "" else moves.split(sep=MOVE_SEP)):
            parsed_move: Optional[Coord] = str_to_coord(str_coord)

            if parsed_move is None:
                return -1

            parsed_moves.append(str_to_coord(str_coord))

        # load assignment
        if self.current_board.load(content) != 0:
            self.current_board.matrix = matrix_save
            return -1

        # load history
        for move in parsed_moves:
            if self.request_click(move) == -1:
                # invalid move requested
                self.current_board.matrix = matrix_save
                return -1

        return 0  # ok

    def to_string(self) -> str:
        """
        converts current session to string to be saved
        does not save future :( maybe in later versions
        resulting string compatible with the load() function
        :return: string representation of the current session
        """

        res: str

        aux: Matrix = self.current_board.matrix
        self.current_board.matrix = self.past_boards[0] if self.past_boards else aux
        res = self.current_board.to_string()
        self.current_board.matrix = aux

        str_moves: List[str] = [str(x) + COORD_SEP + str(y) for x, y in self.past_moves]

        res += MOVE_SEP + MOVE_SEP.join(str_moves)

        return res


def play_session(session: Session) -> str:
    """
    play given session

    commands:
    intCOORD_SEPint : click this tile
    z : undo
    y : redo
    a verbose : auto-solve; verbose: True | False
    s : save & exit
    h : help

    :param session: Session to be played
    :return: the string representation of the session to be saved
    """

    while True:
        print_board(session.current_board)

        inp: str = input(SESSION_PROMPT)

        if inp == "z":
            print("undo success" if session.undo() == 0 else "undo fail")
            continue

        if inp == "y":
            print("redo success" if session.redo() == 0 else "redo fail")
            continue

        if inp == "a True" or inp == "a False":
            solution: List[Coord] = []

            # todo theres something weird going on in Board.solve() ->
            # todo for now lets use it on a copy in order to not mess up session
            aux_board: Board = Board()
            aux_board.matrix = session.current_board.duplicate_matrix()

            if aux_board.solve(inp == "a True", solution):
                print(f"solution found! {solution}")
            else:
                print("no solution for this board :(")

            continue

        if inp == "s":
            return session.to_string()

        if inp == "h":
            print(PLAY_SESSION_HELP)
            continue

        move: Optional[Coord] = str_to_coord(inp)
        if move is None:
            print("unrecognised command; try again")
            continue

        print(f"requested move: {move}")
        if session.request_click(move) != 0:
            print("invalid coordinates; try again")
        else:
            print(f"played move {move[0]};{move[1]}")


def session_from_file(path: str) -> Optional[Session]:
    """
    load session from path
    :param path: path of the session
    :return: the loaded session if success else None
    """
    str_session: str
    session: Session = Session(Board())

    try:
        with open(path, 'r') as source:
            str_session = source.readline()
    except FileNotFoundError:
        return None

    # print(f"loaded string: \"{str_session}\"")
    return session if session.load(str_session) == 0 else None


def play_session_from_file(path: str) -> int:
    """
    ui for playing a session given path to file where chosen session is stored
    :param path: path of the file containing chosen session
    :return: 0 if success else 1
    """

    session: Session = session_from_file(path)
    if session is None:  # loaded invalid representation of a session
        return -1

    session_result: str = play_session(session)
    with open(path, 'w') as target:
        target.write(session_result)

    return 0


def session_from_assignment(assignment: str, session: str) -> int:
    """
    creates session from assignment
    (no moves so far ie only copies the string representation of assignment to another file)
    :param assignment: assignment path
    :param session: session path
    :return: 0 on success (loaded file is a valid assignment) else -1
    """

    str_session: str

    try:
        with open(assignment, 'r') as source:
            str_session = source.readline() + MOVE_SEP  # MOVE_SEP necessary to indicate no moves yet
    except FileNotFoundError:
        return -1

    if Session(Board()).load(str_session) != 0:
        return -1  # loaded file is a valid assignment

    with open(session, 'w') as target:
        target.write(str_session)

    return 0


def player() -> int:
    """
    player UI

    commands:
    c assignment_path output_path : create session from assignment_path in output_path
    p session_path : play session session_path
    e : exit player interface
    :return: current implementation only returns 0
    """

    inp: str

    while True:
        inp = input(PLAYER_PROMPT)

        if len(inp) < 1:
            print("invalid input")

        if inp[0] == 'c':
            split_input: List[str] = inp.split(' ')  # todo what about filepaths containing ' '

            if len(split_input) != 3:
                print("invalid input")
                continue

            if session_from_assignment(split_input[1], split_input[2]) != 0:
                print("given assignment not valid")
                continue

            print(f"success! session available at: {split_input[2]}")

        elif inp[0] == 'p':
            split_input: List[str] = inp.split(' ')

            if len(split_input) != 2:
                print("invalid input")
                continue

            if play_session_from_file(split_input[1]) != 0:
                print("given session not valid")
                continue

            print(f"successfully played a session at: {split_input[1]}")

        elif inp[0] == 'e':
            if inp != "e":
                print("invalid input")
                continue

            return 0  # exit player interface

        elif inp[0] == 'h':
            if inp != "h":
                print("invalid input")
                continue

            print(PLAYER_HELP)

        else:
            print("invalid input")


def taskmaster() -> int:
    """
    taskmaster UI

    commands:
    l picture_path assignment_path : load assignment from picture
    v session_path : view player session (assignment, moves, final board)
    e : exit taskmaster interface
    :return:
    """

    while True:
        inp: str = input(TASKMASTER_PROMPT)

        if len(inp) < 1:
            print("invalid input")
            continue

        if inp[0] == 'l':
            board: Board = Board()

            split_input: List[str] = inp.split(' ')
            if len(split_input) != 3:
                print("invalid input")
                continue

            str_board: Optional[str] = pic_processor(split_input[1])
            if str_board is None:
                print(f"cannot open file {split_input[1]}")
                continue

            assert board.load(str_board) == 0  # output of pic_processor compatible

            # check with user result ok
            print("loaded board:")
            print_board(board)
            confirmation: str = input(CONFIRM_PROMPT)

            if confirmation != 'y':
                print("loading cancelled")
                continue

            with open(split_input[2], 'w') as target:
                target.write(board.to_string())

        elif inp[0] == 'v':
            split_string: List[str] = inp.split(" ")

            if len(split_string) != 2:
                print("invalid input")
                continue

            session: Optional[Session] = session_from_file(split_string[1])
            if session is None:
                print("could not obtain valid session from given file")
                continue

            print("assignment:")
            assignment: Board = Board()
            assignment.matrix = session.current_board.matrix if len(session.past_boards) == 0 else session.past_boards[0]
            print_board(assignment)
            print("moves:")
            print(session.past_moves)
            print("result:")
            print_board(session.current_board)

        elif inp[0] == 'e':
            if len(inp) != 1:
                print("invalid input")
                continue

            return 0  # exit taskmaster ui

        elif inp[0] == 'h':
            if inp != "h":
                print("invalid input")
                continue

            print(TASKMASTER_HELP)

        else:
            print("invalid input")


def admin_add(login: str, password: str, taskmaster_auth: bool, player_auth: bool) -> int:
    """

    format of the db entry shall be
    "login password taskmaster_auth player_auth"

    login: each character alphanumeric, not empty string; store input directly
    password: each character alphanumeric, not empty string; store input directly
    taskmaster_auth: True ~> "t", False ~> "f"
    player_auth: True ~> "t", False ~> "f"

    :param login: login
    :param password: password
    :param taskmaster_auth: taskmaster authentication
    :param player_auth: player authentication
    :return: 0 = success, 1 = already present, 2 = invalid format
    """

    if not login.isalnum() or not password.isalnum():
        return 2  # invalid format / characters in password or login; only alnum allowed

    with open(USERDB, 'r') as userdb:
        line: str

        while True:
            line = userdb.readline()

            if not line:
                break

            if line.split(' ')[0] == login:
                return 1  # already present

    # input checked, uniqueness checked, lets add
    entry: str = login + USERDB_SEP +\
                 password + USERDB_SEP +\
                 (AUTH_TRUE if taskmaster_auth else AUTH_FALSE) + USERDB_SEP +\
                 (AUTH_TRUE if player_auth else AUTH_FALSE)

    with open(USERDB, 'a') as userdb:
        userdb.write(entry + "\n")

    return 0  # ok


def admin_delete(login: str) -> int:
    """
    remove login user from database (fail if not present)
    :param login: login of the to-be-deleted user
    :return: 0 if success else -1 (no user with such login in database)
    """

    status: int = -1  # not seen user of given login yet

    # todo this does not feel very efficient
    with open(USERDB, "r+") as userdb:
        aux: List[str] = userdb.readlines()
        userdb.seek(0)

        for line in aux:
            if line.split(' ')[0] == login:
                assert status != 0  # this would mean same login multiple times in db
                status = 0  # note that seen & deleted user
                continue

            userdb.write(line)

        userdb.truncate()

    return status


def admin_update(login: str, password: str, taskmaster_auth: bool, player_auth: bool) -> int:
    """
    update data stored about <login> user

    :param login: login of the to-be-updated user
    :param password: new password
    :param taskmaster_auth: new taskmaster (not)authentication
    :param player_auth: new player (not)authentication
    :return: 0 on success else -1 (if user with given login not in database)
    """

    if admin_delete(login) != 0:
        return -1

    # add should not fail now since deleted that
    # also inefficient since no need to check login not in database, todo ? meh
    assert admin_add(login, password, taskmaster_auth, player_auth) == 0
    return 0


def admin_view() -> None:
    print("login\ttaskmaster\tplayer")
    print("--------------------------")
    with open(USERDB, 'r') as userdb:
        while True:
            line: str = userdb.readline()

            if not line:
                return

            split_line: List[str] = line.split(USERDB_SEP)
            print(f"{split_line[0]}\t\t{split_line[2]}\t{split_line[3]}", end="")


def admin_parse(inp: str) -> Optional[Tuple[str, str, bool, bool]]:
    split_input: List[str] = inp.split(" ")

    if len(split_input) != 5:
        print("invalid input")
        return None

    login: str = split_input[1]
    password: str = split_input[2]

    taskmaster_auth: bool
    player_auth: bool

    if split_input[3] == "True":
        taskmaster_auth = True
    elif split_input[3] == "False":
        taskmaster_auth = False
    else:
        print("invalid input")
        return None

    if split_input[4] == "True":
        player_auth = True
    elif split_input[4] == "False":
        player_auth = False
    else:
        print("invalid input")
        return None

    if login in BLACKLIST:
        if taskmaster_auth or player_auth:
            print(f"user {login} is not allowed this authorization")
            return None

    return login, password, taskmaster_auth, player_auth


def admin() -> None:
    """
    admin UI

    commands:
    a login password taskmaster_auth player_auth : add user to the database
    d login : delete user from the database
    u login password taskmaster_auth player_auth : update user
    v : view user database
    e : exit admin UI

    boolean values "True", "False"

    :return:
    """

    while True:
        inp: str = input(ADMIN_PROMPT)

        if not inp:
            print("invalid input")
            continue

        if inp[0] == 'a':
            login: str
            password: str
            taskmaster_auth: bool
            player_auth: bool

            aux: Optional[Tuple[str, str, bool, bool]] = admin_parse(inp)
            if aux is None:
                continue  # printing handled by admin_parse()

            login, password, taskmaster_auth, player_auth = aux

            report: int = admin_add(login, password, taskmaster_auth, player_auth)
            if report == 0:
                print(f"user {login} successfully added to the database")
            elif report == 1:
                print(f"user {login} had already been in database")
            else:
                assert report == 2
                print("invalid format")

        elif inp[0] == 'd':
            split_input: List[str] = inp.split(" ")

            if len(split_input) != 2:
                print("invalid format")
                continue

            login: str = split_input[1]
            if admin_delete(login) == 0:
                print(f"successfully deleted user {login} from the database")
            else:
                print(f"user {login} had not been in the database")

        elif inp[0] == 'u':
            login: str
            password: str
            taskmaster_auth: bool
            player_auth: bool

            aux: Optional[Tuple[str, str, bool, bool]] = admin_parse(inp)
            if aux is None:
                continue  # printing handled by admin_parse()

            login, password, taskmaster_auth, player_auth = aux

            report: int = admin_update(login, password, taskmaster_auth, player_auth)
            if report == 0:
                print(f"user {login} successfully updated")
            else:
                assert report == 1
                print(f"user {login} not in database")

        elif inp[0] == 'v':
            if inp != "v":
                print("invalid input")
                continue

            admin_view()

        elif inp[0] == 'e':
            if inp != "e":
                print("invalid input")
                continue

            return  # exit admin interface

        elif inp[0] == 'h':
            if inp != "h":
                print("invalid input")
                continue

            print(ADMIN_HELP)

        else:
            print("invalid input")


def enter_admin() -> None:
    """
    admin authentication

    commands:
    l : initialize authentication process
    e : exit
    :return:
    """

    login: str = input(ADMIN_LOGIN_PROMPT)
    password: str = input(ADMIN_PASSWORD_PROMPT)

    if login != ADMIN_LOGIN or password != ADMIN_PASSWORD:
        print("access denied")
        return

    # access granted
    admin()
    return


def get_users_auths(login: str, password: str) -> Optional[Tuple[bool, bool]]:
    """
    if user in database and if password correct, return authorization tuple

    :param login: login
    :param password: password
    :return: taskmaster authorization, player authorization
    """

    with open(USERDB, 'r') as userdb:
        while True:
            line: str = userdb.readline()

            if not line:
                return None  # no such login in database

            split_line: List[str] = line.split(' ')
            if login == split_line[0]:
                if password == split_line[1]:
                    return (True if split_line[2] == AUTH_TRUE else False),\
                           (True if split_line[3] == AUTH_TRUE + '\n' else False)
                else:
                    return None  # incorrect password


def enter_taskmaster() -> None:
    """
    authenticate taskmaster, enter if authorized
    :return:
    """

    login: str = input(TASKMASTER_LOGIN_PROMPT)
    password: str = input(TASKMASTER_PASSWORD_PROMPT)

    aux: Optional[Tuple[bool, bool]] = get_users_auths(login, password)
    if aux is None:
        print("incorrect credentials; access denied")
        return

    taskmaster_auth: bool
    taskmaster_auth, _ = aux
    if not taskmaster_auth:
        print(f"user {login} is not authorized")
        return

    # access granted
    taskmaster()
    return


def enter_player():
    """
    authenticate player, enter if authorized
    :return:
    """

    login: str = input(PLAYER_LOGIN_PROMPT)
    password: str = input(PLAYER_PASSWORD_PROMPT)

    aux: Optional[Tuple[bool, bool]] = get_users_auths(login, password)
    if aux is None:
        print("incorrect credentials; access denied")
        return

    player_auth: bool
    _, player_auth = aux
    if not player_auth:
        print(f"user {login} is not authorized")
        return

    # access granted
    player()
    return


def main_menu() -> None:
    """
    stoner main menu

    commands:
    a : admin
    t : taskmaster
    p : player
    e : exit
    h : help

    :return:
    """

    try:
        open(USERDB, 'r')
    except FileNotFoundError:
        with open(USERDB, 'w') as userdb:
            print(f"created user database")

    while True:
        inp: str = input(MENU_PROMPT)

        # print(f"input: \"{inp}\"")

        if inp == "a":
            enter_admin()
        elif inp == "t":
            enter_taskmaster()
        elif inp == "p":
            enter_player()
        elif inp == "e":
            return  # exit stoner
        elif inp == "h":
            print(MENU_HELP)
        else:
            print("invalid input")


if __name__ == '__main__':
    main_menu()

