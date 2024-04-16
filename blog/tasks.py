from celery import shared_task
from PIL import Image

from blog.models import Post


@shared_task
def image_resize_task(instance_id):
    try:
        instance = Post.objects.get(id=instance_id)
        # Open the image using PIL
        img = Image.open(instance.image.path)

        # Resize the image to the desired dimensions
        resized_img = img.resize((500, 500))

        # Save the resized image back to the same path
        resized_img.save(instance.image.path)
    except Post.DoesNotExist:
        # Handle the case when the object does not exist
        print(f"Post object with id={instance_id} does not exist.")
