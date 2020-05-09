{%- extends "webui/html.tpl" -%}

{%- block b_html_head -%}
  <link rel="stylesheet" type="text/css" href="/static/webui/vendor/bootstrap/bootstrap{% if page_langdir == 'rtl' %}-rtl{% endif %}.min.css">
  <link rel="stylesheet" type="text/css" href="/static/webui/vendor/fontawesome/css/all.min.css">
  <link rel="stylesheet" type="text/css" href="/static/webui/vendor/pnotify/pnotify.min.css">
  <link rel="stylesheet" type="text/css" href="/static/webui/css/webui.min.css">
  <script type="text/javascript" src="/static/webui/vendor/jquery/jquery.min.js"></script>
  <script type="text/javascript" src="/static/webui/vendor/jquery/jquery.i18n.min.js"></script>
  <script type="text/javascript" src="/static/webui/vendor/bootstrap/bootstrap.bundle.min.js"></script>
  <script type="text/javascript" src="/static/webui/vendor/pnotify/pnotify.min.js"></script>
  <script type="text/javascript" src="/static/webui/js/webui.js"></script>
  {% block b_page_head %}{% endblock %}
{%- endblock -%}

{%- block b_html_body -%}
  {% block b_page_body %}{% endblock %}
  {% block b_page_scripts %}
    <script type="text/javascript">
      $(document).ready(function(){WebUI.init()});
    </script>
  {% endblock %}
{%- endblock -%}
