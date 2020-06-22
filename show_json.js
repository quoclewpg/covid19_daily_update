window.onload = function loadServers(){
	var xHttp = new XMLHttpRequest();
	xHttp.open('GET', 'new_data.json', true);

	xHttp.onload = function(){
		if(this.status == 200)
		{
			var data = JSON.parse(this.responseText);
			var table = "";
			
			for(var i = 0; i < data.length; i++)
			{
				table += "<tr><td>" + data[i].id + "</td><td>"
					  + data[i].date + "</td><td>"
					  + data[i].cases + "</td></tr>";
				document.getElementById("sortable").innerHTML = table;		
			}	
		}
	}
	xHttp.send();
}
