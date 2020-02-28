{%- extends "webui/simplepage.tpl" -%}

{% block b_page_head %}
  <script type="text/javascript" src="/static/webui/vendor/cryptojs/md5.min.js"></script>
  {%- if page_lang and page_lang != 'en' -%}
  <script type="text/javascript" src="/static/i18n/{{page_lang}}.min.js"></script>
  {%- endif %}
  <link rel="icon" type="image/png" href="/static/images/favicon.png">
  <link rel="apple-touch-icon" type="image/png" href="/static/images/favicon.png">
  <meta name="theme-color" content="#343a40">
{% endblock %}

{% block b_page_body %}
  <div id="loginpage-wrapper">
    <div class="container-fluid ">
      <div class="row">
        <div class="col-xs-12 p-4">
          <img src="/static/images/logo.png" height="50px">
        </div>
      </div>
      <div class="row">
        <div class="col-xs-12 col-sm-6 col-md-4 col-lg-3 mx-auto pt-5">
          {{loginform|safe}}
          <div class="btn-group-sm float-left">
            <a class="btn btn-link px-3" href="?lang=en">English</a>
            <a class="btn btn-link px-3" href="?lang=ar">عربي</a>
            <a class="btn btn-link px-3" href="?lang=fr">Français</a>
          </div>
        </div>
      </div>
    </div>
  </div>
{% endblock %}
