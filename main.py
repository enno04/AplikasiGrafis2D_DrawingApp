from browser import document, html, window
import math
import copy

# --- Inisialisasi Elemen ---
canvas = document["canvas"]
ctx = canvas.getContext("2d")

# Elemen Mode Utama
mode_draw_radio = document["mode-draw"]
mode_transform_radio = document["mode-transform"]

# Panel Kontrol
drawing_controls_panel = document["drawing-controls"]
transform_controls_panel = document["transform-controls"]
object_inspector_panel = document["object-inspector"]

# Kontrol Gambar
shape_select = document["shape"]
color_picker = document["color"]
line_width_input = document["line-width"]
line_width_value_span = document["line-width-value"]

# Kontrol Aksi
clear_button = document["clear-button"]
undo_button = document["undo-button"]
redo_button = document["redo-button"]

# Kontrol Transformasi
translate_x_input = document["translate-x"]
translate_y_input = document["translate-y"]
scale_input = document["scale-factor"]
scale_value_span = document["scale-value"]
rotation_input = document["rotation-angle"]
rotation_value_span = document["rotation-value"]

# Kontrol Inspector
inspector_output = document["inspector-output"]
coords_output_span = document["coords-output"]

# --- Variabel State Management ---
drawn_objects = []
selected_object = None
start_pos = {'x': 0, 'y': 0}
history = []
history_index = -1
is_drawing = False
preview_object = None

# --- Fungsi Helper ---
def get_main_mode():
    return "transform" if mode_transform_radio.checked else "draw"

# --- Manajemen State & Undo/Redo ---
def save_state():
    global history, history_index
    history = history[0:history_index + 1]
    history.append(copy.deepcopy(drawn_objects))
    history_index += 1
    update_button_states()

def restore_state(index):
    global drawn_objects, selected_object
    if 0 <= index < len(history):
        drawn_objects = copy.deepcopy(history[index])
        selected_object = None
        hide_side_panels()
        redraw_canvas()

def update_button_states():
    undo_button.disabled = history_index <= 0
    redo_button.disabled = history_index >= len(history) - 1

def undo_action(evt):
    global history_index
    if history_index > 0:
        history_index -= 1
        restore_state(history_index)
        update_button_states()

def redo_action(evt):
    global history_index
    if history_index < len(history) - 1:
        history_index += 1
        restore_state(history_index)
        update_button_states()

# --- Fungsi Menggambar Ulang ---
def redraw_canvas():
    ctx.clearRect(0, 0, canvas.width, canvas.height)
    
    # 1. Gambar semua objek permanen
    for obj in drawn_objects:
        ctx.save()
        center_x, center_y = obj['cx'], obj['cy']
        
        ctx.translate(center_x + obj['transform']['tx'], center_y + obj['transform']['ty'])
        ctx.rotate(obj['transform']['angle'] * math.pi / 180)
        ctx.scale(obj['transform']['scale'], obj['transform']['scale'])
        ctx.translate(-center_x, -center_y)
        
        ctx.strokeStyle, ctx.fillStyle = obj['color'], obj['color']
        ctx.lineWidth = obj['lineWidth']
        
        ctx.beginPath()
        shape_type = obj['type']
        if shape_type == 'rect': ctx.strokeRect(obj['x'], obj['y'], obj['w'], obj['h'])
        elif shape_type == 'line':
            ctx.moveTo(obj['x'], obj['y'])
            ctx.lineTo(obj['x'] + obj['w'], obj['y'] + obj['h'])
            ctx.stroke()
        elif shape_type == 'dot':
            ctx.arc(obj['x'], obj['y'], obj['lineWidth'] / 2 or 1, 0, 2 * math.pi)
            ctx.fill()
        elif shape_type == 'circle':
            ctx.arc(obj['x'], obj['y'], math.sqrt(obj['w']**2 + obj['h']**2), 0, 2 * math.pi)
            ctx.stroke()
        elif shape_type == 'ellipse':
            ctx.ellipse(obj['cx'], obj['cy'], abs(obj['w']/2), abs(obj['h']/2), 0, 0, 2 * math.pi)
            ctx.stroke()

        if obj is selected_object:
            ctx.restore()
            ctx.save()
            tx, ty = obj['transform']['tx'], obj['transform']['ty']
            ctx.strokeStyle, ctx.lineWidth = '#4e54c8', 2
            ctx.setLineDash([6, 4])
            ctx.strokeRect(obj['x']-5+tx, obj['y']-5+ty, obj['w']+10, obj['h']+10)
            ctx.setLineDash([])
        ctx.restore()

    # 2. Gambar pratinjau
    if preview_object:
        ctx.save()
        ctx.strokeStyle, ctx.lineWidth = "rgba(100, 100, 100, 0.6)", 2
        ctx.setLineDash([8, 4])
        p_obj = preview_object
        ctx.beginPath()
        shape_type = p_obj['type']
        if shape_type == 'rect': ctx.strokeRect(p_obj['x'], p_obj['y'], p_obj['w'], p_obj['h'])
        elif shape_type == 'line':
            ctx.moveTo(p_obj['x'], p_obj['y'])
            ctx.lineTo(p_obj['x'] + p_obj['w'], p_obj['y'] + p_obj['h'])
            ctx.stroke()
        elif shape_type == 'circle':
            ctx.arc(p_obj['x'], p_obj['y'], math.sqrt(p_obj['w']**2 + p_obj['h']**2), 0, 2 * math.pi)
            ctx.stroke()
        elif shape_type == 'ellipse':
            cx, cy = p_obj['x'] + p_obj['w'] / 2, p_obj['y'] + p_obj['h'] / 2
            ctx.ellipse(cx, cy, abs(p_obj['w']/2), abs(p_obj['h']/2), 0, 0, 2 * math.pi)
            ctx.stroke()
        ctx.restore()

# --- Event Handler Mouse ---
def mousedown_action(evt):
    global start_pos, selected_object, is_drawing
    start_pos = {'x': evt.offsetX, 'y': evt.offsetY}
    if get_main_mode() == 'transform':
        clicked_object = None
        for obj in reversed(drawn_objects):
            tx, ty = obj['transform']['tx'], obj['transform']['ty']
            if (obj['x']+tx <= start_pos['x'] <= obj['x']+obj['w']+tx and obj['y']+ty <= start_pos['y'] <= obj['y']+obj['h']+ty):
                clicked_object = obj
                break
        selected_object = clicked_object
        if selected_object: show_side_panels(); update_transform_inputs()
        else: hide_side_panels()
        redraw_canvas()
    elif get_main_mode() == 'draw':
        is_drawing = True

def mouseup_action(evt):
    global is_drawing, preview_object, drawn_objects
    if get_main_mode() == 'transform' or not is_drawing:
        if selected_object: save_state()
        return
    is_drawing = False
    x, y = start_pos['x'], start_pos['y']
    end_x, end_y = evt.offsetX, evt.offsetY
    new_object = {'type': shape_select.value, 'color': color_picker.value, 'lineWidth': int(line_width_input.value),
                  'transform': {'tx':0,'ty':0,'scale':1,'angle':0}, 'x':x,'y':y,'w':end_x-x,'h':end_y-y}
    shape_type = new_object['type']
    if shape_type in ['rect', 'line', 'ellipse']:
        new_object['cx'], new_object['cy'] = new_object['x']+new_object['w']/2, new_object['y']+new_object['h']/2
    elif shape_type in ['dot', 'circle']:
        new_object['cx'], new_object['cy'] = new_object['x'], new_object['y']
    if shape_type == 'dot' or (new_object['w'] != 0 or new_object['h'] != 0):
        drawn_objects.append(new_object)
    preview_object = None
    redraw_canvas()
    save_state()

def handle_mouse_move(evt):
    global preview_object
    update_mouse_coords(evt)
    if not is_drawing: return
    x, y = start_pos['x'], start_pos['y']
    end_x, end_y = evt.offsetX, evt.offsetY
    if shape_select.value != 'dot':
        preview_object = {'type': shape_select.value, 'x': x, 'y': y, 'w': end_x - x, 'h': end_y - y}
    redraw_canvas()

def update_mouse_coords(evt):
    coords_output_span.textContent = f"X: {evt.offsetX}, Y: {evt.offsetY}"
def clear_mouse_coords(evt):
    coords_output_span.textContent = "X: -, Y: -"

# --- Kontrol Panel & Inspector ---
def show_side_panels():
    transform_controls_panel.style.display = 'flex'
    object_inspector_panel.style.display = 'block'
def hide_side_panels():
    transform_controls_panel.style.display = 'none'
    object_inspector_panel.style.display = 'none'

def update_inspector():
    if not selected_object: return
    obj, trans = selected_object, selected_object['transform']
    inspector_output.textContent = (f"Tipe      : {obj['type']}\nPosisi    : X={obj['x']}, Y={obj['y']}\nDimensi   : W={obj['w']}, H={obj['h']}\n"
                                  f"--------------------------\nTranslasi : dX={trans['tx']}, dY={trans['ty']}\nSkala     : {trans['scale']:.2f}\nRotasi    : {trans['angle']}°")
def update_transform_inputs():
    if not selected_object: return
    trans = selected_object['transform']
    translate_x_input.value, translate_y_input.value = trans['tx'], trans['ty']
    scale_input.value, scale_value_span.text = trans['scale'], f"{trans['scale']:.1f}"
    rotation_input.value, rotation_value_span.text = trans['angle'], f"{trans['angle']}°"
    update_inspector()
def apply_transformation(evt):
    if not selected_object: return
    trans = selected_object['transform']
    trans['tx'], trans['ty'] = int(translate_x_input.value), int(translate_y_input.value)
    trans['scale'] = float(scale_input.value)
    trans['angle'] = int(rotation_input.value)
    scale_value_span.text, rotation_value_span.text = f"{trans['scale']:.1f}", f"{trans['angle']}°"
    redraw_canvas()
    update_inspector()

# --- Handler & Inisialisasi ---
def handle_main_mode_change(evt):
    global selected_object
    selected_object = None
    hide_side_panels()
    redraw_canvas()
    if get_main_mode() == 'transform':
        drawing_controls_panel.classList.add('disabled')
        canvas.classList.add('transform-mode')
    else:
        drawing_controls_panel.classList.remove('disabled')
        canvas.classList.remove('transform-mode')

def clear_all_objects(evt):
    # Bug diperbaiki di sini: deklarasi global ada di paling atas
    global drawn_objects, selected_object
    if not drawn_objects: return
    if window.confirm("Apakah Anda yakin ingin menghapus semua objek?"):
        drawn_objects = []
        selected_object = None
        hide_side_panels()
        redraw_canvas()
        save_state()

# --- Pemasangan Event Listener ---
line_width_input.bind("input", lambda e: setattr(line_width_value_span, 'text', e.target.value))
canvas.bind("mousedown", mousedown_action)
canvas.bind("mouseup", mouseup_action)
clear_button.bind("click", clear_all_objects)
undo_button.bind("click", undo_action)
redo_button.bind("click", redo_action)
mode_draw_radio.bind('change', handle_main_mode_change)
mode_transform_radio.bind('change', handle_main_mode_change)
for ctrl in [translate_x_input, translate_y_input, scale_input, rotation_input]:
    ctrl.bind("input", apply_transformation)
    ctrl.bind("mouseup", lambda e: save_state() if selected_object else None)
canvas.bind("mousemove", handle_mouse_move)
canvas.bind("mouseleave", clear_mouse_coords)

# --- Inisialisasi Awal ---
def initial_setup():
    line_width_value_span.text = line_width_input.value
    handle_main_mode_change(None) 
    save_state()
    update_button_states()
    redraw_canvas()

initial_setup()