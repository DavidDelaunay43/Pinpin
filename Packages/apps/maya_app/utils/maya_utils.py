from maya import cmds


def get_time_slider_range() -> tuple:
    return cmds.playbackOptions(query = True, minTime = True), cmds.playbackOptions(query = True, maxTime = True)

