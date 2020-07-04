<script type="text/javascript">
  WebUI.loadCss.after("/static/webui/vendor/querybuilder/custom-query-builder.min.css","link[href$='webui.min.css']");
</script>
<div id="qbuilder_{{id}}" class="qbuilder qbuilder-wrapper {{styles}}"></div>
<script type="text/javascript">
  $(document).ready(function(){
    WebUI.loadScript("/static/webui/vendor/js/extendext.min.js",function(){
    WebUI.loadScript("/static/webui/vendor/js/doT.min.js",function(){
    WebUI.loadScript("/static/webui/vendor/js/moment.min.js",function(){
    WebUI.loadScript("/static/webui/vendor/querybuilder/custom-query-builder.min.js",function(){
      $('#qbuilder_{{id}}').queryBuilder({
        plugins:['invert','not-group'],
        filters:[{{filters|safe}}],
        rules:{{rules|safe}},
        allow_groups:{{allow_groups|safe}},
        allow_empty:{{allow_empty|safe}},
        default_condition:'{{default_condition}}',
        inputs_separator:'{{inputs_separator}}',
        lang:{
          add_rule:"{{gettext('Add rule')}}",
          add_group:"{{gettext('Add group')}}",
          delete_rule:"{{gettext('Delete')}}",
          delete_group:"{{gettext('Delete')}}",
          invert:"{{gettext('Invert')}}",
          NOT:"{{gettext('NOT')}}",
          conditions:{
            AND:"{{gettext('AND')}}",
            OR:"{{gettext('OR')}}"
          },
          operators: {
            equal:"{{gettext('equal')}}",
            not_equal:"{{gettext('not equal')}}",
            in:"{{gettext('in')}}",
            not_in:"{{gettext('not in')}}",
            less:"{{gettext('less')}}",
            less_or_equal:"{{gettext('less or equal')}}",
            greater:"{{gettext('greater')}}",
            greater_or_equal:"{{gettext('greater or equal')}}",
            between:"{{gettext('between')}}",
            not_between:"{{gettext('not between')}}",
            begins_with:"{{gettext('begins with')}}",
            not_begins_with:"{{gettext('does not begin with')}}",
            contains:"{{gettext('contains')}}",
            not_contains:"{{gettext('does not contain')}}",
            ends_with:"{{gettext('ends with')}}",
            not_ends_with:"{{gettext('does not end with')}}",
            is_empty:"{{gettext('is empty')}}",
            is_not_empty:"{{gettext('is not empty')}}",
            is_null:"{{gettext('is null')}}",
            is_not_null:"{{gettext('is not null')}}"
          },
          errors: {
            no_filter:"{{gettext('No filter selected')}}",
            empty_group:"{{gettext('The group is empty')}}",
            radio_empty:"{{gettext('No value selected')}}",
            checkbox_empty:"{{gettext('No value selected')}}",
            select_empty:"{{gettext('No value selected')}}",
            string_empty:"{{gettext('Empty value')}}",
            string_exceed_min_length:"{{gettext('Must contain at least {0} characters')}}",
            string_exceed_max_length:"{{gettext('Must not contain more than {0} characters')}}",
            string_invalid_format:"{{gettext('Invalid format ({0})')}}",
            number_nan:"{{gettext('Not a number')}}",
            number_not_integer:"{{gettext('Not an integer')}}",
            number_not_double:"{{gettext('Not a real number')}}",
            number_exceed_min:"{{gettext('Must be greater than {0}')}}",
            number_exceed_max:"{{gettext('Must be lower than {0}')}}",
            number_wrong_step:"{{gettext('Must be a multiple of {0}')}}",
            number_between_invalid:"{{gettext('Invalid values, {0} is greater than {1}')}}",
            datetime_empty:"{{gettext('Empty value')}}",
            datetime_invalid:"{{gettext('Invalid date format ({0})')}}",
            datetime_exceed_min:"{{gettext('Must be after {0}')}}",
            datetime_exceed_max:"{{gettext('Must be before {0}')}}",
            datetime_between_invalid:"{{gettext('Invalid values, {0} is greater than {1}')}}",
            boolean_not_valid:"{{gettext('Not a boolean')}}",
            operator_not_multiple:"{{gettext('Operator ({1}) cannot accept multiple values')}}"
          }
        }
      });

    })})})});
  });
</script>
