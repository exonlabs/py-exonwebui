{% extends "webui/menuboard.tpl" %}

{% block b_board_head %}
  {{super()}}
  <link rel="icon" type="image/png" href="/static/images/favicon.png">
  <link rel="apple-touch-icon" type="image/png" href="/static/images/favicon.png">
  <meta name="theme-color" content="#343a40">
{% endblock %}

{% block b_board_menuhead %}
  <div class="p-3">
    <img class="img-fluid" src="/static/images/logo.png">
  </div>
{% endblock %}

{% block b_board_pagehead %}
  {{super()}}
  <div class="px-3 text-right text-info" style="line-height:18px; margin-bottom:-20px">
    <small>[info bar]</small>
  </div>
{% endblock %}

{% block b_pagehead_title %}
  <span>{{gettext("Sample Portal")}}</span>
{% endblock %}

{% block b_pagehead_widgets %}
  <div class="btn-group">
    <button type="button" class="btn btn-sm dropdown-toggle" data-toggle="dropdown">
      <i class="fa fas fa-user"></i>
    </button>
    <div class="dropdown-menu dropdown-menu-right">
      <a class="dropdown-item btn-sm px-3" href="#?toogleboard=1">{{gettext("Toogle boards")}}</a>
      <div class="dropdown-divider"></div>
      <a class="dropdown-item btn-sm px-3 pagelink" href="/?lang=en">English</a>
      <a class="dropdown-item btn-sm px-3 pagelink" href="/?lang=ar">عربي</a>
      <a class="dropdown-item btn-sm px-3 pagelink" href="/?lang=fr">Français</a>
      <div class="dropdown-divider"></div>
      <a class="dropdown-item btn-sm px-3" href="/loginpage">
        <i class="fa fas fa-flip fa-sign-out fa-sign-out-alt"></i>
      </a>
    </div>
  </div>
{% endblock %}

{% block b_board_pagebody %}
  <div id="pagebody-contents" class="pt-3"></div>
{% endblock %}

{% block b_board_scripts %}
  {% if doc_lang and doc_lang != 'en' %}<script type="text/javascript" src="/static/i18n/{{doc_lang}}.min.js"></script>{% endif %}
  {{super()}}
{% endblock %}
