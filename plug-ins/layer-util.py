#!/usr/bin/env python

from gimpfu import *

## Utility

def get_layer(obj, layer_name):
    for layer in obj.layers:
        if layer.name == layer_name:
            return layer
    return None

## Create Initial Layers

def create_layers(img, layer):
    if get_layer(img, 'all'):
        return
    img.undo_group_start()
    all_group = gimp.GroupLayer(img, 'all')
    lineart_group = gimp.GroupLayer(img, 'lineart group')
    sketch_group = gimp.GroupLayer(img, 'sketch group')
    color_group = gimp.GroupLayer(img, 'color group')

    sketch = gimp.Layer(img, 'sketch', img.width, img.height, RGBA_IMAGE, 100, NORMAL_MODE)

    img.add_layer(all_group, 0)
    pdb.gimp_image_insert_layer(img, lineart_group, all_group, 0)
    pdb.gimp_image_insert_layer(img, sketch_group, all_group, 1)
    pdb.gimp_image_insert_layer(img, color_group, all_group, 2)
    pdb.gimp_image_insert_layer(img, sketch, sketch_group, 0)

    img.undo_group_end()

## Create Sketch Layer

def new_sketch_layer(img, layer):
    all_group = get_layer(img, 'all')
    if not all_group:
        return
    sketch_group = get_layer(all_group, 'sketch group')
    if not sketch_group:
        return
    img.undo_group_start()
    if len(sketch_group.layers) >= 1:
        sketch = sketch_group.layers[0]
        sketch.opacity = 10.0
        sketch.flush()
    if len(sketch_group.layers) >= 2:
        sketch = sketch_group.layers[1]
        sketch.opacity = 100.0
        sketch.visible = False
        sketch.flush()
    sketch = gimp.Layer(img, 'sketch', img.width, img.height, RGBA_IMAGE, 100, NORMAL_MODE)
    pdb.gimp_image_insert_layer(img, sketch, sketch_group, 0)
    sketch.flush()
    img.undo_group_end()

## Create Lineart Layer

def new_lineart_layer(img, layer, name):
    all_group = get_layer(img, 'all')
    if not all_group:
        return
    lineart_group = get_layer(all_group, 'lineart group')
    if not lineart_group:
        return
    sel, x1, y1, x2, y2 = pdb.gimp_selection_bounds(img)
    if not sel:
        return
    w = x2 - x1
    h = y2 - y1
    img.undo_group_start()
    if len(lineart_group.layers) < 1:
        sketch_group = get_layer(all_group, 'sketch group')
        if sketch_group:
            if len(sketch_group.layers) >= 1:
                sketch_group.layers[0].opacity = 10.0
            if len(sketch_group.layers) >= 2:
                sketch_group.layers[1].opacity = 100.0
                sketch_group.layers[1].visible = False
    lineart = gimp.Layer(img, name + ' - lineart', w, h, RGBA_IMAGE, 100, NORMAL_MODE)
    pdb.gimp_image_insert_layer(img, lineart, lineart_group, 0)
    pdb.gimp_layer_translate(lineart, x1, y1)
    lineart.flush()
    img.undo_group_end()

## Create Color Layer

def new_color_layer(img, layer, name):
    all_group = get_layer(img, 'all')
    if not all_group:
        return
    color_group = get_layer(all_group, 'color group')
    if not color_group:
        return
    sel, x1, y1, x2, y2 = pdb.gimp_selection_bounds(img)
    if not sel:
        return
    w = x2 - x1
    h = y2 - y1
    img.undo_group_start()
    if len(color_group.layers) < 1:
        sketch_group = get_layer(all_group, 'sketch group')
        if len(sketch_group.layers) >= 1:
            sketch_group.layers[0].opacity = 100.0
            sketch_group.layers[0].visible = False
        sketch_group.visible = False
    color = gimp.Layer(img, name + ' - color', w, h, RGBA_IMAGE, 100, NORMAL_MODE)
    pdb.gimp_image_insert_layer(img, color, color_group, 0)
    pdb.gimp_layer_translate(color, x1, y1)
    color.flush()
    img.undo_group_end()

## Register Plug-ins

register(
    'edii_create_layers',
    'Creates a number of layers to start a new project',
    'Creates a number of layers to start a new project',
    'ediiknorand',
    'ediiknorand',
    '2018',
    '<Image>/Layer/Create Initial Layers',
    '*',
    [],
    [],
    create_layers)

register(
    'edii_new_sketch',
    'Creates a sketch layer',
    'Creates a sketch layer',
    'ediiknorand',
    'ediiknorand',
    '2018',
    '<Image>/Layer/New Sketch Layer',
    '*',
    [],
    [],
    new_sketch_layer)

register(
    'edii_new_lineart_layer',
    'Creates a lineart layer from selection',
    'Creates a lineart layer from selection',
    'ediiknorand',
    'ediiknorand',
    '2018',
    '<Image>/Layer/New Lineart Layer from Selection',
    '*',
    [
        (PF_STRING, 'name', 'Layer name', '')
    ],
    [],
    new_lineart_layer)

register(
    'edii_new_color_layer',
    'Creates a color layer from selection',
    'Creates a color layer from selection',
    'ediiknorand',
    'ediiknorand',
    '2018',
    '<Image>/Layer/New Color Layer from Selection',
    '*',
    [
        (PF_STRING, 'name', 'Layer name', '')
    ],
    [],
    new_color_layer)

main()
