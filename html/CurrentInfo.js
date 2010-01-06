//
// halo_radio - Philip J. Freeman
//

// loop_limit - number of seconds till the data reload times out.
var loop_limit=3600;

var t;
var time_started;
var timer_is_on=0;


function loadXMLDoc(url)
{
if (window.XMLHttpRequest)
{// code for IE7+, Firefox, Chrome, Opera, Safari
xmlhttp=new XMLHttpRequest();
}
else
{// code for IE6, IE5
xmlhttp=new ActiveXObject("Microsoft.XMLHTTP");
}
xmlhttp.open("GET",url,false);
xmlhttp.send(null);
document.getElementById('content').innerHTML=xmlhttp.responseText;
}

function infiniteLoop()
{
var d = new Date();
if ( d.getTime()/1000 > time_started + loop_limit )
  {
  loadXMLDoc('Timeout.html');
  return 1;
  }
loadXMLDoc('HaloRadio.cgi?action=currentInfoContent');
t=setTimeout("infiniteLoop()",5*1000);
}
function doLoop()
{
if (!timer_is_on)
  {
    var d = new Date();
    time_started = d.getTime()/1000;
    timer_is_on=1;
    infiniteLoop();
  }
  timer_is_on=0;
}
