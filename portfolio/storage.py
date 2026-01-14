from cloudinary_storage.storage import RawMediaCloudinaryStorage

class PublicMediaStorage(RawMediaCloudinaryStorage):
    """Custom Cloudinary storage that forces public access for all uploads"""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Force all uploads to be public and use 'raw' resource type
        self.CLOUDINARY_RESOURCE_OPTIONS = {
            'resource_type': 'raw',
            'type': 'upload',
            'access_mode': 'public',
        }
    
    def _upload_options(self):
        """Override upload options to ensure public access"""
        options = super()._upload_options()
        options.update({
            'resource_type': 'raw',
            'type': 'upload', 
            'access_mode': 'public',
        })
        return options
