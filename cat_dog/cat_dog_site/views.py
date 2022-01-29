from django.shortcuts import render, redirect
from cat_dog_site.forms import ImageForm

from .models import Image

from io import StringIO
from PIL import Image, ImageOps
import os
from django.core.files import File

from fastai.vision.all import *

import base64

def is_cat(x): 
    return x[0].isupper()

learn_inference = load_learner("../train/model.pkl")

##https://stackoverflow.com/questions/623698/resize-image-on-save
def handle_uploaded_image(i):

        # create PIL Image instance
        #https://stackoverflow.com/questions/55191466/how-to-get-the-files-uploaded-in-inmemoryuploadedfile-django
        image = Image.open(i.file)

        # if not RGB, convert
        if image.mode not in ("L", "RGB"):
            image = image.convert("RGB")

        #define file output dimensions (ex 60x60)
        x = 224
        y = 224

        image = image.resize((x,y))

        #https://jdhao.github.io/2019/07/06/python_opencv_pil_image_to_bytes/
        buf = io.BytesIO()
        image.save(buf, format='JPEG')
        byte_im = buf.getvalue()

        is_cat,_,probs = learn_inference.predict(byte_im)

        return (is_cat, probs[1].item())

def obtain_text_description(prob_cat):
    if prob_cat > 0.95:
        return "Most likely a cat"
    if prob_cat < 0.05:
        return "Most likely a dog"
    if prob_cat > 0.6:
        return "Looks a bit like a cat"
    if prob_cat < 0.4:
        return "Looks a bit like a dog"
    else:
        return "The image is unclear"

def index(request):
    """Process images uploaded by users"""
    if request.method == 'POST':
        form = ImageForm(request.POST, request.FILES)
        if form.is_valid():
            is_cat, prob_cat = handle_uploaded_image(request.FILES['image'])

            image_data = base64.b64encode(request.FILES['image'].file.getvalue()).decode()

            return render(request, 
                    'cat_dog_site/index.html', 
                    {
                        'form': form, 
                        'img_obj': image_data, 
                        'desc': obtain_text_description(prob_cat)
                    }
                    )
    else:
        form = ImageForm()
    return render(request, 'cat_dog_site/index.html', {'form': form})
