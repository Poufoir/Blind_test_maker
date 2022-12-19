# Blind_test_maker

This library lets you create your own Blind test

## Download

First of all, you need [ffmpeg](https://ffmpeg.org/download.html), [miniconda](https://docs.conda.io/en/latest/miniconda.html) or [anaconda](https://www.anaconda.com/products/distribution) and [Blind test maker repository](https://github.com/Poufoir/Blind_test_maker.git) <br />
You do not need to install them, just download the files and extract them.

## Activate environment

Open a command prompt shell and go to your miniconda files (example : D:/Miniconda3/)

```bash
cd D:
cd Miniconda3/condabin
activate.bat
```

## Build the environment

Go to your location of BLind test maker repository (example : D:/Download/Blind_test_maker)

```bash
cd D:
cd /Download/Blind_test_maker
conda env create -f environment.yml
conda activate blind_test_maker
```

## Using Python

```bash
python -m VideoMakerFromImage
```

# How to use the interface

## Paths

   - Path for video : video you download with countdown (example : D:/Download/Blind_test_maker/VideoMakerFromImage/5 SECOND TIMER.mp4)
   - Path for image : image you want to display when you display the answer (example : D:/Download/Blind_test_maker/VideoMakerFromImage/sunrise.webp)

## Video

   - Time to start video : Start the video you download with countdown from the duration entered
   - Duration of the video : If you want a coundown of 5s and got a video of 10...
   - Color of Answer : Enter in lowercase a basic color

## Music 

   - Add music and Answer :
      - Link or Path : You must enter a download audio
      - Start of music : If you want to start listening music from a time
   - Remove music :
      - Answer : if you want to delete the answer
      - row : if you did not enter Answer and want to delete a row
   - Show Answer : show music entered and Answer, good use for removing music. You can close this, there will not any changes

Note: you cannot create a video longer than 40 minutes