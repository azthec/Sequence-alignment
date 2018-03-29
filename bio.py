


def protein():

	import requests

	url = "https://blast.ncbi.nlm.nih.gov/Blast.cgi?PAGE=Proteins&PROGRAM=blastp&BLAST_PROGRAMS=blastp&PAGE_TYPE=BlastSearch&BLAST_SPEC=blast2seq"

	headers = {
    	'content-type': "application/json",
    	'x-apikey': "560bd47058e7ab1b2648f4e7",
    	'cache-control': "no-cache"
    	}

	response = requests.request("GET", url, headers=headers)

	print(response.text)

def gene():

	import requests

	url = "https://blast.ncbi.nlm.nih.gov/Blast.cgi?PAGE_TYPE=BlastSearch&BLAST_SPEC=blast2seq&LINK_LOC=align2seq"

	headers = {
    	'content-type': "application/json",
    	'x-apikey': "560bd47058e7ab1b2648f4e7",
    	'cache-control': "no-cache"
    	}

	response = requests.request("GET", url, headers=headers)

	print(response.text)

def main():
	
	user_input = input("Insert 1 for Protein or 2 for Nucleotide\n")
	
	
	if user_input == '1':
		protein()

	else: gene()

main()

