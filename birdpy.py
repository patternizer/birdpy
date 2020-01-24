#!/usr/bin/env python

# PROGRAM: birdpy.py
#-----------------------------------------------------------------------
# Version 0.3
# 23 January, 2020
# patternizer AT gmail DOT com
# https://patternizer.github.io
#-----------------------------------------------------------------------

import cv2
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
        .fx( vfx.speedx, 1.0) # single speed
        .fx( vfx.colorx, 1.0)) # darken the picture

# Get clip dimensions
clip_w, clip_h = clip.size

# Loop #1: repeat speed
loop1 = (VideoFileClip("film.MOV", audio=False)
        .volumex(0.1) 
        .subclip(11.5,15) 
        .fx( vfx.resize, width=800) 
        .fx( vfx.speedx, 1.0) 
        .fx( vfx.colorx, 1.0))

# Loop #2: 75% speed
loop2 = (VideoFileClip("film.MOV", audio=False)
        .volumex(0.1) 
        .subclip(11.5,15) 
        .fx( vfx.resize, width=800) 
        .fx( vfx.speedx, 0.75) 
        .fx( vfx.colorx, 1.0))

# Loop #3: 50% speed
loop3 = (VideoFileClip("film.MOV", audio=False)
        .volumex(0.1) 
        .subclip(11.5,15) 
        .fx( vfx.resize, width=800) 
        .fx( vfx.speedx, 0.5) 
        .fx( vfx.colorx, 1.0)) 

# Loop #4: 25% speed
loop4 = (VideoFileClip("film.MOV", audio=False)
        .volumex(0.1) 
        .subclip(11.5,13.5) 
        .fx( vfx.resize, width=800) 
        .fx( vfx.speedx, 0.25) 
        .fx( vfx.colorx, 1.0))

loop1.write_videofile('clip_untracked.avi', fps=25, codec='libx264')

#--------------------
# AI Motion Detection
#--------------------

# Open AVI for AI capture
cap = cv2.VideoCapture('clip_untracked.avi')
frame_width = int( cap.get( cv2.CAP_PROP_FRAME_WIDTH) )
frame_height = int( cap.get( cv2.CAP_PROP_FRAME_HEIGHT) )

# Begin AI motion tracking
fourcc = cv2.VideoWriter_fourcc('X','V','I','D')
out = cv2.VideoWriter("clip_tracked.avi", fourcc, 25.0, (clip_w,clip_h))
ret, frame1 = cap.read()
ret, frame2 = cap.read()

while cap.isOpened():

    try:
        diff = cv2.absdiff(frame1, frame2)
        gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray, (5,5), 0)
        _, thresh = cv2.threshold(blur, 70, 255, cv2.THRESH_BINARY)
        dilated = cv2.dilate(thresh, None, iterations=3)
        contours, _ = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        for contour in contours:
            (x, y, w, h) = cv2.boundingRect(contour)

            if cv2.contourArea(contour) > 500:
                continue
            cv2.rectangle(frame1, (x, y), (x+w, y+h), (0, 255, 0), 2)
            cv2.putText(frame1, "Status: {}".format('Movement'), (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)
            #cv2.drawContours(frame1, contours, -1, (0, 255, 0), 2)

        image = cv2.resize(frame1, (clip_w,clip_h))
        out.write(image)
        cv2.imshow("feed", frame1)
        frame1 = frame2
        ret, frame2 = cap.read()

        if cv2.waitKey(40) == 27:
            break

    except:
        pass

cv2.destroyAllWindows()
cap.release()
out.release()

clip_tracked = VideoFileClip("clip.tracked.avi", audio=False)

# Save start and end frames
clip.save_frame("frame_start.png", t=0) # saves the frame a t=0s
clip_tracked.save_frame("frame_end.png", t=clip_tracked.duration-0.2) # saves the last frame

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
final = concatenate_videoclips([title, author, clip, loop1, loop2, loop3, loop4, clip_tracked, end, credits]).set_audio(audioclip)

# Write to file
final.write_videofile('ornithography_1.mp4',fps=25)
#-----------------------------------------------------------------------------------------------

print('** END')


