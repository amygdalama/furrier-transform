This was an attempt at creating a sound from an image of my cat. The idea was that, since a spectrogram is an "image" representation of a sound, an arbitrary image could be interpreted as a spectrogram of a sound. With that assumption, I attempted to create a sound that would have the spectrogram of an image of my cat.

I quickly realized that starting with an image of my cat was a bad idea, because I had no way of telling if the sound I created was correct or not. So, I decided to start with an actual spectrogram of an actual sound, and then try to reconstruct the original sound from the spectrogram. Then I could tell if I was even close or not.

Later I found that this is actually a ["longstanding problem in audio signal processing"](http://arxiv.org/abs/1209.2076) and is anything but trivial. So, needless to say, I never "completed" this project. But I think I'm finally okay with that.

Fair warning: you do not want to listen to any audio files that this program creates. They are wildly unpleasant.

I really need to work on organizing this repository. In the meantime, pay most attention to [furrier-transform.py](https://github.com/amygdalama/furrier-transform/blob/master/furrier-transform.py) and [additive-synthesis.ipynb](http://nbviewer.ipython.org/github/amygdalama/furrier-transform/blob/master/additive-synthesis.ipynb).

## Dependencies

* libjpeg
* libsndfile
* pil
* scikits.audiolab


