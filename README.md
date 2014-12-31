questions
=========
Project Documentation

Introduction:
	The project is a question answer website, similar to Quora. Users can login, post questions and answers, vote on posts and of course view them, etc.

Design:
	The system has been designed to run on google app engine. It is built on Python and Django. For storing data, I am using ndb and blobstorage on google.

Components of code:
	main.py - the main handler and entry point to the backend code
	home.py - the main controller for all the backend services
	model.py - the data model for storing the data using appengine ndb storage
	static - holds allt eh static contents like the css, javascripts and images
	templates - holds all the html templates used to render using django to display all the ui pages

Components of home.py
	This is the main controller and has the following classes:
	MainPage - Renders the main home page of the 
	DisplaySameTagQuestion - Displays all the questions having the same tags
	AddQuestion - Adds a new Question
	UpdateQuestion - Updates an existing Question
	ViewQuestion - Handles the request to display a question and related answers
	AddAnswer - Adds an answer to an existing question
	PostDescription - Adds a description to the question
	VotePost - Posts a vote
	UpdateAnswer - Update an existing answer
	UploadImagePage - Handles the upload image page
	UploadImage - Uploads an image to the blobstore
	ImageServeHandler - Displays and image
	Search - Searches for posts
	RSSQuestion - Generates RSS for a question and related information

To Use:
	Go to the link:
		http://question-ost.appspot.com

	While logged out:
		- You can view the question and answers
		- You can search
		- You cannot post any questions or answers
		- You cannot edit any post
		- You cannot cast votes
		- If you view a post, its view count will not increase
		- You cannot upload any images
		- All user info (user Id) for posts will be hidden from you
		- You can generate RSS but all user info (user Id) will not be included

	While logged in:
		- You can view the question and answers
		- You can search
		- You can post new questions or answer any existing questions
		- You can view user info (user Id) of the questions and answers
		- You can edit only those posts which have been posted by you. You cannot edit other users posts (Edit option comes when you hover over your post)
		- You can cast vote and change your vote
		- If you visit a post for the first time, the view count increases by 1
		- You can Upload images and view all images you have uploaded earlier
		- You can generate RSS for each question which will include all information related to the question
