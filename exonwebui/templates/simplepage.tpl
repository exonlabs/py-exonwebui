{% extends "webui/html.tpl" %}

{% block b_html_head %}
  <link rel="stylesheet" type="text/css" href="/static/webui/vendor/bootstrap/bootstrap{% if doc_langdir == 'rtl' %}-rtl{% endif %}.min.css">
  <link rel="stylesheet" type="text/css" href="/static/webui/vendor/fontawesome/css/fa4.min.css">
  <link rel="stylesheet" type="text/css" href="/static/webui/vendor/pnotify/pnotify.min.css">
  {% block b_page_head %}
    <link rel="stylesheet" type="text/css" href="/static/webui/css/webui.min.css">
  {% endblock %}
{% endblock %}

{% block b_html_body %}
  {% block b_page_body %}{% endblock %}
  <script type="text/javascript" src="/static/webui/vendor/jquery/jquery.min.js"></script>
  <script type="text/javascript" src="/static/webui/vendor/jquery/jquery.i18n.min.js"></script>
  <script type="text/javascript" src="/static/webui/vendor/bootstrap/bootstrap.bundle.min.js"></script>
  <script type="text/javascript" src="/static/webui/vendor/pnotify/pnotify.min.js"></script>
  {% block b_page_scripts %}
    <script type="text/javascript" src="/static/webui/js/webui.min.js"></script>
  {% endblock %}
{% endblock %}
