# uPER = ( 1 / MP ) * [ 3P + ( 2 / 3 ) * AST + ( 2 - factor * ( team_AST / team_FG ) ) *
#  FG + ( FT * 0.5 * ( 1 + ( 1 - ( team_AST / team_FG ) ) + ( 2 / 3 ) * 
# ( team_AST / team_FG ) ) ) - VOP * TOV - VOP * DRB% * ( FGA - FG ) - VOP * 0.44 * 
# ( 0.44 + ( 0.56 * DRB% ) ) * ( FTA - FT ) + VOP * ( 1 - DRB% ) * ( TRB - ORB ) + VOP *
#  DRB% * ORB + VOP * STL + VOP * DRB% * BLK - PF * ( ( lg_FT / lg_PF ) - 0.44 * 
# ( lg_FTA / lg_PF ) * VOP ) ] 


# aPER = uPER * lg_Pace / tm_Pace 

# factor = ( 2 / 3 ) - ( 0.5 * ( lg_AST / lg_FG ) ) / (2 * ( lg_FG / lg_FT ) ) 

def averageLeague():



def per(player):
    