from .models import StoreOwner
from django.core.exceptions import PermissionDenied
from django.core.cache import cache

def check_permission(method,model):
    def decorator(view_func):
        def _wrapper_view(self , request, *args,**kwargs):

            print("Helo")
            store_owner = StoreOwner.objects.filter(user = request.user)
            print(store_owner)
            if store_owner:
                store_owner = store_owner.first()
                if store_owner.owner_type == "ADMIN":
                    return view_func(self, request,*args,**kwargs)

                user_permissins = set()
                cache_key = f'user_permission_{request.user.id}'

                print(cache.get(cache_key))
                if cache.get(cache_key):
                    permissions =  cache.get(cache_key)
                else:
                    permissions = request.user.get_all_permissions()
                    cache.set(cache_key, permissions, 60 * 60)



                for perm in permissions:
                    user_permissins.add(perm)

                print(user_permissins)
                if method == 'GET':
                    permission = f'{model._meta.app_label}.view_{model._meta.model_name}'
                elif method == "POST":
                    permission = f'{model._meta.app_label}.add_{model._meta.model_name}'
                elif method == "PUT" or method == "PATCH":
                    permission = f'{model._meta.app_label}.change_{model._meta.model_name}'
                elif method == "DELETE":
                    permission = f'{model._meta.app_label}.delete_{model._meta.model_name}'
                else:
                    raise PermissionDenied("Un-supported method")


                if permission in user_permissins:
                    return view_func(self, request,*args,**kwargs)
                else:
                    raise PermissionDenied("You dont have permission")

            return view_func(self, request,*args,**kwargs)
        return _wrapper_view
    return decorator


