import copy

try:
    from Main_Files.Logic import Board, Turn
except ModuleNotFoundError:
    from willse_backgammon.Main_Files.Logic import Board, Turn

def Full_Run(ActiveBoard: Board, ActiveTurn: Turn):
    pipsList = []
    ActiveTurn.updatePossibleMovesStandardFormat(ActiveBoard)

    for Moves in ActiveTurn.current_possible_moves:
        algoBoard = copy.deepcopy(ActiveBoard)
        algoBoard.makeMoves(Moves, ActiveTurn.player)
        algoBoard.updatePip()
        pipDiff = (algoBoard.pip[1] - algoBoard.pip[0]) if ActiveTurn.player == 1 else (
                    algoBoard.pip[0] - algoBoard.pip[1])
        pipsList.append(pipDiff)

    if len(pipsList) == 0:
        return []

    maxPipDiff = max(pipsList)
    indexOfMove = pipsList.index(maxPipDiff)

    return ActiveTurn.current_possible_moves[indexOfMove]
