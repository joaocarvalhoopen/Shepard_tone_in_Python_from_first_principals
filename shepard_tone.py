# Project name: Shepard tone in Python from first principals
# Author:       João Nuno Carvalho
# Date:         2021.03.30
# License:      MIT Open Source License
#
# Description:  This is my attempt to do a sound illusion called The Shepard
#               Tone from first principles in  Python. I say that it is my
#               attempt because it generates everything necessary to make the 
# sound illusion of a note that is always going up or always going down, but 
# the transition when repeating isn't perfect and I simply can't figure it out,
# why it isn't a perfect transition. <br>
#
# I have implemented everything:
# * A tone generator/oscillator for every note in the scale, for every scale.
#   With fade in and fade out in each tone so that it's smother on the speakers.
# * I have implemented 3 simultaneous tones going up or down in pitch (semi-tone). 
# * I have implemented the logarithmic attenuation mechanism to fade out the
#   amplitude of the upper note, and to fade in the lower note has the notes
#   progress in the scale.
# * I have implemented 12 note scale, the first note and the last note of the next
#   scale as half the time, sow that the transition is smother between repeats. 
#   (See the first link in references).    
# * I have implemented the save to wav file with the correct time and repetition.
#
# But although it's all working and seems all correct, the illusion of continuum
# of notes always going up or always going down simply isn't there because of the
# transition at the beginning of the repetitions, it isn't smooth, and currently I
# don't know why. 
#
# In the repository you will find two wave files, my two attempts at creating a
# shepard note and a Shepard glissando (continuum in frequency tone).
#
# I share this work, in the hope that it can be useful to others.
#
#
# References
# * Because it's Friday: The Shepard Tone 
#  https://blog.revolutionanalytics.com/2017/08/because-its-friday-the-shepard-tone.html
#
# * The Infinite Sound That Can Drive You Insane—Shepard Tones <br>
#   https://www.youtube.com/watch?v=oEW3F8B-lhU
#
# * The Shepard Tone - Python code <br>
#   http://randbrown.com/python/music/2017/11/05/shepard-tone.html
#
# * Physics of Music - Notes
#   https://pages.mtu.edu/~suits/NoteFreqCalcs.html
#

import math
import numpy as np
import wave

DIR_CONST = 'DIR_CONST'
UP        = 'DIR_UP'
DOWN      = 'DIR_DOWN'

UPPER  = 'UPPER'
BOTTOM = 'BOTTOM'

# For the calculations of the music scale.
TWELVE_ROOT_OF_2 = math.pow(2, 1.0 / 12)


def cos_oscillator(sample_rate, freq, time_of_each_note, amplitude):
    last_step = int(sample_rate * time_of_each_note)
    increment = (2 * math.pi * freq) / sample_rate
    buf_list = []
    for i in range(0, last_step):
        val = math.cos(increment * i) * amplitude
        if i < 50:
            val = val * (1.0 / 50) * i
        elif i > (last_step - 50):
            val = val * (1.0 / 50) * (last_step - i)
        buf_list.append(val)
    return buf_list


def cos_wave_with_movement(sample_rate, freq_start, freq_end, freq_time):
    last_step = int(sample_rate * freq_time)
    freq_step = (freq_end - freq_start) / float(last_step)
    buf_list = []
    val = 0.0
    freq = freq_start
    for i in range(0, last_step):
        increment = (2 * math.pi * (freq + freq_step * i)) / sample_rate
        val = increment * i
        buf_list.append(math.cos(val))
        # buf_list.append(math.sin(val))
    return buf_list


def shepard_tone_glissando(sample_rate, freq_middle_start, velocity_time, num_octaves_down=3, num_octaves_up=3):
    # Generate the middle tone.
    freq_start = freq_middle_start
    freq_end   = freq_start * 2.0
    freq_time = velocity_time
    values = cos_wave_with_movement(sample_rate, freq_start, freq_end, freq_time)
    
    # Generate the simultaneous lower octaves.
    for i in range(0, num_octaves_down):
        freq_start = freq_middle_start * 2.0**(-(i+1))
        freq_end   = freq_middle_start * 2.0**(-(i+2))
        values_i = cos_wave_with_movement(sample_rate, freq_start, freq_end, freq_time)
        if i == (num_octaves_down - 1):
            # The first (lowest) octave will be attenuated (faded in).
            intensity_step = 1.0 / len(values_i)
            for i in range(0, len(values_i)):
                values_i[i] = values_i[i] * intensity_step * i
        for i in range(0, len(values)):
            values[i] += values_i[i]
 
    # Generate the simultaneous upper octaves.
    for i in range(0, num_octaves_up):
        freq_start = freq_middle_start * 2.0**(i+1)
        freq_end   = freq_middle_start * 2.0**(i+2)
        values_i = cos_wave_with_movement(sample_rate, freq_start, freq_end, freq_time)
        if i == (num_octaves_up-1):
            # The last (upper) octave will be attenuated (fadded out).
            intensity_step = 1.0 / len(values_i)
            for i in range(0, len(values_i)):
                values_i[i] = values_i[i] * (1.0 - intensity_step  * i)
        for i in range(0, len(values)):
            values[i] += values_i[i]
 
    # Normalize.
    factor = 1.0 + num_octaves_down + num_octaves_up
    for i in range(0, len(values)):
        values[i] /= factor

    return values


def freq_for_note(base_note, note_index):
    # See Physics of Music - Notes
    #     https://pages.mtu.edu/~suits/NoteFreqCalcs.html
    
    A4 = 440.0

    base_notes_freq = {"A2" : A4 / 4,   # 110.0 Hz
                       "A3" : A4 / 2,   # 220.0 Hz
                       "A4" : A4,       # 440.0 Hz
                       "A5" : A4 * 2,   # 880.0 Hz
                       "A6" : A4 * 4 }  # 1760.0 Hz  

    scale_notes = { "C"  : -9.0,
                    "C#" : -8.0,
                    "D"  : -7.0,
                    "D#" : -6.0,
                    "E"  : -5.0,
                    "F"  : -4.0,
                    "F#" : -3.0,
                    "G"  : -2.0,
                    "G#" : -1.0,
                    "A"  :  1.0,
                    "A#" :  2.0,
                    "B"  :  3.0,
                    "Cn" :  4.0}

    scale_notes_index = list(range(-9, 5)) # Has one more note.
    note_index_value = scale_notes_index[note_index]
    freq_0 = base_notes_freq[base_note]
    freq = freq_0 * math.pow(TWELVE_ROOT_OF_2, note_index_value) 
    return freq


def calc_log_attenuation(index):
    return abs(1 - abs(math.log10( (index+1) / 13 ))) # 12


def gen_notes_sequence(sample_rate, base_note, time, direction=UP, attenuated=False, layer=None):
    note_range = None
    amplitude = 1.0
    amplitude_step = 0.0
    offset = 0
    # lower_to_upper = range(0, 12)
    # upper_to_lower = range(11, -1, -1)
    lower_to_upper = range(0, 13)
    upper_to_lower = range(12, -1, -1)
    if direction == UP:

        note_range = lower_to_upper
        if attenuated:
            amplitude_step = 1.0
            if layer == BOTTOM:
                offset = 0
            elif layer == UPPER:
                # offset = 11
                offset = 12
    elif direction == DOWN:
        note_range = upper_to_lower
        if attenuated:
            amplitude_step = 1.0
            if layer == BOTTOM:
                # offset = 11
                offset = 12
            elif layer == UPPER:
                offset = 0

    wave_buf = []
    for i in note_range:
        note_index = i
        if attenuated:
            amplitude = calc_log_attenuation(abs(offset - amplitude_step * i))
        freq = freq_for_note(base_note, note_index)
        # buf = cos_oscillator(sample_rate, freq, time / 12.0, amplitude * 0.5)
        note_time = time / 12.0
        if i == 0:
            note_time /= 2
        elif i == 12:
            note_time /= 2
        print("i:", i, "amplitude_step * i:", amplitude_step * i, 'amplitude:', amplitude, " note_time:", note_time, " freq:", freq)
        
        buf = cos_oscillator(sample_rate, freq, note_time, amplitude )
        wave_buf.extend(buf)
    return wave_buf


def shepard_tone(sample_rate, time, direction=UP):
    values = gen_notes_sequence(sample_rate, 'A4', time, direction, attenuated=False)
    
    # Generate the simultaneous lower octave.
    values_lower = gen_notes_sequence(sample_rate, 'A3', time, direction, attenuated=True, layer=BOTTOM)

    # Generate the simultaneous upper octave.
    values_upper = gen_notes_sequence(sample_rate, 'A5', time, direction, attenuated=True, layer=UPPER)

    for i in range(0, len(values)):
        values[i] = (values[i] + values_lower[i] + values_upper[i]) / 3.0
    return values


def shepard_tone_5_notes(sample_rate, time, direction=UP):
    values = gen_notes_sequence(sample_rate, 'A4', time, direction, attenuated=False)
    
    # Generate the simultaneous lower octave.
    values_lower_1 = gen_notes_sequence(sample_rate, 'A3', time, direction, attenuated=False)
    values_lower_0 = gen_notes_sequence(sample_rate, 'A2', time, direction, attenuated=True, layer=BOTTOM)
    # Generate the simultaneous upper octave.
    values_upper_0 = gen_notes_sequence(sample_rate, 'A5', time, direction, attenuated=False)
    values_upper_1 = gen_notes_sequence(sample_rate, 'A6', time, direction, attenuated=True, layer=UPPER)
    for i in range(0, len(values)):
        values[i] = (values[i] + values_lower_0[i] + values_lower_1[i] + values_upper_0[i] + values_upper_1[i]) / 5.0
    return values


def writeArrayToWavFilename(signalArray, sampleFreq, destinationWavFilename):
    # Converts the NumPy contiguous array into frames to be written into the file.
    # From range [-1, 1] to -/+ 2^15 , 16 bits signed
    signalTemp = np.zeros(len(signalArray), np.int16)
    for i in range(0, len(signalTemp)):
        signalTemp[i] = int( signalArray[i] * (2.0**15) )
        #signalTemp[i] = int( signalArray[i] )   # Data already in a float of 16bit unsigned range.

    # Convert float64 into Int16.
    # This means that the sound pressure values are mapped to integer values that can range from -2^15 to (2^15)-1.
    numFrames = signalTemp.tostring()

    # Write file from harddisc.
    wavHandler = wave.open(destinationWavFilename,'wb') # Write only.
    wavHandler.setnframes(len(signalArray))
    wavHandler.setframerate(sampleFreq)
    wavHandler.setnchannels(1)
    wavHandler.setsampwidth(2) # 2 bytes
    wavHandler.writeframes(numFrames)


def main_glissando():
    sample_rate   = 44100
    wav_duration  = 20.0
    velocity_time = 12.0 # seconds
    freq_A4       = 440  # Hz
    freq_middle_start = freq_A4
    values = shepard_tone_glissando(sample_rate, freq_middle_start, velocity_time, num_octaves_down=1, num_octaves_up=1)

    # Create numpy array from a list.
    signal_array = np.array(values)
    stack_num = math.ceil(wav_duration / velocity_time)
    stack_list = []
    for i in range(0, stack_num):
        stack_list.append(signal_array)
    signal_array = np.hstack(stack_list)
    max_sample = int(wav_duration * sample_rate)
    signal_array = signal_array[0:max_sample]
    destinationWavFilename = "sound_sheppard_tone_glissando.wav"
    writeArrayToWavFilename(signal_array, sample_rate, destinationWavFilename)


def main_individual_notes():
    sample_rate          = 44100
    wav_duration         = 12.0 # 12.0
    time_each_repetition = 4.0 # seconds
    direction            = UP
    values = shepard_tone(sample_rate, time_each_repetition, direction)

    # Create numpy array from a list.
    signal_array = np.array(values)
    stack_num = math.ceil(wav_duration / time_each_repetition)
    stack_list = []
    for i in range(0, stack_num):
        stack_list.append(signal_array)
    signal_array = np.hstack(stack_list)
    max_sample = int(wav_duration * sample_rate)
    signal_array = signal_array[0:max_sample]
    destinationWavFilename = "sound_sheppard_tone.wav"
    writeArrayToWavFilename(signal_array, sample_rate, destinationWavFilename)


if __name__ == "__main__":
    main_individual_notes()
    # main_glissando()    

