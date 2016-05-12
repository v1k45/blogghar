# blogghar
_Home for bloggers_ (Yeah, a really bad pun)

This project is part of the internship assignment by qwikpik.

## Feature requirements:

1. Blog – A blog consists of text, images and other media objects and data which could be arranged as required.

2.       Tags – Each blog will be having some tags associated with it. (e.g. Name of blog – Trip to paris; could have tags like Europe, France associated with it.) The tags could be added to multiple blogs and a blog could have multiple tags associated with it. User should be able to create, edit and delete the tags.

3.       Users – There will be different sets of user having different permission, roles and actions, along with basic profile info about them.

a.       Blogger –

*         Blogger should able to add, create, edit and delete blogs.

*        Add and arrange different text and media elements to the blog.

*         Associate tags with the blogs

b.      Readers – Reader could login into the application. Read,and comment on the blog.

c.       Admin – Admin should be able to control and manage users, blogs, tags and display of blogs

## Features included in project:

* User authentication (Using django-allauth)
* Different types of users (Readers/ Bloggers)
* User profile with basic info like avatar and about.
* Role based access control.
* Blog details update functionality.
* Blog publicly inaccessible switch
* Post publish/draft status
* Post create/delete ability
* Post cover (fancy thing nowadays)
* Tags with autocomplete.
* Anyone can read posts (I thought it was to restrictive to let only readers to see posts.)
* User comments (accessible to only users)
* Markdown rendered posts (using python-markdown)
* WYSIYWG Markdown editor using SimpleMDE
* Extended feature of Markdown editor to upload images
* Material design.
* Django Admin support.

## Opensource projects used:

* django-allauth
* django-autocomplete-light (3.0.4)
* django-crispy-forms
* materializecss

## Colophon

I did many things for the first time in project. Tried Atom editor (I normally stick with subl/pycharm). It is a nice editor, has virtualenv support, nice linter and gutters and other awesome features. I really liked it.

Along with the editor, one major thing I decided to try was django's class based views. I used to stay away from it and stick to fbvs, this is why I decided to write this project using class based views (because where is the fun in doing same thing again and again).

Using class-based-views was a really nice experience. It makes sure that your code is dry and saves you from repeating same things again and again.

Ps: Screenshots are available in directory named `screenshots`.

Pps: This project was developed for demonstration purpose only. This may not be _production-ready_.
