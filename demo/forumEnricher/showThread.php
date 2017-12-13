<img id="loading"/>
<?php
		require_once("header.php");
?>	
		<div id="buttonWrapper">
			<button id= 'back' type='button' class='btn btn-primary'> &#8612; Back</button>
			<button id='showPostRelevance' type='button' class='topButton btn btn-danger'>Show Post Relevance</button>
			<button id='showUserRelevance' type='button' class='topButton btn btn-warning'>Show User Relevance</button>
			<!--<button id='showUserRoles' type='button' class='topButton btn btn-success'>Show User Roles</button>!-->
			<button id='showRelevantConcepts' type='button' class='topButton btn btn-purple'>Show Relevant Concepts</button>
		</div>
		<div class="topDivs" id="userRelevance" class="col-md-12"></div>
		<div class="topDivs" id="userRoles" class="col-md-12"></div>
		<div class="topDivs" id="relevantConcepts" class="col-md-12"></div>



<div id="content">
<?php
		$file = $_GET["thread"];

		$string = file_get_contents('./json/'.$file);
		$json_a = json_decode($string, true);
		$i=0;
		echo "<div id='threadId' class='".$json_a[0]["idFile"]."'></div>";
		foreach($json_a as $json_elem)
		{
			echo "<div class='total_container col-md-12'>";
				echo "<div class='hiddenBoxes entity_hidden col-md-8'></div>";
				echo "<div class='hiddenBoxes coreference_hidden col-md-8'></div>";
				echo "<div class='hiddenBoxes linkedEntities_hidden col-md-8'></div>";
				echo "<div class='hiddenBoxes postFeatures_hidden col-md-8'></div>";
				echo "<div class='hiddenBoxes sentences_hidden col-md-8'></div>";

				echo "<div id='".$json_elem["user"]."'></div>";
				echo "<div class='container col-md-8'>";
					echo "<div class = 'wrapper'>";
							echo "<div class='postHeader'><div class='userPostHeader'><span class='idPost' style='border-radius:70%; border:solid black 3px;padding:3px'><b>".$i."</span> ".$json_elem["user"]."</b></div> <div class='datePostHeader'>".$json_elem["date"]."</div></div>";
						
						if($json_elem["citation"] != "")
						{
							echo "<p class='citation'>".$json_elem["citation"];
						}
						

						echo "<p class='postContent'>".$json_elem["post"];
						echo "</p>";
						echo "<div class='relevanceDivs' id='postRelevance_".$i."'></div>";
				
					echo "</div>";
				
				echo "</div>";
				echo "<div id='".$json_elem["idFileEnriched"]."' class = 'col-md-4 button_pannel'>";

?>
				
				<button type="button" class="col-md-6 btn btn-primary entities">Entities</button>
				<button type="button" class="col-md-6 btn btn-success coreferences">Coreferences</button>
				<button type="button" class="col-md-6 btn btn-warning linkedEntities">Linked Entities</button>
				<button type="button" class="col-md-6 btn btn-default sentences">Sentences</button>
				<button type="button" class="col-md-12 btn btn-black postFeatures">Post Features</button>
				<button type="button" class="col-md-12 btn btn-danger clear">Clear</button>
<?php
				echo "</div>";
			echo "</div>";
			$i++;
		}

?>

</div>