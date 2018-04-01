import needle
import easygui

def isInt(s):
    try: 
        int(s)
        return True
    except ValueError:
        return False

try:
    msg ="""
    Welcome to our dynamic alignment program.

    This program allows you to align two strings, that may represent proteins, genes, or even just two strings you want to calculate the indel distance of.

    The program allows for global alignment calculated offline using Needleman-Wunsch, it also allows for local aligment calculated via the BLAST restful API hosted by NCBI.

    The offline global aligment can calculate only one or all paths and use a linear or affine gap penalty.

    Rui Balau & Simon Afonso - March 2018


    """
    title = "Dynamic Alignment"
    choices = ["Offline global aligment (Needleman-Wunsch)", "Online local aligment (BLAST@NCBI)"]
    choice = easygui.choicebox(msg, title, choices)

    if choice == choices[0]:
        msg = "Return one of the closest alignments or all closest alignments?"
        choices = ["One", "All"]
        choice = easygui.choicebox(msg, title, choices)
        if choice == choices[0]:
            traceback = needle.TRACEBACK_SINGLE_PATH
        elif choice == choices[1]:
            traceback = needle.TRACEBACK_MULTI_PATH
        else:
            print("User canceled the operation.")
            exit(1)

        msg = "Use linear or affine gap penalty?"
        gap_choices = ["Linear", "Affine"]
        gap_choice = easygui.choicebox(msg, title, gap_choices)


        msg = "Enter Needleman-Wunsch with appropriate gap parameters, customarily match is a positive integer and mismatch and gap penalties are negative integers.\n\n Do not enter fasta sequence headers."
        if gap_choice == gap_choices[0]:
            fieldNames = ["Sequence 1", "Sequence 2", "Match bonus", "Mismatch penalty", "Gap penalty"]
        elif gap_choice == gap_choices[1]:
            fieldNames = ["Sequence 1", "Sequence 2", "Match bonus", "Mismatch penalty", "Gap penalty", "Gap extension penalty"]
        else:
            print("User canceled the operation.")
            exit(1)
        fieldValues = []  # we start with blanks for the values
        fieldValues = easygui.multenterbox(msg,title, fieldNames)

        # make sure that none of the fields was left blank
        while 1:
            if fieldValues == None: break
            errmsg = ""
            for i in range(len(fieldNames)):
                if fieldValues[i].strip() == "":
                    errmsg = errmsg + ('"%s" is a required field.\n\n' % fieldNames[i])
                elif not isInt(fieldValues[i]):
                    if i >= 2:
                        errmsg = errmsg + ('"%s" is not an integer.\n\n' % fieldNames[i])
            if errmsg == "": break # no problems found
            fieldValues = easygui.multenterbox(errmsg, title, fieldNames, fieldValues)
        
        
        if fieldValues == None:
            print("User canceled the operation.")
            exit(1)

        # print("Reply was: {}".format(fieldValues))
        if gap_choice == gap_choices[0]:
            fieldValues[0] = ''.join(e for e in fieldValues[0] if e.isalnum())
            fieldValues[1] = ''.join(e for e in fieldValues[1] if e.isalnum())
            result1, result2 = needle.needleman_wunsch_linear(fieldValues[0], fieldValues[1], traceback, int(fieldValues[2]), int(fieldValues[3]), int(fieldValues[4]))
        elif gap_choice == gap_choices[1]:
            fieldValues[0] = ''.join(e for e in fieldValues[0] if e.isalnum())
            fieldValues[1] = ''.join(e for e in fieldValues[1] if e.isalnum())
            result1, result2 = needle.needleman_wunsch_affine(fieldValues[0], fieldValues[1], traceback, int(fieldValues[2]), int(fieldValues[3]), int(fieldValues[4]), int(fieldValues[5]))
        else:
            print("User canceled the operation.")
            exit(1)

        text = ''
        n_results = len(result1)
        for i in range(n_results):
            text += result1[i] + '\n' + result2[i] + '\n\n\n'
        easygui.codebox("Aligned sequences: ", "Aligned Sequences" ,text)

    elif choice == choices[1]:
        # TODO implement choices for BLAST
        pass
    else:
        print("User canceled the operation.")
        exit(1)
except:
    easygui.exceptionbox()