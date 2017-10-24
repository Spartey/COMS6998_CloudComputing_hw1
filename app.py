from flask import Flask
from flask import render_template

app = Flask(__name__)
@app.route('/hello')
def hello():
    return """
<!DOCTYPE html>
<html>
<head>
<script src="http://maps.googleapis.com/maps/api/js?key=AIzaSyBzE9xAESye6Kde-3hT-6B90nfwUkcS8Yw&sensor=false">
</script>

<script>
function initialize()
{
    var mapProp = {
        center:new google.maps.LatLng(27.8188024,-7.3606365),
        zoom:2,
        mapTypeId:google.maps.MapTypeId.ROADMAP
    };
    var map=new google.maps.Map(document.getElementById("googleMap"), mapProp);
}
 
google.maps.event.addDomListener(window, 'load', initialize);
</script>
</head>
 
<body>
<div id="googleMap" style="width:1000px;height:600px;"></div>
 
</body>
</html>
"""

if __name__ == '__main__':
    app.run()