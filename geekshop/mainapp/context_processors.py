from basketapp.models import Basket


def basket(request):
    basket_item = []

    if request.user.is_authenticated:
        basket_item = Basket.objects.filter(user=request.user).order_by('product__category').select_related()

    return {
        'basket': basket_item
    }