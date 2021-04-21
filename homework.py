#%%
from copy import deepcopy
from os import close
from os.path import exists
class Checkers:
    
    class AnswerTypeError(Exception):
        def __init__(self, value):
            message='Data Type of '+str(value)+' is '+str(type(value))+' :Wrong data type. Should be tuple or list'
            super().__init__(message)
    class GameTree:
        def __init__(self,board,_id:int,black:bool,is_max:bool,depth,last_move=None,parent=None,root=False) -> None:
            self.id=_id
            self.parent=parent
            self.board=board
            self.black=black
            self.is_max=is_max
            self.depth=depth
            self.last_move=last_move
            self.score= None#self.get_score() #* No need to calculate score if not leaf
            self.next=[]
            self.is_root=root
            self.alpha=float('-inf')
            self.beta=float('inf')
            #self.minimax=None         

        def is_out_of_bounds(self,pos:tuple)->bool:
            return pos[1]>7 or pos[0]>7 or pos[0]<0 or pos[1]<0

        def get_score(self):
            self.my_score=0
            self.opp_score=0
            self.my_men_count=0
            self.my_king_count=0
            self.opp_men_count=0
            self.opp_king_count=0
            self.vulnerable_count=0
            self.attackable_count=0
            self.advanced_position_score=0
            self.opp_advanced_position_score=0
            self.centre_score=0
            self.king_row_count=0
            self.double_jump=0
            centre = (3.5,3.5)
            surrounding_1=[(1,1),(1,-1),(-1,-1),(-1,1)]
            jumps={(1,1):(2,2),(1,-1):(2,-2),(-1,-1):(-2,-2),(-1,1):(-2,2)}
            for i in range(8): 
                for j in range(8):
                    k=self.board[i][j]
                    surrounding_1=[(1,1),(1,-1),(-1,-1),(-1,1)]
                    jumps={(1,1):(2,2),(1,-1):(2,-2),(-1,-1):(-2,-2),(-1,1):(-2,2)}
                    if k=='.': continue
                    if self.black:
                        vulnerable_from=[(1,1),(1,-1)]
                        if k=='b':
                            self.advanced_position_score+=i
                            self.centre_score+=(i-centre[0])**2+(j-centre[1])**2
                            self.my_men_count+=1
                            if i==0: self.king_row_count+=1
                            for ar in surrounding_1:
                                i_1,j_1=i+ar[0],j+ar[1]
                                i_2,j_2=i-ar[0],j-ar[1]
                                if self.is_out_of_bounds((i_1,j_1)): continue
                                
                                if self.board[i_1][j_1]=='w' and ar in vulnerable_from:         #* if opp man on attacking position
                                    if self.is_out_of_bounds((i_2,j_2)):                        #* if opp attack not possible due to it going out of board
                                        i_3,j_3=i+jumps[ar][0],j+jumps[ar][1]                   #* my attack position
                                        if self.is_out_of_bounds((i_3,j_3)): continue           #* if my attack position is out of bounds
                                        if self.board[i_3][j_3]=='.': self.attackable_count+=1  #* if opp man attack not possible and my attack possible
                                    elif self.board[i_2][j_2]=='.':                             #* if opp attack is possible
                                        self.vulnerable_count+=1
                                        for a in vulnerable_from:
                                            i_4,j_4=i_2+a[0],j_2+a[1]
                                            if self.is_out_of_bounds((i_4,j_4)):continue
                                            if self.board[i_4][j_4]=='b' or self.board[i_4][j_4]=='B':
                                                i_5,j_5=i_2+jumps[ar][0],j_2+jumps[ar][1]
                                                if self.is_out_of_bounds((i_5,j_5)):continue
                                                if self.board[i_5][j_5]=='.': 
                                                    self.double_jump+=1
                                                    self.vulnerable_count+=1

                                    else:                                                       #* if opp attack not possible because jump pos not empty
                                        i_3,j_3=i+jumps[ar][0],j+jumps[ar][1] 
                                        if self.is_out_of_bounds((i_3,j_3)): continue
                                        if self.board[i_3][j_3]=='.': self.attackable_count+=1  #* if opp man attack not possible and my attack possible
                                
                                elif self.board[i_1][j_1]=='W' :                                #* if opp king on attack possition
                                    if self.is_out_of_bounds((i_2,j_2)):                        #* if opp attack not possible due to it going out of board
                                        i_3,j_3=i+jumps[ar][0],j+jumps[ar][1]                   #* my attack position
                                        if self.is_out_of_bounds((i_3,j_3)): continue           #* if my attack position is out of bounds
                                        if self.board[i_3][j_3]=='.': self.attackable_count+=1  #* if opp king attack not possible and my attack possible
                                    elif self.board[i_2][j_2]=='.':
                                        self.vulnerable_count+=1
                                        for a in surrounding_1:
                                            i_4,j_4=i_2+a[0],j_2+a[1]
                                            if self.is_out_of_bounds((i_4,j_4)):continue
                                            if self.board[i_4][j_4]=='b' or self.board[i_4][j_4]=='B':
                                                i_5,j_5=i_2+jumps[ar][0],j_2+jumps[ar][1]
                                                if self.is_out_of_bounds((i_5,j_5)):continue
                                                if self.board[i_5][j_5]=='.': 
                                                    self.double_jump+=1
                                                    self.vulnerable_count+=1
                                    else:                                                       #* if opp attack not possible because jump pos not empty
                                        i_3,j_3=i+jumps[ar][0],j+jumps[ar][1] 
                                        if self.is_out_of_bounds((i_3,j_3)): continue
                                        if self.board[i_3][j_3]=='.' and ar in vulnerable_from: self.attackable_count+=1  #* if opp king attack not possible and my attack possible
                                                                        #* this condition because 'b' can only attack forward 
                        
                        elif k=='B':
                            self.advanced_position_score+=i*2
                            self.centre_score+=(i-centre[0])**2+(j-centre[1])**2
                            self.my_king_count+=1
                            if i==0: self.king_row_count+=1
                            for ar in surrounding_1:
                                i_1,j_1=i+ar[0],j+ar[1]
                                i_2,j_2=i_1-ar[0],j_1-ar[1]
                                if self.is_out_of_bounds((i_1,j_1)): continue
                                
                                if self.board[i_1][j_1]=='w' and ar in vulnerable_from:         #* if opp man on attacking position
                                    if self.is_out_of_bounds((i_2,j_2)):                        #* if opp attack not possible due to it going out of board
                                        i_3,j_3=i+jumps[ar][0],j+jumps[ar][1]                   #* my attack position
                                        if self.is_out_of_bounds((i_3,j_3)): continue           #* if my attack position is out of bounds
                                        if self.board[i_3][j_3]=='.': self.attackable_count+=1  #* if opp man attack not possible and my attack possible
                                    elif self.board[i_2][j_2]=='.':                             #* if opp attack is possible
                                        self.vulnerable_count+=1
                                        for a in vulnerable_from:
                                            i_4,j_4=i_2+a[0],j_2+a[1]
                                            if self.is_out_of_bounds((i_4,j_4)):continue
                                            if self.board[i_4][j_4]=='b' or self.board[i_4][j_4]=='B':
                                                i_5,j_5=i_2+jumps[ar][0],j_2+jumps[ar][1]
                                                if self.is_out_of_bounds((i_5,j_5)):continue
                                                if self.board[i_5][j_5]=='.': 
                                                    self.double_jump+=1
                                                    self.vulnerable_count+=1
                                    else:                                                       #* if opp attack not possible because jump pos not empty
                                        i_3,j_3=i+jumps[ar][0],j+jumps[ar][1] 
                                        if self.is_out_of_bounds((i_3,j_3)): continue
                                        if self.board[i_3][j_3]=='.': self.attackable_count+=1  #* if opp man attack not possible and my attack possible
                                
                                elif self.board[i_1][j_1]=='W' :                                #* if opp king on attack possition
                                    if self.is_out_of_bounds((i_2,j_2)):                        #* if opp attack not possible due to it going out of board
                                        i_3,j_3=i+jumps[ar][0],j+jumps[ar][1]                   #* my attack position
                                        if self.is_out_of_bounds((i_3,j_3)): continue           #* if my attack position is out of bounds
                                        if self.board[i_3][j_3]=='.': self.attackable_count+=1  #* if opp king attack not possible and my attack possible
                                    elif self.board[i_2][j_2]=='.':
                                        self.vulnerable_count+=1
                                        for a in surrounding_1:
                                            i_4,j_4=i_2+a[0],j_2+a[1]
                                            if self.is_out_of_bounds((i_4,j_4)):continue
                                            if self.board[i_4][j_4]=='b' or self.board[i_4][j_4]=='B':
                                                i_5,j_5=i_2+jumps[ar][0],j_2+jumps[ar][1]
                                                if self.is_out_of_bounds((i_5,j_5)):continue
                                                if self.board[i_5][j_5]=='.': 
                                                    self.double_jump+=1
                                                    self.vulnerable_count+=1
                                    else:                                                       #* if opp attack not possible because jump pos not empty
                                        i_3,j_3=i+jumps[ar][0],j+jumps[ar][1] 
                                        if self.is_out_of_bounds((i_3,j_3)): continue
                                        if self.board[i_3][j_3]=='.': self.attackable_count+=1  #* if opp king attack not possible and my attack possible
                        
                        elif k=='w':
                            self.opp_advanced_position_score+=(7-i)
                            self.opp_men_count+=1
                        
                        else: 
                            self.opp_advanced_position_score+=(7-i)*2
                            self.opp_king_count+=1
                    
                    else:
                        vulnerable_from=[(-1,-1),(-1,1)]
                        if k=='b':
                            self.opp_advanced_position_score+=i
                            self.opp_men_count+=1
                        
                        elif k=='B':
                            self.opp_advanced_position_score+=i*2
                            self.opp_king_count+=1
                        
                        elif k=='w':
                            self.advanced_position_score+=(7-i)
                            self.my_men_count+=1
                            self.centre_score+=(i-centre[0])**2+(j-centre[1])**2
                            if i==7: self.king_row_count+=1
                            for ar in surrounding_1:
                                i_1,j_1=i+ar[0],j+ar[1]
                                i_2,j_2=i-ar[0],j-ar[1]
                                if self.is_out_of_bounds((i_1,j_1)): continue
                                
                                if self.board[i_1][j_1]=='b' and ar in vulnerable_from:         #* if opp man on attacking position
                                    if self.is_out_of_bounds((i_2,j_2)):                        #* if opp attack not possible due to it going out of board
                                        i_3,j_3=i+jumps[ar][0],j+jumps[ar][1]                   #* my attack position
                                        if self.is_out_of_bounds((i_3,j_3)): continue           #* if my attack position is out of bounds
                                        if self.board[i_3][j_3]=='.': self.attackable_count+=1  #* if opp man attack not possible and my attack possible
                                    elif self.board[i_2][j_2]=='.':                             #* if opp attack is possible
                                        self.vulnerable_count+=1
                                        for a in vulnerable_from:
                                            i_4,j_4=i_2+a[0],j_2+a[1]
                                            if self.is_out_of_bounds((i_4,j_4)):continue
                                            if self.board[i_4][j_4]=='' or self.board[i_4][j_4]=='W':
                                                i_5,j_5=i_2+jumps[ar][0],j_2+jumps[ar][1]
                                                if self.is_out_of_bounds((i_5,j_5)):continue
                                                if self.board[i_5][j_5]=='.': 
                                                    self.double_jump+=1
                                                    self.vulnerable_count+=1

                                    else:                                                       #* if opp attack not possible because jump pos not empty
                                        i_3,j_3=i+jumps[ar][0],j+jumps[ar][1] 
                                        if self.is_out_of_bounds((i_3,j_3)): continue
                                        if self.board[i_3][j_3]=='.': self.attackable_count+=1  #* if opp man attack not possible and my attack possible
                                
                                elif self.board[i_1][j_1]=='B' :                                #* if opp king on attack possition
                                    if self.is_out_of_bounds((i_2,j_2)):                        #* if opp attack not possible due to it going out of board
                                        i_3,j_3=i+jumps[ar][0],j+jumps[ar][1]                   #* my attack position
                                        if self.is_out_of_bounds((i_3,j_3)): continue           #* if my attack position is out of bounds
                                        if self.board[i_3][j_3]=='.': self.attackable_count+=1  #* if opp king attack not possible and my attack possible
                                    elif self.board[i_2][j_2]=='.':
                                        self.vulnerable_count+=1
                                        for a in surrounding_1:
                                            i_4,j_4=i_2+a[0],j_2+a[1]
                                            if self.is_out_of_bounds((i_4,j_4)):continue
                                            if self.board[i_4][j_4]=='w' or self.board[i_4][j_4]=='W':
                                                i_5,j_5=i_2+jumps[ar][0],j_2+jumps[ar][1]
                                                if self.is_out_of_bounds((i_5,j_5)):continue
                                                if self.board[i_5][j_5]=='.': 
                                                    self.double_jump+=1
                                                    self.vulnerable_count+=1
                                    else:                                                       #* if opp attack not possible because jump pos not empty
                                        i_3,j_3=i+jumps[ar][0],j+jumps[ar][1] 
                                        if self.is_out_of_bounds((i_3,j_3)): continue
                                        if self.board[i_3][j_3]=='.' and ar in vulnerable_from: self.attackable_count+=1  #* if opp king attack not possible and my attack possible
                                                                        #* this condition because 'b' can only attack forward 
                        
                        else:
                            self.advanced_position_score+=(7-i)*2 
                            self.my_king_count+=1
                            self.centre_score+=(i-centre[0])**2+(j-centre[1])**2
                            if i==7: self.king_row_count+=1
                            for ar in surrounding_1:
                                i_1,j_1=i+ar[0],j+ar[1]
                                i_2,j_2=i_1-ar[0],j_1-ar[1]
                                if self.is_out_of_bounds((i_1,j_1)): continue
                                
                                if self.board[i_1][j_1]=='b' and ar in vulnerable_from:         #* if opp man on attacking position
                                    if self.is_out_of_bounds((i_2,j_2)):                        #* if opp attack not possible due to it going out of board
                                        i_3,j_3=i+jumps[ar][0],j+jumps[ar][1]                   #* my attack position
                                        if self.is_out_of_bounds((i_3,j_3)): continue           #* if my attack position is out of bounds
                                        if self.board[i_3][j_3]=='.': self.attackable_count+=1  #* if opp man attack not possible and my attack possible
                                    elif self.board[i_2][j_2]=='.':                             #* if opp attack is possible
                                        self.vulnerable_count+=1
                                        for a in vulnerable_from:
                                            i_4,j_4=i_2+a[0],j_2+a[1]
                                            if self.is_out_of_bounds((i_4,j_4)):continue
                                            if self.board[i_4][j_4]=='w' or self.board[i_4][j_4]=='W':
                                                i_5,j_5=i_2+jumps[ar][0],j_2+jumps[ar][1]
                                                if self.is_out_of_bounds((i_5,j_5)):continue
                                                if self.board[i_5][j_5]=='.': 
                                                    self.double_jump+=1
                                                    self.vulnerable_count+=1
                                    else:                                                       #* if opp attack not possible because jump pos not empty
                                        i_3,j_3=i+jumps[ar][0],j+jumps[ar][1] 
                                        if self.is_out_of_bounds((i_3,j_3)): continue
                                        if self.board[i_3][j_3]=='.': self.attackable_count+=1  #* if opp man attack not possible and my attack possible
                                
                                elif self.board[i_1][j_1]=='B' :                                #* if opp king on attack possition
                                    if self.is_out_of_bounds((i_2,j_2)):                        #* if opp attack not possible due to it going out of board
                                        i_3,j_3=i+jumps[ar][0],j+jumps[ar][1]                   #* my attack position
                                        if self.is_out_of_bounds((i_3,j_3)): continue           #* if my attack position is out of bounds
                                        if self.board[i_3][j_3]=='.': self.attackable_count+=1  #* if opp king attack not possible and my attack possible
                                    elif self.board[i_2][j_2]=='.':
                                        self.vulnerable_count+=1
                                        for a in surrounding_1:
                                            i_4,j_4=i_2+a[0],j_2+a[1]
                                            if self.is_out_of_bounds((i_4,j_4)):continue
                                            if self.board[i_4][j_4]=='w' or self.board[i_4][j_4]=='W':
                                                i_5,j_5=i_2+jumps[ar][0],j_2+jumps[ar][1]
                                                if self.is_out_of_bounds((i_5,j_5)):continue
                                                if self.board[i_5][j_5]=='.': 
                                                    self.double_jump+=1
                                                    self.vulnerable_count+=1
                                    else:                                                       #* if opp attack not possible because jump pos not empty
                                        i_3,j_3=i+jumps[ar][0],j+jumps[ar][1] 
                                        if self.is_out_of_bounds((i_3,j_3)): continue
                                        if self.board[i_3][j_3]=='.': self.attackable_count+=1  #* if opp king attack not possible and my attack possible                  
            #if self.advanced_position_score==0: self.my_score=0
            #else: 
            self.my_score=self.my_men_count+self.my_king_count*3+self.attackable_count*3#+self.advanced_position_score/(self.my_men_count+self.my_king_count)
            #if self.opp_advanced_position_score==0: self.opp_score=0
            #else: 
            self.opp_score=self.opp_men_count+self.opp_king_count*6+self.vulnerable_count*5#+self.opp_advanced_position_score/(self.opp_men_count+self.opp_king_count)
            #print(self.is_max, self.vulnerable_count, self.attackable_count)
            #print(self.king_row_count)
            #print(self.centre_score)
            if self.opp_men_count==0: return float('inf')
            if self.my_men_count==0: return float('-inf')
            return (self.my_score-self.opp_score-self.double_jump*7+self.king_row_count*2)*(self.my_men_count/self.centre_score) if self.centre_score!=0 else float('-inf') #if not self.is_max else self.opp_score-self.my_score
        
        def is_leaf(self)->bool:
            return len(self.next)==0

        def __gt__(self,o:object) -> bool:
            return self.score>o.score
        def __lt__(self,o:object) -> bool:
            return self.score<o.score
        def __ge__(self,o:object) -> bool:
            return self.score>=o.score
        def __le__(self,o:object) -> bool:
            return self.score<=o.score
        def __hash__(self) -> int:
            return hash(self.score)
        def __eq__(self, o: object) -> bool:
            return self.board==o.board

    def __init__(self) -> None:
        f=open('input.txt','r').read()
        lines=f.split('\n')
        self.type=lines[0]
        self.start=lines[1]
        self.single_mode=True if self.type=='SINGLE' else False
        self.time=lines[2]
        self.board=[[i for i in line.strip()] for line in lines[3:11]]
        cols=['a','b','c','d','e','f','g','h']
        self.board_dict={(i,j):cols[j]+str(8-i) for i in range(8) for j in range(8)}
        self.men_moves=[(1,1),(1,-1)] if self.start=='BLACK'else [(-1,1),(-1,-1)]
        self.king_moves=[(1,1),(1,-1),(-1,-1),(-1,1)]
        self.jump_moves={(1,1):(2,2),(1,-1):(2,-2),(-1,-1):(-2,-2),(-1,1):(-2,2)}
        self.men_positions={}
        self.king_positions={}
        self.possible_moves=[]
        self.testlist=[]
        self.game_tree={}
        self.game_tree_root=None
        self.tree_depth=None
    
    def update_positions(self,board,black:bool)->tuple:
        men_pos={}
        king_pos={}
        r=range(8) if not black else range(7,-1,-1)
        for i in r: 
            for j in r:
                k=board[i][j]
                if not black:
                    if k=='w': men_pos[(i,j)]=[]
                    elif k=='W': king_pos[(i,j)]=[]
                else:
                    if k=='b': men_pos[(i,j)]=[]
                    elif k=='B': king_pos[(i,j)]=[]
        return men_pos,king_pos
    
    def is_out_of_bounds(self,pos:tuple)->bool:
        return pos[1]>7 or pos[0]>7 or pos[0]<0 or pos[1]<0

    def get_jump_moves(self,board,pos,move_list:list,possible_moves,black:bool,end=False):
        possible_jumps=[]
        small_letter='w' if black else 'b' #* man to kill
        big_letter='W' if black else 'B' #* king to kill
        for move in possible_moves:
            adj_to=pos[0]+move[0],pos[1]+move[1]
            jump_to=pos[0]+self.jump_moves[move][0],pos[1]+self.jump_moves[move][1]
            if self.is_out_of_bounds(adj_to) or self.is_out_of_bounds(jump_to): continue 
            if board[jump_to[0]][jump_to[1]]=='.' and (board[adj_to[0]][adj_to[1]]==small_letter or board[adj_to[0]][adj_to[1]]==big_letter):
                possible_jumps.append(jump_to)
        if not possible_jumps: return move_list,True
        #print(black)
        for i in possible_jumps:
            jump_to=i
            board[pos[0]][pos[1]],board[i[0]][i[1]]=board[i[0]][i[1]],board[pos[0]][pos[1]]
            j_mid=(pos[0]+i[0])//2,(pos[1]+i[1])//2
            board[j_mid[0]][j_mid[1]]='.'
            move_list.append(('J',pos,i))
            board_copy=deepcopy(board)
            move_list,end=self.get_jump_moves(board_copy,jump_to,move_list,possible_moves,black)
            if end:
                self.testlist.append(deepcopy(move_list))
                #if self.single_mode: break
                del move_list[-1]
        return move_list,False
    
    def get_simple_moves(self,board,pos,possible_moves):
        for move in possible_moves:
            if not self.is_out_of_bounds((pos[0]+move[0],pos[1]+move[1])):
                if board[pos[0]+move[0]][pos[1]+move[1]]=='.':
                    self.testlist.append(('E',pos,(pos[0]+move[0],pos[1]+move[1])))
                    #if self.single_mode: break # If only move move is req, append the single move and exit
    
    def perform_jump(self,board,move)->list:
        if move[0]=='E':
            board[move[1][0]][move[1][1]],board[move[2][0]][move[2][1]] = board[move[2][0]][move[2][1]],board[move[1][0]][move[1][1]] #* simple move by exchanging string value
            if move[2][0]==0 or move[2][0]==7: board[move[2][0]][move[2][1]]=board[move[2][0]][move[2][1]].upper() #* Crowning the piece
            return board
        else:
            for j in move:
                j_from=j[1]
                j_to=j[2]
                j_mid=(j[2][0]+j[1][0])//2,(j[2][1]+j[1][1])//2
                board[j_from[0]][j_from[1]],board[j_to[0]][j_to[1]] = board[j_to[0]][j_to[1]],board[j_from[0]][j_from[1]] #* performing jump by exchanging final and initial position and making middle empty
                if j_to[0]==0 or j_to[0]==7: board[j_to[0]][j_to[1]]=board[j_to[0]][j_to[1]].upper() #* Crowning the piece
                board[j_mid[0]][j_mid[1]]='.'
            return board

    def get_my_moves(self,current_game:GameTree,black:bool):
        state=deepcopy(current_game.board)
        #print(current_game.last_move,state,sep='\n')
        mp,kp=self.update_positions(state,black)
        piece_list={}
        #print(state)
        self.testlist.clear()
        king_moves=[(1,1),(1,-1),(-1,-1),(-1,1)]
        if black:
            men_moves=[(1,1),(1,-1)]
            for pos in mp:
                current_board=deepcopy(state)
                self.get_jump_moves(current_board,pos,[],men_moves,True)
                if len(self.testlist)==0: self.get_simple_moves(deepcopy(state),pos,men_moves)
                #self.men_positions[pos]=deepcopy(self.testlist)
                piece_list[pos]=deepcopy(self.testlist)
                self.testlist.clear()
            for pos in kp:
                current_board=deepcopy(state)
                self.get_jump_moves(current_board,pos,[],king_moves,True)
                if len(self.testlist)==0: self.get_simple_moves(deepcopy(state),pos,king_moves)
                #self.king_positions[pos]=deepcopy(self.testlist)
                piece_list[pos]=deepcopy(self.testlist)
                self.testlist.clear()
        else:
            men_moves=[(-1,1),(-1,-1)]
            for pos in mp:
                current_board=deepcopy(state)
                self.get_jump_moves(current_board,pos,[],men_moves,False)
                if len(self.testlist)==0: self.get_simple_moves(deepcopy(state),pos,men_moves)
                #self.men_positions[pos]=deepcopy(self.testlist)
                piece_list[pos]=deepcopy(self.testlist)
                self.testlist.clear()
            for pos in kp:
                current_board=deepcopy(state)
                self.get_jump_moves(current_board,pos,[],king_moves,False)
                if len(self.testlist)==0: self.get_simple_moves(deepcopy(state),pos,king_moves)
                #self.men_positions[pos]=deepcopy(self.testlist)
                piece_list[pos]=deepcopy(self.testlist)
                self.testlist.clear()
        #print(piece_list)
        simple_moves={}
        jump_moves={}
        jump_found=False
        for piece in piece_list:
            for m in piece_list[piece]:
                if m[0]=='E':
                    if not jump_found: simple_moves[piece]=piece_list[piece]
                else:
                    jump_found=True
                    jump_moves[piece]=piece_list[piece]
        #print(jump_moves if jump_found else simple_moves)
        return jump_moves if jump_found else simple_moves

    def no_piece_left(self,black:bool,board:list):
        to_check1 = 'b' if black else 'w'
        to_check2 = 'B' if black else 'W'
        x=0
        for i in range(8):
            for j in range(8):
                if board[i][j]==to_check1 or board[i][j]==to_check2: x+=1
        return x==0

    def create_tree(self,root:GameTree,depth:int,root_black:bool):
        is_max=not root.is_max
        self.game_tree[0]=[]
        self.game_tree[0].append(root)
        id=1
        bl=root_black
        b=False
        #import time
        #t1=time.time()
        for d in range(1,depth):
            if d==2 and len(self.game_tree[d-1])==1: break
            self.game_tree[d]=[]
            for state in self.game_tree[d-1]:
                #print(state.last_move,state.board,sep='\n')
                #print(state.id)
                moves= self.get_my_moves(state,bl)
                #print(state.black)
                #print(moves)
                if self.no_piece_left(bl,state.board):
                    b=True
                    break
                for piece in moves:
                    for move in moves[piece]:
                        #print('\nmove',piece,moves[piece])
                        new_board=self.perform_jump(deepcopy(state.board),move)
                        new_node=self.GameTree(board=new_board,_id=id,black= root_black,is_max=is_max,depth=d,last_move=move,parent=state)
                        #print(new_node.parent.board,new_node.parent.depth,new_node.depth,new_node.board,new_node.last_move,new_node.black,'****',sep='\n')
                        #print(new_node.parent.black,new_node.black)
                        id+=1
                        #print(new_node.parent.board==new_node.board)
                        new_node.parent.next.append(new_node)
                        self.game_tree[d].append(new_node)
            if b:
                for i in self.game_tree[d]: i.parent.next=[]
                del self.game_tree[d] 
                break
            self.tree_depth=d+1
            #root_black = not root_black
            bl = not bl
            is_max = not is_max
            #print('Depth Compelte',d,'time taken ',time.time()-t1)
        return root

    def single_move(self,root_black:bool):
        board=deepcopy(self.board)
        mp,kp=self.update_positions(board,root_black)
        self.testlist.clear()
        for pos in mp: 
            self.get_jump_moves(board,pos,move_list=[],possible_moves=[(1,1),(1,-1)] if root_black else [(-1,1),(-1,-1)],black=root_black)
            if len(self.testlist)!=0: return self.testlist[0] # If there is a jump move, return the jump move and exit
            self.testlist.clear()
        for pos in kp: 
            self.get_jump_moves(board,pos,move_list=[],possible_moves=[(1,1),(1,-1),(-1,-1),(-1,1)],black=root_black)
            if len(self.testlist)!=0: return self.testlist[0]
            self.testlist.clear()
        for pos in mp:
            self.get_simple_moves(deepcopy(self.board),pos,[(1,1),(1,-1)] if root_black else [(-1,1),(-1,-1)]) # If there is no jump move, find simple move
            if len(self.testlist)!=0: return self.testlist[0] # If there is a simple move, return the move and exit, else continue
            self.testlist.clear()
        for pos in kp: 
            self.get_jump_moves(deepcopy(self.board),pos,[(1,1),(1,-1),(-1,-1),(-1,1)])
            if len(self.testlist)!=0: return self.testlist[0]
            self.testlist.clear()
        return []

    def alpha_beta_search(self,state:GameTree):
        if state.is_max:
            state.alpha = self.max_value(state)
            for child in state.next:
                if child.beta==state.alpha: return child.last_move
        else: 
            state.beta = self.min_value(state)
            for child in state.next:
                if child.alpha==state.beta: return child.last_move
        return []
    
    def max_value(self,state:GameTree):
        if state.is_leaf(): 
            state.alpha=state.score
            return state.score
        v = float('-inf')
        for child in state.next:
            v = max(v,self.min_value(child))
            if v>=state.beta: return v
            state.alpha=max(state.alpha,v)
        return v
    
    def min_value(self,state:GameTree):
        if state.is_leaf(): 
            state.beta=state.score
            return state.score
        v = float('inf')
        for child in state.next:
            v = min(v,self.max_value(child))
            if v<=state.alpha: return v
            state.beta=min(state.beta,v)
        return v

    def output_move(self,move):
        if type(move)==tuple:
            answer_string=move[0]+' '+self.board_dict[move[1]]+' '+self.board_dict[move[2]]
        elif type(move)==list:
            answer_string='\n'.join([m[0]+' '+self.board_dict[m[1]]+' '+self.board_dict[m[2]] for m in move])
        else:
            raise self.AnswerTypeError(move)
        #print('Answer',answer_string)
        open('output.txt','w').write(answer_string)
    
    def my_piece_count(self,black:bool)->int:
        cnt=0
        small_letter='b' if black else 'w' #* man to kill
        big_letter='B' if black else 'W' #* king to kill
        for i in range(8): 
                for j in range(8):
                    k=self.board[i][j]
                    if k==small_letter or k==big_letter: cnt+=1
        return cnt

    def playdata(self)->int: # 0 means first move, 1 means within first 3 moves so use depth 1, 2 means using minimax 
        ex=exists('playdata.txt')
        pdata = ''
        if ex:
            f=open('playdata.txt','r')
            pdata=f.read()
            f.close()
        else:
            f=open('playdata.txt','w+')
            f.close()
        if pdata=='': 
            open('playdata.txt','w').write('1 '+self.time)
            return 0
        elif int(pdata.split(' ')[0])<=4: # First few moves
            #print('FFF')
            open('playdata.txt','w').write(str(int(pdata.split(' ')[0])+1)+' '+self.time)
            return 1
        else:
            open('playdata.txt','w').write(str(int(pdata.split(' ')[0])+1)+' '+self.time)
            return 2

    def play(self)->None:
        self.next_move = self.single_play() if self.type=='SINGLE' else self.agent_play()
        #import time
        #t2=time.time()
        #for i in self.perform_jump(deepcopy(self.board),self.next_move):print(i)
        self.output_move(self.next_move)
        #print(time.time()-t2,'output time')
    
    def single_play(self):
        is_black=True if self.start=='BLACK' else False
        #import time 
        #t1=time.time()
        #print('Single Move Time',time.time()-t1)
        return self.single_move(is_black)

    def agent_play(self)->None:
        move_no = self.playdata()
        if float(self.time)<=0.01:
            self.single_mode=True
            return self.single_play()
        is_black=True if self.start=='BLACK' else False
        mp,kp=self.update_positions(self.board,is_black)
        if len(mp)+len(kp)==1: return self.single_play()
        if move_no==0:
            if is_black:
                return ('E',(2,5),(3,4)) #* The 'Old Faithful' Move always if first move on new board
            else: # Reply to black's first move
                if self.board[3][4]=='b': 
                    if self.board[2][5]=='.':
                        return ('E',(5,4),(4,5)) #* reply to Old Faithful
                    elif self.board[2][3]=='.':
                        return ('E',(5,4),(4,3)) #* reply to the second Old Faithful
                #* Gathering all possible tandem moves for the first move
                elif self.board[3][2]=='b': 
                    if self.board[2][1]=='.':
                        return ('E',(5,2),(4,1))
                    elif self.board[2][3]=='.':
                        return ('E',(5,2),(4,1))
                elif self.board[3][0]=='b':
                    return ('E',(5,0),(4,1))
                elif self.board[3][6]=='b':
                    if self.board[2][5]=='.':
                        return ('E',(5,6),(4,5))
                    elif self.board[2][7]=='.':
                        return ('E',(5,6),(4,7))
                return ('E',(5,0),(4,1))
        elif move_no==1:
            #self.single_mode=True
            #return self.single_play()   
            tree_depth=3
        #print('Full Mode')
        #print('time',self.time)
        else:
            if float(self.time)<=0.1:
                tree_depth=2
            elif float(self.time)<=1:
                tree_depth=3
            else:
                my_men=self.my_piece_count(is_black)
                if my_men<=5: tree_depth=2
                elif my_men<=7: tree_depth=3
                else:
                    #print('F') 
                    tree_depth=3
        self.tree_depth=tree_depth
        root = self.GameTree(board=deepcopy(self.board),_id=0,black=is_black,is_max=True,depth=0,last_move=None,parent=None,root=True)
        #print('tree depth',tree_depth)
        self.game_tree_root=self.create_tree(root=root,depth=tree_depth,root_black=is_black)
        for leaf in self.game_tree[self.tree_depth-1]: leaf.score=leaf.get_score()
        return self.alpha_beta_search(self.game_tree_root)

if __name__=="__main__":
    #import time
    #t=time.time()
    ch = Checkers()
    ch.play()
    #print(time.time()-t,'for complete game')