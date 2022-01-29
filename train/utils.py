#Necessary to have this outside for deployment,
#as fastai saves the context and we can not have
#the context as __main__

# Decide if training image is cat or dog, based on the
# filename
def is_cat(x): return x[0].isupper()
