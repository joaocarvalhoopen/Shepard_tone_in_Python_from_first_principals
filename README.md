# Shepard tone in Python from first principals
Fighting with a sound illusion!

# Description
This is my attempt to do a sound illusion called The Shepard Tone from first principles in  Python. I say that it is my attempt because it generates everything necessary to make the sound illusion of a note that is always going up or always going down, but the transition when repeating isn't perfect and I simply can't figure it out, why it isn't a perfect transition. <br>
<br>
**I have implemented everything:**
* A tone generator/oscillator for every note in the scale, for every scale. With fade in and fade out in each tone so that it's smother on the speakers.
* I have implemented 3 simultaneous tones going up or down in pitch (semi-tone). 
* I have implemented the logarithmic attenuation mechanism to fade out the amplitude of the upper note, and to fade in the lower note has the notes progress in the scale.
* I have implemented 12 note scale, the first note and the last note of the next scale as half the time, sow that the transition is smother between repeats. (See the first link in references).    
* I have implemented the save to wav file with the correct time and repetition.

But although it's all working and seems all correct, the illusion of continuum of notes always going up or always going down simply isn't there because of the transition at the beginning of the repetitions, it isn't smooth, and currently I don't know why. <br>
<br>
In the repository you will find two wave files, my two attempts at creating a shepard note and a Shepard glissando (continuum in frequency tone). <br>
<br>
I share this work, in the hope that it can be useful to others.


# References
* Because it's Friday: The Shepard Tone <br>
  [https://blog.revolutionanalytics.com/2017/08/because-its-friday-the-shepard-tone.html](https://blog.revolutionanalytics.com/2017/08/because-its-friday-the-shepard-tone.html)

* The Infinite Sound That Can Drive You Insane—Shepard Tones <br>
  [https://www.youtube.com/watch?v=oEW3F8B-lhU](https://www.youtube.com/watch?v=oEW3F8B-lhU)

* The Shepard Tone - Python code <br>
  [http://randbrown.com/python/music/2017/11/05/shepard-tone.html](http://randbrown.com/python/music/2017/11/05/shepard-tone.html)

* Physics of Music - Notes <br>
  [https://pages.mtu.edu/~suits/NoteFreqCalcs.html](https://pages.mtu.edu/~suits/NoteFreqCalcs.html) 


# License
MIT Open Source License


# Have Fun!
Best regards, <br>
João Nuno Carvalho
