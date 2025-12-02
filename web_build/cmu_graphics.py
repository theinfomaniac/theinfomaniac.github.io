import js
import math
from pyodide.ffi import create_proxy
import io
import base64

# Global state
_app_instance = None
_loop_running = False
_held_keys = set()
_mouse_down = False
_mouse_pos = (0, 0)

class App:
    def __init__(self):
        self.width = 400
        self.height = 400
        self.background = 'white'
        self.stepsPerSecond = 30
        self.group = Group()
        self.tycoon = None # Specific to this game, but harmless to add
        
    def stop(self):
        pass

class Group(list):
    def add(self, item):
        self.append(item)
    def clear(self):
        super().clear()

class CMUImage:
    def __init__(self, pil_image):
        self.pil_image = pil_image
        self.width = pil_image.width
        self.height = pil_image.height
        
        # Convert to JS Image for drawing
        buffered = io.BytesIO()
        pil_image.save(buffered, format="PNG")
        img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")
        
        self._js_image = js.Image.new()
        self._js_image.src = "data:image/png;base64," + img_str

def rgb(r, g, b):
    return f"rgb({int(r)}, {int(g)}, {int(b)})"

def gradient(*args, **kwargs):
    # Simplified gradient support (just returns first color or black)
    return "black"

# Drawing functions
def _get_ctx():
    canvas = js.document.getElementById("gameCanvas")
    return canvas.getContext("2d")

def _apply_styles(ctx, fill, border, borderWidth, opacity, rotateAngle, x, y):
    ctx.globalAlpha = opacity / 100.0 if opacity is not None else 1.0
    
    if rotateAngle is not None and rotateAngle != 0:
        ctx.translate(x, y)
        ctx.rotate(math.radians(rotateAngle))
        ctx.translate(-x, -y)
        
    if fill is not None:
        ctx.fillStyle = fill
    if border is not None:
        ctx.strokeStyle = border
        ctx.lineWidth = borderWidth if borderWidth is not None else 1

def drawRect(x, y, w, h, fill='black', border=None, borderWidth=1, opacity=100, rotateAngle=0, align='left'):
    ctx = _get_ctx()
    ctx.save()
    
    if align == 'center':
        x -= w / 2
        y -= h / 2
        
    _apply_styles(ctx, fill, border, borderWidth, opacity, rotateAngle, x + w/2, y + h/2)
    
    if fill is not None:
        ctx.fillRect(x, y, w, h)
    if border is not None:
        ctx.strokeRect(x, y, w, h)
        
    ctx.restore()

def drawCircle(x, y, r, fill='black', border=None, borderWidth=1, opacity=100):
    ctx = _get_ctx()
    ctx.save()
    _apply_styles(ctx, fill, border, borderWidth, opacity, 0, x, y)
    
    ctx.beginPath()
    ctx.arc(x, y, r, 0, 2 * math.pi)
    
    if fill is not None:
        ctx.fill()
    if border is not None:
        ctx.stroke()
        
    ctx.restore()

def drawOval(x, y, w, h, fill='black', border=None, borderWidth=1, opacity=100, rotateAngle=0, align='center'):
    ctx = _get_ctx()
    ctx.save()
    
    # Canvas ellipse takes center x, y. 
    # CMU drawOval usually takes center x, y if align='center' (default for oval?)
    # Let's assume x,y is center for oval as per standard CMU usage usually?
    # Wait, CMU docs say: drawOval(centerX, centerY, width, height)
    
    _apply_styles(ctx, fill, border, borderWidth, opacity, rotateAngle, x, y)
    
    ctx.beginPath()
    ctx.ellipse(x, y, w/2, h/2, 0, 0, 2 * math.pi)
    
    if fill is not None:
        ctx.fill()
    if border is not None:
        ctx.stroke()
        
    ctx.restore()

def drawLine(x1, y1, x2, y2, fill='black', lineWidth=1, opacity=100):
    ctx = _get_ctx()
    ctx.save()
    ctx.globalAlpha = opacity / 100.0
    ctx.strokeStyle = fill
    ctx.lineWidth = lineWidth
    
    ctx.beginPath()
    ctx.moveTo(x1, y1)
    ctx.lineTo(x2, y2)
    ctx.stroke()
    ctx.restore()

def drawPolygon(*args, fill='black', border=None, borderWidth=1, opacity=100, rotateAngle=0):
    # args is x1, y1, x2, y2, ...
    points = []
    for i in range(0, len(args), 2):
        if i+1 < len(args):
            points.append((args[i], args[i+1]))
            
    if not points: return

    ctx = _get_ctx()
    ctx.save()
    
    # Calculate center for rotation
    cx = sum(p[0] for p in points) / len(points)
    cy = sum(p[1] for p in points) / len(points)
    
    _apply_styles(ctx, fill, border, borderWidth, opacity, rotateAngle, cx, cy)
    
    ctx.beginPath()
    ctx.moveTo(points[0][0], points[0][1])
    for i in range(1, len(points)):
        ctx.lineTo(points[i][0], points[i][1])
    ctx.closePath()
    
    if fill is not None:
        ctx.fill()
    if border is not None:
        ctx.stroke()
    ctx.restore()

def drawStar(centerX, centerY, radius, points, fill='black', border=None, borderWidth=1, opacity=100, rotateAngle=0, roundness=0.5):
    ctx = _get_ctx()
    ctx.save()
    
    _apply_styles(ctx, fill, border, borderWidth, opacity, rotateAngle, centerX, centerY)
    
    ctx.beginPath()
    
    inner_radius = radius * 0.382
    if points == 4: inner_radius = radius * 0.4
    
    angle_step = math.pi / points
    current_angle = -math.pi / 2
    
    for i in range(points * 2):
        r = radius if i % 2 == 0 else inner_radius
        x = centerX + math.cos(current_angle) * r
        y = centerY + math.sin(current_angle) * r
        
        if i == 0:
            ctx.moveTo(x, y)
        else:
            ctx.lineTo(x, y)
            
        current_angle += angle_step
        
    ctx.closePath()
    
    if fill is not None:
        ctx.fill()
    if border is not None:
        ctx.stroke()
        
    ctx.restore()

def drawArc(centerX, centerY, width, height, startAngle, sweepAngle, fill=None, border='black', borderWidth=1, opacity=100, rotateAngle=0):
    ctx = _get_ctx()
    ctx.save()
    
    _apply_styles(ctx, fill, border, borderWidth, opacity, rotateAngle, centerX, centerY)
    
    ctx.beginPath()
    
    start_rad = math.radians(startAngle)
    end_rad = math.radians(startAngle + sweepAngle)
    
    if fill is not None:
        ctx.moveTo(centerX, centerY)
        
    ctx.ellipse(centerX, centerY, width/2, height/2, 0, start_rad, end_rad)
    
    if fill is not None:
        ctx.lineTo(centerX, centerY)
        ctx.fill()
        
    if border is not None:
        ctx.stroke()
             
    ctx.restore()

def drawLabel(value, x, y, size=12, font='arial', bold=False, fill='black', opacity=100, align='center'):
    ctx = _get_ctx()
    ctx.save()
    ctx.globalAlpha = opacity / 100.0
    ctx.fillStyle = fill
    
    font_style = "bold " if bold else ""
    ctx.font = f"{font_style}{int(size)}px {font}"
    
    ctx.textAlign = align
    ctx.textBaseline = 'middle' # CMU usually centers vertically
    
    ctx.fillText(str(value), x, y)
    ctx.restore()

def drawImage(image, x, y, align='left-top', opacity=100, rotateAngle=0, width=None, height=None):
    if image is None: return
    
    ctx = _get_ctx()
    ctx.save()
    
    w = width if width is not None else image.width
    h = height if height is not None else image.height
    
    if align == 'center':
        x -= w / 2
        y -= h / 2
        
    _apply_styles(ctx, None, None, None, opacity, rotateAngle, x + w/2, y + h/2)
    
    try:
        ctx.drawImage(image._js_image, x, y, w, h)
    except:
        pass
        
    ctx.restore()

# Main Loop
def runApp(width=400, height=400):
    global _app_instance
    _app_instance = App()
    _app_instance.width = width
    _app_instance.height = height
    
    canvas = js.document.getElementById("gameCanvas")
    canvas.width = width
    canvas.height = height
    
    # Import main module to get callbacks
    import main
    
    if hasattr(main, 'onAppStart'):
        main.onAppStart(_app_instance)
        
    # Input handling
    def key_down(e):
        key = e.key
        if key == "ArrowUp": key = "up"
        elif key == "ArrowDown": key = "down"
        elif key == "ArrowLeft": key = "left"
        elif key == "ArrowRight": key = "right"
        elif key == " ": key = "space"
        elif key == "Enter": key = "enter"
        
        _held_keys.add(key)
        if hasattr(main, 'onKeyPress'):
            main.onKeyPress(_app_instance, key)
            
    def key_up(e):
        key = e.key
        if key == "ArrowUp": key = "up"
        elif key == "ArrowDown": key = "down"
        elif key == "ArrowLeft": key = "left"
        elif key == "ArrowRight": key = "right"
        elif key == " ": key = "space"
        elif key == "Enter": key = "enter"
        
        if key in _held_keys:
            _held_keys.remove(key)
            
        if hasattr(main, 'onKeyRelease'):
            main.onKeyRelease(_app_instance, key)
            
    def mouse_down(e):
        rect = canvas.getBoundingClientRect()
        x = e.clientX - rect.left
        y = e.clientY - rect.top
        if hasattr(main, 'onMousePress'):
            main.onMousePress(_app_instance, x, y)
            
    def mouse_up(e):
        rect = canvas.getBoundingClientRect()
        x = e.clientX - rect.left
        y = e.clientY - rect.top
        if hasattr(main, 'onMouseRelease'):
            main.onMouseRelease(_app_instance, x, y)
            
    def mouse_move(e):
        rect = canvas.getBoundingClientRect()
        x = e.clientX - rect.left
        y = e.clientY - rect.top
        if e.buttons == 1: # Dragging
             if hasattr(main, 'onMouseDrag'):
                main.onMouseDrag(_app_instance, x, y)
                
    def mouse_wheel(e):
        rect = canvas.getBoundingClientRect()
        x = e.clientX - rect.left
        y = e.clientY - rect.top
        # e.deltaY is usually +/- 100. CMU expects +/- 1? Or just direction.
        # Let's pass raw delta or sign?
        # seal_simulator_custom.py uses onMouseScroll(app, mouseX, mouseY, scrollAmount)
        # scrollAmount > 0 is up?
        scroll = -1 if e.deltaY > 0 else 1
        if hasattr(main, 'onMouseScroll'):
            main.onMouseScroll(_app_instance, x, y, scroll)
            
    js.window.addEventListener("keydown", create_proxy(key_down))
    js.window.addEventListener("keyup", create_proxy(key_up))
    canvas.addEventListener("mousedown", create_proxy(mouse_down))
    canvas.addEventListener("mouseup", create_proxy(mouse_up))
    canvas.addEventListener("mousemove", create_proxy(mouse_move))
    canvas.addEventListener("wheel", create_proxy(mouse_wheel))
    
    # Game Loop
    last_step_time = 0
    
    def step(timestamp):
        nonlocal last_step_time
        
        # Throttle logic to match stepsPerSecond
        step_interval = 1000 / _app_instance.stepsPerSecond
        elapsed = timestamp - last_step_time
        
        if elapsed >= step_interval:
            last_step_time = timestamp - (elapsed % step_interval) # Keep sync
            
            if hasattr(main, 'onStep'):
                main.onStep(_app_instance)
                
            if hasattr(main, 'onKeyHold') and _held_keys:
                main.onKeyHold(_app_instance, list(_held_keys))
        
        # Draw every frame (interpolated if we had logic for it, but here just latest state)
        ctx = canvas.getContext("2d")
        ctx.fillStyle = _app_instance.background
        ctx.fillRect(0, 0, width, height)
        
        if hasattr(main, 'redrawAll'):
            main.redrawAll(_app_instance)
            
        js.requestAnimationFrame(create_proxy(step))
        
    js.requestAnimationFrame(create_proxy(step))

