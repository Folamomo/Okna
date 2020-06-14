import bpy
import os
from math import *
from mathutils import *
from random import *

#Parameters
save_path = 'D:/Render/model1/side3/'
#camera object
camera = bpy.data.objects["Camera"]
selectedGroups = ["Okno5", "Okno6"]
#object containing selected groups (if multiple
ob = bpy.data.objects["Cottage_Free"]
#Target for camera
lookAt = Vector((0.0, 0.0, 1.0))
#Possible camera locations
xmin = 15.0
xmax = 30.0
ymin = -30.0
ymax = -15.0
zmin = 0.10
zmax = 3.0
#Number of locations to render
amount = 25


def render(name):
    bpy.context.scene.render.image_settings.file_format = 'PNG'
    bpy.context.scene.render.filepath = name + ".png"
    bpy.ops.render.render(write_still = True)

def setCamera():
    x = xmin + random() * (xmax - xmin)
    y = ymin + random() * (ymax - ymin)
    z = zmin + random() * (zmax - zmin)
    roll = -10.0 + 20.0 * random()
    
    camera.location = Vector((x, y, z))
    bpy.context.view_layer.update()
    
    loc_camera = camera.matrix_world.to_translation()

    direction = lookAt - loc_camera
    # point the cameras '-Z' and use its 'Y' as up
    rot_quat = direction.to_track_quat('-Z', 'Y')

    # assume we're using euler rotation
    camera.rotation_euler = rot_quat.to_euler()
    camera.rotation_euler[1] = radians(roll)
    bpy.context.view_layer.update()

def moveCameraRight(by):
    right = camera.matrix_world.to_quaternion() @ Vector((by, 0.0, 0.0))
    camera.location += right
    bpy.context.view_layer.update()
    
def inOrder(corners):
    center = sum(corners, Vector((0.0, 0.0, 0.0)))/4
    for c in corners:
        if c.x < center.x and c.z > center.z:
            lg = c
        elif c.x > center.x and c.z > center.z:
            pg = c
        if c.x < center.x and c.z < center.z:
            ld = c
        elif c.x > center.x and c.z < center.z:
            pd = c
    return [lg, pg, ld, pd]

def saveNumbers(file, i):
    if i != 0: file.write(", ")
    file.write("{ ")
    file.write("'leftEye' : 'left" + str(i) + ".png',\n")
    file.write("'rightEye' : 'right" + str(i) + ".png',\n")
    cameraTilt = camera.rotation_euler[0]
    file.write("'tilt' : " + str(cameraTilt) + ",\n")
    cameraRoll = camera.rotation_euler[1]
    file.write("'roll' : " + str(cameraRoll) + ",\n")
    cameraPan =  camera.rotation_euler[2]
    rot = Matrix.Rotation(-cameraPan, 4, 'Z')
    file.write("'windows' : [")
    for name in selectedGroups:
        corners = []
        index = ob.vertex_groups[name].index
        for v in ob.data.vertices:
            for g in v.groups:
                if g.group == index:
                    corner = rot @ ((ob.matrix_world @ v.co) - camera.matrix_world.translation)
                    corners.append(corner)
        if len(corners) != 4:
            print("Invalid corner count in group", name, len(corners), "expected 4")
        corners = inOrder(corners)
        for corner in corners:
            if i != 0: file.write(", ")
            file.write("[" + str(corner.x) + ", " + str(corner.y) + ", " + str(corner.z) +"]")
        file.write("\n")
    file.write("]\n}\n")



try:
    os.makedirs(save_path)
except FileExistsError:
    print("Directory already exists") 
         
with open(save_path + 'out.json', 'w+') as file:
    file.write("[")
    for i in range(amount):
        setCamera()
        print("rendering left #", i)
        render(save_path + "left" + str(i))
        saveNumbers(file, i)
        moveCameraRight(0.1)
        print("rendering right #", i)
        render(save_path + "right" + str(i))
    file.write("]")

print("Sucess!")