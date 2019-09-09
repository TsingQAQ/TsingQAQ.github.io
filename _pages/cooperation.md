---
title: "Open Cooperation"
permalink: /open_coop/
author_profile: True
---

"The path to greatness is along with others."
                                       Baltasar Gracian y Morales
{: .notice--success}


{% include base_path %}


{% for post in site.open_coop reversed %}
  {% include archive-single-talk.html %}
{% endfor %}
