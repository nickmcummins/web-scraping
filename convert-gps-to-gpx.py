with open("waveg-buildings.gps") as f: 
    buildings = f.readlines()
    
    
def gps_to_gpx_wpt(name, lat, lon): 
    with open('waveg-buildings.gpx', "a") as f: 
        f.write('<wpt lat="' + lat + '" lon="' + lon + '">\n')
        f.write('  <name>' + name + '</name>\n')
        f.write('  <sym>Flag, Blue</sym>\n')
        f.write('</wpt>\n')
        
for building in buildings:
    buildingName = building.split("\t")[0]
    lat = building.split("\t")[1].split(",")[0]
    lon = building.split("\t")[1].split(",")[1] 
    gps_to_gpx_wpt(buildingName, lat, lon) 


        
