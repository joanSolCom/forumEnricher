
$( document ).ready(function() {

	var ajaxDone; //create a global variable called ajaxDone
	$(document).ajaxStart(function() {
	    ajaxDone = false; //by default, set the ajax as not completed each time the ajax request is sent
	    setTimeout(function() { 
	        if(!ajaxDone) $("img#loading").show();
	    }, 500);

	}).ajaxSuccess(function() {
	    ajaxDone=true;//When the ajax request finishes, it sets ajaxDone to true
	    $("img#loading").hide();
	});
	$( "#back" ).click(function() {
		window.history.back();

	});

	/**
		LATERAL BUTTONS
	**/

	$( "button.entities" ).click(function() 
	{
		$(this).parent().parent().find(".sentences_hidden").hide();
		$(this).parent().parent().find(".postFeatures_hidden").hide();
		$(this).parent().parent().find(".entity_hidden").hide();
		$(this).parent().parent().find(".coreference_hidden").hide();
		$(this).parent().parent().find(".linkedEntities_hidden").hide();
		$(this).parent().parent().find(".container").show();

		var idFileEnriched = $(this).parent().attr("id");
		var idFile = idFileEnriched.split("_")[0];

		var height = $(this).parent().parent().find(".wrapper").height();
		var width = $(this).parent().parent().find(".wrapper").width();

		$(this).parent().parent().find(".container").hide();

		$(this).parent().parent().find(".entity_hidden").height(height);

		var bgcolor = $(this).css("background-color");
		$(this).parent().parent().find(".entity_hidden").css("background-color", bgcolor)
		$(this).parent().parent().find(".entity_hidden").show();

		var that = $(this);

		$.getJSON( "http://10.80.28.153:5000/getEntityInfo?callback=?", { "idFile": idFile, "idFileEnriched":idFileEnriched} ,function( data ) {
			var stringVal = "";
			for(var i in data){
				stringVal+= " [" + data[i] + "] ";
			}
			that.parent().parent().find(".entity_hidden").text(stringVal);
		});
		

	});

	$( "button.coreferences" ).click(function()
	{
		$(this).parent().parent().find(".sentences_hidden").hide();
		$(this).parent().parent().find(".postFeatures_hidden").hide();
		$(this).parent().parent().find(".entity_hidden").hide();
		$(this).parent().parent().find(".coreference_hidden").hide();
		$(this).parent().parent().find(".linkedEntities_hidden").hide();
		$(this).parent().parent().find(".container").show();

		var idFileEnriched = $(this).parent().attr("id");
		var idFile = idFileEnriched.split("_")[0];

		var height = $(this).parent().parent().find(".wrapper").height();

		$(this).parent().parent().find(".container").hide();

		$(this).parent().parent().find(".coreference_hidden").height(height);

		var bgcolor = $(this).css("background-color");
		$(this).parent().parent().find(".coreference_hidden").css("background-color", bgcolor)
		$(this).parent().parent().find(".coreference_hidden").show();

		var that = $(this);

		$.getJSON( "http://10.80.28.153:5000/getCoreferenceInfo?callback=?", { "idFile": idFile, "idFileEnriched":idFileEnriched} ,function( data ) {
			var stringVal = "";
			for(var i in data){
				stringVal+= " [" + data[i] + "] ";
			}
			that.parent().parent().find(".coreference_hidden").text(stringVal);
		});
	});

	$( "button.linkedEntities" ).click(function() 
	{
		$(this).parent().parent().find(".sentences_hidden").hide();
		$(this).parent().parent().find(".postFeatures_hidden").hide();
		$(this).parent().parent().find(".entity_hidden").hide();
		$(this).parent().parent().find(".coreference_hidden").hide();
		$(this).parent().parent().find(".linkedEntities_hidden").hide();
		$(this).parent().parent().find(".container").show();

		var idFileEnriched = $(this).parent().attr("id");
		var idFile = idFileEnriched.split("_")[0];

		var height = $(this).parent().parent().find(".wrapper").height();

		$(this).parent().parent().find(".container").hide();

		$(this).parent().parent().find(".linkedEntities_hidden").height(height);

		var bgcolor = $(this).css("background-color");
		$(this).parent().parent().find(".linkedEntities_hidden").css("background-color", bgcolor)
		$(this).parent().parent().find(".linkedEntities_hidden").show();

		var that = $(this);

		$.getJSON( "http://10.80.28.153:5000/getLinkedEntities?callback=?", { "idFile": idFile, "idFileEnriched":idFileEnriched} ,function( data ) {
			var stringVal = "";
			for(var i in data)
			{
				stringVal+= data[i][0] + " " + data[i][1]+"<br/>";
			}
			that.parent().parent().find(".linkedEntities_hidden").html(stringVal);
		});
	});

	$( "button.sentences" ).click(function()
	{
		$(this).parent().parent().find(".sentences_hidden").hide();
		$(this).parent().parent().find(".postFeatures_hidden").hide();
		$(this).parent().parent().find(".entity_hidden").hide();
		$(this).parent().parent().find(".coreference_hidden").hide();
		$(this).parent().parent().find(".linkedEntities_hidden").hide();
		$(this).parent().parent().find(".container").show();

		var idFileEnriched = $(this).parent().attr("id");
		var idFile = idFileEnriched.split("_")[0];

		var height = $(this).parent().parent().find(".wrapper").height();

		$(this).parent().parent().find(".container").hide();

		$(this).parent().parent().find(".sentences_hidden").height(height);

		var bgcolor = $(this).css("background-color");
		$(this).parent().parent().find(".sentences_hidden").css("background-color", bgcolor)
		$(this).parent().parent().find(".sentences_hidden").show();

		var that = $(this);

		$.getJSON( "http://10.80.28.153:5000/getSentences?callback=?", { "idFile": idFile, "idFileEnriched":idFileEnriched} ,function( data ) {
			var stringVal = "";
			for(var i in data){
				stringVal+= " [" + data[i] + "]<br/>";
			}
			that.parent().parent().find(".sentences_hidden").html(stringVal);
		});
	});

	$( "button.postFeatures" ).click(function() 
	{
		$(this).parent().parent().find(".sentences_hidden").hide();
		$(this).parent().parent().find(".postFeatures_hidden").hide();
		$(this).parent().parent().find(".entity_hidden").hide();
		$(this).parent().parent().find(".coreference_hidden").hide();
		$(this).parent().parent().find(".linkedEntities_hidden").hide();
		$(this).parent().parent().find(".container").show();

		var idFileEnriched = $(this).parent().attr("id");
		var idFile = idFileEnriched.split("_")[0];
		var idPost = $(this).parent().parent().find(".container").find(".wrapper").find(".postHeader").find(".userPostHeader").find(".idPost").text();
		var height = $(this).parent().parent().find(".wrapper").height();

		$(this).parent().parent().find(".container").hide();

		$(this).parent().parent().find(".postFeatures_hidden").height(height);

		var bgcolor = $(this).css("background-color");
		$(this).parent().parent().find(".postFeatures_hidden").css("background-color", bgcolor)
		$(this).parent().parent().find(".postFeatures_hidden").show();

		var that = $(this);

		$.getJSON( "http://10.80.28.153:5000/getPostFeatures?callback=?", { "idFile": idFile, "idPost":idPost} ,function( data ) {
			var stringVal = "";
			for(var i in data)
			{
				stringVal+= data[i][0] + " " + data[i][1]+"<br/>";
			}
			that.parent().parent().find(".postFeatures_hidden").html(stringVal);
		});
	});


	$( "button.clear" ).click(function() {

		$(this).parent().parent().find(".sentences_hidden").hide();
		$(this).parent().parent().find(".postFeatures_hidden").hide();
	    $(this).parent().parent().find(".entity_hidden").hide();
		$(this).parent().parent().find(".coreference_hidden").hide();
		$(this).parent().parent().find(".linkedEntities_hidden").hide();
		$(this).parent().parent().find(".container").show();

	});

	/**
		TOP BUTTONS	
	**/

	$( "#showUserRelevance" ).click(function() {
		
		//$(".topDivs").hide();

		if($("#showUserRelevance").text() == "Show User Relevance")
		{
			$("#showUserRelevance").text("Clear User Relevance");
			var idFile = $("#threadId").attr("class");
		
			$.getJSON( "http://10.80.28.153:5000/getUserRelevance?callback=?", { "idFile": idFile} ,function( data ) {
				
				var stringRel = "";
				for(i=0;i<data.length;i++)
				{
					var userName = data[i][0];
					var relevance = data[i][1];
					stringRel+=userName+" -> "+relevance.toFixed(2) + "<br/>";
				}
				$("#userRelevance").html(stringRel);
				$("#userRelevance").show();
			});
			
		}
		else
		{
			$("#showUserRelevance").text("Show User Relevance");
			$("#userRelevance").hide();
		}


	});

	$( "#showPostRelevance" ).click(function() {
		if($("#postRelevance_0").text()=="")
		{
			var idFile = $("#threadId").attr("class");
			var max = 0;
			$.getJSON( "http://10.80.28.153:5000/getPostRelevance?callback=?", { "idFile": idFile} ,function( data ) {
				var max = data[0][1];
				var min = data[data.length-1][1];

				for(i=0;i<data.length;i++)
				{
					var idPost = data[i][0];
					var relevance = data[i][1];
					var r,g,b;
					var variable = Math.ceil((relevance*255)/max);

					r = 255;
					g = 255 - variable;
					b = 255 - variable;


					var color = "rgb("+r+","+g+","+b+")";
					console.log(color);
					$(".wrapper").css("color","black");
					//$(".wrapper").css("font-weight","bold");
					$("#postRelevance_"+idPost).parent().css("background-color",color);
					$("#postRelevance_"+idPost).text("Post Relevance: "+relevance);
				}

	   		});

	   		$("#showPostRelevance").text("Clear Post Relevance");
		}
		else{
			$("#showPostRelevance").text("Show Post Relevance");
			$(".wrapper").css("background-color","#e7f3ff");
			$(".wrapper").css("color","black");
			$(".wrapper").css("font-weight","normal");
			$(".relevanceDivs").text("");
		}
		
	});


	$( "#showRelevantConcepts" ).click(function() {
		//$(".topDivs").hide();
		if($("#showRelevantConcepts").text() == "Show Relevant Concepts")
		{
			$("#showRelevantConcepts").text("Clear Relevant Concepts");
			var idFile = $("#threadId").attr("class");
		
			$.getJSON( "http://10.80.28.153:5000/getRelevantConcepts?callback=?", { "idFile": idFile} ,function( data ) {
				
				var stringConcepts = "";
				for(i=0;i<data.length;i++)
				{
					stringConcepts += " ["+data[i]+"]<br/>";
				}
				$("#relevantConcepts").html(stringConcepts);
				$("#relevantConcepts").show();
			});
			
		}
		else
		{
			$("#showRelevantConcepts").text("Show Relevant Concepts");
			$("#relevantConcepts").hide();
		}


	});
	$( "#showUserRoles" ).click(function() {
		alert("NOT IMPLEMENTED");
	});
	$( "#showThreadFeatures" ).click(function() {
		alert("NOT IMPLEMENTED");
	});
});