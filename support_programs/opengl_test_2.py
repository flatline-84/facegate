import pygame
from pygame.locals import *
import math

from OpenGL.GL import *
from OpenGL.GLU import *

# http://www.petercollingridge.co.uk/tutorials/3d/pygame/using-matrices/

"""Node Object"""
class Node:
    # Node in 3D space. Between -1 -> 1
    def __init__(self, coordinates):
        self.x = coordinates[0]
        self.y = coordinates[1]
        self.z = coordinates[2]

"""Edge Object"""    
class Edge:
    # Links up two nodes
    def __init__(self, start, stop):
        self.start = start
        self.stop  = stop

"""Main Wireframe Object"""
class Wireframe:
    def __init__(self):
        self.nodes = []
        self.edges = []

    """Adding parts"""
    def addNodes(self, nodeList):
        for node in nodeList:
            self.nodes.append(Node(node))
    def addEdges(self, edgeList):
        for (start, stop) in edgeList:
            self.edges.append(Edge(self.nodes[start], self.nodes[stop]))
    
    """Modifications"""
    def translate(self, axis, d):
        #Translate each node of a wireframe by d along a given axis.
        if axis in ['x', 'y', 'z']:
            for node in self.nodes:
                setattr(node, axis, getattr(node, axis) + d)
    def scale(self, centre_x, centre_y, scale):
        # Scale the wireframe from the centre of the screen.
        for node in self.nodes:
            node.x = centre_x + scale * (node.x - centre_x)
            node.y = centre_y + scale * (node.y - centre_y)
            node.z *= scale
    def rotateZ(self, centre, radians):
        cx,cy,cz = centre        
        for node in self.nodes:
            x      = node.x - cx
            y      = node.y - cy
            d      = math.hypot(y, x)
            theta  = math.atan2(y, x) + radians
            node.x = cx + d * math.cos(theta)
            node.y = cy + d * math.sin(theta)
    def rotateX(self, centre, radians):
        cx,cy,cz = centre  
        for node in self.nodes:
            y      = node.y - cy
            z      = node.z - cz
            d      = math.hypot(y, z)
            theta  = math.atan2(y, z) + radians
            node.z = cz + d * math.cos(theta)
            node.y = cy + d * math.sin(theta)
    def rotateY(self, centre, radians):
        cx,cy,cz = centre  
        for node in self.nodes:
            x      = node.x - cx
            z      = node.z - cz
            d      = math.hypot(x, z)
            theta  = math.atan2(x, z) + radians
            node.z = cz + d * math.cos(theta)
            node.x = cx + d * math.sin(theta)


    """Debugging output"""
    def findCentre(self):
        """ Find the centre of the wireframe. """
        num_nodes = len(self.nodes)
        meanX = sum([node.x for node in self.nodes]) / num_nodes
        meanY = sum([node.y for node in self.nodes]) / num_nodes
        meanZ = sum([node.z for node in self.nodes]) / num_nodes
        return (meanX, meanY, meanZ)

    def outputNodes(self):
        print ("\n --- Nodes --- ")
        for i, node in enumerate(self.nodes):
            print (" %d: (%.2f, %.2f, %.2f)" % (i, node.x, node.y, node.z))   
    def outputEdges(self):
        print ("\n --- Edges --- ")
        for i, edge in enumerate(self.edges):
            print (" %d: (%.2f, %.2f, %.2f) to (%.2f, %.2f, %.2f)" % (i, edge.start.x, edge.start.y, edge.start.z, edge.stop.x,  edge.stop.y,  edge.stop.z))


class ProjectionViewer:
    """ Displays 3D objects on a Pygame screen """
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption('Arm Simulation')
        self.background = (10,10,50)
        self.wireframes = {} #hold object dictionary to draw
        self.displayNodes = True
        self.displayEdges = True
        self.nodeColour = (255,255,255)
        self.edgeColour = (200,200,200)
        self.nodeRadius = 4

        self.key_to_function = {
            pygame.K_LEFT:   (lambda x: x.translateAll('x', -10)),
            pygame.K_RIGHT:  (lambda x: x.translateAll('x',  10)),
            pygame.K_DOWN:   (lambda x: x.translateAll('y',  10)),
            pygame.K_UP:     (lambda x: x.translateAll('y', -10)),
            pygame.K_EQUALS: (lambda x: x.scaleAll(1.25)),
            pygame.K_MINUS:  (lambda x: x.scaleAll( 0.8)),
            pygame.K_q: (lambda x: x.rotateAll('X',  0.1)),
            pygame.K_w: (lambda x: x.rotateAll('X', -0.1)),
            pygame.K_a: (lambda x: x.rotateAll('Y',  0.1)),
            pygame.K_s: (lambda x: x.rotateAll('Y', -0.1)),
            pygame.K_z: (lambda x: x.rotateAll('Z',  0.1)),
            pygame.K_x: (lambda x: x.rotateAll('Z', -0.1))
            }


    def run(self):
        """ Create a pygame screen until it is closed. """
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            
                elif event.type == pygame.KEYDOWN:
                    if event.key in self.key_to_function:
                        # print("Got event:", event.key)
                        self.key_to_function[event.key](self)

            self.screen.fill(self.background)
            self.display()

            pygame.display.flip()

    def addWireframe(self, name, wireframe):
        #Add a named wireframe object.
        self.wireframes[name] = wireframe
    def translateAll(self, axis, d):
        # Translate all wireframes along a given axis by d units.
        for wireframe in self.wireframes.values():
            wireframe.translate(axis, d)
    def scaleAll(self, scale):
        # Scale all wireframes by a given scale, centred on the centre of the screen.
        centre_x = self.width/2
        centre_y = self.height/2
        for wireframe in self.wireframes.values():
            wireframe.scale(centre_x, centre_y, scale)
    def rotateAll(self, axis, theta):
        # Rotate all wireframe about their centre, along a given axis by a given angle.
        rotateFunction = 'rotate' + axis
        centre = (320, 240, 320) #centre of window
        for wireframe in self.wireframes.values():
            # centre = wireframe.findCentre()
            getattr(wireframe, rotateFunction)(centre, theta)

    def display(self):
        #Draw the wireframes on the screen.
        self.screen.fill(self.background)
        for wireframe in self.wireframes.values():
            if self.displayEdges:
                for edge in wireframe.edges:
                    pygame.draw.aaline(self.screen, self.edgeColour, (edge.start.x, edge.start.y), (edge.stop.x, edge.stop.y), 1)
            if self.displayNodes:
                for node in wireframe.nodes:
                    pygame.draw.circle(self.screen, self.nodeColour, (int(node.x), int(node.y)), self.nodeRadius, 0)


if __name__ == '__main__':
    base = Wireframe()
    base.addNodes([(x ,y, z) for x in (270, 330) for y in (310, 370) for z in (270, 330)])
    base.addEdges([(n,n+4) for n in range(0,4)]+[(n,n+1) for n in range(0,8,2)]+[(n,n+2) for n in (0,1,4,5)])

    # shoulder, elbow, wrist, fingers
    shoulder = Wireframe()
    shoulder.addNodes([(x ,y, z) for x in (280, 320) for y in (240, 320) for z in (280, 320)])
    shoulder.addEdges([(n,n+4) for n in range(0,4)]+[(n,n+1) for n in range(0,8,2)]+[(n,n+2) for n in (0,1,4,5)])

    elbow = Wireframe()
    elbow.addNodes([(x ,y, z) for x in (280, 320) for y in (180, 250) for z in (280, 320)])
    elbow.addEdges([(n,n+4) for n in range(0,4)]+[(n,n+1) for n in range(0,8,2)]+[(n,n+2) for n in (0,1,4,5)])

    wrist = Wireframe()
    wrist.addNodes([(x ,y, z) for x in (285, 315) for y in (120, 190) for z in (285, 315)])
    wrist.addEdges([(n,n+4) for n in range(0,4)]+[(n,n+1) for n in range(0,8,2)]+[(n,n+2) for n in (0,1,4,5)])

    hand = Wireframe()
    hand.addNodes([(x ,y, z) for x in (260, 340) for y in (100, 125) for z in (290, 310)])
    hand.addEdges([(n,n+4) for n in range(0,4)]+[(n,n+1) for n in range(0,8,2)]+[(n,n+2) for n in (0,1,4,5)])

    pv = ProjectionViewer(640,480)
    pv.addWireframe('base', base)
    pv.addWireframe('shoulder', shoulder)
    pv.addWireframe('elbow', elbow)
    pv.addWireframe('wrist', wrist)
    pv.addWireframe('hand', hand)

    pv.run()