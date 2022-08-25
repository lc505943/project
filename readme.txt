# Kamenožrout game available at https://is.muni.cz/auth/hry/01/

# update:
# rn, implementing the rest of GUI (part still available, follow steps below)
#	and working on structuring the project a bit better
# studying PostgreSQL, hopefully to be used here soon

# note that the code might differ from the requirements in the other files;
# 	this app went through some changes after the initial submition

# also note that the app is not as polished as i would like it to be
# 	the Board.solve() fctions overhead could be dramatically reduced...
#	not all edge cases are handled properly...
#	UI needs a lot of work...
#	saving user credentials in pt is obviously a big no-no...
# 	and lots of more...
# but i believe, that this version still presents the general idea quite well
# and since i want to release this version asap, this will have to do for now


# now, i will take you through the app so that you get the general idea on what
# it is useful for, feel free to look around whenever you feel like it

# start the app; this is what you should see on the console

	created user database  # first time starting the app
	stoner>>>

# type "h" whenever you feel lost

	stoner>>>h
	commands:
	a : admin
	t : taskmaster
	p : player
	e : exit
	h : help

# first, lets create an user using admin (admin credentials are admin, admin)

	stoner>>>a
	stoner>admin login>>>admin
	stoner>admin password>>>admin
	stoner>admin>>>h
	commands:
	a login password taskmaster_auth player_auth : add user to the database
	d login : delete user from the database
	u login password taskmaster_auth player_auth : update user
	v : view user database
	e : exit admin UI
	boolean values to be input as "True", "False"

# user (for the purposes of this showcase almighty "super" user) creation

	stoner>admin>>>a super password True True
	user super successfully added to the database

# check what users are in the database

	stoner>admin>>>v
	login	taskmaster	player
	--------------------------
	super		True	True

# lets go to taskmaster interface

	stoner>admin>>>e
	stoner>>>t

# use the user "super" to access the taskmaster functionality

	stoner>taskmaster login>>>super
	stoner>taskmaster password>>>password
	stoner>taskmaster>>>h
	commands:
	l picture_path assignment_path : load assignment from picture
	v session_path : view player session (assignment, moves, final board)
	e : exit taskmaster interface

# the "load" command is the one we care about;
# lets load boards captured in file "board1.png", "board_almost_solved.png"

	stoner>taskmaster>>>l board1.png assignment1
	loaded board:
	1 3 5 2 4 4 3 1 1 3 5 4 2 3 3 1 4 5 3 2 
	1 4 4 4 1 2 4 2 3 4 5 4 4 2 5 3 4 3 3 4 
	3 1 1 2 1 5 2 1 3 4 1 2 2 1 1 1 5 3 2 1 
	4 2 5 1 4 1 5 1 1 1 1 5 2 4 4 1 3 5 5 5 
	4 5 4 2 5 2 4 4 1 1 1 5 3 2 4 3 3 4 1 2 
	2 3 4 3 3 4 5 1 1 1 1 2 3 5 2 4 4 5 2 1 
	5 1 5 2 1 4 5 1 1 2 1 3 1 3 1 5 1 1 1 4 
	1 2 1 1 3 1 3 1 3 4 1 3 1 2 1 2 1 2 4 4 
	2 1 5 1 4 3 2 2 1 3 1 1 2 3 1 3 4 1 4 1 
	1 4 1 1 2 1 3 3 5 2 1 1 1 5 5 5 3 5 1 4 
	resolved ^this board; proceed to save?
	input 'y' to confirm, anything else to cancel
	>>>y
	stoner>taskmaster>>>l board_almost_solved.png assignment_almost_solved
	loaded board:
	                                        
	                                        
	                                        
	                                        
	                                        
	                                        
	4 5 1 5 4 2 4 1                         
	5 5 5 5 5 5 1 5                         
	4 5 4 4 2 2 5 5                         
	1 5 1 1 4 5 5 5                         
	resolved ^this board; proceed to save?
	input 'y' to confirm, anything else to cancel
	>>>y

# now to the player interface

	stoner>taskmaster>>>e
	stoner>>>p
	stoner>player login>>>super
	stoner>player password>>>password
	stoner>player>>>h
	commands:
	c assignment_path output_path : create session from assignment_path in output_path
	p session_path : play session session_path
	e : exit player interface

# create session to work with an assingment

	stoner>player>>>c assignment1 session1
	success! session available at: session1

# play the session

	stoner>player>>>p session1
	
	# this is where the changes are;
	# GUI should appear - play with it!
	# closing the window saves the progress
	
	successfully played a session at: session1

# since this is the core of the whole app, i encourage you to play with it!
# notice commands z & y (undo & redo), which are not available in the original!
# once session is saved, it can be loaded again without losing progress!

# now lets try the auto-solve feature;
# sadly, it is only useful on "small inputs"
# also, interacting with the GUI while auto-solve is running crashes the app
# this part needs a bit of polishing

	stoner>player>>>c assignment_almost_solved session_almost_solved
	success! session available at: session_almost_solved
	stoner>player>>>p session_almost_solved
	                                        
	                                        
	                                        
	                                        
	                                        
	                                        
	4 5 1 5 4 2 4 1                         
	5 5 5 5 5 5 1 5                         
	4 5 4 4 2 2 5 5                         
	1 5 1 1 4 5 5 5                         

# input "a True" if you want to see the steps the AI tries

	playing session>>>a False
	solution found! [(0, 2), (0, 0), (3, 1), (4, 0), (1, 0), (0, 0)]
	                                        
	                                        
	                                        
	                                        
	                                        
	                                        
	4 5 1 5 4 2 4 1                         
	5 5 5 5 5 5 1 5                         
	4 5 4 4 2 2 5 5                         
	1 5 1 1 4 5 5 5                         

# the found solution actually seems to be a solution

	playing session>>>0;2
	requested move: (0, 2)
	played move 0;2
	                                        
	                                        
	                                        
	                                        
	                                        
	                                        
	          4 1                           
	4 1   4 2 1 5                           
	4 4 4 2 2 5 5                           
	1 1 1 4 5 5 5                           
	playing session>>>0;0
	requested move: (0, 0)
	played move 0;0
	                                        
	                                        
	                                        
	                                        
	                                        
	                                        
	          4 1                           
	      4 2 1 5                           
	4 1   2 2 5 5                           
	4 4 4 4 5 5 5                           
	playing session>>>3;1
	requested move: (3, 1)
	played move 3;1
	                                        
	                                        
	                                        
	                                        
	                                        
	                                        
	          4 1                           
	          1 5                           
	4 1   4   5 5                           
	4 4 4 4 5 5 5                           
	playing session>>>4;0
	requested move: (4, 0)
	played move 4;0
	                                        
	                                        
	                                        
	                                        
	                                        
	                                        
	                                        
	                                        
	4 1   4 4                               
	4 4 4 4 1 1                             
	playing session>>>1;0
	requested move: (1, 0)
	played move 1;0
	                                        
	                                        
	                                        
	                                        
	                                        
	                                        
	                                        
	                                        
	                                        
	1 1 1                                   
	playing session>>>0;0
	requested move: (0, 0)
	played move 0;0
	                                        
	                                        
	                                        
	                                        
	                                        
	                                        
	                                        
	                                        
	                                        
	                                        
	playing session>>>s
	successfully played a session at: session_almost_solved
	stoner>player>>>e
	stoner>>>e
	
	Process finished with exit code 0

# now, i believe you should be able to work with the app on your own
# as said, i encourage you to look around and play with it
# if you have any questions, do not hesitate to contact the support
#	lukas.chudicek@seznam.cz
