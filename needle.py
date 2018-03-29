import numpy as np
import pprint
from string import *

ORIGIN = -1
DIAGONAL = 0
VERTICAL = 1
HORIZONTAL = 2

class Point:
    def __init__(self, score, paths):
        self.score = score
        self.paths = paths

    def __repr__(self):
        return str(self.score)
        # return str(self.paths[0])


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

def calculate_paths_affine(str1, str2, match, mismatch, gap, i, j, v_matrix):
    pass

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

    return res1[::-1], res2[::-1] # reverse the strings


def traceback_multiple():
    res1 = ''
    res2 = ''
    while(m!=0 or n!=0): # iterate until we are at root
        for path in v_matrix[m][n].paths: # iterate over each path to this point
            pass
    return res1[::-1], res2[::-1]

# gap = -2, mismatch = -1, match = 1
#     _ | a | b | c | g | e
# _ | 0 | -2| -4| -6| -8|-10
# a | -2| 1 | -1| -3| -5| -7
# b | -4| -1| 2 | 0 | -2| -4
# c | -6| -3| 0 | 3 | 1 | -1
# d | -8| -5| -2| 1 | 2 | 0
# e |-10| -7| -4| -1| 0 | 3

# TODO affine gap | A + B * L
# A is known as the gap opening penalty
# B the gap extension penalty
# L the length of the gap
def needleman_wunsch_linear(str1, str2, 
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
            score, paths = calculate_paths_linear(str1, str2, 
                             match, mismatch, gap, i, j, v_matrix)
            v_matrix[i][j] = Point(score, paths)

    res1, res2 = traceback_static(str1, str2, m-1, n-1, v_matrix)
    print(res1)
    print(res2)
    pp = pprint.PrettyPrinter(width=len(str1), compact=True)
    pp.pprint(np.matrix(v_matrix))

needleman_wunsch_linear('abcde','abcdef',1,-1,-2)