# bookpad
#IIITHyderabad #CloudComputing #CSE565 #Monsoon15 #SIEL #docspad #bookpad
initial.py is to create the database tables of sqlite
start.py starts the Flask server
apis format:
REST api 			call Function
127.0.0.1:5000/ 		        Project HomePage
127.0.0.1:5000/		       	  list Lists all the documents the user owns
			                      The list is displayed as two columns id in column1 and name in the other column
127.0.0.1:5000/upload 		  The User can Upload a document to his db
		                    	  Here the user is expected to upload a pdf file . A unique Id is assigned to the pdf
		                    	  and displayed to the user.
127.0.0.1:5000/preview?id=xyz 	        Displays the contest in the pdf in html page.
			                                  Here the content in the pdf is displayed in the html page . 
127.0.0.1:5000/edit?id=xyz 	        Opens the document in edit mode
				                            The page has save button , which can be used to save the document in the cloud
				                            after making required changes .
127.0.0.1:5000/rename?id=xyz&name=’new_name’ 			    The name of the pdf
							                                        corresponding to id is changed to new_name
127.0.0.1:5000/download?id=xyz 				Can download the document corresponding to id
127.0.0.1:5000/delete?id=xyz 				The document corresponding to Id is deleted
