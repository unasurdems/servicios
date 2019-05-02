import requests
from typing import List, Dict
from django.conf import settings

from .models import Usuario, Menu, UsuarioMenu


def get_menu_user(user: Usuario) -> List[Dict]:
    """
    Return dinamic menus for each user

    Paramters:
        user (Usuario): User owner of menu

    Returns:
        List(Dict): All menus for the user
    """
    menus = UsuarioMenu.objects.filter(usuario=user).values_list('menu_id', flat=True)

    user_menu = []

    def get_parents(menu_id):
        if menu_id:
            if not list(filter(lambda x: x['id'] == menu_id, user_menu)):
                menu = Menu.objects.values('id', 'menu', 'navbar', 'icon', 'url_path', 'component', 'orden', 'parent_id').get(id=menu_id)
                user_menu.append((menu))

                if menu['parent_id']:
                    get_parents(menu['parent_id'])

    def get_ordered(parent_id: int):
        menu_level = list(filter(lambda x: x['parent_id'] == parent_id, user_menu))

        for menu_item in menu_level:
            menu_item['children'] = get_ordered(menu_item['id'])

        return sorted(menu_level, key=lambda x: x['orden'])

    for item in menus:
        menu = Menu.objects.values('id', 'menu', 'navbar', 'icon', 'url_path', 'component', 'orden', 'parent_id').get(id=item)
        user_menu.append(menu)
        get_parents(menu['parent_id'])

    return get_ordered(None)