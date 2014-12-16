var originalTag;
var originalId;

function logoutConfirmation() {    
	return confirm("You will be logged out of all Google accounts!");
}

function addQuestion(loginUrl) {
	if (loginUrl) {
		window.location.assign(loginUrl);		
	} else {
		document.getElementById('addQuestion').style.display = 'block';
		document.getElementById('add_question_button').value = "Add Question";
		document.getElementById('operation_title_q').innerHTML = "Add";
		document.getElementById('operation_title_t').innerHTML = "Add";
		document.getElementById('add_question_button').onclick = postQuestion;
	}
}

function closeAddQuestion() {
	document.getElementById('addQuestion').style.display = 'none';
	clearForm();
}

function closeAddTags() {
	document.getElementById('addTags').style.display = 'none';
	clearForm();
}

function addTags () {
	var q = document.getElementById('question').value;
	document.getElementById('addQuestion').style.display = 'none';
	document.getElementById('addTags').style.display = 'block';
	document.getElementById('question_entered').innerHTML = q;
}

function goBack() {	
	document.getElementById('addTags').style.display = 'none';
	document.getElementById('addQuestion').style.display = 'block';
}

function removeTag(tag) {
	tag.parentNode.removeChild(tag);
}

function clearForm() {
	document.getElementById('question_entered').innerHTML="";
	document.getElementById('question').value="";
	document.getElementById('tags_entered').innerHTML ="";
	document.getElementById('tags').value = "Enter comma seperated list of tags";
}

function addTag() {		
	var prev_tag = document.getElementById('tags_entered').innerHTML;	
	prev_tag = prev_tag.split("</li>");
	var uniqueTags = {};
	for (i = 0; i < prev_tag.length; i++) {
		var temp = prev_tag[i].replace(/<a.*<\/a>/g, "");
		temp = temp.replace(/<li.*>/g, "").replace(/ +/g,"_");				
		uniqueTags[temp] = true;		
	}
	if(document.getElementById('tags').value == "Enter comma seperated list of tags")
		return;
 	var tag = document.getElementById('tags').value.split(",");
 	var tags = ""
 	for (i = 0; i < tag.length; i++) {
 		var singleWord = tag[i].trim().replace(/ +/g, "_"); 
 		singleWord = singleWord.replace(/[.'?+-@#!^%~*()|\\\/]/g,"");		
 		if (singleWord != "" && !uniqueTags[singleWord]) {
 			tags += "<li class='close' id='tag_"+singleWord+"'>" + tag[i].trim() + "<a href='#' class='close_img' onclick='removeTag(tag_"+singleWord+")'/></a></li>";
 			//tags += "<li id="+tag[i]+">" + tag[i] + "<div class='remove_tag'><img src='/img/close.jpg' onclick='removeTag("+tag[i]+")'/></div></li>";
 			uniqueTags[singleWord] = true;
 		}  		
 	}
	document.getElementById('tags_entered').innerHTML += tags;
	document.getElementById('tags').value = "Enter comma seperated list of tags";
}

function post(path, params, method) {
    method = method || "post"; // Set method to post by default if not specified.

    // The rest of this code assumes you are not using a library.
    // It can be made less wordy if you use one.
    var form = document.createElement("form");
    form.setAttribute("method", method);
    form.setAttribute("action", path);

    for(var key in params) {
        if(params.hasOwnProperty(key)) {
            var hiddenField = document.createElement("input");
            hiddenField.setAttribute("type", "hidden");
            hiddenField.setAttribute("name", key);
            hiddenField.setAttribute("value", params[key]);

            form.appendChild(hiddenField);
         }
    }
    document.body.appendChild(form);
    form.submit();
}

function postAnswer(qId) {
	var answer = document.getElementById('answer').value;
	post('/addAnswer',{a:answer,q:qId});
}

function editQuestion(loginUrl) {
	var question = document.getElementById('question_to_edit').innerHTML;
	document.getElementById('question').value = question;
	var tags = document.getElementById('all_existing_tags').innerHTML;
	tags = tags.trim();
	tags = tags.replace(/<\/a.*>/g, ",");
	tags = tags.replace(/<li.*>/g, "");
	document.getElementById('tags').value = tags;
	document.getElementById('operation_title_q').innerHTML = "Edit";
	document.getElementById('operation_title_t').innerHTML = "Edit";
	document.getElementById('add_question_button').value = "Update Question";
	document.getElementById('add_question_button').onclick = updateQuestion;
	addTag();
	document.getElementById('addQuestion').style.display = 'block';
}

function vote(id, loginUrl, vote) {
	if (loginUrl) {
		window.location.assign(loginUrl);		
	} else {
		var url = document.URL;
		var data = {
			id:id,
			vote:vote,
			url:url
		}
		post('/vote',data);
	}
}

function postQuestion(){	
	var tags = document.getElementById('tags_entered').innerHTML.split("</li>");
	tagList="";
	for(i=0;i<tags.length;i++) {
		tagList+= tags[i].replace(/<a.*>/g,"").replace(/<li.*>/g,"") + ",";
	}
	var question_title = document.getElementById('question_entered').innerHTML;
	if(question_title.match(/^[ \t]*$/))
		alert("Question title cannot be left blank")
	else
		post('/question',{question:question_title,tags:tagList});	
}

function updateQuestion(){	
	var tags = document.getElementById('tags_entered').innerHTML.split("</li>");
	tagList="";
	for(i=0;i<tags.length;i++) {
		tagList+= tags[i].replace(/<a.*>/g,"").replace(/<li.*>/g,"") + ",";
	}
	var question_title = document.getElementById('question_entered').innerHTML;
	var qId = document.getElementById('qId').innerHTML.trim();	
	if(question_title.match(/^[ \t]*$/))
		alert("Question title cannot be left blank");
	else
		post('/updateQuestion',{qId:qId, question:question_title, tags:tagList});	
}

function editAnswer(aId) {	
	if (originalId !== undefined) {
		document.getElementById(originalId).innerHTML = originalTag;
	}
	originalTag = document.getElementById(aId).innerHTML;
	originalId = aId;
	var answer = originalTag.replace(/<span class="display_userId".*>/g, "").trim();
	document.getElementById(aId).innerHTML = "<textarea id='edit_this_answer' class='donot_display_edit' style='height:100px;width:100%'>"+
											answer+"</textarea><div> <input class='btn' type='button' value='Update Answer' onclick='postEditAnswer("+aId+")' /> "+
											"<input id='cancel_btn' class='btn' type='button' value='Cancel' /></div>";
	document.getElementById('cancel_btn').onclick=function(){document.getElementById(aId).innerHTML = originalTag;};
	document.getElementById('edit_this_answer').focus();		
}

function addQuestionDescription(qId,isEdit) {
	var prev_option = document.getElementById('question_description_to_edit').innerHTML;	
	var newInnerHTML = "<textarea id='add_description' class='donot_display_edit' style='height:100px;width:100%'>"	
	if (isEdit == 'true') {
		newInnerHTML += prev_option.trim() + "</textarea><div> <input class='btn' type='button' value='Update Description' onclick='postDescription("+qId+")' /> "
	} else {
		newInnerHTML += "</textarea><div> <input class='btn' type='button' value='Add Description' onclick='postDescription("+qId+")' /> "
	}
	newInnerHTML += "<input id='cancel_btn_description' class='btn' type='button' value='Cancel' /></div>";	
	document.getElementById('question_description_to_edit').innerHTML = newInnerHTML					
	document.getElementById('cancel_btn_description').onclick=function(){document.getElementById('question_description_to_edit').innerHTML = prev_option;};
	document.getElementById('add_description').focus();
}

function postDescription(qId) {
	var q_description = document.getElementById('add_description').value; 	
	var data = {
			q:qId,
			q_description:q_description,		
		}
	post('/postDescription',data)
}

function postEditAnswer(aId) {
	var answer = document.getElementById('edit_this_answer').value;
	var url = document.URL;
	var data = {
			aId:aId,
			answer:answer,
			url:url
		} 
	post('/updateAnswer',data);
}

