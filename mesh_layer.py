﻿import bpy
import bmesh
from .ui_constants import *
from bpy.props import StringProperty, BoolProperty, IntProperty, CollectionProperty, FloatProperty, PointerProperty
from bgl import *
from mathutils import *
from math import *

def AddPathMeshLayers(bm):
    bm.verts.layers.float.new(NODE_WIDTH)
    bm.verts.layers.int.new(NODE_BAHAVIOUR)
    bm.verts.layers.int.new(NODE_ISDEADEND)
    bm.verts.layers.int.new(NODE_ISIGNORED)
    bm.verts.layers.int.new(NODE_ISROADBLOCK)
    bm.verts.layers.int.new(NODE_ISEMERGENCYVEHICLEONLY)
    bm.verts.layers.int.new(NODE_ISRESTRICTEDACCESS)
    bm.verts.layers.int.new(NODE_ISDONTWANDER)
    bm.verts.layers.int.new(NODE_SPEEDLIMIT)
    bm.verts.layers.int.new(NODE_SPAWNPROBABILITY)
    
    bm.verts.layers.string.new(NODE_TYPE)
    bm.verts.layers.int.new(NODE_AREAID)
    bm.verts.layers.int.new(NODE_ID)
    bm.verts.layers.int.new(NODE_FLOOD)

    bm.edges.layers.float.new(EDGE_WIDTH)
    bm.edges.layers.int.new(EDGE_TRAFFICLIGHTDIRECTION)
    bm.edges.layers.int.new(EDGE_TRAFFICLIGHTBEHAVIOUR)
    bm.edges.layers.int.new(EDGE_NUMLEFTLANES)
    bm.edges.layers.int.new(EDGE_NUMRIGHTLANES)
    bm.edges.layers.int.new(EDGE_ISTRAINCROSSING)

# per vertex path node information viewer
class MESH_OT_layer_add(bpy.types.Operator):
    """Tooltip"""
    bl_label = "Convert selection to path mesh"
    bl_idname = "mesh.layer_add"
    
    @classmethod
    def poll(cls, context):
        return (context.object is not None and
                context.object.type == 'MESH' and
                context.object.mode == 'EDIT')

    def execute(self, context):
        bm = bmesh.from_edit_mesh(context.object.data)
        try:
            bm.verts.layers.float[NODE_WIDTH]
        except KeyError:
            AddPathMeshLayers(bm)
        else:
            return {'CANCELLED'} 
        return {'FINISHED'}
        
class MeshVertLayerEditable(bpy.types.PropertyGroup):
    def updateVertWidth(self, context):
        me = context.object.data
        bm=bmesh.from_edit_mesh(me)
        bm.verts[self.index][bm.verts.layers.float[NODE_WIDTH]] = self.width
        bmesh.update_edit_mesh(me, tessface=False, destructive=False)
    
    def updateVertBehaviour(self, context):
        me = context.object.data
        bm=bmesh.from_edit_mesh(me)
        bm.verts[self.index][bm.verts.layers.int[NODE_BAHAVIOUR]] = self.behaviour
        bmesh.update_edit_mesh(me, tessface=False, destructive=False)
        
    def updateVertIsdeadEnd(self, context):
        me = context.object.data
        bm=bmesh.from_edit_mesh(me)
        bm.verts[self.index][bm.verts.layers.int[NODE_ISDEADEND]] = self.behaviour
        bmesh.update_edit_mesh(me, tessface=False, destructive=False)
        
    def updateVertIsIgnoredNode(self, context):
        me = context.object.data
        bm=bmesh.from_edit_mesh(me)
        bm.verts[self.index][bm.verts.layers.int[NODE_ISIGNORED]] = self.isIgnoredNode
        bmesh.update_edit_mesh(me, tessface=False, destructive=False)
        
    def updateVertIsRoadBlock(self, context):
        me = context.object.data
        bm=bmesh.from_edit_mesh(me)
        bm.verts[self.index][bm.verts.layers.int[NODE_ISROADBLOCK]] = self.isRoadBlock
        bmesh.update_edit_mesh(me, tessface=False, destructive=False)
        
    def updateVertIsEmergencyVehicleOnly(self, context):
        me = context.object.data
        bm=bmesh.from_edit_mesh(me)
        bm.verts[self.index][bm.verts.layers.int[NODE_ISEMERGENCYVEHICLEONLY]] = self.isEmergencyVehicleOnly
        bmesh.update_edit_mesh(me, tessface=False, destructive=False)
        
    def updateVertIsRestrictedAccess(self, context):
        me = context.object.data
        bm=bmesh.from_edit_mesh(me)
        bm.verts[self.index][bm.verts.layers.int[NODE_ISRESTRICTEDACCESS]] = self.isRestrictedAccess
        bmesh.update_edit_mesh(me, tessface=False, destructive=False)
        
    def updateVertIsDontWander(self, context):
        me = context.object.data
        bm=bmesh.from_edit_mesh(me)
        bm.verts[self.index][bm.verts.layers.int[NODE_ISDONTWANDER]] = self.isDontWander
        bmesh.update_edit_mesh(me, tessface=False, destructive=False)
        
    def updateVertSpeedlimit(self, context):
        me = context.object.data
        bm=bmesh.from_edit_mesh(me)
        bm.verts[self.index][bm.verts.layers.int[NODE_SPEEDLIMIT]] = self.speedlimit
        bmesh.update_edit_mesh(me, tessface=False, destructive=False)
        
    def updateVertSpawnProbability(self, context):
        me = context.object.data
        bm=bmesh.from_edit_mesh(me)
        bm.verts[self.index][bm.verts.layers.int[NODE_SPAWNPROBABILITY]] = self.spawnProbability
        bmesh.update_edit_mesh(me, tessface=False, destructive=False)
        
    index = IntProperty()

    width                   = FloatProperty(soft_min=0.0, soft_max=31, update=updateVertWidth)
    behaviour               = IntProperty(update=updateVertBehaviour)
    isdeadEnd               = BoolProperty(update=updateVertIsdeadEnd)
    isIgnoredNode           = BoolProperty(update=updateVertIsIgnoredNode)
    isRoadBlock             = BoolProperty(update=updateVertIsRoadBlock)
    isEmergencyVehicleOnly  = BoolProperty(update=updateVertIsEmergencyVehicleOnly)
    isRestrictedAccess      = BoolProperty(update=updateVertIsRestrictedAccess)
    isDontWander            = BoolProperty(update=updateVertIsDontWander)
    speedlimit              = IntProperty(soft_min=0, soft_max=3, update=updateVertSpeedlimit)
    spawnProbability        = IntProperty(soft_min=0, soft_max=15, update=updateVertSpawnProbability)
    
    type                    = StringProperty()
    area                    = IntProperty()
    nodeid                  = IntProperty()
    flood                   = IntProperty()
        
class MeshEdgeLayerEditable(bpy.types.PropertyGroup):
    def updateEdgeWidth(self, context):
        me = context.object.data
        bm = bmesh.from_edit_mesh(me)
        bm.edges[self.index][bm.edges.layers.float[EDGE_WIDTH]] = self.width
        bmesh.update_edit_mesh(me, tessface=False, destructive=False)
        
    def updateEdgeLeftLanes(self, context):
        me = context.object.data
        bm = bmesh.from_edit_mesh(me)
        bm.edges[self.index][bm.edges.layers.int[EDGE_NUMLEFTLANES]] = self.LeftLanes
        bmesh.update_edit_mesh(me, tessface=False, destructive=False)
        
    def updateEdgeRightLanes(self, context):
        me = context.object.data
        bm = bmesh.from_edit_mesh(me)
        bm.edges[self.index][bm.edges.layers.int[EDGE_NUMRIGHTLANES]] = self.RightLanes
        bmesh.update_edit_mesh(me, tessface=False, destructive=False)
        
    def updateEdgeTrainCross(self, context):
        me = context.object.data
        bm = bmesh.from_edit_mesh(me)
        bm.edges[self.index][bm.edges.layers.int[EDGE_ISTRAINCROSSING]] = self.isTrainCrossing
        bmesh.update_edit_mesh(me, tessface=False, destructive=False)
        
    def updateEdgeTRL_DIR(self, context):
        me = context.object.data
        bm = bmesh.from_edit_mesh(me)
        bm.edges[self.index][bm.edges.layers.int[EDGE_TRAFFICLIGHTDIRECTION]] = self.trafficLightDirection
        bmesh.update_edit_mesh(me, tessface=False, destructive=False)
        
    def updateEdgeTRL_BEH(self, context):
        me = context.object.data
        bm = bmesh.from_edit_mesh(me)
        bm.edges[self.index][bm.edges.layers.int[EDGE_TRAFFICLIGHTBEHAVIOUR]] = self.trafficLightBehaviour
        bmesh.update_edit_mesh(me, tessface=False, destructive=False)
        
    index = IntProperty()

    width                            = FloatProperty(soft_min=0.0, soft_max=31, update=updateEdgeWidth)
    LeftLanes                        = IntProperty(soft_min=0, soft_max=7, update=updateEdgeLeftLanes)
    RightLanes                       = IntProperty(soft_min=0, soft_max=7, update=updateEdgeRightLanes)
    isTrainCrossing                  = BoolProperty(update=updateEdgeTrainCross)
    trafficLightDirection            = IntProperty(update=updateEdgeTRL_DIR)
    trafficLightBehaviour            = IntProperty(update=updateEdgeTRL_BEH)

class MeshLayerEditable(bpy.types.PropertyGroup):
    bDisplayEdgeDirection = BoolProperty(default=False)
    
    currentObj = StringProperty()
    bSelectOnListClick = BoolProperty(default=False)
    
    vIndex = IntProperty()
    eIndex = IntProperty()
    
    vertList = CollectionProperty(type=MeshVertLayerEditable)
    edgeList = CollectionProperty(type=MeshEdgeLayerEditable)

    @staticmethod
    def ClearCollection(context):
        wm = context.window_manager
        wm.mesh_layer_editable.vertList.clear()
        wm.mesh_layer_editable.edgeList.clear()
        wm.mesh_layer_editable.vIndex = -1
        wm.mesh_layer_editable.eIndex = -1
        
        global prevEdgeSelection, prevVertSelection
        prevVertSelection = -1
        prevEdgeSelection = -1

    @staticmethod
    def ClearCollectionIfNecessary(context):
        ob = context.object
        wm = context.window_manager
    
        if ob is None or \
                ob.type != 'MESH' or \
                ob.mode != 'EDIT' or \
                wm.mesh_layer_editable.currentObj != ob.name: 
            MeshLayerEditable.ClearCollection(context)
            return
    
    @staticmethod
    def UpdateCollectionToSelection(self, context):
        MeshLayerEditable.ClearCollection(context)
        
        wm = context.window_manager
        bm = bmesh.from_edit_mesh(context.object.data)
        
        selectedVertices = [v.index for v in bm.verts if v.select]
        selectedEdges = [e.index for e in bm.edges if e.select]
        
        #BAD CODE
        bm.verts.ensure_lookup_table()
        bm.edges.ensure_lookup_table()
        #END BAD CODE
        
        for i in selectedVertices:
            item = wm.mesh_layer_editable.vertList.add()
            item.name = "v #%i" %i
            item.index = i
            bmvert = bm.verts[i]
            item.width                    = bmvert[bm.verts.layers.float[NODE_WIDTH]]               
            item.behaviour                = bmvert[bm.verts.layers.int[NODE_BAHAVIOUR]]             
            item.isdeadEnd                = bmvert[bm.verts.layers.int[NODE_ISDEADEND]] == 1
            item.isIgnoredNode            = bmvert[bm.verts.layers.int[NODE_ISIGNORED]] == 1
            item.isRoadBlock              = bmvert[bm.verts.layers.int[NODE_ISROADBLOCK]] == 1
            item.isEmergencyVehicleOnly   = bmvert[bm.verts.layers.int[NODE_ISEMERGENCYVEHICLEONLY]] == 1
            item.isRestrictedAccess       = bmvert[bm.verts.layers.int[NODE_ISRESTRICTEDACCESS]] == 1
            item.isDontWander             = bmvert[bm.verts.layers.int[NODE_ISDONTWANDER]] == 1
            item.speedlimit               = bmvert[bm.verts.layers.int[NODE_SPEEDLIMIT]]            
            item.spawnProbability         = bmvert[bm.verts.layers.int[NODE_SPAWNPROBABILITY]]      
            item.type                     = bmvert[bm.verts.layers.string[NODE_TYPE]].decode()
            item.area                     = bmvert[bm.verts.layers.int[NODE_AREAID]]                
            item.nodeid                   = bmvert[bm.verts.layers.int[NODE_ID]]                    
            item.flood                    = bmvert[bm.verts.layers.int[NODE_FLOOD]]   
        
        for i in selectedEdges:
            item = wm.mesh_layer_editable.edgeList.add()
            item.name = "e #%i" %i
            item.index = i
            bmedge = bm.edges[i]
            item.width                    = bmedge[bm.edges.layers.float[EDGE_WIDTH]]   
            item.LeftLanes                = bmedge[bm.edges.layers.int[EDGE_NUMLEFTLANES]]          
            item.RightLanes               = bmedge[bm.edges.layers.int[EDGE_NUMRIGHTLANES]]         
            item.isTrainCrossing          = bmedge[bm.edges.layers.int[EDGE_ISTRAINCROSSING]]                     
            item.trafficLightDirection    = bmedge[bm.edges.layers.int[EDGE_TRAFFICLIGHTDIRECTION]] 
            item.trafficLightBehaviour    = bmedge[bm.edges.layers.int[EDGE_TRAFFICLIGHTBEHAVIOUR]] 
        
        objname = context.object.name
        wm.mesh_layer_editable.currentObj = objname
    
prevVertSelection = -1
class MeshVertLayerListUI(bpy.types.UIList):
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname):
        if self.layout_type in {'DEFAULT', 'COMPACT'}:
            row = layout.row(align=True)
            row.scale_x = 0.5
            row.scale_y = 1
            row.label(item.name)
            row.label("A:" + str(item.area) + " N: " + str(item.nodeid))
            row.label("F:" + str(item.flood) + " T: " + str(item.type))
            row.prop(item, "width", text="width", emboss=False)
            row.prop(item, "behaviour", text="behaviour", emboss=False)
            row.prop(item, "isdeadEnd", text="DeadEnd", emboss=False)
            row.prop(item, "isIgnoredNode", text="Ignore", emboss=False)
            row.prop(item, "isRoadBlock", text="RoadBlock", emboss=False)
            row.prop(item, "isEmergencyVehicleOnly", text="EmergencyVehicle", emboss=False)
            row.prop(item, "isRestrictedAccess", text="Restricted", emboss=False)
            row.prop(item, "isDontWander", text="DontWander", emboss=False)
            row.prop(item, "speedlimit", text="speed", emboss=False)
            row.prop(item, "spawnProbability", text="spawn", emboss=False)

        elif self.layout_type in {'GRID'}:
            layout.alignment = 'CENTER'
            layout.label(text="")
        
        wm = context.window_manager
        vertList = wm.mesh_layer_editable.vertList
        vIndex = wm.mesh_layer_editable.vIndex
        ob = context.object
        me = ob.data
        bm = bmesh.from_edit_mesh(me)
        
        global prevVertSelection
        if prevVertSelection == vIndex or wm.mesh_layer_editable.bSelectOnListClick == False:
            return
        
        print("Changing vert for " + ob.name + "from: " + str(prevVertSelection) + " to: " + str(vIndex))
        if item.index != -1 and len(vertList) > 0:
            for i in range(len(vertList)):
                if i != vIndex:
                    bm.verts[vertList[i].index].select = False
        
            bm.verts[vertList[vIndex].index].select = True
        prevVertSelection = vIndex

prevEdgeSelection = -1        
class MeshEdgeLayerListUI(bpy.types.UIList):
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname):
        if self.layout_type in {'DEFAULT', 'COMPACT'}:
            row = layout.row(align=True)
            row.scale_x = 0.5
            row.scale_y = 1
            row.label(item.name)
            row.prop(item, "LeftLanes", text="LeftLanes", emboss=False)
            row.prop(item, "RightLanes", text="RightLanes", emboss=False)
            row.prop(item, "width", text="width", emboss=False)
            
        elif self.layout_type in {'GRID'}:
            layout.alignment = 'CENTER'
            layout.label(text="")
        
        wm = context.window_manager
        edgeList = wm.mesh_layer_editable.edgeList
        eIndex = wm.mesh_layer_editable.eIndex
        ob = context.object
        me = ob.data
        bm = bmesh.from_edit_mesh(me)
        
        global prevEdgeSelection
        if prevEdgeSelection == eIndex or wm.mesh_layer_editable.bSelectOnListClick == False:
            return
        
        print("Changing edge for " + ob.name + "from: " + str(prevEdgeSelection) + " to: " + str(eIndex))
        if item.index != -1 and len(edgeList) > 0:
            for i in range(len(edgeList)):
                if i != eIndex:
                    bm.edges[edgeList[i].index].select = False
        
            bm.edges[edgeList[eIndex].index].select = True
        prevEdgeSelection = eIndex
    
class DisplayOrRefreshMeshLayerEditable(bpy.types.Operator):
    bl_idname = "paths.display_selected"
    bl_label = "List/Refresh Properties"

    @classmethod
    def poll(cls, context):
        return (context.object is not None and
                context.object.type == 'MESH' and
                context.object.mode == 'EDIT')
        
    def execute(self, context):
        MeshLayerEditable.UpdateCollectionToSelection(self, context)
        return {'FINISHED'}

# TODO: Find a way to update list per selection change event not every draw event
class PathNodePropertiesPanel(bpy.types.Panel):
    """Creates a Panel in the Object properties window"""
    bl_label = "Path Ultimatum: PathNode"
    bl_idname = "OBJECT_PT_pathnode"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'
    bl_category = 'PathUltimatum:Tools'
    
    @classmethod
    def poll(cls, context):
        MeshLayerEditable.ClearCollectionIfNecessary(context)
        ob = context.object
        return (ob is not None and \
                ob.type == 'MESH' and \
                ob.mode == 'EDIT')
        
    def draw(self, context):
        layout = self.layout
        wm = context.window_manager
        ob = context.object
        me = ob.data
        bm = bmesh.from_edit_mesh(me)
        try:
            bm.verts.layers.float[NODE_WIDTH]
        except KeyError:
            layout.label("Current selected object is not a path mesh!")
            layout.operator("mesh.layer_add")
            return

        selectedMode = 'Vertex'

        if bm.select_mode == {'EDGE'}:
            selectedMode = 'Edge'
        
        if bm.select_mode != {'VERT'} and bm.select_mode != {'EDGE'}:
            layout.label("Vertex or Edge select only", icon = 'INFO')
            return
        
        # BAD CODE
        selectedEdges = [e.index for e in bm.edges if e.select]
        myEdges = [e.index for e in wm.mesh_layer_editable.edgeList] 
        if set(selectedEdges) != set(myEdges):
            print("updating")
            MeshLayerEditable.UpdateCollectionToSelection(self, context)
        #END BAD CODE
            
        layout.label(text="Selected " + selectedMode+"(s)")
        row = layout.row(align=True)
        row.scale_y = 1.5
        props = row.operator(DisplayOrRefreshMeshLayerEditable.bl_idname)
        row.prop(wm.mesh_layer_editable, "bSelectOnListClick", text="Select " + selectedMode+"(s)" + " on Highlight")
        
        if bm.select_mode == {'VERT'}:
            layout.label(text="Node Attributes")
            layout.template_list("MeshVertLayerListUI", "", wm.mesh_layer_editable, "vertList", wm.mesh_layer_editable, "vIndex")
        
        layout.label(text="Edge Attributes")
        layout.template_list("MeshEdgeLayerListUI", "", wm.mesh_layer_editable, "edgeList", wm.mesh_layer_editable, "eIndex")
        layout.prop(wm.mesh_layer_editable, "bDisplayEdgeDirection", text="Display Link Helpers")
        
class LinkInfoHelper:
    gllistIndex = -1
    
    @staticmethod
    def create_display_list(context):
        ob = context.object
        if ob is None:
            return
        
        if bpy.context.active_object.mode != 'EDIT':
            return
            
        ob = context.edit_object
        bm = bmesh.from_edit_mesh(ob.data)
        index = glGenLists(1)
        
        glNewList(index, GL_COMPILE)
        
        for e in bm.edges:
            vecFrom = e.verts[0].co
            vecTo = e.verts[1].co
    
            middle = (vecTo + vecFrom) / 2.0
            
            v = vecTo - vecFrom
            v.normalize()
            
            # if vector is straight pointing up only on z axis ignore it
            #if abs(v.x) < 0.0001 and abs(v.y) < 0.0001:
                #continue
            
            vPerp1 = Vector((-v.y, v.x, 0.0))
            vPerp2 = Vector((v.y, -v.x, 0.0))
            
            v1 = (vPerp1 - v).normalized()
            v2 = (vPerp2 - v).normalized()
            
            arrow_vertices = (
                (-0.5,-1.0, 0.0 ),
                ( 0.0, 1.0, 0.0 ),
                ( 0.0, 0.0, 0.0 ),
                ( 0.5,-1.0, 0.0 ),
            )
            
            line_vertices = (
                (-0.5, 0.5, 0.0 ) ,     
                (-0.5, -0.5, 0.0 ),
                ( 0.5, -0.5, 0.0 ),
                ( 0.5, 0.5, 0.0 ) ,
            )
            
            
            SCALE = 1.0
            
            hAngle = 0
            try:
                hAngle = v.xy.angle_signed(Vector((0,1)))
            except ValueError:
                pass
            # rotate towards x = 0, to find out the signed angle 
            v.rotate(Euler((0.0,0.0,-hAngle)))
            
            vAngle = radians(90)
            try:
                vAngle = v.yz.angle_signed(v.yx)
            except ValueError:
                if v.yz.length == 0.00:
                    continue
                vAngle = v.yz.angle_signed(Vector((1,0)))
                pass
            eulerRot = Euler((vAngle, 0.0, hAngle))
            
            glColor3f(0.0,1.0,1.0)
            glBegin(GL_TRIANGLE_STRIP)
            for i in arrow_vertices:
                vert = Vector(i)
                vert *= SCALE
                vert.rotate(eulerRot)
                vert += middle
                glVertex3f(*vert)      
            glEnd()
            
            # Lane Information
            glColor3f(1.0,0.0,1.0)
            for j in range(e[bm.edges.layers.int[EDGE_NUMLEFTLANES]]):
                glBegin(GL_LINES)
                for i in line_vertices:
                    vert = Vector(i)
                    vert = Vector((vert.x, vert.y  * (vecTo - vecFrom).length, vert.z)) # scale
                    vert += Vector((-1.0 * (j + 1), 0.0, 0.0)) #left
                    vert.rotate(eulerRot)
                    vert += middle
                    glVertex3f(*vert)      
                glEnd()
            
            glColor3f(0.0,1.0,0.0)
            for j in range(e[bm.edges.layers.int[EDGE_NUMRIGHTLANES]]):
                glBegin(GL_LINES)
                for i in line_vertices:
                    vert = Vector(i)
                    vert = Vector((vert.x, vert.y  * (vecTo - vecFrom).length, vert.z)) # scale
                    vert += Vector((1.0 * (j + 1), 0.0, 0.0)) #left
                    vert.rotate(eulerRot)
                    vert += middle
                    glVertex3f(*vert)      
                glEnd()
            """
            glBegin(GL_LINE_STRIP)
            glVertex3f(*(middle + v1))
            glVertex3f(*(middle))
            glVertex3f(*(middle + v2))
            glEnd()
            """
        glEndList()
        LinkInfoHelper.gllistIndex = index
        return index
    
    @staticmethod
    def delete_display_list():
        if LinkInfoHelper.gllistIndex != -1:
            glDeleteLists(LinkInfoHelper.gllistIndex, 1)
            LinkInfoHelper.gllistIndex = -1
    
    @staticmethod
    def draw_callback_px():
        context = bpy.context
        wm = context.window_manager
        if wm.mesh_layer_editable.bDisplayEdgeDirection == False:
            LinkInfoHelper.delete_display_list()            
            return
        
        ob = context.object
        if ob is None or \
                ob.type != 'MESH' or \
                ob.mode != 'EDIT' or \
                wm.mesh_layer_editable.currentObj != ob.name:
            LinkInfoHelper.delete_display_list()
            return
            
        if LinkInfoHelper.gllistIndex == -1:
            LinkInfoHelper.gllistIndex = LinkInfoHelper.create_display_list(context)
        
        #LinkInfoHelper.delete_display_list()
        #LinkInfoHelper.create_display_list(context)
    
        # 50% alpha, 2 pixel width line
        #glEnable(GL_BLEND)
        glColor4f(1.0, 1.0, 1.0, 0.5)
        #glLineWidth(2)
        
        glPushMatrix()
        glScalef(*ob.scale)
        glTranslatef(*ob.location)
        glCallList(LinkInfoHelper.gllistIndex)
        glPopMatrix()
    
        # restore opengl defaults
        glLineWidth(1)
        glDisable(GL_BLEND)
        glColor4f(0.0, 0.0, 0.0, 1.0)
     
    @staticmethod
    def cleanup():
        LinkInfoHelper.delete_display_list()

drawFnHandle = -1
addon_keymaps = []
def setupProps():
    bpy.types.WindowManager.mesh_layer_editable = PointerProperty(type=MeshLayerEditable)
    
    wm = bpy.context.window_manager
    km = wm.keyconfigs.addon.keymaps.new(name="3D View", space_type="VIEW_3D")
    kmi = km.keymap_items.new(DisplayOrRefreshMeshLayerEditable.bl_idname, 'Q', 'PRESS', alt=True)
    addon_keymaps.append(km)
    
    args = ()
    global drawFnHandle
    drawFnHandle = bpy.types.SpaceView3D.draw_handler_add(LinkInfoHelper.draw_callback_px,args,'WINDOW', 'POST_VIEW')
    
def removeProps():
    wm = bpy.context.window_manager
    for km in addon_keymaps:
        wm.keyconfigs.addon.keymaps.remove(km)
    addon_keymaps.clear()
    
    LinkInfoHelper.cleanup()
    global drawFnHandle
    bpy.types.SpaceView3D.draw_handler_remove(drawFnHandle, 'WINDOW')
    
    del bpy.types.WindowManager.mesh_layer_editable

def register():
    bpy.utils.register_module(__name__)
    setupProps()
    
def unregister():
    bpy.utils.unregister_module(__name__)
    removeProps()

if __name__ == "__main__":
    register()