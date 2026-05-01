"""
DIGM 131 - Assignment 3: Function Library (main_scene.py)
==========================================================

OBJECTIVE:
    Use the functions you wrote in scene_functions.py to build a complete
    scene. This file demonstrates how importing and reusing functions makes
    scene creation clean and readable.

REQUIREMENTS:
    1. Import scene_functions (the module you completed).
    2. Call each of your 5+ functions at least once.
    3. Use place_in_circle with at least one of your create functions.
    4. The final scene should contain at least 15 objects total.
    5. Comment your code explaining what you are building.

GRADING CRITERIA:
    - [30%] All 5+ functions from scene_functions.py are called.
    - [25%] place_in_circle is used at least once.
    - [20%] Scene contains 15+ objects and looks intentional.
    - [15%] Code is well-commented.
    - [10%] Script runs without errors from top to bottom.
"""


import maya.cmds as cmds
import scene_functions as sf
 
# ---------------------------------------------------------------------------
# Scene Setup — wipe any existing scene before building
# ---------------------------------------------------------------------------
cmds.file(new=True, force=True)
 
# Large ground plane that the whole neighbourhood sits on
ground = cmds.polyPlane(
    name="ground",
    width=60,
    height=60,
    subdivisionsX=1,
    subdivisionsY=1
)[0]                                                        # object 1
 
# ---------------------------------------------------------------------------
# Central Plaza — a ring of 8 trees surrounding the town square
# Each tree is two objects (trunk + canopy) inside a group, so
# 8 trees = 8 groups = 16 individual meshes + 8 group nodes.
# place_in_circle returns a list of the 8 group names.
# ---------------------------------------------------------------------------
plaza_trees = sf.place_in_circle(                          # objects 2–9 (groups)
    sf.create_tree,
    count=8,
    radius=12,
    center=(0, 0, 0),
    trunk_height=4,
    canopy_radius=2.5
)
 
# ---------------------------------------------------------------------------
# Town Buildings — four buildings arranged around the plaza
# Each polyCube is a single object.
# ---------------------------------------------------------------------------
# Large civic building at the north end
sf.create_building(width=8, height=12, depth=6,
                   position=(0, 0, -20))                   # object 10
 
# Smaller shop on the east side
sf.create_building(width=5, height=6, depth=5,
                   position=(18, 0, -5))                   # object 11
 
# Residential block on the west side
sf.create_building(width=6, height=9, depth=7,
                   position=(-18, 0, -5))                  # object 12
 
# Warehouse at the south end
sf.create_building(width=10, height=5, depth=8,
                   position=(0, 0, 16))                    # object 13
 
# ---------------------------------------------------------------------------
# Street Fencing — two fence sections lining the main road
# Each fence is a group of posts + a rail.
# ---------------------------------------------------------------------------
# East side of the road
sf.create_fence(length=14, height=1.5, post_count=6,
                position=(6, 0, -8))                       # object 14 (group)
 
# West side of the road
sf.create_fence(length=14, height=1.5, post_count=6,
                position=(-8, 0, -8))                      # object 15 (group)
 
# ---------------------------------------------------------------------------
# Street Lighting — four lamp posts at the corners of the plaza
# Each lamp is a group of a pole + a light sphere.
# ---------------------------------------------------------------------------
sf.create_lamp_post(pole_height=6, light_radius=0.4,
                    position=(8, 0, 8))                    # object 16 (group)
 
sf.create_lamp_post(pole_height=6, light_radius=0.4,
                    position=(-8, 0, 8))                   # object 17 (group)
 
sf.create_lamp_post(pole_height=6, light_radius=0.4,
                    position=(8, 0, -8))                   # object 18 (group)
 
sf.create_lamp_post(pole_height=6, light_radius=0.4,
                    position=(-8, 0, -8))                  # object 19 (group)
 
# ---------------------------------------------------------------------------
# Park Corner — a small cluster of trees in the south-west corner
# Three individual trees placed by hand for a natural, uneven look.
# ---------------------------------------------------------------------------
sf.create_tree(trunk_height=3, canopy_radius=2,
               position=(-22, 0, 10))                      # object 20 (group)
 
sf.create_tree(trunk_height=5, canopy_radius=3,
               position=(-25, 0, 14))                      # object 21 (group)
 
sf.create_tree(trunk_height=2.5, canopy_radius=1.5,
               position=(-20, 0, 17))                      # object 22 (group)
 
# ---------------------------------------------------------------------------
# Final viewport framing (do not remove).
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    cmds.viewFit(allObjects=True)
    print("Main scene built successfully!")
