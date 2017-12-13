<?php
	require_once("header.php");
?>

<body>

<h1></h1>
<?php
	$files = scandir('./json/');
	echo "<div id='main_container'>";
	echo "<h1>Forum Threads</h1>";

	foreach ($files as $file) {
	    if ($file != '.' && $file != '..') 
	    {
    	
	    	$files_in_directory = scandir("./enriched/".$file."/");
			$items_count = count($files_in_directory);
			if ($items_count > 2)
			{
				echo "<div class='link'><a href='showThread.php?thread=".$file."'>".$file."</a></div>";
			}
	    }
	}	
	echo "</div>";
?>


</body>
</html>