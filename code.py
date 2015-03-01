import sys
import random
import signal
import time


infinite = 9999999999
#Timer handler, helper function




class TimedOutExc(Exception):
        pass

def handler(signum, frame):
    #print 'Signal handler called with signal', signum
    raise TimedOutExc()


class Manual_player:
	def __init__(self):
		pass
	def move(self, temp_board, temp_block, old_move, flag):
		print 'Enter your move: <format:row column> (you\'re playing with', flag + ")"	
		mvp = raw_input()
		mvp = mvp.split()
		return (int(mvp[0]), int(mvp[1]))
		

class Player1:
	
	def __init__(self):
		pass

	def move(self,temp_board,temp_block,old_move,flag):
#		while(1):
#			pass
		for_corner = [0,2,3,5,6,8]

		#List of permitted blocks, based on old move.
		blocks_allowed  = []

		if old_move[0] in for_corner and old_move[1] in for_corner:
			## we will have 3 representative blocks, to choose from

			if old_move[0] % 3 == 0 and old_move[1] % 3 == 0:
				## top left 3 blocks are allowed
				blocks_allowed = [0, 1, 3]
			elif old_move[0] % 3 == 0 and old_move[1] in [2, 5, 8]:
				## top right 3 blocks are allowed
				blocks_allowed = [1,2,5]
			elif old_move[0] in [2,5, 8] and old_move[1] % 3 == 0:
				## bottom left 3 blocks are allowed
				blocks_allowed  = [3,6,7]
			elif old_move[0] in [2,5,8] and old_move[1] in [2,5,8]:
				### bottom right 3 blocks are allowed
				blocks_allowed = [5,7,8]
			else:
				print "SOMETHING REALLY WEIRD HAPPENED!"
				sys.exit(1)
		else:
		#### we will have only 1 block to choose from (or maybe NONE of them, which calls for a free move)
			if old_move[0] % 3 == 0 and old_move[1] in [1,4,7]:
				## upper-center block
				blocks_allowed = [1]
	
			elif old_move[0] in [1,4,7] and old_move[1] % 3 == 0:
				## middle-left block
				blocks_allowed = [3]
		
			elif old_move[0] in [2,5,8] and old_move[1] in [1,4,7]:
				## lower-center block
				blocks_allowed = [7]

			elif old_move[0] in [1,4,7] and old_move[1] in [2,5,8]:
				## middle-right block
				blocks_allowed = [5]
			elif old_move[0] in [1,4,7] and old_move[1] in [1,4,7]:
				blocks_allowed = [4]

		for i in reversed(blocks_allowed):
				if temp_block[i] != '-':
					blocks_allowed.remove(i)
	# We get all the empty cells in allowed blocks. If they're all full, we get all the empty cells in the entire board.
		
		cells = get_empty_out_of(temp_board, blocks_allowed,temp_block)
		

	#code to get all possible blocks allowed for the next move
	

		if(blocks_allowed == []):
			for i in range(9):
				if(temp_block[i]=='-'):
					blocks_allowed.append(i)
		

		if(old_move[0]==-1 and old_move[1]==-1):
			blocks_allowed=[0,1,2,3,4,5,6,7,8]

		print "blocks_allowed"
		for k in blocks_allowed:
			print k,
		selected_block = self.blockselect(temp_block , flag , blocks_allowed)
		print selected_block
#		time.sleep(3)		
		
		print "I returned from selectCell"
		
		ret = self.selectCell(temp_board , temp_block , selected_block , flag)
		print ret
		print "MOVE PRNTED"
#		time.sleep(2)		
		#return self.selectCell(temp_board , temp_block , selected_block , flag)
		print print_lists(temp_board , temp_block)
		return ret
		return cells[random.randrange(len(cells))]	


	def selectCell(self , temp_board , block_stat , block_selected , flag):
		prev = '-'
		block = ['-','-','-','-','-','-','-','-','-']
		move_selected = 0
		r_start = (block_selected / 3) * 3
		c_start = (block_selected % 3) * 3 
		c = 0
		for i in range(r_start , r_start+3):
			for j in range(c_start , c_start+3):
				block[c] = temp_board[i][j]
				c = c+1
		print "BLOCK"
		print block
		utility = -1*infinite

		nextBlocks = []

		if(flag == 'x'):
			for i in range(9):
				if(block[i]=='-'):
					block[i] = 'x'
					prev = block_stat[i]
					hv1 = self.getHeuristic(block , i , block_stat ,  flag , 1)
					temp_board[r_start + (i%3)][c_start + (i/3)] = 'x'

										
					nextBlocks = self.getNextBlocks(temp_board , block_stat  , (r_start + (i%3) , c_start + (i/3) ), 'o')
					##print "nextBlocks"
					#for k in nextBlocks:
					#	print k

					'''
					for k in nextBlocks:
						
						#print "K"
						#print k
						
						t = ['-','-','-','-','-','-','-','-','-']
						t_r_start = (k / 3) * 3
						t_c_start = (k % 3) * 3 
						
						#print "(k/3) * 3"
						#print (k / 3) * 3
						#print "(k % 3) * 3 "
						#print (k % 3) * 3 
						
						c = 0
						for g in range(t_r_start , t_r_start+3):
							for f in range(t_c_start , t_c_start+3):
								t[c] = temp_board[g][f]
								c = c+1								

						hv2 = self.getBlockValue(t,'o')
						if((hv1 - hv2) > utility):
							print "HHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHH"	
							utility = (hv1 - hv2)
							move_selected = i								

					'''		
					hv2 = self.getHeuristic(block, i , block_stat , 'x' , 0)
					if((hv1 - hv2) > utility):	
						utility = (hv1 - hv2)
						move_selected = i
					#'''
					block[i] = '-'	
					

					temp_board[r_start + (i%3)][c_start + (i/3)] = '-'
					block_stat[i] = prev
				

					#if the block is won update temp_block , doing this in heuristic function
					#this is to be done for all the available cells of 'o'
					
					hv2 = self.getHeuristic(block, i , block_stat , 'o' , 0)
					if((hv1 - hv2) > utility):	
						utility = (hv1 - hv2)
						move_selected = i
					block[i] = '-'	
					

					temp_board[r_start + (i%3)][c_start + (i/3)] = '-'
					block_stat[i] = prev


		if(flag == 'o'):
			for i in range(9):
				if(block[i]=='-'):
					prev = block_stat[i]
					block[i] = 'o'
					hv1 = self.getHeuristic(block , i , block_stat ,  flag , 1)
					temp_board[r_start + (i%3)][c_start + (i/3)] = 'o'
					print "FLAG"
					print_lists(temp_board , block_stat)
					#if the block is won update temp_block , doing this in heuristic function
					#this is to be done for all the available cells of 'o'
					
					nextBlocks = self.getNextBlocks(temp_board , block_stat  , (r_start + (i%3) , c_start + (i/3) ), 'x')
					##print "nextBlocks"
					#for k in nextBlocks:
					#	print k

					'''
					for k in nextBlocks:
						
						#print "K"
						#print k
						
						t = ['-','-','-','-','-','-','-','-','-']
						t_r_start = (k / 3) * 3
						t_c_start = (k % 3) * 3 
						
						#print "(k/3) * 3"
						#print (k / 3) * 3
						#print "(k % 3) * 3 "
						#print (k % 3) * 3 
						
						c = 0
						for g in range(t_r_start , t_r_start+3):
							for f in range(t_c_start , t_c_start+3):
						
						#		print "CAUSE"
						#		print g , 
						#		print f
						
								t[c] = temp_board[g][f]
								c = c+1																
						hv2 = self.getBlockValue(t,'x')
						if((hv1 - hv2) > utility):
							print "HHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHH"	
							utility = (hv1 - hv2)
							move_selected = i								

					'''		
					hv2 = self.getHeuristic(block, i , block_stat , 'x' , 0)
					if((hv1 - hv2) > utility):	
						utility = (hv1 - hv2)
						move_selected = i
					#'''
					block[i] = '-'	
					

					temp_board[r_start + (i%3)][c_start + (i/3)] = '-'
					block_stat[i] = prev
		print "MY MOVE"			
		print (move_selected/3+(block_selected/3)*3,move_selected%3+(block_selected%3)*3)						
		return (move_selected/3+(block_selected/3)*3,move_selected%3+(block_selected%3)*3)			


	def getNextBlocks(self , temp_board , block_stat  , old_move , flag):
		for_corner = [0,2,3,5,6,8]

		#List of permitted blocks, based on old move.
		blocks_allowed  = []

		if old_move[0] in for_corner and old_move[1] in for_corner:
			## we will have 3 representative blocks, to choose from

			if old_move[0] % 3 == 0 and old_move[1] % 3 == 0:
				## top left 3 blocks are allowed
				blocks_allowed = [0, 1, 3]
			elif old_move[0] % 3 == 0 and old_move[1] in [2, 5, 8]:
				## top right 3 blocks are allowed
				blocks_allowed = [1,2,5]
			elif old_move[0] in [2,5, 8] and old_move[1] % 3 == 0:
				## bottom left 3 blocks are allowed
				blocks_allowed  = [3,6,7]
			elif old_move[0] in [2,5,8] and old_move[1] in [2,5,8]:
				### bottom right 3 blocks are allowed
				blocks_allowed = [5,7,8]
			else:
				print "SOMETHING REALLY WEIRD HAPPENED!"
				sys.exit(1)
		else:
		#### we will have only 1 block to choose from (or maybe NONE of them, which calls for a free move)
			if old_move[0] % 3 == 0 and old_move[1] in [1,4,7]:
				## upper-center block
				blocks_allowed = [1]
	
			elif old_move[0] in [1,4,7] and old_move[1] % 3 == 0:
				## middle-left block
				blocks_allowed = [3]
		
			elif old_move[0] in [2,5,8] and old_move[1] in [1,4,7]:
				## lower-center block
				blocks_allowed = [7]

			elif old_move[0] in [1,4,7] and old_move[1] in [2,5,8]:
				## middle-right block
				blocks_allowed = [5]
			elif old_move[0] in [1,4,7] and old_move[1] in [1,4,7]:
				blocks_allowed = [4]

		for i in reversed(blocks_allowed):
				if block_stat[i] != '-':
					blocks_allowed.remove(i)
	# We get all the empty cells in allowed blocks. If they're all full, we get all the empty cells in the entire board.
		
		cells = get_empty_out_of(temp_board, blocks_allowed,block_stat)
		

	#code to get all possible blocks allowed for the next move
	

		if(blocks_allowed == []):
			for i in range(9):
				if(block_stat[i]=='-'):
					blocks_allowed.append(i)
		
		return blocks_allowed			


		
	def blockselect(self , temp_block , flag , blocks_allowed):
			utility = -1 * infinite
			if(flag == 'x'):
				for i in blocks_allowed:
					if(temp_block[i]=='-'):
						temp_block[i] = flag
						heuristic_value_f  = self.getBlockValue(temp_block , flag)
						heuristic_value_nf = self.getBlockValue(temp_block , 'o')
						
						if((heuristic_value_f - heuristic_value_nf) > utility ):
							utility = (heuristic_value_f - heuristic_value_nf)
							selected_block = i
						temp_block[i] = '-'	
				return selected_block			

			if(flag == 'o'):	
				for i in blocks_allowed:
					if(temp_block[i]=='-'):
						temp_block[i] = flag
						heuristic_value_f  = self.getBlockValue(temp_block , flag)
						heuristic_value_nf = self.getBlockValue(temp_block , 'x')
						if((heuristic_value_f - heuristic_value_nf) > utility ):
							utility = (heuristic_value_f - heuristic_value_nf)
							selected_block = i
						temp_block[i] = '-'			
				return selected_block		


	def getHeuristic(self , block , block_number , block_stat , flag , update):		
		c=0;
		z= [0,3,6]
		for i in z:
			#print " i =" ,i
			#print block
			if(block[i] == flag or block[i]=='-') and (block[i+1] == flag or block[i+1]=='-') and (block[i+2] == flag or block[i+2]=='-'):
				r = 0
				if(block[i] == flag):
					r=r+1
				if(block[i+1]==flag):
					r=r+1
				if(block[i+2]==flag):
					r=r+1
				if r==1:
					c = 10+c
				if r==2:
					c=100+c
				if r==3:
					c=1000+c
					if(update == 1):
						block_stat[block_number] = flag
		z= [0,1,2]
		for i in z:
			if(block[i] == flag or block[i]=='-') and (block[i+3] == flag or block[i+3]=='-') and (block[i+6] == flag or block[i+6]=='-'):
				r = 0
				if(block[i] == flag):
					r=r+1
				if(block[i+3]==flag):
					r=r+1
				if(block[i+6]==flag):
					r=r+1
				if r==1:
					c = 10+c
				if r==2:
					c=100+c
				if r==3:
					c=1000+c
					if(update == 1):
						block_stat[block_number] = flag
		if(block[0] == flag or block[0]=='-') and (block[4] == flag or block[4]=='-') and (block[8] == flag or block[8]=='-'):
			r = 0
			if(block[0] == flag):
				r=r+1
			if(block[4]==flag):
				r=r+1
			if(block[8]==flag):
				r=r+1
			if r==1:
				c = 10+c
			if r==2:
				c=100+c
			if r==3:
				c=1000+c
				if(update == 1):
						block_stat[block_number] = flag

		if(block[2] == flag or block[2]=='-') and (block[4] == flag or block[4]=='-') and (block[6] == flag or block[6]=='-'):
			r = 0
			if(block[2] == flag):
				r=r+1
			if(block[4]==flag):
				r=r+1
			if(block[6]==flag):
				r=r+1
			if r==1:
				c = 10+c
			if r==2:
				c=100+c
			if r==3:
				c=1000+c
				if(update == 1):
						block_stat[block_number] = flag

		return c

	def getBlockValue(self , block  , flag ):		
		c=0;
		z= [0,3,6]
		for i in z:
			#print " i =" ,i
			#print block
			if(block[i] == flag or block[i]=='-') and (block[i+1] == flag or block[i+1]=='-') and (block[i+2] == flag or block[i+2]=='-'):
				r = 0
				if(block[i] == flag):
					r=r+1
				if(block[i+1]==flag):
					r=r+1
				if(block[i+2]==flag):
					r=r+1
				if r==1:
					c = 10+c
				if r==2:
					c=100+c
				if r==3:
					c=1000+c
		z= [0,1,2]
		for i in z:
			if(block[i] == flag or block[i]=='-') and (block[i+3] == flag or block[i+3]=='-') and (block[i+6] == flag or block[i+6]=='-'):
				r = 0
				if(block[i] == flag):
					r=r+1
				if(block[i+3]==flag):
					r=r+1
				if(block[i+6]==flag):
					r=r+1
				if r==1:
					c = 10+c
				if r==2:
					c=100+c
				if r==3:
					c=1000+c
		if(block[0] == flag or block[0]=='-') and (block[4] == flag or block[4]=='-') and (block[8] == flag or block[8]=='-'):
			r = 0
			if(block[0] == flag):
				r=r+1
			if(block[4]==flag):
				r=r+1
			if(block[8]==flag):
				r=r+1
			if r==1:
				c = 10+c
			if r==2:
				c=100+c
			if r==3:
				c=1000+c

		if(block[2] == flag or block[2]=='-') and (block[4] == flag or block[4]=='-') and (block[6] == flag or block[6]=='-'):
			r = 0
			if(block[2] == flag):
				r=r+1
			if(block[4]==flag):
				r=r+1
			if(block[6]==flag):
				r=r+1
			if r==1:
				c = 10+c
			if r==2:
				c=100+c
			if r==3:
				c=1000+c


		return c







class Player2:
	
	def __init__(self):
		pass
	def move(self,temp_board,temp_block,old_move,flag):
		for_corner = [0,2,3,5,6,8]

		#List of permitted blocks, based on old move.
		blocks_allowed  = []

		if old_move[0] in for_corner and old_move[1] in for_corner:
			## we will have 3 representative blocks, to choose from

			if old_move[0] % 3 == 0 and old_move[1] % 3 == 0:
				## top left 3 blocks are allowed
				blocks_allowed = [0, 1, 3]
			elif old_move[0] % 3 == 0 and old_move[1] in [2, 5, 8]:
				## top right 3 blocks are allowed
				blocks_allowed = [1,2,5]
			elif old_move[0] in [2,5, 8] and old_move[1] % 3 == 0:
				## bottom left 3 blocks are allowed
				blocks_allowed  = [3,6,7]
			elif old_move[0] in [2,5,8] and old_move[1] in [2,5,8]:
				### bottom right 3 blocks are allowed
				blocks_allowed = [5,7,8]
			else:
				print "SOMETHING REALLY WEIRD HAPPENED!"
				sys.exit(1)
		else:
		#### we will have only 1 block to choose from (or maybe NONE of them, which calls for a free move)
			if old_move[0] % 3 == 0 and old_move[1] in [1,4,7]:
				## upper-center block
				blocks_allowed = [1]
	
			elif old_move[0] in [1,4,7] and old_move[1] % 3 == 0:
				## middle-left block
				blocks_allowed = [3]
		
			elif old_move[0] in [2,5,8] and old_move[1] in [1,4,7]:
				## lower-center block
				blocks_allowed = [7]

			elif old_move[0] in [1,4,7] and old_move[1] in [2,5,8]:
				## middle-right block
				blocks_allowed = [5]
			elif old_move[0] in [1,4,7] and old_move[1] in [1,4,7]:
				blocks_allowed = [4]
                
                for i in reversed(blocks_allowed):
                    if temp_block[i] != '-':
                        blocks_allowed.remove(i)

	# We get all the empty cells in allowed blocks. If they're all full, we get all the empty cells in the entire board.
		cells = get_empty_out_of(temp_board,blocks_allowed,temp_block)
		return cells[random.randrange(len(cells))]

#Initializes the game
def get_init_board_and_blockstatus():
	board = []
	for i in range(9):
		row = ['-']*9
		board.append(row)
	
	block_stat = ['-']*9
	return board, block_stat

# Checks if player has messed with the board. Don't mess with the board that is passed to your move function. 
def verification_fails_board(board_game, temp_board_state):
	return board_game == temp_board_state	

# Checks if player has messed with the block. Don't mess with the block array that is passed to your move function. 
def verification_fails_block(block_stat, temp_block_stat):
	return block_stat == temp_block_stat	

#Gets empty cells from the list of possible blocks. Hence gets valid moves. 
def get_empty_out_of(gameb, blal,block_stat):
	cells = []  # it will be list of tuples
	#Iterate over possible blocks and get empty cells
	for idb in blal:
		id1 = idb/3
		id2 = idb%3
		for i in range(id1*3,id1*3+3):
			for j in range(id2*3,id2*3+3):
				if gameb[i][j] == '-':
					cells.append((i,j))

	# If all the possible blocks are full, you can move anywhere
	if cells == []:
		for i in range(9):
			for j in range(9):
                                no = (i/3)*3
                                no += (j/3)
				if gameb[i][j] == '-' and block_stat[no] == '-':
					cells.append((i,j))	
	return cells
		
# Note that even if someone has won a block, it is not abandoned. But then, there's no point winning it again!
# Returns True if move is valid
def check_valid_move(game_board,block_stat, current_move, old_move):

	# first we need to check whether current_move is tuple of not
	# old_move is guaranteed to be correct
	if type(current_move) is not tuple:
		return False
	
	if len(current_move) != 2:
		return False

	a = current_move[0]
	b = current_move[1]	

	if type(a) is not int or type(b) is not int:
		return False
	if a < 0 or a > 8 or b < 0 or b > 8:
		return False

	#Special case at start of game, any move is okay!
	if old_move[0] == -1 and old_move[1] == -1:
		return True


	for_corner = [0,2,3,5,6,8]

	#List of permitted blocks, based on old move.
	blocks_allowed  = []

	if old_move[0] in for_corner and old_move[1] in for_corner:
		## we will have 3 representative blocks, to choose from

		if old_move[0] % 3 == 0 and old_move[1] % 3 == 0:
			## top left 3 blocks are allowed
			blocks_allowed = [0,1,3]
		elif old_move[0] % 3 == 0 and old_move[1] in [2,5,8]:
			## top right 3 blocks are allowed
			blocks_allowed = [1,2,5]
		elif old_move[0] in [2,5,8] and old_move[1] % 3 == 0:
			## bottom left 3 blocks are allowed
			blocks_allowed  = [3,6,7]
		elif old_move[0] in [2,5,8] and old_move[1] in [2,5,8]:
			### bottom right 3 blocks are allowed
			blocks_allowed = [5,7,8]

		else:
			print "SOMETHING REALLY WEIRD HAPPENED!"
			sys.exit(1)

	else:
		#### we will have only 1 block to choose from (or maybe NONE of them, which calls for a free move)
		if old_move[0] % 3 == 0 and old_move[1] in [1,4,7]:
			## upper-center block
			blocks_allowed = [1]
	
		elif old_move[0] in [1,4,7] and old_move[1] % 3 == 0:
			## middle-left block
			blocks_allowed = [3]
		
		elif old_move[0] in [2,5,8] and old_move[1] in [1,4,7]:
			## lower-center block
			blocks_allowed = [7]

		elif old_move[0] in [1,4,7] and old_move[1] in [2,5,8]:
			## middle-right block
			blocks_allowed = [5]

		elif old_move[0] in [1,4,7] and old_move[1] in [1,4,7]:
			blocks_allowed = [4]

        #Check if the block is won, or completed. If so you cannot move there. 

        for i in reversed(blocks_allowed):
            if block_stat[i] != '-':
                blocks_allowed.remove(i)
        
        # We get all the empty cells in allowed blocks. If they're all full, we get all the empty cells in the entire board.
        cells = get_empty_out_of(game_board, blocks_allowed,block_stat)

	#Checks if you made a valid move. 
        if current_move in cells:
     	    return True
        else:
    	    return False

def update_lists(game_board, block_stat, move_ret, fl):
	#move_ret has the move to be made, so we modify the game_board, and then check if we need to modify block_stat
	game_board[move_ret[0]][move_ret[1]] = fl

	block_no = (move_ret[0]/3)*3 + move_ret[1]/3
	id1 = block_no/3
	id2 = block_no%3
	mg = 0
	mflg = 0
	if block_stat[block_no] == '-':
		if game_board[id1*3][id2*3] == game_board[id1*3+1][id2*3+1] and game_board[id1*3+1][id2*3+1] == game_board[id1*3+2][id2*3+2] and game_board[id1*3+1][id2*3+1] != '-':
			mflg=1
		if game_board[id1*3+2][id2*3] == game_board[id1*3+1][id2*3+1] and game_board[id1*3+1][id2*3+1] == game_board[id1*3][id2*3 + 2] and game_board[id1*3+1][id2*3+1] != '-':
			mflg=1
		
                if mflg != 1:
                    for i in range(id2*3,id2*3+3):
                        if game_board[id1*3][i]==game_board[id1*3+1][i] and game_board[id1*3+1][i] == game_board[id1*3+2][i] and game_board[id1*3][i] != '-':
                                mflg = 1
                                break

                ### row-wise
		if mflg != 1:
                    for i in range(id1*3,id1*3+3):
                        if game_board[i][id2*3]==game_board[i][id2*3+1] and game_board[i][id2*3+1] == game_board[i][id2*3+2] and game_board[i][id2*3] != '-':
                                mflg = 1
                                break

	
	if mflg == 1:
		block_stat[block_no] = fl
	
        #check for draw on the block.

        id1 = block_no/3
	id2 = block_no%3
        cells = []
	for i in range(id1*3,id1*3+3):
	    for j in range(id2*3,id2*3+3):
		if game_board[i][j] == '-':
		    cells.append((i,j))

        if cells == [] and mflg!=1:
            block_stat[block_no] = 'd' #Draw
        
        return

def terminal_state_reached(game_board, block_stat):
	
        #Check if game is won!
        bs = block_stat
	## Row win
	if (bs[0] == bs[1] and bs[1] == bs[2] and bs[1]!='-' and bs[1]!='d') or (bs[3]!='d' and bs[3]!='-' and bs[3] == bs[4] and bs[4] == bs[5]) or (bs[6]!='d' and bs[6]!='-' and bs[6] == bs[7] and bs[7] == bs[8]):
		print block_stat
		return True, 'W'
	## Col win
	elif (bs[0]!='d' and bs[0] == bs[3] and bs[3] == bs[6] and bs[0]!='-') or (bs[1]!='d'and bs[1] == bs[4] and bs[4] == bs[7] and bs[4]!='-') or (bs[2]!='d' and bs[2] == bs[5] and bs[5] == bs[8] and bs[5]!='-'):
		print block_stat
		return True, 'W'
	## Diag win
	elif (bs[0] == bs[4] and bs[4] == bs[8] and bs[0]!='-' and bs[0]!='d') or (bs[2] == bs[4] and bs[4] == bs[6] and bs[2]!='-' and bs[2]!='d'):
		print block_stat
		return True, 'W'
	else:
		smfl = 0
		for i in range(9):
			for j in range(9):
				if game_board[i][j] == '-' and block_stat[(i/3)*3+(j/3)] == '-':
					smfl = 1
					break
		if smfl == 1:
                        #Game is still on!
			return False, 'Continue'
		
		else:
                        #Changed scoring mechanism
                        # 1. If there is a tie, player with more boxes won, wins.
                        # 2. If no of boxes won is the same, player with more corner move, wins. 
                        point1 = 0
                        point2 = 0
                        for i in block_stat:
                            if i == 'x':
                                point1+=1
                            elif i=='o':
                                point2+=1
			if point1>point2:
				return True, 'P1'
			elif point2>point1:
				return True, 'P2'
			else:
                                point1 = 0
                                point2 = 0
                                for i in range(len(game_board)):
                                    for j in range(len(game_board[i])):
                                        if i%3!=1 and j%3!=1:
                                            if game_board[i][j] == 'x':
                                                point1+=1
                                            elif game_board[i][j]=='o':
                                                point2+=1
			        if point1>point2:
				    return True, 'P1'
			        elif point2>point1:
				    return True, 'P2'
                                else:
				    return True, 'D'	


def decide_winner_and_get_message(player,status, message):
	if player == 'P1' and status == 'L':
		return ('P2',message)
	elif player == 'P1' and status == 'W':
		return ('P1',message)
	elif player == 'P2' and status == 'L':
		return ('P1',message)
	elif player == 'P2' and status == 'W':
		return ('P2',message)
	else:
		return ('NO ONE','DRAW')
	return


def print_lists(gb, bs):
	print '=========== Game Board ==========='
	for i in range(9):
		if i > 0 and i % 3 == 0:
			print
		for j in range(9):
			if j > 0 and j % 3 == 0:
				print " " + gb[i][j],
			else:
				print gb[i][j],

		print
	print "=================================="

	print "=========== Block Status ========="
	for i in range(0, 9, 3):
		print bs[i] + " " + bs[i+1] + " " + bs[i+2] 
	print "=================================="
	print
	

def simulate(obj1,obj2):
	
	# Game board is a 9x9 list, block_stat is a 1D list of 9 elements
	game_board, block_stat = get_init_board_and_blockstatus()

	pl1 = obj1 
	pl2 = obj2

	### basically, player with flag 'x' will start the game
	pl1_fl = 'x'
	pl2_fl = 'o'

	old_move = (-1, -1) # For the first move

	WINNER = ''
	MESSAGE = ''

        #Make your move in 6 seconds!
	TIMEALLOWED = 60

	print_lists(game_board, block_stat)

	while(1):

		# Player1 will move
		
		temp_board_state = game_board[:]
		temp_block_stat = block_stat[:]
	
		signal.signal(signal.SIGALRM, handler)
		signal.alarm(TIMEALLOWED)
		# Player1 to complete in TIMEALLOWED secs. 
		try:
			ret_move_pl1 = pl1.move(temp_board_state, temp_block_stat, old_move, pl1_fl)
		except TimedOutExc as e:
			WINNER, MESSAGE = decide_winner_and_get_message('P1', 'L',   'TIMED OUT')
			break
		signal.alarm(0)
	
                #Checking if list hasn't been modified! Note: Do not make changes in the lists passed in move function!
		if not (verification_fails_board(game_board, temp_board_state) and verification_fails_block(block_stat, temp_block_stat)):
			#Player1 loses - he modified something
			WINNER, MESSAGE = decide_winner_and_get_message('P1', 'L',   'MODIFIED CONTENTS OF LISTS')
			break
		
		# Check if the move made is valid
		if not check_valid_move(game_board, block_stat,ret_move_pl1, old_move):
			## player1 loses - he made the wrong move.
			WINNER, MESSAGE = decide_winner_and_get_message('P1', 'L',   'MADE AN INVALID MOVE')
			break


		print "Player 1 made the move:", ret_move_pl1, 'with', pl1_fl

                #So if the move is valid, we update the 'game_board' and 'block_stat' lists with move of pl1
                update_lists(game_board, block_stat, ret_move_pl1, pl1_fl)

		# Checking if the last move resulted in a terminal state
		gamestatus, mesg =  terminal_state_reached(game_board, block_stat)
		if gamestatus == True:
			print_lists(game_board, block_stat)
			WINNER, MESSAGE = decide_winner_and_get_message('P1', mesg,  'COMPLETE')	
			break

		
		old_move = ret_move_pl1
		print_lists(game_board, block_stat)

                # Now player2 plays

                temp_board_state = game_board[:]
                temp_block_stat = block_stat[:]


		signal.signal(signal.SIGALRM, handler)
		signal.alarm(TIMEALLOWED)
		try:
                	ret_move_pl2 = pl2.move(temp_board_state, temp_block_stat, old_move, pl2_fl)
		except TimedOutExc as e:
			WINNER, MESSAGE = decide_winner_and_get_message('P2', 'L',   'TIMED OUT')
			break
		signal.alarm(0)

                if not (verification_fails_board(game_board, temp_board_state) and verification_fails_block(block_stat, temp_block_stat)):
			WINNER, MESSAGE = decide_winner_and_get_message('P2', 'L',   'MODIFIED CONTENTS OF LISTS')
			break
			
                if not check_valid_move(game_board, block_stat,ret_move_pl2, old_move):
			WINNER, MESSAGE = decide_winner_and_get_message('P2', 'L',   'MADE AN INVALID MOVE')
			break


		print "Player 2 made the move:", ret_move_pl2, 'with', pl2_fl
                
                update_lists(game_board, block_stat, ret_move_pl2, pl2_fl)

		gamestatus, mesg =  terminal_state_reached(game_board, block_stat)
                if gamestatus == True:
			print_lists(game_board, block_stat)
                        WINNER, MESSAGE = decide_winner_and_get_message('P2', mesg,  'COMPLETE' )
                        break
		old_move = ret_move_pl2
		print_lists(game_board, block_stat)
	
	print WINNER + " won!"
	print MESSAGE

if __name__ == '__main__':
	## get game playing objects

	if len(sys.argv) != 2:
		print 'Usage: python simulator.py <option>'
		print '<option> can be 1 => Random player vs. Random player'
		print '                2 => Human vs. Random Player'
		print '                3 => Human vs. Human'
		sys.exit(1)
 
	obj1 = ''
	obj2 = ''
	option = sys.argv[1]	
	if option == '1':
		obj1 = Player1()
		obj2 = Player2()

	elif option == '2':
		obj1 = Player1()
		obj2 = Manual_player()
	elif option == '3':
		obj1 = Manual_player()
		obj2 = Manual_player()
        
        # Deciding player1 / player2 after a coin toss
        # However, in the tournament, each player will get a chance to go 1st. 
	num = random.uniform(0,1)
	#if num > 0.5:
	#	simulate(obj2, obj1)
	#else:
	simulate(obj2, obj1)


