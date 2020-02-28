{%- extends "webui/menuboard.tpl" -%}

{% block b_board_head %}
  {%- if page_lang and page_lang != 'en' -%}
  <script type="text/javascript" src="/static/i18n/{{page_lang}}.min.js"></script>
  {%- endif %}
  <link rel="icon" type="image/png" href="/static/images/favicon.png">
  <link rel="apple-touch-icon" type="image/png" href="/static/images/favicon.png">
  <meta name="theme-color" content="#343a40">
{% endblock %}

{% block b_board_menuhead %}
  <img class="img-fluid" src="/static/images/logo.png">
{% endblock %}

{% block b_board_title %}
  <span>{{gettext("Sample Portal")}}</span>
{% endblock %}
