---
title: "Open Cooperation"
permalink: /open_coop/
author_profile: True
---

{% include base_path %}


{% for post in site.open_coop reversed %}
  {% include archive-single-talk.html %}
{% endfor %}
