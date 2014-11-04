var keys = new Array("C1", "D1", "E1", "F1", "G1", "A1", "B1", "C2", "D2", "E2", "F2", "G2", "A2", "B2",
	"C1#" , "D1#" , "F1#" , "G1#" , "A1#" , "C2#" , "D2#" , "F2#" , "G2#" , "A2#" );

$( document ).ready(function() {
	for(var i = 0; i < keys.length; i++) {
		var keyString = keys[i];
		var keyDiv = document.getElementById(keyString);
		
		//Add Mouse Events
		keyDiv.addEventListener( 'mousedown', function(){
			onPianoKeyDown(this.id);
		}, false );
		
		keyDiv.addEventListener( 'mouseup', function(){
			onPianoKeyUp(this.id);
		}, false );
		
		//Add Touch Events
		keyDiv.addEventListener( 'touchstart', function(){
			onPianoKeyDown(this.id);
		}, false );
		
		keyDiv.addEventListener( 'touchend', function(){
			onPianoKeyUp(this.id);
		}, false );
		
		keyDiv.addEventListener("contextmenu", function (e) {
			e.preventDefault();    // Disables system menu
		}, false);
	}
});

