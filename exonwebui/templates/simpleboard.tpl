{%- extends "webui/html.tpl" -%}

{%- block b_html_head -%}
  <link rel="stylesheet" type="text/css" href="/static/webui/vendor/bootstrap/bootstrap{% if page_langdir == 'rtl' %}-rtl{% endif %}.min.css">
  <link rel="stylesheet" type="text/css" href="/static/webui/vendor/fontawesome/css/all.min.css">
  <link rel="stylesheet" type="text/css" href="/static/webui/vendor/pnotify/pnotify.min.css">
  <link rel="stylesheet" type="text/css" href="/static/webui/css/webui.min.css">
  <link rel="stylesheet" type="text/css" href="/static/webui/css/webui_simpleboard.min.css">
  <script type="text/javascript" src="/static/webui/vendor/jquery/jquery.min.js"></script>
  <script type="text/javascript" src="/static/webui/vendor/jquery/jquery.i18n.min.js"></script>
  <script type="text/javascript" src="/static/webui/vendor/bootstrap/bootstrap.bundle.min.js"></script>
  <script type="text/javascript" src="/static/webui/vendor/pnotify/pnotify.min.js"></script>
  <script type="text/javascript" src="/static/webui/js/webui.min.js"></script>
  <script type="text/javascript" src="/static/webui/js/webui_simpleboard.min.js"></script>
  {% block b_board_head %}{% endblock %}
{%- endblock -%}

{%- block b_html_body -%}
  {% block b_board_body %}
    <div id="board-wrapper">
      <div id="board-menubar" class="scroll d-print-none">
        <div id="menubar-head">
          {% block b_board_menuhead -%}{{menubar_head|safe}}{%- endblock %}
        </div>
        <div id="menubar-body">
          {% block menubar_body %}
            {%- set links = get_menulinks() -%}
            {%- for i in links.keys()|sort -%}
              {%- if 'menu' in links[i] and links[i].menu.keys() -%}
                <div class="list-group pb-2">
                  <div class="list-group-item list-group-item-secondary py-2">{{links[i].label}}</div>
                  {%- for j in links[i].menu.keys()|sort -%}
                    <a class="pagelink list-group-item list-group-item-action" href="{{links[i].menu[j].url}}">{{links[i].menu[j].label}}</a>
                  {%- endfor -%}
                </div>
              {%- elif links[i].url != '#' -%}
                <div class="list-group pb-2">
                  <a class="pagelink list-group-item list-group-item-action" href="{{links[i].url}}">{{links[i].label}}</a>
                </div>
              {%- endif -%}
            {%- endfor -%}
          {% endblock %}
        </div>
      </div>
      <div id="board-page">
        <div id="board-head" class="d-flex">
          <div id="board-title" class="text-truncate text-left px-3">
            {% block b_board_title %}{{board_title|safe}}{% endblock %}
          </div>
        </div>
        <div id="board-body">
          {% block b_board_content %}
            <div id="board-content" class="text-left"></div>
          {% endblock %}
        </div>
      </div>
    </div>
    <div id="board-backdrop" class="d-print-none"></div>
  {% endblock %}
  {% block b_board_scripts %}
    <script type="text/javascript">
      $(document).ready(function(){WebUI.board_init()});
    </script>
  {% endblock %}
{%- endblock -%}
