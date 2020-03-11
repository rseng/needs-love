---
tags: 
title: "[needs-love] Singularity Registry Server add contributors to collection"
html_url: "https://github.com/rseng/needs-love/issues/8"
user: vsoch
repo: rseng/needs-love
---

## Description

A user has requested that an admin (a super user to be specific) is allowed to add custom users to a collection contributors or owners. This is something that seems reasonable in that it can be done with the manage.py (direct interaction with the container) but this is different from the user interface. For this needs love issue, if someone has some experience with jinja2 and python, we would want to update the view to allow this functionality, and make sure it doesn't break teams. See https://github.com/singularityhub/sregistry/issues/280.

## How can we help?

 - Update the shub/apps/main/templates/collections/_collection_settings_users.html and matching views in shub/apps/main/views/collections.py to allow for a super user to add users to be contributors or owners. I also think this should be set to be allowed (or not) as a global environment variable, with the default not allowing it (I don't see it being a pattern for any other registry, although I'm definitely not the super user there!)

Please open up discussion  here if you have any questions and would like to work on this issue to learn about Django, containers, or jinja2.