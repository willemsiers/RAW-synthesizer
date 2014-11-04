var current_id = 0;

function updateGUI () {
	
	var xhttp=new XMLHttpRequest();
	xhttp.onreadystatechange=function() { 
		if (xhttp.readyState != 4) return; // Not there yet
		if (xhttp.status != 200) {
			alert("Connection Failed!");
		}
		var xmlresponse = xhttp.responseXML; 
		var updateElems = xmlresponse.getElementsByTagName("changeset")[0].childNodes;
		
		for(var i=0;i<updateElems.length;i++) { 
			console.log(updateElems[i].localName);
		}
	} 

	//Send the XML File
	xhttp.open("GET","../api?id"+current_id,true); 
	xhttp.setRequestHeader("Content-type","application/xml"); 
	xhttp.send(); 
}