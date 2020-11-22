{% extends "webui/html.tpl" %}

{% block b_html_head %}
  <link rel="stylesheet" type="text/css" href="/static/webui/vendor/bootstrap/bootstrap{% if doc_langdir == 'rtl' %}-rtl{% endif %}.min.css">
  <link rel="stylesheet" type="text/css" href="/static/webui/vendor/fontawesome/css/fa4.min.css">
  <link rel="stylesheet" type="text/css" href="/static/webui/vendor/pnotify/pnotify.min.css">
  {% block b_board_head %}
    <link rel="stylesheet" type="text/css" href="/static/webui/css/webui.min.css">
    <link rel="stylesheet" type="text/css" href="/static/webui/css/webui_simpleboard.min.css">
  {% endblock %}
{% endblock %}

{% block b_html_body %}
  {% block b_board_body %}
    <div id="board-wrapper" class="ease h-100" style="display:none">
      <div id="board-menu" class="ease h-100 d-print-none">
        <div id="board-menubody" class="h-100 scroll">
          <div id="board-menuhead">
            {% block b_board_menuhead %}{% endblock %}
          </div>
          {% block board_menubody %}
            {% set links = get_menulinks() %}
            {% for i in links.keys()|sort %}
              <div class="list-group pb-2">
                {% if 'menu' in links[i] and links[i].menu.keys() %}
                  <div class="list-group-item list-group-item-secondary py-2">{% if links[i].icon %}<i class="fa fas fa-fw fa-ta {{links[i].icon}}"></i>{% endif %}{{links[i].label|safe}}</div>
                  {% for j in links[i].menu.keys()|sort %}
                    <a class="pagelink list-group-item list-group-item-action" href="{{links[i].menu[j].url}}">{% if links[i].menu[j].icon %}<i class="fa fas fa-fw fa-ta {{links[i].menu[j].icon}}"></i>{% endif %}{{links[i].menu[j].label|safe}}</a>
                  {% endfor %}
                {% elif links[i].url != '#' %}
                  <a class="pagelink list-group-item list-group-item-action" href="{{links[i].url}}">{% if links[i].icon %}<i class="fa fas fa-fw fa-ta {{links[i].icon}}"></i>{% endif %}{{links[i].label|safe}}</a>
                {% endif %}
              </div>
            {% endfor %}
          {% endblock %}
        </div>
      </div>
      <div id="board-page" class="h-100 scroll">
        <div id="board-pagehead">
          {% block b_board_pagehead %}
            <div id="pagehead-bar" class="d-flex">
              <div id="pagehead-title" class="flex-grow-1 text-truncate text-left">
                {% block b_pagehead_title %}{% endblock %}
              </div>
            </div>
          {% endblock %}
        </div>
        <div id="board-pagebody" class="h-100">
          {% block b_board_pagebody %}
            <div id="pagebody-contents"></div>
          {% endblock %}
        </div>
      </div>
    </div>
  {% endblock %}
  <script type="text/javascript" src="/static/webui/vendor/jquery/jquery.min.js"></script>
  <script type="text/javascript" src="/static/webui/vendor/jquery/jquery.i18n.min.js"></script>
  <script type="text/javascript" src="/static/webui/vendor/bootstrap/bootstrap.bundle.min.js"></script>
  <script type="text/javascript" src="/static/webui/vendor/pnotify/pnotify.min.js"></script>
  {% block b_board_scripts %}
    <script type="text/javascript" src="/static/webui/js/webui.min.js"></script>
    <script type="text/javascript" src="/static/webui/js/webui_simpleboard.min.js"></script>
  {% endblock %}
{% endblock %}
