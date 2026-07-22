from rest_framework import serializers
from .models import Good, GoodImage

class GoodImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = GoodImage
        fields = ['id', 'image', 'uploaded_at']
        read_only_fields = ['id', 'uploaded_at']

class GoodSerializer(serializers.ModelSerializer):
    # Read-only nested representation of images
    images = GoodImageSerializer(many=True, read_only=True)

    # Write-only field to accept new image files when creating/updating a Good.
    # NOTE: this changed from URLField -> ImageField because GoodImage.image_url
    # was switched to a real ImageField upload (Step 2a, MVP sprint). Not wired
    # up to a live endpoint yet since DRF write paths are deferred post-demo.
    upload_images = serializers.ListField(
        child=serializers.ImageField(),
        write_only=True,
        required=False
    )

    class Meta:
        model = Good
        fields = [
            'id', 'seller', 'category', 'title', 'description', 
            'price', 'condition', 'status', 'created_at', 'updated_at', 
            'images', 'upload_images'
        ]
        # The seller is set automatically based on the logged-in user
        read_only_fields = ['id', 'created_at', 'updated_at', 'seller']

    def validate(self, attrs):
        upload_images = attrs.get('upload_images', [])
        
        # Check limit during creation
        if not self.instance and len(upload_images) > 15:
            raise serializers.ValidationError({"upload_images": "A maximum of 15 images is allowed per good."})
        
        # Check limit during updates
        if self.instance:
            current_count = self.instance.images.count()
            if current_count + len(upload_images) > 15:
                raise serializers.ValidationError({
                    "upload_images": f"Adding these images exceeds the 15-image limit. Current count: {current_count}"
                })
                
        return attrs

    def create(self, validated_data):
        upload_images = validated_data.pop('upload_images', [])
        good = Good.objects.create(**validated_data)
        
        for image_file in upload_images:
            GoodImage.objects.create(good=good, image=image_file)
            
        return good

    def update(self, instance, validated_data):
        upload_images = validated_data.pop('upload_images', [])
        
        for image_file in upload_images:
            GoodImage.objects.create(good=instance, image=image_file)
            
        return super().update(instance, validated_data)