function getGrid(){
    grid = []
    for (var i=0; i<9; i++){
        grid.push(document.getElementById(i.toString()).innerHTML);
    }
    console.log(grid)
    return grid
}
function setGrid(grid){
    console.log(grid)
    winner = grid['winner']
    grid = grid['grid']
    
    for (var i=0; i<9; i++){
	document.getElementById(i.toString()).innerHTML = grid[i];
    }
    /*
    if (winner==''){ // empty string is tie
	document.getElementById("winner").innerHTML = "TIE"
    } else if (winner!=' '){
	document.getElementById("winner").innerHTML = "Winner: "+winner
    }*/
}

function maybeSendPost(index){
    if (document.getElementById(index.toString()).innerHTML != ' '){
	return null
    }
    if (document.getElementById("winner").innerHTML!=''){
	return null
    }
    document.getElementById(index.toString()).innerHTML = 'X';
    // send post request

    /*
    $.post(
	"/ttt/play",
	JSON.stringify( {"grid":getGrid()}),
	function(data) {
	    setGrid(data);
	}
	);*/
    // new post: Send move instead
    console.log("Cool")
    $.post(
	"/ttt/play",
	JSON.stringify( {"move":index}),
	function(data) {
	    setGrid(data);
	}
    );
}

// can't use a for loop, because of Javascript Scope to add eventListeners....
document.getElementById('0').addEventListener("click", function(){ maybeSendPost(0) });
document.getElementById('1').addEventListener("click", function(){ maybeSendPost(1) });
document.getElementById('2').addEventListener("click", function(){ maybeSendPost(2) });
document.getElementById('3').addEventListener("click", function(){ maybeSendPost(3) });
document.getElementById('4').addEventListener("click", function(){ maybeSendPost(4) });
document.getElementById('5').addEventListener("click", function(){ maybeSendPost(5) });
document.getElementById('6').addEventListener("click", function(){ maybeSendPost(6) });
document.getElementById('7').addEventListener("click", function(){ maybeSendPost(7) });
document.getElementById('8').addEventListener("click", function(){ maybeSendPost(8) });




/*
for (var i=0; i<9; i++){
    console.log(i.toString())
    x = i
    document.getElementById(i.toString()).addEventListener("click", function(){ maybeSendPost(i) });
}*/

							  

