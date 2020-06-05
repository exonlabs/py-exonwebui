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

{% block b_board_widgets %}
  <div class="btn-group">
    <button type="button" class="btn btn-sm dropdown-toggle" data-toggle="dropdown">
      <i class="fas fa-user"></i>
    </button>
    <div class="dropdown-menu dropdown-menu-right">
      <a class="dropdown-item btn-sm px-3" href="#?toogleboard=1">{{gettext("Toogle boards")}}</a>
      <div class="dropdown-divider"></div>
      <a class="dropdown-item btn-sm px-3" href="#?lang=en">English</a>
      <a class="dropdown-item btn-sm px-3" href="#?lang=ar">عربي</a>
      <a class="dropdown-item btn-sm px-3" href="#?lang=fr">Français</a>
      <div class="dropdown-divider"></div>
      <a class="dropdown-item btn-sm px-3" href="/loginpage">
        <i class="fas fa-flip fa-sign-out-alt"></i>
      </a>
    </div>
  </div>
{% endblock %}
