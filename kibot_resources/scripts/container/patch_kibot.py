"""Guarded camera and shadow-free profile for the pinned KiBot 10 CLI path."""
from pathlib import Path

source = Path('/opt/kibot-env/lib/python3.11/site-packages/kibot/out_render_3d.py')
text = source.read_text()
old = "               '--pan', f\"{self.move_x},{self.move_y},{self.zoom}\","
new = """               # Legacy zoom is a number of viewer steps, not a Z translation.
               # KiCad's 3D zoom controls use 1.26 (three steps per doubling).
               '--zoom', str(1.26 ** self.zoom),
               '--pan', f"{self.move_x},{self.move_y},0","""
if text.count(old) != 1:
    raise RuntimeError('Pinned KiBot render code changed; review the camera fix')
text = text.replace(old, new)

# KiCad's high preset forces a floor and cast shadows, even for transparent
# PNGs. Use an explicit profile with the same quality features and no shadows.
old = "               '--quality', 'high' if self.ray_tracing else 'basic',"
new = "               '--quality', 'user' if self.ray_tracing else 'basic',"
if text.count(old) != 1:
    raise RuntimeError('Pinned KiBot render code changed; review the quality fix')
text = text.replace(old, new)
old = '        # Save the new config\n'
new = '''        # Keep high-quality ray tracing without a floor or cast shadows.
        old_cfg.setdefault('render', {}).update({
            'raytrace_anti_aliasing': True,
            'raytrace_backfloor': False,
            'raytrace_shadows': False,
            'raytrace_post_processing': True,
            'raytrace_procedural_textures': True,
            'raytrace_reflections': True,
            'raytrace_refractions': True,
            'differentiate_plated_copper': True,
        })
        # Save the new config
'''
if text.count(old) != 1:
    raise RuntimeError('Pinned KiBot render code changed; review the shadow profile')
source.write_text(text.replace(old, new))
