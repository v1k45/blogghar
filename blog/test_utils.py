from django.contrib.auth.models import User
from authapp.models import UserProfile
from .models import Blog


class DdtDict(dict):
    pass


def annotate_dict(value_dict, key_name):
    obj = DdtDict(**value_dict)
    obj.__name__ = value_dict[key_name]
    return obj


def auth_dict(username, password):
    val_dict = {'username': username, 'password': password}
    return val_dict


def auth_ddt_data(username, password, key_name='username'):
    value_dict = auth_dict(username, password)
    obj = annotate_dict(value_dict, key_name)
    return obj


def initial_users():

        # user_with_blog
        user_with_blog = User.objects.create_user(
            'user_with_blog', 'user_with@bl.og', 'user_with_blog@pw',
            )
        UserProfile.objects.create(user=user_with_blog, user_type='b')
        blog_1 = Blog(title='Sample blog', tag_line='Sample tag line',
                      short_description='Sample description',
                      author=user_with_blog)
        blog_1.save()

        # user_without_blog
        user_without_blog = User.objects.create_user(
            'user_without_blog', 'user_without@bl.og', 'user_without_blog@pw',
            )
        UserProfile.objects.create(user=user_without_blog, user_type='b')

        # reader
        reader_without_blog = User.objects.create_user(
            'reader_without_blog', 'reader_without@bl.og',
            'reader_without_blog@pw',
            )
        UserProfile.objects.create(user=reader_without_blog, user_type='r')

        data = {
            'user_with_blog': user_with_blog,
            'user_without_blog': user_without_blog,
            'reader_without_blog': reader_without_blog,
        }

        return data
