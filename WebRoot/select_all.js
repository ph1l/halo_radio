function checkall(formname,checkname,thestate){
var el_collection=eval("document.forms."+formname+"."+checkname);
el_collection.checked=thestate;
for ( c = 0; c < el_collection.length; c++) {
        el_collection[c].checked=thestate;
	}
}


