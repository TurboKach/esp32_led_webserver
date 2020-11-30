function setColor(white_value=undefined) {
    let color = document.getElementById('rgb-picker').value;

    console.log(white_value)
    if (white_value !== undefined) {
        color = '000000'+ white_value
    }
    console.log(color)
    let url = '?color=' + color;
    httpGet(url);
}

function update(picker) {
    document.getElementById('hex-str').innerHTML = picker.toHEXString();
    document.getElementById('rgb-str').innerHTML = picker.toRGBString();
    let HEXcolor = picker.toHEXString();
    let RGBcolor = picker.toRGBString();
    console.log(HEXcolor);
    console.log(RGBcolor);
    console.log(picker.toHEXString());

    document.getElementById('rgb').innerHTML =
        Math.round(picker.rgb[0]) + ', ' +
        Math.round(picker.rgb[1]) + ', ' +
        Math.round(picker.rgb[2]);

    document.getElementById('hsv').innerHTML =
        Math.round(picker.hsv[0]) + '&deg;, ' +
        Math.round(picker.hsv[1]) + '%, ' +
        Math.round(picker.hsv[2]) + '%';

    let url = '?color=' + picker.toHEXString().slice(1);
    httpGet(url);
}

function httpGet(theUrl) {
    let xmlHttp = new XMLHttpRequest();
    xmlHttp.open( "GET", theUrl, true ); // false for synchronous request
    xmlHttp.send( null );
    return xmlHttp.responseText;
}