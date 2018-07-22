from main.models import Item, Category, Cart, Image
from rest_framework import serializers
from django.contrib.auth.models import User


class ItemSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField()
    description = serializers.CharField()
    price = serializers.DecimalField(max_digits=10, decimal_places=2)
    status = serializers.CharField()
    cover_img = serializers.PrimaryKeyRelatedField(queryset=Image.objects.all())
    cover_img_file = serializers.SerializerMethodField()
    currency = serializers.CharField()

    def get_cover_img_file(self, obj):
        return obj.cover_img.file.name


class CategorySerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField()
    img = serializers.PrimaryKeyRelatedField(queryset=Image.objects.all())
    cover_img_file = serializers.SerializerMethodField()

    def get_cover_img_file(self, obj):
        return obj.img.file.name

    def create(self, validated_data):
        return Category.objects.create(**validated_data)

# class SellerSerializer(serializers.Serializer):
#     id = serializers.IntegerField(read_only=True)
#     user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
#     name = models.CharField(max_length=255)
#     description = models.TextField()
#     photo = models.ForeignKey('Image', on_delete=models.PROTECT)
#     rank = models.CharField(max_length=30)
#     accepted_payment = models.CharField(max_length=30)
#     def create(self, validated_data):
#         return Category.objects.create(**validated_data)

class CartSerializer(serializers.Serializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    item = serializers.PrimaryKeyRelatedField(queryset=Item.objects.all())
    price = serializers.DecimalField(max_digits=10, decimal_places=2)
    quantity = serializers.IntegerField()
    charge = serializers.DecimalField(max_digits=10, decimal_places=2)
    total = serializers.DecimalField(max_digits=10, decimal_places=2)
    timestamp_added = serializers.CharField(max_length=30)
    currency = serializers.CharField(max_length=3)
    item_name = serializers.SerializerMethodField()
    cover_img_file = serializers.SerializerMethodField()

    def get_cover_img_file(self, obj):
        return obj.item.cover_img.file.name

    def get_item_name(self, obj):
        return obj.item.name

    def create(self, validated_data):
        return Cart.objects.create(**validated_data)

class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ('file', 'pk')

