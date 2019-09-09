---
title: "Open Cooperation"
permalink: /open_coop/
author_profile: True
---

{% include base_path %}


{% for post in site.projects reversed %}
  {% include archive-single-talk.html %}
{% endfor %}
