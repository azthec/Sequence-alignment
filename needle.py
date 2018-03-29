import numpy as np
import pprint

DEBUG = 1

ORIGIN = -1
DIAGONAL = 0
VERTICAL = 1
HORIZONTAL = 2

TRACEBACK_SINGLE_PATH = 95
TRACEBACK_MULTI_PATH = 68

class Point:
    def __init__(self, score, paths):
        self.score = score
        self.paths = paths

    # repr for debugging prints
    def __repr__(self):
        return str(self.score)
        #return str(self.paths[0])

def calculate_paths_linear(str1, str2, match, mismatch, gap, i, j, v_matrix):
    if str1[j-1] == str2[i-1]:
        diagonal_score = v_matrix[i-1][j-1].score + match
    else:
        diagonal_score = v_matrix[i-1][j-1].score + mismatch
    vertical_score = v_matrix[i-1][j].score + gap
    horizontal_score = v_matrix[i][j-1].score + gap
    
    max_score = max(horizontal_score, vertical_score, diagonal_score)
    paths = []
    if diagonal_score == max_score:
        paths.append(DIAGONAL)
    if vertical_score == max_score:
        paths.append(VERTICAL)
    if horizontal_score == max_score:
        paths.append(HORIZONTAL)
    return max_score, paths

# gap + gap_extension * gap_len
# gap is known as the gap opening penalty
# gap_extension the gap extension penalty
def calculate_paths_affine(str1, str2, match, mismatch, gap, gap_extension, i, j, v_matrix):
    if str1[j-1] == str2[i-1]:
        diagonal_score = v_matrix[i-1][j-1].score + match
    else:
        diagonal_score = v_matrix[i-1][j-1].score + mismatch
    if v_matrix[i-1][j].paths[0] == VERTICAL:
        # vertical gap already exists
        vertical_score = v_matrix[i-1][j].score + gap_extension
    else:
        # new vertical gap
        vertical_score = v_matrix[i-1][j].score + gap
    if v_matrix[i][j-1].paths[0] == HORIZONTAL:
        # horizontal gap already exists
        horizontal_score = v_matrix[i][j-1].score + gap_extension
    else:
        # new horizontal gap
        horizontal_score = v_matrix[i][j-1].score + gap
    
    max_score = max(horizontal_score, vertical_score, diagonal_score)
    paths = []
    if diagonal_score == max_score:
        paths.append(DIAGONAL)
    if vertical_score == max_score:
        paths.append(VERTICAL)
    if horizontal_score == max_score:
        paths.append(HORIZONTAL)
    return max_score, paths

def traceback_static(str1, str2, m, n, v_matrix):
    res1 = ''
    res2 = ''
    while(m!=0 or n!=0): # iterate until we are at root
        path = v_matrix[m][n].paths[0] # iterate over the first path in the point
        if path == DIAGONAL:
            res1 += str1[n-1]
            res2 += str2[m-1]
            n -= 1
            m -= 1
        elif path == VERTICAL:
            res1 += '-'
            res2 += str2[m-1]
            m -= 1
        elif path == HORIZONTAL:
            res1 += str1[n-1]
            res2 += '-'
            n -= 1
    return res1[::-1], res2[::-1] # reverse and return the strings


def traceback_multiple(str1, str2, m, n, v_matrix):
    result1 = []
    result2 = []
    for path in v_matrix[m][n].paths: # iterate over each path to this point
        prefix1 = ''
        prefix2 = ''
        suffix1 = []
        suffix2 = []
        if path == DIAGONAL:
            prefix1 += str1[n-1]
            prefix2 += str2[m-1]
            suffix1, suffix2 = traceback_multiple(str1, str2, m-1, n-1, v_matrix)
        elif path == VERTICAL:
            prefix1 += '-'
            prefix2 += str2[m-1]
            suffix1, suffix2 = traceback_multiple(str1, str2, m-1, n, v_matrix)
        elif path == HORIZONTAL:
            prefix1 += str1[n-1]
            prefix2 += '-'
            suffix1, suffix2 = traceback_multiple(str1, str2, m, n-1, v_matrix)
        elif path == ORIGIN:
            prefix1 = ''
            prefix2 = ''
            result1.append(prefix1)
            result2.append(prefix2)

        for suffix in suffix1:
            result1.append(prefix1+suffix)
        for suffix in suffix2:
            result2.append(prefix2+suffix)
    return result1, result2

def traceback(str1,str2, traceback_type, m, n, v_matrix):
    result1 = []
    result2 = []
    if traceback_type == TRACEBACK_SINGLE_PATH:
        res1, res2 = traceback_static(str1, str2, m-1, n-1, v_matrix)
        result1.append(res1)
        result2.append(res2)
    elif traceback_type == TRACEBACK_MULTI_PATH:
        res1, res2 = traceback_multiple(str1, str2, m-1, n-1, v_matrix)
        for elem in res1:
            result1.append(elem[::-1])
        for elem in res2:
            result2.append(elem[::-1])
    else:
        print("Invalid traceback_type: {}".format(traceback_type))
        exit(1)
        
    if DEBUG == 1:
        pp = pprint.PrettyPrinter(width=len(str1), compact=True)
        pp.pprint(np.matrix(v_matrix))

    return result1, result2

def needleman_wunsch_linear(str1, str2, traceback_type,
                             match, mismatch, gap):
    n = len(str1) + 1 # +1 on each for empty string origin
    m = len(str2) + 1 

    # object allows us to store our custom points
    v_matrix = np.zeros((m, n), dtype=object)

    # initialize origin
    v_matrix[0][0] = Point(0,[ORIGIN])
    # initialize column 0
    for i in range(1, m):
        v_matrix[i][0] = Point(gap*i,[VERTICAL])
    # initialize row 0
    for i in range(1, n):
        v_matrix[0][i] = Point(gap*i,[HORIZONTAL])

    for i in range(1,m):
        for j in range(1,n):
            score, paths = calculate_paths_linear(str1, str2, match, mismatch, gap,
                                            i, j, v_matrix)
            v_matrix[i][j] = Point(score, paths)

    # traceback and return
    return traceback(str1,str2, traceback_type, m, n, v_matrix)


def needleman_wunsch_affine(str1, str2, traceback_type, 
                             match, mismatch, gap, gap_extension):
    n = len(str1) + 1 # +1 on each for empty string origin
    m = len(str2) + 1 

    # object allows us to store our custom points
    v_matrix = np.zeros((m, n), dtype=object)

    # initialize origin
    v_matrix[0][0] = Point(0,[ORIGIN])
    # initialize column 0
    for i in range(1, m):
        v_matrix[i][0] = Point(gap + gap_extension*(i-1),[VERTICAL])
    # initialize row 0
    for i in range(1, n):
        v_matrix[0][i] = Point(gap + gap_extension*(i-1),[HORIZONTAL])

    for i in range(1,m):
        for j in range(1,n):
            score, paths = calculate_paths_affine(str1, str2, match, mismatch, gap, gap_extension,
                                            i, j, v_matrix)
            v_matrix[i][j] = Point(score, paths)

    # traceback and return
    return traceback(str1,str2, traceback_type, m, n, v_matrix)

# print(needleman_wunsch_linear('ATTGACCTGA', 'ATCCTGA', TRACEBACK_MULTI_PATH, 1, -1, -2))
# print(needleman_wunsch_affine('ATTGACCTGA', 'ATCCTGA', TRACEBACK_SINGLE_PATH, 1, -1, -2, -1))
# print(needleman_wunsch_affine('ATTGACCTGA', 'ATCCTGA', TRACEBACK_MULTI_PATH, 1, -1, -2, -1))
