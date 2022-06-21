import json
from PIL import Image,ImageDraw


#Read the Json, and append make List with Polygons and their countries, if Country has no ISO code, dont append it
polygons = []
with open("countries.json") as f:
    file = json.load(f)
    for country in file:

        coords = country["fields"]["geo_shape"]["coordinates"]
        try:
            code = country["fields"]["iso_3166_1_alpha_2_codes"]
        except KeyError:
            pass
        else:
            for polygon in coords:
                #For some reason some lists are different so I did this, let me know if its stupid
                if type(polygon[0][0]) == float:
                    polygons.append([polygon,code])
                elif type(polygon[0][0][0]) == float:
                    polygons.append([polygon[0],code])
                else:
                    print("Error")



#Size of the World Map (from -180 to 180, from -90 to 90)
size = (180,90)
#How much Pixels is in one degree
multiplier = 100
#Create Empty Map, Color is the Color of the sea and and the borders
map = Image.new("RGBA",(size[0]*2*multiplier,size[1]*2*multiplier),(0,105,148))

#Convert Longitude and Latitude to Image Coordinates
def to_coords(coordinates):
    latitude, longitude = coordinates
    return (int((latitude + 180) * multiplier), int((-longitude + 90) * multiplier))

#Get Box of the Polygon (Corner x and y, width and height)
def get_box(polygon):
    x1,y1,x2,y2 = min([x[0] for x in polygon]),min([y[1] for y in polygon]),max([x[0] for x in polygon]),max([y[1] for y in polygon])
    return [x1,y1,x2-x1,y2-y1]

#Draw Shapes
for polygon,code in polygons:
    #Just to keep track
    print(code)
    #Convert all coordinates to pixel coordinates
    polygon = [to_coords(coords) for coords in polygon]
    #Get the Box values
    x,y,w,h = get_box(polygon)
    if w == 0 or h == 0:
        print("Island/Country too small")
    else:
        #Create Mask for the Flag
        mask = Image.new("L",(w,h),0)
        draw_mask = ImageDraw.Draw(mask)
        draw_mask.polygon([(coordinates[0]-x,coordinates[1]-y) for coordinates in polygon],outline="black",fill="white")


        #Open The Flag, resize, and paste on the map
        flag = Image.open(f".\\flags\{code.lower()}.png").resize((w,h))
        map.paste(flag,(x,y),mask)

#Show and save the Map
map.show()
map.save("map.png")