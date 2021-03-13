import pyglet
from pyglet.window import key


def playVideoLoop():
    while True:
        # Prompt user for location of video file
        vidpath = input("Please specify path to video file: ")

        # Loop until user chooses to quit
        if (vidpath == "q") or (vidpath == "quit"):
            break

        playVideo(vidpath)


def playVideo(vidpath):
    window = pyglet.window.Window()
    player = pyglet.media.Player()
    source = pyglet.media.StreamingSource()
    video = pyglet.media.load(vidpath)
    window.width, window.height = get_video_size(video.video_format.width,
                                                 video.video_format.height,
                                                 video.video_format.sample_aspect)
    player.queue(video)
    player.play()

    @window.event
    def on_draw():
        window.clear()
        if player.source and player.source.video_format:
            player.get_texture().blit(0, 0)

    @window.event
    def on_key_press(symbol, modifiers):
        if symbol == key.SPACE:
            playPause(player)
        elif symbol == key.LEFT:
            seek(player, -15)
        elif symbol == key.RIGHT:
            seek(player, -15)
        elif symbol == key.UP:
            volumeAdjust(player, 0.1)
        elif symbol == key.DOWN:
            volumeAdjust(player, -0.1)

    pyglet.app.run()


def playPause(player):
    if player.playing:
        player.pause()
    else:
        player.play()


def seek(player, amount):
    to = player.time + amount
    if to >= 0:
        player.seek(to)
    else:
        player.seek(0.01)


def volumeAdjust(player, amount):
    if 1 >= player.volume + amount >= 0:
        player.volume += amount


def showHelp():
    print("\"h\" - show help")
    print("\"p\" - play video")
    print("\"q\" - quit")


def get_video_size(width, height, sample_aspect):
    if sample_aspect > 1.:
        return width * sample_aspect, height
    elif sample_aspect < 1.:
        return width, height / sample_aspect
    else:
        return width, height

# Begin main loop
while True:
    # Prompt user for commands until they choose to quit
    command = input("Enter command (h for help): ")
    if command.lower() == "p":
        playVideoLoop()
    elif command.lower() == "h":
        showHelp()
    elif command.lower() == "q":
        break