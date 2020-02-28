{%- extends "webui/html.tpl" -%}

{%- block b_html_head -%}
  <link rel="stylesheet" type="text/css" href="/static/webui/vendor/bootstrap/bootstrap.min.css">
  <link rel="stylesheet" type="text/css" href="/static/webui/vendor/fontawesome/css/all.min.css">
  <link rel="stylesheet" type="text/css" href="/static/webui/vendor/pnotify/pnotify.min.css">
  <link rel="stylesheet" type="text/css" href="/static/webui/vendor/metismenu/metisMenu.min.css">
  <link rel="stylesheet" type="text/css" href="/static/webui/css/webui.min.css">
  <link rel="stylesheet" type="text/css" href="/static/webui/css/webui_menuboard.min.css">
  <script type="text/javascript" src="/static/webui/vendor/jquery/jquery.min.js"></script>
  <script type="text/javascript" src="/static/webui/vendor/jquery/jquery.i18n.min.js"></script>
  <script type="text/javascript" src="/static/webui/vendor/bootstrap/bootstrap.bundle.min.js"></script>
  <script type="text/javascript" src="/static/webui/vendor/pnotify/pnotify.min.js"></script>
  <script type="text/javascript" src="/static/webui/vendor/metismenu/metisMenu.min.js"></script>
  <script type="text/javascript" src="/static/webui/js/webui.min.js"></script>
  <script type="text/javascript" src="/static/webui/js/webui_menuboard.min.js"></script>
  {% block b_board_head %}{% endblock %}
{%- endblock -%}

{%- block b_html_body -%}
  {% block b_board_body %}
    <div id="board-wrapper" class="ease">
      <div id="board-menubar" class="text-center ease d-print-none">
        <div id="menubar-head">
          {% block b_board_menuhead -%}{{menubar_head|safe}}{%- endblock %}
        </div>
        <div id="menubar-body">
          {% block menubar_body %}
            <ul class="metismenu">
              {%- set links = get_menulinks() -%}
              {%- for i in links.keys()|sort -%}
                {%- if 'menu' in links[i] and links[i].menu.keys() -%}
                  <li><a href="#" class="has-arrow">{{links[i].label}}</a>
                    <ul>
                      {%- for j in links[i].menu.keys()|sort -%}
                        <li><a class="pagelink" href="{{links[i].menu[j].url}}">{{links[i].menu[j].label}}</a></li>
                      {%- endfor -%}
                    </ul>
                  </li>
                {%- elif links[i].url != '#' -%}
                  <li><a class="pagelink" href="{{links[i].url}}">{{links[i].label}}</a></li>
                {%- endif -%}
              {%- endfor -%}
              <li><a></a></li>
            </ul>
          {% endblock %}
        </div>
      </div>
      <div id="board-page">
        <div id="menubar-toggle" class="ease d-print-none">
          <a title="Toggle Menu"><i class="fas fa-bars"></i></a>
        </div>
        <div id="board-head" class="d-flex ease">
          <div id="board-title" class="text-truncate text-left">
            {% block b_board_title %}{{board_title|safe}}{% endblock %}
          </div>
          <div id="board-widgets" class="d-print-none">
            {% block b_board_widgets %}{{board_widgets|safe}}{% endblock %}
          </div>
        </div>
        <div id="board-content" class="text-left"></div>
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
