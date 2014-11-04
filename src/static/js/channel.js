var wavs = new Array("square", "sinus", "triangle", "sawtooth");
var myChannels;
var chanelsActive;

function getSubchannelStyle (subchannels) {
	switch(subchannels) {
		case 1: return "channel_bar_size_single";
		case 2: return "channel_bar_size_double";
		case 3: return "channel_bar_size_triple";
		case 4: return "channel_bar_size_quadruple";
		case 5: return "channel_bar_size_quintuple";
		default: return "";
	}
}

//Create a channel for the piano on startup
$( document ).ready(function() {
	//Load the user configured settings
	var att = document.getElementById("attack_slider").value * 0.01;
	var dec = document.getElementById("decay_slider").value * 0.01;
	var sus = document.getElementById("sustain_slider").value * 0.01;
	var rel = document.getElementById("release_slider").value * 0.01;

	//Prepare the XML file
	var xhttp=new XMLHttpRequest();
	var xmlDocument = $.parseXML("<raw />"); 
	var channeldoc = xmlDocument.createElement('new_chan_block'); 
	channeldoc.setAttribute("size", "5");
	channeldoc.setAttribute("waveform", "3");
	channeldoc.setAttribute("attack", att);
	channeldoc.setAttribute("decay", dec);
	channeldoc.setAttribute("sustain", sus);
	channeldoc.setAttribute("release", rel);
	xmlDocument.documentElement.appendChild(channeldoc); 
	var xmldata = new XMLSerializer().serializeToString(xmlDocument);
	
	
	xhttp.onreadystatechange=function() { 
		if (xhttp.readyState != 4) return; // Not there yet
		if (xhttp.status != 200) {
			alert("Connection Failed!");
		}
		var xmlresponse = xhttp.responseXML; 
		var updateElems = xmlresponse.getElementsByTagName("channel");
		myChannels = new Array(updateElems.length);
		
		for(var i=0;i<updateElems.length;i++) { 
			myChannels[i]= updateElems[i].getAttribute("id"); 
		}
	} 

	//Send the XML File
	xhttp.open("POST","../api",true); 
	xhttp.setRequestHeader("Content-type","application/xml"); 
	xhttp.send(xmldata); 
	window.setInterval(function(){updateGUI()}, 1000);
});

function modWave (id) {

}

function addChannel (id, subchannels,waveform) {
	var headerBox = document.getElementById("channel_header_box");
	var chanelBox = document.getElementById("channel_box");
	chanelBox.setAttribute("id","channel-box-"+id);
	
	if(subchannels.length>5) {
		throw "To many subchannels";
	}
	
	var channelHeaderDiv = document.createElement('div');
	channelHeaderDiv.setAttribute("class","channel_bar_header channel_bar_header_active "
		+ getSubchannelStyle(subchannels.length));
	channelHeaderDiv.setAttribute("id","channel-header-"+id);
	var waveformIcon = document.createElement('img');
	waveformIcon.setAttribute("src","img/ico/"+wavs[waveform]+".png");
	waveformIcon.setAttribute("class","channel_bar_header_icon");
	waveformIcon.setAttribute("id","channel-header-icon-"+id);
	channelHeaderDiv.appendChild(waveformIcon);
	headerBox.appendChild(channelHeaderDiv);
	
	for(var i = 0;i < subchannels.length; i++) {
		var channelDiv = document.createElement('div'); 
		channelDiv.setAttribute("class","channel_bar");
		channelDiv.setAttribute("id","c"+subchannels[i]);
		chanelBox.appendChild(channelDiv);
	}
}

function removeChannel (id) {
	$("#chanel-box-"+id).remove();
	$("#chanel-header-"+id).remove();
}

function modChannel (id, waveform) {
	$("#chanel-header-icon"+id).setAttribute(wavs[waveform]);
}

function addNote (channel, notenumber) {
	if ($("#c"+channel).childNodes.length > 10) {
		$("#c"+channelr+" > .note_box").slice(-1).remove();
	}
	var noteDiv = document.createElement('div'); 
	noteDiv.setAttribute("class","note_box note_box_blue");
	noteDiv.innerHTML = getNoteName(notenumber);
	$("#c"+channel).appendChild(noteDiv);
}

window.addEventListener("beforeunload", function(e){
	var xhttp=new XMLHttpRequest();
	var xmlDocument = $.parseXML("<raw />"); 
	
	for (var i = 0; i < myChannels.length; i++) {
		var channeldoc = xmlDocument.createElement('close_chan');
		channeldoc.setAttribute("id", myChannels[i]);
		xmlDocument.documentElement.appendChild(channeldoc); 
	}
	var xmldata = new XMLSerializer().serializeToString(xmlDocument);
	
	xhttp=new XMLHttpRequest();
	xhttp.open("POST","../api",true); 
	xhttp.setRequestHeader("Content-type","application/xml"); 
	xhttp.send(xmldata); 
}, false);