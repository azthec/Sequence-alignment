import offline_needleman
import emboss_align
import easygui
import multiprocessing


def is_int(s):
    """
    Test if object is an int.

    :param s:
    :return: True if object can be cast to an int, False if not.
    """
    try:
        int(s)
        return True
    except ValueError:
        return False


def timebox(msg):
    """
    Creates easygui msgbox to be launched by separate process can be killed.

    :param msg:
    """
    easygui.msgbox(msg)


if __name__ == "__main__":
    try:
        msg = """
        Welcome to our dynamic alignment program.

        This program allows you to align two strings, that may represent proteins, genes, or even just two strings you \
        want to calculate the indel distance of.

        Global alignment calculated offline using Needleman-Wunsch.

        Various alignment types calculated via the EMBOSS restful API hosted by EBI.

        Rui Balau & Simon Afonso - March 2018


        """
        title = "Dynamic Alignment"
        choices = ["Offline global alignment (Needleman-Wunsch)", "Various online alignments (EMBOSS)"]
        choice = easygui.choicebox(msg, title, choices)

        if choice == choices[0]:
            msg = "Return one of the closest alignments or all closest alignments?"
            choices = ["One", "All"]
            choice = easygui.choicebox(msg, title, choices)
            if choice == choices[0]:
                traceback = offline_needleman.TRACEBACK_SINGLE_PATH
            elif choice == choices[1]:
                traceback = offline_needleman.TRACEBACK_MULTI_PATH
            else:
                print("User canceled the operation.")
                exit(1)

            msg = "Choose the gap penalty type to use."
            gap_choices = ["Linear", "Affine"]
            gap_choice = easygui.choicebox(msg, title, gap_choices)

            if gap_choice == gap_choices[0]:
                fieldNames = ["Sequence 1", "Sequence 2", "Match bonus", "Mismatch penalty", "Gap penalty"]
            elif gap_choice == gap_choices[1]:
                fieldNames = ["Sequence 1", "Sequence 2", "Match bonus", "Mismatch penalty", "Gap penalty",
                              "Gap extension penalty"]
            else:
                print("User canceled the operation.")
                exit(1)

            msg = """Enter arguments for Needleman-Wunsch with appropriate gap parameters. Customarily match is a \
            positive integer and mismatch and gap penalties are negative integers.\n\n Do not enter fasta sequence \
            headers."""
            
            fieldValues = []  # we start with blanks for the values
            fieldValues = easygui.multenterbox(msg,title, fieldNames)

            # make sure that none of the fields was left blank
            while 1:
                if fieldValues is None: break
                errmsg = ""
                for i in range(len(fieldNames)):
                    if fieldValues[i].strip() == "":
                        errmsg = errmsg + ('"%s" is a required field.\n\n' % fieldNames[i])
                    elif not is_int(fieldValues[i]):
                        if i >= 2:
                            errmsg = errmsg + ('"%s" is not an integer.\n\n' % fieldNames[i])
                if errmsg == "":
                    break  # no problems found
                fieldValues = easygui.multenterbox(errmsg, title, fieldNames, fieldValues)

            if fieldValues is None:
                print("User canceled the operation.")
                exit(1)

            # process = multiprocessing.Process(target=timebox, args=('Running...',))
            # process.start()
            
            if gap_choice == gap_choices[0]:
                fieldValues[0] = ''.join(e for e in fieldValues[0] if e.isalnum())
                fieldValues[1] = ''.join(e for e in fieldValues[1] if e.isalnum())
                result1, result2 = offline_needleman.needleman_wunsch_linear(fieldValues[0], fieldValues[1], traceback,
                                                                             int(fieldValues[2]), int(fieldValues[3]),
                                                                             int(fieldValues[4]))
            elif gap_choice == gap_choices[1]:
                fieldValues[0] = ''.join(e for e in fieldValues[0] if e.isalnum())
                fieldValues[1] = ''.join(e for e in fieldValues[1] if e.isalnum())
                result1, result2 = offline_needleman.needleman_wunsch_affine(fieldValues[0], fieldValues[1], traceback,
                                                                             int(fieldValues[2]), int(fieldValues[3]),
                                                                             int(fieldValues[4]), int(fieldValues[5]))
            else:
                # process.terminate()
                print("User canceled the operation.")
                exit(1)

            # process.terminate()

            text = ''
            n_results = len(result1)
            for i in range(n_results):
                text += result1[i] + '\n' + result2[i] + '\n\n\n'
            easygui.codebox("Aligned sequences: ", "Aligned Sequences", text)

        elif choice == choices[1]:
            # EMBOSS implementation

            msg = "Please select which EMBOSS algorithm implementation you wish to use."
            title = "EMBOSS Alignment"
            choices = ["Smith-Waterman", "Needleman-Wunsch", "Needleman-Wunsch (Stretcher Modification)",
                       "Matcher (LALIGN based)"]
            choice = easygui.choicebox(msg, title, choices)

            if choice not in choices:
                print("User canceled the operation.")
                exit(1)

            msg = """Please enter the sequences to align.\n\nPer EMBOSS only alphabetical characters allowed. \
            \n\nDo not include FASTA headers."""
            fieldNames = ["Sequence 1", "Sequence 2"]
            fieldValues = []  # we start with blanks for the values
            fieldValues = easygui.multenterbox(msg, title, fieldNames)

            # make sure that none of the fields was left blank
            while 1:
                if fieldValues is None: break
                errmsg = ""

                for i in range(len(fieldNames)):
                    if fieldValues[i].strip() == "":
                        errmsg = errmsg + ('"%s" is a required field.\n\n' % fieldNames[i])

                fieldValues[0] = fieldValues[0].upper().replace("\n", "")
                fieldValues[1] = fieldValues[1].upper().replace("\n", "")
                valid_dna = "ACGT"
                valid_protein = "ARNDCQEGHILKMFPSTWYV"
                seqa_isDNA = all(i in valid_dna for i in fieldValues[0])
                seqa_isAMIN = all(i in valid_protein for i in fieldValues[0])
                if not (seqa_isDNA or seqa_isAMIN):  # check if a is dna or amin
                    errmsg = errmsg + ('"%s" is neither DNA or Protein sequence.\n\n' % fieldNames[0])
                seqb_isDNA = all(i in valid_dna for i in fieldValues[1]) 
                seqb_isAMIN = all(i in valid_protein for i in fieldValues[1])

                if not (seqb_isDNA or seqb_isAMIN):  # check if b is dna or amin
                    errmsg = errmsg + ('"%s" is neither DNA or Protein sequence.\n\n' % fieldNames[1])
                if not seqa_isAMIN == seqb_isAMIN: # check if one is dna and another prot
                    errmsg = errmsg + "Both sequences must be either DNA or Proteins.\n\n"

                if errmsg == "":
                    break #  no problems found
                fieldValues = easygui.multenterbox(errmsg, title, fieldNames, fieldValues)
            
            if fieldValues is None:
                print("User canceled the operation.")
                exit(1)

            if seqa_isAMIN and seqb_isAMIN:
                seq_type = 'protein'
            else:
                seq_type = 'dna'

            # process = multiprocessing.Process(target=timebox, args=('Awaiting reply.',))
            # process.start()

            if choice == choices[0]:
                text = emboss_align.emboss_smith_waterman(fieldValues[0], fieldValues[1], seq_type)
            elif choice == choices[1]:
                text = emboss_align.emboss_needleman_wunsch(fieldValues[0], fieldValues[1], seq_type)
            elif choice == choices[2]:
                text = emboss_align.emboss_stretcher(fieldValues[0], fieldValues[1], seq_type)
            else:
                text = emboss_align.emboss_matcher(fieldValues[0], fieldValues[1], seq_type)

            # process.terminate()

            easygui.codebox("Aligned sequences: ", "Aligned Sequences", text)

        else:
            print("User canceled the operation.")
            exit(1)

    except:
        easygui.exceptionbox()