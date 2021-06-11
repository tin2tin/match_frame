import bpy

bl_info = {
    "name": "Match Frame",
    "author": "tintwotin",
    "version": (0, 1, 0),
    "blender": (2, 90, 0),
    "description": "Jump to a matching frame in a different scene",
    "location": "Sequencer > Strip > Match Frame",
    "tracker_url": "",
    "category": "Sequencer",
}

import bpy


class SEQUENCER_OT_match_frame(bpy.types.Operator):
    """Jump to a matching frame in a different scene."""

    bl_idname = "sequencer.match_frame"
    bl_label = "Match Frame"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        current_scene = bpy.context.scene
        current_frame = current_scene.frame_current
        active = current_scene.sequence_editor.active_strip

        frame_start = (active.frame_start + active.frame_offset_start)
        frame_end = (active.frame_start + active.frame_offset_start + active.frame_final_duration)

        if current_frame >=frame_start and current_frame <= frame_end:
            find_frame = current_frame - active.frame_start
        else:
            find_frame = 0

        for sce in bpy.data.scenes:
            seq = sce.sequence_editor

            for strip in seq.sequences_all:
                if find_frame and current_scene.name != sce.name and active.type == strip.type and (active.name == strip.name or active.name[:-4].find(strip.name)):
                    frame_current = (find_frame + strip.frame_start)
                    frame_start = (strip.frame_start + strip.frame_offset_start)
                    frame_end = (strip.frame_start + strip.frame_offset_start + strip.frame_final_duration)

                    if frame_current >= frame_start and frame_current <= frame_end:
                        win = bpy.context.window_manager.windows[0]
                        win.scene = bpy.data.scenes[sce.name]
                        bpy.context.scene.frame_current = frame_current
                        bpy.context.scene.sequence_editor.active_strip = strip
                        bpy.ops.sequencer.view_frame()
                        break
                        break
        return {"FINISHED"}


def menu_match_frame(self, context):
    self.layout.separator()
    self.layout.operator("sequencer.match_frame")


def register():
    bpy.utils.register_class(SEQUENCER_OT_match_frame)
    bpy.types.SEQUENCER_MT_strip.append(menu_match_frame)


def unregister():
    bpy.utils.unregister_class(SEQUENCER_OT_match_frame)
    bpy.types.SEQUENCER_MT_strip.remove(menu_match_frame)


if __name__ == "__main__":
    register()
