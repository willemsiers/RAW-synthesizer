var octave = 2; //The ammount of octaves added to the key

function onPianoKeyDown (key) {		
	var xmlDocument = $.parseXML("<raw />"); 
	var eventdoc = xmlDocument.createElement('key_down'); 
	eventdoc.setAttribute("note", getMidiNumber(key));
	eventdoc.setAttribute("chan", myChannels[0]);
	eventdoc.setAttribute("vol", "1");
	xmlDocument.documentElement.appendChild(eventdoc); 
	var xmldata = new XMLSerializer().serializeToString(xmlDocument);
	
	xhttp=new XMLHttpRequest();
	xhttp.open("POST","../api",true); 
	xhttp.setRequestHeader("Content-type","application/xml"); 
	xhttp.send(xmldata); 
}

function onPianoKeyUp (key) {
	var xmlDocument = $.parseXML("<raw />"); 
	var eventdoc = xmlDocument.createElement('key_up');
	eventdoc.setAttribute("chan", myChannels[0]);
	xmlDocument.documentElement.appendChild(eventdoc); 
	var xmldata = new XMLSerializer().serializeToString(xmlDocument);
	
	xhttp=new XMLHttpRequest();
	xhttp.open("POST","../api",true); 
	xhttp.setRequestHeader("Content-type","application/xml"); 
	xhttp.send(xmldata); 
}

function modOctave (amount) {
	if(octave + amount >= 0 && octave + amount <= 6) {
		octave = octave + amount;
	}
}


function getMidiNumber (key) {
	var value;
	switch(key) {
		case "C1" :	value = 0;	break;
		case "C1#":	value = 1;	break;
		case "D1" :	value = 2;	break;
		case "D1#":	value = 3;	break;
		case "E1" :	value = 4;	break;
		case "F1" :	value = 5;	break;
		case "F1#":	value = 6;	break;
		case "G1" :	value = 7;	break;
		case "G1#":	value = 8;	break;
		case "A1" :	value = 9;	break;
		case "A1#":	value = 10;	break;
		case "B1" :	value = 11;	break;
		case "C2" :	value = 12;	break;
		case "C2#":	value = 13;	break;
		case "D2" :	value = 14;	break;
		case "D2#":	value = 15;	break;
		case "E2" :	value = 16;	break;
		case "F2" :	value = 17;	break;
		case "F2#":	value = 18;	break;
		case "G2" :	value = 19;	break;
		case "G2#":	value = 20;	break;
		case "A2" :	value = 21;	break;
		case "A2#":	value = 22;	break;
		case "B2" :	value = 23;	break;
		default: return 0;
	}
	return value + octave * 12;
}




