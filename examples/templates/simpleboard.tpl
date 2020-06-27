{% extends "webui/simpleboard.tpl" %}

{% block b_board_head %}
  {{super()}}
  <link rel="icon" type="image/png" href="/static/images/favicon.png">
  <link rel="apple-touch-icon" type="image/png" href="/static/images/favicon.png">
  <meta name="theme-color" content="#343a40">
{% endblock %}

{% block b_board_menuhead %}
  <div class="pb-2">
    <img class="img-fluid" src="/static/images/logo.png">
  </div>
{% endblock %}

{% block b_pagehead_title %}
  <span>{{gettext("Sample Portal")}}</span>
{% endblock %}

{% block b_board_scripts %}
  {% if doc_lang and doc_lang != 'en' %}<script type="text/javascript" src="/static/i18n/{{doc_lang}}.min.js"></script>{% endif %}
  {{super()}}
{% endblock %}
