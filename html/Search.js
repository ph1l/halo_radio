var t;
var xmlhttp=null;
var old_str="";

function showHint()
{
  str = document.getElementById("searchQueryBox").value;
  if (str.length==0)
  {
    document.getElementById("txtHint").innerHTML="";
    old_str=str;
  }
  else if (str.length > 2 &&  old_str != str )
  {
    old_str=str;
    if (window.XMLHttpRequest)
    {
      // code for IE7+, Firefox, Chrome, Opera, Safari
      xmlhttp=new XMLHttpRequest();
    }
    else
    {
      // code for IE6, IE5
      xmlhttp=new ActiveXObject("Microsoft.XMLHTTP");
    }
    var url="HaloRadio.cgi?action=searchHints&q=" + str;
    url=url+"&sid="+Math.random();
    xmlhttp.open("GET",url,false);
    xmlhttp.send(null);
    document.getElementById("txtHint").innerHTML=xmlhttp.responseText;
  }
  setTimeout("showHint()",2000);
}

