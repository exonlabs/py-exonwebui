{%- extends "webui/simplepage.tpl" -%}

{% block b_page_head %}
  {%- if doc_lang and doc_lang != 'en' -%}
  <script type="text/javascript" src="/static/i18n/{{doc_lang}}.min.js"></script>
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
        <div class="col-xs-12 col-sm-6 col-lg-4 mx-auto pt-5">
          <div class="card bg-light">
            <div class="card-body pb-3">
              {{loginform|safe}}
            </div>
          </div>
          <div class="btn-group-sm float-left">
            <a class="btn btn-link px-2" href="?lang=en">English</a>
            <a class="btn btn-link px-2" href="?lang=ar">عربي</a>
            <a class="btn btn-link px-2" href="?lang=fr">Français</a>
          </div>
        </div>
      </div>
    </div>
  </div>
{% endblock %}
