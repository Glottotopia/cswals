/**
	 * 
	 * Copyright by the Author. Do not use/change/ any content or parts of it without permission. Thanks.
	 * @author Hagen Jung jung@incedure.com
	 * 
 * */
// to make Y globally accessible
var Y;

// YUI 3
YUI().use('node', 'event', function (Yui) {
   var s,c=console;
   Y=Yui;
   
   // parse geocoords 
   node = Y.one('#geocoords')  
   coords = node.get('value') 
   node = Y.one('#geocenter')  
   center = node.get('value') 
   node = Y.one('#geostretch')  
   stretch = node.get('value')  
   s=INC.parseGeocoords(coords,center,stretch) 
   if(c && s)console.info('INC Maps Module: Parsed some coordinates.');
   if(c && !s)c.warn('INC Maps Module: Failed to parse some coordinates.');
    
   // init the map
   s=INC.initMap(Y.one('#geomap')._node);
   if(c && s)c.info('INC Maps Module: Initialized Google Map.');
   if(c && !s)c.warn('INC Maps Module: Failed to load Google Map.');
   
   // draw points
   s=INC.drawGeocoords();
   if(c && s)c.info('INC Maps Module: Draw geocoords.');
   if(c && !s)c.warn('INC Maps Module: Failed to draw geocoords.');
});


// Namespace Incedure : INC
INC={};
INC.util={};

/**
	 * Parses the geocoords from a string given in a format used by Sebastian Nordhoff for glottolog and stores it global
	 * @param String  s
 	 * @return boolean - success status
 * */
INC.parseGeocoords = function(coords,center,stretch){
	INC.geocoords=[];
	try{
	    var coordsarray = coords.split(';'); 
	    if (coordsarray){
		    for (var i=0,n=coordsarray.length;i<n;i++){
			    var c=coordsarray[i];
			    lls=c.split(',') 
			    if (lls.length==2){
				    var lng=parseFloat(lls[0]);
				    var lat=parseFloat(lls[1]);  
				    if(lat && lng){
					    INC.geocoords[INC.geocoords.length]=[lat,lng];
				    }
			    }
		    }
	    }
	    if (center){
		lls=center.split(',') 
		if (lls.length==2){
		    var lng=parseFloat(lls[0]);
		    var lat=parseFloat(lls[1]); 	 
		    if(lat && lng){
			    INC.center=[lat,lng];
		    }
		}
	    }
	    if (stretch){
		lls=center.split(',')  
		if (lls.length==2){
		    var lng=parseFloat(lls[0]);
		    var lat=parseFloat(lls[1]);  
		    if(lat && lng){
			    INC.stretch=[lat,lng];
		    }
		}
	    } 
	    if(INC.geocoords.length<1)return false;
	    if(INC.center.length<2)return false;
	    if(INC.stretch.length<2)return false;    
	    return true;
	}catch(err){}
	return false;
}

/**
	 * Creates a google map 
	 * @param DOM element for the map to print on
 	 * @return boolean - success status
	 * 
 * */
INC.initMap = function(domelem){
	if (GBrowserIsCompatible()) {
		try{
			// unload existing map if
			GUnload();	
			// initial properties   
			INC.map = new GMap2(domelem,{
// 				size: new GSize(domelem.offsetWidth,domelem.offsetHeight),
				size: new GSize(300,150),
				mapTypes: [G_PHYSICAL_MAP,G_SATELLITE_MAP],
				backgroundColor: '#fff', 
				key:'AIzaSyDGlzwcHFBj7uqfPbLPdA312QsscAMbDE4'
			});
			// additional properties
			INC.map.enableContinuousZoom();
			INC.map.addControl(new GMapTypeControl(), new GControlPosition(G_ANCHOR_TOP_RIGHT, new GSize(1,1)));
			INC.map.addControl(new GLargeMapControl());
			INC.map.setMapType(G_PHYSICAL_MAP);			
// 			INC.map.setCenter(new GLatLng(0, 0), 1);
// 			INC.map.setCenter(new GLatLng(INC.geocoords[0]), 1);
			a=INC.center[0]
			b=INC.center[1]
			INC.map.setCenter(new GLatLng(parseFloat(a),parseFloat(b)), 1);
			
			GEvent.addListener(INC.map, "zoomend", function(vo,vn) {
				INC.drawGeocoords();
			});
			
			return true;
		}catch(err){}
	}
	return false;
}

/**
 	* Draws coords on the map
 	* @return boolean - success status
 */
INC.drawGeocoords = function(){
	try{
// 		INC.mapClearOverlays(); 
		for(var i=0,n=INC.geocoords.length;i<n;i++){ 
			// latlng coords
			var c=INC.geocoords[i],lat=c[0],lng=c[1]; 
			var latlng = new GLatLng(lat,lng);  
			var color = '#ff0000';
			var shape = 'default';
			var radius = 3;
			var lineWidth = 1; 
			INC.util.drawShape(INC.map, latlng, INC.util.getMapPane(), color, shape, radius, lineWidth);
		}		 
		return true;
	}catch(err){}
	alert(2)
	return false;
}

/**
	 * Draws a shape on google map.
	 *
	 * @param GoogleMap map - the map
	 * @param GLatLng dot_ll - the coordinate
	 * @param HTMLElement div - the canvas to draw on
	 * @param string hexcolor - e.g.'#345f6c'
	 * @param string shape - '1','2',...
	 * @param float r  - the radius
	 * @param int stroke - the line width
	 * @param boolean hideStroke - hides the outline
	 * @param boolean hideFill - hides the filling
	 * @return void
 */
INC.util.drawShape = function(map, latlng, div, hexcolor, shape, r, stroke, hideStroke, hideFill){
	// line width
	var lw=stroke||1;
	// radius 2
	var r2=r*4/5;
	// context
	var ctx = div.getContext('2d');
	// color
	var c = INC.util.hextorgba(hexcolor,1);
	
	// transfotmations
	var p = INC.util.calcDivpixel(latlng),x=p.x,y=p.y;
	
	ctx.fillStyle = "rgba("+c.r+","+c.g+","+c.b+",1)";
	ctx.lineJoin= "miter";
	ctx.strokeStyle ="rgba(70,70,70,1)";
	ctx.lineWidth=lw;
	ctx.beginPath();
	if(shape == '1'){
		if (hideFill !== false) {
			ctx.moveTo(x - r, y + r);
			ctx.lineTo(x, y - r / 2);
			ctx.lineTo(x + r, y + r);
			ctx.lineTo(x - r, y + r);
			ctx.fill();
		}
		if (hideStroke !== false) {
			ctx.moveTo(x-r, y+r);
			ctx.lineTo(x, y-r/2);
			ctx.lineTo(x+r, y+r);
			ctx.lineTo(x-r, y+r);
			ctx.stroke();
		}
	}
	else if(shape == '2'){
		if (hideFill !== false) {
			ctx.moveTo(x - r, y - r);
			ctx.lineTo(x, y + r / 2);
			ctx.lineTo(x + r, y - r);
			ctx.lineTo(x - r, y - r);
			ctx.fill();
		}
		if (hideStroke !== false) {
			ctx.moveTo(x-r, y-r);
			ctx.lineTo(x, y+r/2);
			ctx.lineTo(x+r, y-r);
			ctx.lineTo(x-r, y-r);
			ctx.stroke();
		}
	}
	else if(shape == '3'){
		if (hideFill !== false) {
			ctx.moveTo(x - r2, y - r2);
			ctx.lineTo(x + r2, y - r2);
			ctx.lineTo(x + r2, y + r2);
			ctx.lineTo(x - r2, y + r2);
			ctx.lineTo(x - r2, y - r2);
			ctx.fill();
		}
		if (hideStroke !== false) {
			ctx.moveTo(x-r2, y-r2);
			ctx.lineTo(x+r2, y-r2);
			ctx.lineTo(x+r2, y+r2);
			ctx.lineTo(x-r2, y+r2);
			ctx.lineTo(x-r2, y-r2);
			ctx.stroke();
		}
	}
	else if(shape=='4'){
		if (hideFill!== false) {
			ctx.moveTo(x, y - r);
			ctx.lineTo(x + r, y);
			ctx.lineTo(x, y + r);
			ctx.lineTo(x - r, y);
			ctx.lineTo(x, y - r);
			ctx.fill();
		}
		if (hideStroke !== false) {
			ctx.moveTo(x,y-r);
			ctx.lineTo(x+r,y);
			ctx.lineTo(x,y+r);
			ctx.lineTo(x-r,y);
			ctx.lineTo(x,y-r);
			ctx.stroke();
		}
	}
	else {
		// circle as default
		if (hideFill !== false) {
			ctx.arc(x, y, r, 0, Math.PI * 2, 0);
			ctx.fill();
		}
		if (hideStroke !== false) {
			ctx.arc(x, y, r, 0, Math.PI * 2, 0);
			ctx.stroke();
		}		
	}
	ctx.closePath()
			
		
}

/**
	 * Converts a hex coded String and an alpha value into a self coed rgba object
	 * @param string h - the hexvaule string
	 * @param float a - the alpha value [0-1]
	 * @return Object: {r,g,b,a}
 */
INC.util.hextorgba=function(h,a){
	if(!h){return{r:0,g:0,b:0,a:1}}
	var r={a:a}
	h=""+h // microsoft hack
	if(h.substring(0,1)=='#'){h=h.substring(1,h.length);};
	if(h.length==3){
		r.r=parseInt(h.substring(0,1),8);
		r.g=parseInt(h.substring(1,2),8);
		r.b=parseInt(h.substring(2,3),8);
	}else{
		r.r=parseInt(h.substring(0,2),16);
		r.g=parseInt(h.substring(2,4),16);
		r.b=parseInt(h.substring(4,6),16);
	}
	return r;
}

/**
	 * Fetches the Canvas to draw on
	 * @return HTMLCanvasElement  - the canvas
 */
INC.util.getMapPane = function(){
	
	// overlaypane with two canvases below
	var op = INC.util.ensureINCDrawingCanvases();
	//canvases
	var c = op.getElementsByTagName('canvas');
			
	if(c && c[0]) return c[0];
	return null;
}	

/**
	 * Ensures and returns two canvases to draw on polygons
	 * @return GOverLayPane  - with two canvases to draw on
 */
INC.util.ensureINCDrawingCanvases = function(){
		// find the google layer
		var op = INC.map.getPane(G_MAP_OVERLAY_LAYER_PANE);
		
		if (op.getElementsByTagName('canvas').length <2) {	
			
			// delete not main canvases
			if((cs=op.getElementsByTagName('canvas'))){
				for(var i=0,n=cs.length;i<n;i++){
					if(cs.context!="support"){
						op.removeChild(cs[0]);
					}
				}
			}
			
			// find the  visible google clip
			var ct = op.parentNode.parentNode.parentNode
			// measure the size
			var h = ct.offsetHeight
			var w = ct.offsetWidth
			// measure the offset from a new canvas layer around the visible clip to google layer
			var ox=0, oy=0;
			if( op && ct && (off=INC.util.getOffsetsTo(op,ct))){
				ox = off[0]+w;oy = off[1]+h;
			}
			INC.util.divmapOffsetBounds=[ox,oy,3*w,3*h];
		
			// create new canvases
			var ca = INC.util.appendCanvas(op,3*w,3*h);
			ca.style.position="absolute";
			ca.style.overflow = "visible";
			ca.setAttribute('zIndex', '0');
			ca.setAttribute('context', 'support');
			ca.style.left = -ox;
			ca.style.top = -oy;
			var hover =INC.util.appendCanvas(op,3*w,3*h);
			hover.style.position="absolute";
			hover.style.overflow = "visible";
			hover.setAttribute('context', 'support');
			hover.setAttribute('zIndex', '2');
			hover.style.left = -ox;
			hover.style.top =-oy;
		}
		return op;
	}

/**
	 * Appends a convas to a HTMLDivElement
	 * @param HTMLDivElement dom
	 * @param int w -the width of the new canvas
	 * @param int h - the height of the new canvas
	 * @return HTMLCanvasElement
 * */
INC.util.appendCanvas=function(dom,w,h){
	var can = document.createElement("canvas");
	can.setAttribute('width', w);
	can.setAttribute('height', h);
	if (typeof G_vmlCanvasManager != 'undefined') {
		G_vmlCanvasManager.initElement(can);
	}
	dom.appendChild(can);
	return can;
};

/**
	 * Calulates the offset X an Y value of two html Elements. Pay attention to the conditions. Recursion would never stop (not catched)
	 * @param HTMLElement  el - an element that must be a descendant of ct
	 * @param HTMLElement ct - an element that must be an ancestor of el
	 * @return Array - obj[0] = xoffset, obj[1] = yoffset
 * */
INC.util.getOffsetsTo = function(el,ct,result){
	if (el==ct)return result
	if (!result){
		result=[el.offsetLeft,el.offsetTop];
	}
	result[0]+=el.offsetLeft;
	result[1]+=el.offsetTop;
	return INC.util.getOffsetsTo(el.parentNode,ct,result);
}

/**
	 * Transforms a GLatLng object into a divpixel object
	 * @param GLatLng latlng
	 * @return Point p {x:float,x:float}
 * */
INC.util.calcDivpixel =function(latlng){
		
	var pixel = INC.map.fromLatLngToDivPixel(latlng);
	
	// because the canvas is expanded in all directions(biger than the visible part that google shows) and therfore does not follows the google divpixelcalulation for the visible part
	pixel.x+=INC.util.divmapOffsetBounds[0];
	pixel.y+=INC.util.divmapOffsetBounds[1];
			
			
	return pixel;
}

/**
 * Clears the canvases
 * @return void
 */
INC.mapClearOverlays = function(){
	if (INC.map) {
		// clear to google pane with google functionality
		INC.map.clearOverlays();
		
		// clear own canvas panes
		var op = INC.map.getPane(G_MAP_OVERLAY_LAYER_PANE);
		while (op.hasChildNodes()) {
			op.removeChild(op.lastChild);
		}
	}
}