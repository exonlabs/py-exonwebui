{%- if category == 'error' -%}
  {%- set alert_type, alert_icon = 'danger', 'fa-exclamation-circle' -%}
{%- elif category == 'warn' -%}
  {%- set alert_type, alert_icon = 'warning', 'fa-exclamation-circle' -%}
{%- elif category == 'info' -%}
  {%- set alert_type, alert_icon = 'info', 'fa-info-circle' -%}
{%- elif category == 'success' -%}
  {%- set alert_type, alert_icon = 'success', 'fa-check-circle' -%}
{%- else -%}
  {%- set alert_type, alert_icon = 'secondary', '' -%}
{%- endif -%}
<div class="alert-wrapper {% if dismissible %}alert-dismissible fade show{% endif %} {{styles}}">
  <div class="alert alert-{{alert_type}} text-left">
    {% if alert_icon %}<i class="fas fa-ta {{alert_icon}}"></i>{% endif %}
    {{message|safe}}
    {% if dismissible -%}
      <button type="button" class="close" data-dismiss="alert"><span>&times;</span></button>
    {%- endif %}
  </div>
</div>
