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
	    if ($file != '.' && $file != '..') {
	    	echo "<div class='link'><a href='showThread.php?thread=".$file."'>".$file."</a></div>";
	    }
	}	
	echo "</div>";
?>


</body>
</html>