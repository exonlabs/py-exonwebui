{% extends "webui/html.tpl" %}

{% block b_html_head %}
  <link rel="stylesheet" type="text/css" href="/static/webui/vendor/bootstrap/bootstrap{% if doc_langdir == 'rtl' %}-rtl{% endif %}.min.css">
  <link rel="stylesheet" type="text/css" href="/static/webui/vendor/fontawesome/css/fa4.min.css">
  <link rel="stylesheet" type="text/css" href="/static/webui/vendor/pnotify/pnotify.min.css">
  <link rel="stylesheet" type="text/css" href="/static/webui/vendor/metismenu/metisMenu.min.css">
  {% block b_board_head %}
    <link rel="stylesheet" type="text/css" href="/static/webui/css/webui.min.css">
    <link rel="stylesheet" type="text/css" href="/static/webui/css/webui_menuboard.min.css">
  {% endblock %}
{% endblock %}

{% block b_html_body %}
  {% block b_board_body %}
    <div id="board-wrapper" class="ease h-100" style="display:none">
      <div id="board-menu" class="ease h-100 d-print-none">
        <div id="board-menutoggle" class="text-right">
          <a title="{{gettext('Toggle Menu')}}"><i class="fa fas fa-bars"></i></a>
        </div>
        <div id="board-menubody" class="h-100 scroll">
          <div id="board-menuhead">
            {% block b_board_menuhead %}{% endblock %}
          </div>
          {% block board_menubody %}
            <ul class="metismenu">
              {% set links = get_menulinks() %}
              {% for i in links.keys()|sort %}
                {% if 'menu' in links[i] and links[i].menu.keys() %}
                  <li>
                    <a href="#" class="has-arrow">{% if links[i].icon %}<i class="fa fas fa-fw fa-ta {{links[i].icon}}"></i>{% endif %}{{links[i].label|safe}}</a>
                    <ul>
                      {% for j in links[i].menu.keys()|sort %}
                        <li><a class="pagelink" href="{{links[i].menu[j].url}}">{% if links[i].menu[j].icon %}<i class="fa fas fa-fw fa-ta {{links[i].menu[j].icon}}"></i>{% endif %}{{links[i].menu[j].label|safe}}</a></li>
                      {% endfor %}
                    </ul>
                  </li>
                {% elif links[i].url != '#' %}
                  <li>
                    <a class="pagelink" href="{{links[i].url}}">{% if links[i].icon %}<i class="fa fas fa-fw fa-ta {{links[i].icon}}"></i>{% endif %}{{links[i].label|safe}}</a>
                  </li>
                {% endif %}
              {% endfor %}
              <li><a></a></li>
            </ul>
          {% endblock %}
        </div>
      </div>
      <div id="board-page" class="h-100 scroll">
        <div id="board-pagehead" class="sticky-top">
          {% block b_board_pagehead %}
            <div id="pagehead-bar" class="d-flex">
              <div id="pagehead-title" class="flex-grow-1 text-truncate text-left">
                {% block b_pagehead_title %}{% endblock %}
              </div>
              <div id="pagehead-widgets" class="text-right d-print-none">
                {% block b_pagehead_widgets %}{% endblock %}
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
    <div id="board-backdrop" class="d-print-none"></div>
  {% endblock %}
  <script type="text/javascript" src="/static/webui/vendor/jquery/jquery.min.js"></script>
  <script type="text/javascript" src="/static/webui/vendor/jquery/jquery.i18n.min.js"></script>
  <script type="text/javascript" src="/static/webui/vendor/bootstrap/bootstrap.bundle.min.js"></script>
  <script type="text/javascript" src="/static/webui/vendor/pnotify/pnotify.min.js"></script>
  <script type="text/javascript" src="/static/webui/vendor/metismenu/metisMenu.min.js"></script>
  {% block b_board_scripts %}
    <script type="text/javascript" src="/static/webui/js/webui.min.js"></script>
    <script type="text/javascript" src="/static/webui/js/webui_menuboard.min.js"></script>
  {% endblock %}
{% endblock %}
