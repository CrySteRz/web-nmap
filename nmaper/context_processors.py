import os
def global_context(request):
    return {
        'product_name': os.getenv('PRODUCT_NAME'),
    }