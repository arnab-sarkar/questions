function logoutConfirmation() {    
	return confirm("You will be logged out of all Google accounts!");
}

function addQuestion(loginUrl) {
	if (loginUrl) {
		window.location.assign(loginUrl);		
	} else {
		document.getElementById('addQuestion').style.display = 'block';
	}
}

function closeAddQuestion() {
	document.getElementById('addQuestion').style.display = 'none';
}

function closeAddTags() {
	document.getElementById('addTags').style.display = 'none';
}

function addTags () {
	var q = document.getElementById('question').value;
	document.getElementById('addQuestion').style.display = 'none';
	document.getElementById('addTags').style.display = 'block';
	document.getElementById('question_entered').innerHTML = q;	
}

function goBack() {
	console.log("here");
	document.getElementById('addTags').style.display = 'none';
	document.getElementById('addQuestion').style.display = 'block';
}

function removeTag(tag) {
	tag.parentNode.removeChild(tag);
}

function addTag() {		
	var prev_tag = document.getElementById('tags_entered').innerHTML;	
	prev_tag = prev_tag.split("</li>");
	var uniqueTags = {};
	for (i = 0; i < prev_tag.length; i++) {
		var temp = prev_tag[i].replace(/<a.*<\/a>/g, "");
		temp = temp.replace(/<li.*>/g, "");				
		uniqueTags[temp] = true;		
	}
 	var tag = document.getElementById('tags').value.split(",");
 	var tags = ""
 	for (i = 0; i < tag.length; i++) {
 		var singleWord = tag[i].split(" ");
 		for (j = 0; j < singleWord.length; j++) {
	 		if (singleWord[j] != "" && !uniqueTags[singleWord[j]]) {
	 			tags += "<li class='close' id='tag_"+singleWord[j]+"'>" + singleWord[j] + "<a href='#' class='close_img' onclick='removeTag(tag_"+singleWord[j]+")'/></a></li>";
	 			//tags += "<li id="+tag[i]+">" + tag[i] + "<div class='remove_tag'><img src='/img/close.jpg' onclick='removeTag("+tag[i]+")'/></div></li>";
	 			uniqueTags[singleWord[j]] = true;
	 		} 
 		}
 	}
	document.getElementById('tags_entered').innerHTML += tags;
	document.getElementById('tags').value = "";
}