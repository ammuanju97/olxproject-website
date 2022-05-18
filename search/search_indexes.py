from haystack import indexes
from seller.models import PostProduct
class BookIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True, template_name="search/product.txt")
    product_name = indexes.CharField(model_attr='product_name')
    user = indexes.CharField()
    image = indexes.CharField()

    def get_model(self):
        return PostProduct
    def prepare_user(self, obj):
        return [ user.name for a in obj.user.all()]
    def prepare_image(self, obj):
        # Get first images for resulted search objects
        return [image.image_main_page.url for image in obj.images.order_by('id')[:1]]
    def index_queryset(self, using=None):
        return self.get_model().objects.all()
    