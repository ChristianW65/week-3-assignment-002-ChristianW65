"""
DIGM 131 - Assignment 3: Function Library (scene_functions.py)
===============================================================

OBJECTIVE:
    Create a library of reusable functions that each generate a specific
    type of scene element. This module will be imported by main_scene.py.

REQUIREMENTS:
    1. Implement at least 5 reusable functions.
    2. Every function must have a complete docstring with Args and Returns.
    3. Every function must accept parameters for position and/or size so
       they can be reused at different locations and scales.
    4. Every function must return the name(s) of the Maya object(s) it creates.
    5. Follow PEP 8 naming conventions (snake_case for functions/variables).

GRADING CRITERIA:
    - [30%] At least 5 functions, each creating a distinct scene element.
    - [25%] Functions accept parameters and use them (not hard-coded values).
    - [20%] Every function has a complete docstring (summary, Args, Returns).
    - [15%] Functions return the created object name(s).
    - [10%] Clean, readable code following PEP 8.
"""

import maya.cmds as cmds
 
 
def create_building(width=4, height=8, depth=4, position=(0, 0, 0)):
    """Create a simple building from a cube, placed on the ground plane.
 
    The building is a single scaled cube whose base sits at ground level
    (y = 0) at the given position.
 
    Args:
        width (float): Width of the building along the X axis. Defaults to 4.
        height (float): Height of the building along the Y axis. Defaults to 8.
        depth (float): Depth of the building along the Z axis. Defaults to 4.
        position (tuple): (x, y, z) ground-level position. The building
            base will rest at this point; y is typically 0.
 
    Returns:
        str: The name of the created building transform node.
    """
    building = cmds.polyCube(
        width=width,
        height=height,
        depth=depth,
        name="building"
    )[0]
    # Raise by half the height so the base sits flush on the ground
    cmds.move(
        position[0],
        position[1] + height / 2.0,
        position[2],
        building
    )
    return building
 
 
def create_tree(trunk_radius=0.3, trunk_height=3, canopy_radius=2,
                position=(0, 0, 0)):
    """Create a simple tree using a cylinder trunk and a sphere canopy.
 
    Args:
        trunk_radius (float): Radius of the cylindrical trunk. Defaults to 0.3.
        trunk_height (float): Height of the trunk cylinder. Defaults to 3.
        canopy_radius (float): Radius of the sphere used for the canopy.
            Defaults to 2.
        position (tuple): (x, y, z) ground-level position for the tree base.
 
    Returns:
        str: The name of a group node containing the trunk and canopy.
    """
    # Trunk — centred so its base sits at y=0
    trunk = cmds.polyCylinder(
        radius=trunk_radius,
        height=trunk_height,
        name="tree_trunk"
    )[0]
    cmds.move(0, trunk_height / 2.0, 0, trunk)
 
    # Canopy — placed on top of the trunk
    canopy = cmds.polySphere(
        radius=canopy_radius,
        name="tree_canopy"
    )[0]
    cmds.move(0, trunk_height + canopy_radius * 0.8, 0, canopy)
 
    # Group both parts then move the whole tree to its scene position
    tree_group = cmds.group(trunk, canopy, name="tree_grp")
    cmds.move(position[0], position[1], position[2], tree_group)
    return tree_group
 
 
def create_fence(length=10, height=1.5, post_count=6, position=(0, 0, 0)):
    """Create a simple fence made of posts and a rail.
 
    The fence runs along the X axis starting at the given position.
 
    Args:
        length (float): Total length of the fence along the X axis.
            Defaults to 10.
        height (float): Height of the fence posts. Defaults to 1.5.
        post_count (int): Number of vertical posts (must be >= 2).
            Defaults to 6.
        position (tuple): (x, y, z) starting position of the fence.
 
    Returns:
        str: The name of a group node containing all fence parts.
    """
    parts = []
    spacing = length / (post_count - 1)
    post_width = 0.15
 
    # Create each vertical post evenly spaced along X
    for i in range(post_count):
        post = cmds.polyCube(
            width=post_width,
            height=height,
            depth=post_width,
            name=f"fence_post_{i}"
        )[0]
        cmds.move(i * spacing, height / 2.0, 0, post)
        parts.append(post)
 
    # Single horizontal rail connecting all posts
    rail = cmds.polyCube(
        width=length,
        height=post_width,
        depth=post_width,
        name="fence_rail"
    )[0]
    cmds.move(length / 2.0, height * 0.6, 0, rail)
    parts.append(rail)
 
    fence_group = cmds.group(*parts, name="fence_grp")
    cmds.move(position[0], position[1], position[2], fence_group)
    return fence_group
 
 
def create_lamp_post(pole_height=5, light_radius=0.5, position=(0, 0, 0)):
    """Create a street lamp using a cylinder pole and a sphere light.
 
    Args:
        pole_height (float): Height of the lamp pole. Defaults to 5.
        light_radius (float): Radius of the sphere representing the light.
            Defaults to 0.5.
        position (tuple): (x, y, z) ground-level position.
 
    Returns:
        str: The name of a group node containing the pole and light.
    """
    # Thin pole centred so its base sits at y=0
    pole = cmds.polyCylinder(
        radius=0.08,
        height=pole_height,
        name="lamp_pole"
    )[0]
    cmds.move(0, pole_height / 2.0, 0, pole)
 
    # Light sphere placed at the very top of the pole
    light_bulb = cmds.polySphere(
        radius=light_radius,
        name="lamp_light"
    )[0]
    cmds.move(0, pole_height + light_radius, 0, light_bulb)
 
    lamp_group = cmds.group(pole, light_bulb, name="lamp_post_grp")
    cmds.move(position[0], position[1], position[2], lamp_group)
    return lamp_group
 
 
def place_in_circle(create_func, count=8, radius=10, center=(0, 0, 0),
                    **kwargs):
    """Place objects created by create_func in a circular arrangement.
 
    This is a higher-order function: it takes another function as an
    argument and calls it repeatedly to place objects around a circle.
 
    Args:
        create_func (callable): A function from this module (e.g.,
            create_tree) that accepts a 'position' keyword argument
            and returns an object name.
        count (int): Number of objects to place around the circle.
            Defaults to 8.
        radius (float): Radius of the circle. Defaults to 10.
        center (tuple): (x, y, z) center of the circle.
        **kwargs: Additional keyword arguments forwarded to create_func
            (e.g., trunk_height=4).
 
    Returns:
        list: A list of object/group names created by create_func.
    """
    results = []
    for i in range(count):
        angle = 2 * math.pi * i / count
        x = center[0] + radius * math.cos(angle)
        z = center[2] + radius * math.sin(angle)
        obj = create_func(position=(x, center[1], z), **kwargs)
        results.append(obj)
    return results
 
