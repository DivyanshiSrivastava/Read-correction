#!/usr/bin/env python
def read_MSA_to_dict():

	""" Gets MSA alignment from clustalo output, finds start and stop for each
	sequence """

	from Bio import AlignIO
	#alignment = AlignIO.read("out_aln1.clu", "clustal")
	alignment = AlignIO.read(file1, "clustal")
	MSA_len = alignment.get_alignment_length()
	D_curr = dict()

	for record in alignment:
		D_curr[record.id] = [record.seq,0,0,0]
	Seq = D_curr.values()

	for seq in Seq:
		#Start pos = seq[1]
		seq[1] = next((index for index,value in enumerate(seq[0],start =1) if value != '-'), None)
		#End pos = seq[2]
		seq[2] = len(seq[0]) - next((index for index,value in enumerate(reversed(seq[0])) if value != '-'), None)
		#Seq flag, 1 is inside, 0 is outside.
		seq[3] = [0] * (seq[1]-1) + [1] * (seq[2]-seq[1] + 1) + [0] * (len(seq[0]) - seq[2])

	return (Seq,MSA_len) #Can return dict itself, in case we need seq_IDS. Don't think they'll be needed here though.

#So each dict key is the id, and value stores seq, start, end, flag.
#I am treating sequences to start with base 1 ( So 1 - based.)

def get_bases_at_pos():

	""" Retrieves all bases at a single position, only for reads which have
	started and not yet ended, ie. we are inside the read, and returns a list """
	
	(Seq, MSA_len) = read_MSA_to_dict()
	
	Bases_at_pos = [[] for i in range(MSA_len)]

	for i in range(MSA_len):
		for element in Seq:	
			if element[3][i] != 0: #Checking flag
				Bases_at_pos[i].append(element[0][i])

	return Bases_at_pos
#So now I have bases at each position of the MSA for whom the read has started.

def get_cons_per_base(p_list):

	""" Takes a list containing all possible bases, at a single position,
	and returns a single base """

	from operator import itemgetter
	c = dict()
	for item in p_list:
		c[item] = c.get(item, 0) + 1
	
	Max = max(c.iteritems(), key=itemgetter(1))
	
	#Checking for non-unique maximum	
	keys = c.values()
	uniq = 0
	for key in keys:
		if key == Max[1]:
			uniq = uniq + 1

	if uniq == 1:
		#There is a unique maximum
		return Max[0]
	else:
		return "N" # Modify this to be more precise.
#Getting a per base consensus.

def construct_cons():

	""" Get final cons sequence! """
	
	allseq_list = get_bases_at_pos()
	final_list= []
	for element in allseq_list:
		final_list.append(get_cons_per_base(element))
		#Error Checking
	return final_list


def write_to_file(P_consensus):

	#fi = open("conses.fa", "w+")
	fi = open(file2, "a")
	print "Name of the file: ", fi.name
	fi.write('\n>Cons_seq\n')
	for element in P_consensus:
		if element == "-":
			pass
		else:
			fi.write(element)
	fi.close()


import sys
file1 = sys.argv[1]
file2 = sys.argv[2]
consensus = construct_cons()
write_to_file(consensus)

#Done.



