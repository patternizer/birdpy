#!/usr/bin/env python

# PROGRAM: birdpy.py
#-----------------------------------------------------------------------
# Version 0.2
# 21 January, 2020
# patternizer AT gmail DOT com
# https://patternizer.github.io
#-----------------------------------------------------------------------

from moviepy.editor import *
from moviepy.video.io.bindings import mplfig_to_npimage
from moviepy.video.tools.segmenting import findObjects
from moviepy.video.tools.drawing import color_gradient
from moviepy.video.tools.drawing import circle
from moviepy.video.tools.credits import credits1
from moviepy.config import change_settings
change_settings({"IMAGEMAGICK_BINARY": r"C:\\Program Files\\ImageMagick-7.0.9-Q16\\magick.exe"})

#-----------------------------------------------------------------------------------------------
# Total duration and audio segment
duration = 58.7
audioclip = AudioFileClip("soundtrack.mp3").set_end(duration)

# Load the raw film and select the subclip 00:00:11 - 00:00:16
clip = (VideoFileClip("film.MOV", audio=False)
        .volumex(0.1) # quieten audio
        .subclip(6,16) # subclip: 00:00:11 - 00:00:16
        .fx( vfx.resize, width=800) # resize (keep aspect ratio)
        .fx( vfx.speedx, 1) # single speed
        .fx( vfx.colorx, 1.0)) # darken the picture

# Loop #1: repeat speed
loop1 = (VideoFileClip("film.MOV", audio=False)
        .volumex(0.1) 
        .subclip(11.5,15) 
        .fx( vfx.resize, width=800) 
        .fx( vfx.speedx, 1.0) 
        .fx( vfx.colorx, 1.0))

# Loop #2: 75% speed
loop1 = (VideoFileClip("film.MOV", audio=False)
        .volumex(0.1) 
        .subclip(11.5,15) 
        .fx( vfx.resize, width=800) 
        .fx( vfx.speedx, 0.75) 
        .fx( vfx.colorx, 1.0))

# Loop #3: 50% speed
loop2 = (VideoFileClip("film.MOV", audio=False)
        .volumex(0.1) 
        .subclip(11.5,15) 
        .fx( vfx.resize, width=800) 
        .fx( vfx.speedx, 0.5) 
        .fx( vfx.colorx, 1.0)) 

# Loop #4: 25% speed
loop3 = (VideoFileClip("film.MOV", audio=False)
        .volumex(0.1) 
        .subclip(11.5,13.5) 
        .fx( vfx.resize, width=800) 
        .fx( vfx.speedx, 0.25) 
        .fx( vfx.colorx, 1.0))

# Get clip dimensions
w,h = clip.size

# Save start and end frames
clip.save_frame("frame_start.png", t=0) # saves the frame a t=0s
clip.save_frame("frame_end.png", t=loop3.duration-0.2) # saves the last frame

# Make title and author clip
first_frame = ImageClip('frame_start.png').set_duration(3)
the_title = TextClip("Ornithography #1", fontsize=50, color="black")
clip_the_title = the_title.set_pos('center').set_duration(3)
title = CompositeVideoClip([first_frame, clip_the_title]) # Overlay text on image

first_frame = ImageClip('frame_start.png').set_duration(3)
the_author = TextClip("Michael Taylor\n patternizer@gmail.com", fontsize=50, color='Black')
clip_the_author = the_author.set_pos('center').set_duration(3)
author = CompositeVideoClip([first_frame, clip_the_author]) # Overlay text on image

# Make the end clip
last_frame = ImageClip('frame_end.png').set_duration(3)
the_end = TextClip("The End", fontsize=50, color="black")
clip_the_end = the_end.set_pos('center').set_duration(3)
end = CompositeVideoClip([last_frame, clip_the_end])

# Make the credits clip
last_frame = ImageClip('frame_end.png').set_duration(5)
the_credits = credits1('credits.txt', int(0.5*w), stretch=0, color='black', 
        stroke_color='black', stroke_width=2, font='Impact-Normal', fontsize=30, gap=30)
clip_the_credits = the_credits.set_pos(lambda t:('center',-5*t)).set_duration(5) 
credits = CompositeVideoClip([last_frame, clip_the_credits])

# Join up the clips
final = concatenate_videoclips([title, author, clip, loop1, loop2, loop3, end, credits]).set_audio(audioclip)

# Write to file
final.write_videofile('ornithography_1.mp4',fps=25)
#-----------------------------------------------------------------------------------------------

print('** END')


