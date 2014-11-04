var isPianoActive = false;
var isSliderActive = false;

function togglePiano() {
	var pianoBox = document.getElementById("piano_box");
	var sliderBox = document.getElementById("slider_box");
	pianoBox.style.visibility = "visible";
	sliderBox.style.visibility = "hidden";
}

function toggleSlider() {
	var pianoBox = document.getElementById("piano_box");
	var sliderBox = document.getElementById("slider_box");
	pianoBox.style.visibility = "hidden";
	sliderBox.style.visibility = "visible";
}
