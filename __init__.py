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
        find_frame = current_frame - active.frame_final_start

        for sce in bpy.data.scenes:
            seq = sce.sequence_editor

            for strip in seq.sequences_all:
                if current_scene.name != sce.name and active.name == strip.name:
                    win = bpy.context.window_manager.windows[0]
                    win.scene = bpy.data.scenes[sce.name]
                    bpy.context.scene.frame_current = (
                        find_frame + strip.frame_final_start
                    )
                    bpy.ops.sequencer.view_frame()
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
